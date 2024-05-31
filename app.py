import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_community.tools.google_trends import GoogleTrendsQueryRun
from langchain_community.utilities.google_trends import GoogleTrendsAPIWrapper
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from tools.semrush_keyword import SemrushKeyWordTools
from tools.semrush_tools import SemrushTools
import re
import sys
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

from datetime import datetime

# Ensure the results directory exists
if not os.path.exists("Results"):
    os.makedirs("Results")
    
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Load environment variables
load_dotenv()

# Setup LLM function
def setup_llm(llm_option):
    if llm_option == 'OpenAI GPT-4o':
        api_key = os.getenv('OPENAI_API_KEY')
        return ChatOpenAI(model="gpt-4o", api_key=api_key)    
    else:  
        api_key = os.getenv('CLAUDE_API_KEY')
        return ChatAnthropic(model="claude-3-haiku-20240307", api_key=api_key)


st.title("SEO Briefing Generator")

llm_options = ['OpenAI GPT-4o', 'Claude-3', 'Groq']
llm_choice = st.selectbox("Select the LLM to use:", llm_options)

llm = setup_llm(llm_choice)

google_search = SerperDevTool()
website_scrapper = ScrapeWebsiteTool()
google_trends_api_wrapper = GoogleTrendsAPIWrapper()
google_trends_tool = GoogleTrendsQueryRun(api_wrapper=google_trends_api_wrapper)


boss_agent = Agent(
    role="Boss Agent",
    goal="Oversee the entire content creation process and ensure quality. This includes managing the team, setting deadlines, and ensuring that all tasks are completed to the highest standard. The goal is to produce high-quality content that meets the client's requirements and exceeds their expectations.",
    backstory="The Boss Agent is an experienced content strategist with a keen eye for SEO optimization. They have a deep understanding of the content creation process and are skilled in managing teams to achieve high-quality results. They are also knowledgeable about the latest trends and best practices in content creation and are able to adapt to changing circumstances.",
    tools=[
        google_search,
        website_scrapper,
        google_trends_tool,
        # SemrushTools.semrush_keyword_research,
        # SemrushTools.semrush_competitor_analysis,
        # SemrushTools.semrush_technical_seo,
    ],
    llm=llm,
    verbose=True
)

outliner_agent = Agent(
    role="Outliner Agent",
    goal="Create the initial outline for the blog post. This includes researching the topic, identifying key points, and structuring the content in a logical and engaging way. The goal is to produce a clear and concise outline that sets the foundation for a high-quality blog post.",
    backstory="The Outliner Agent is a skilled writer with a talent for structuring content in a logical and engaging way. They have a deep understanding of the content creation process and are able to identify key points and themes. They are also knowledgeable about the latest trends and best practices in content creation and are able to adapt to changing circumstances.",
    tools=[
        google_search,
        website_scrapper,
        google_trends_tool,
        # SemrushTools.semrush_keyword_research,
        # SemrushTools.semrush_competitor_analysis,
        # SemrushTools.semrush_technical_seo,
    ],
    llm=llm,
    verbose=True
)

researcher_agent = Agent(
    role="Researcher Agent",
    goal="Conduct thorough research on the topic of the blog post. This includes identifying relevant sources, gathering data and statistics, and synthesizing the information into a coherent and informative format. The goal is to provide the content writer with a solid foundation of research to work with.",
    backstory="The Researcher Agent is a skilled researcher with a keen eye for detail. They have a deep understanding of the research process and are able to quickly identify relevant sources and extract key information. They are also knowledgeable about the latest trends and best practices in content creation and are able to adapt to changing circumstances.",
    tools=[
        google_search,
        website_scrapper,
        google_trends_tool,
        # SemrushTools.semrush_keyword_research,
        # SemrushTools.semrush_competitor_analysis,
        # SemrushTools.semrush_technical_seo,
        
    ],
    llm=llm,
    verbose=True
)

technical_seo_agent = Agent(
    role="Technical SEO Agent",
    goal="Ensure that the blog post is optimized for search engines. This includes identifying relevant keywords, optimizing the meta tags and descriptions, and ensuring that the content is structured in a way that is easy for search engines to crawl and index. The goal is to improve the visibility and ranking of the blog post in search engine results.",
    backstory="The Technical SEO Agent is an expert in search engine optimization. They have a deep understanding of how search engines work and are able to identify and implement the latest best practices in SEO. They are also knowledgeable about the latest trends and changes in the SEO landscape and are able to adapt to changing circumstances.",
    tools=[
        google_search,
        website_scrapper,
        google_trends_tool,
        # SemrushTools.semrush_keyword_research,
        # SemrushTools.semrush_competitor_analysis,
        # SemrushTools.semrush_technical_seo,
    ],
    llm=llm,
    verbose=True
)

content_writer_agent = Agent(
    role="Content Writer Agent",
    goal="Write the blog post based on the outline and research provided by the other agents. This includes crafting engaging and informative content that is tailored to the target audience. The goal is to produce a high-quality blog post that is both informative and entertaining.",
    backstory="The Content Writer Agent is a skilled writer with a talent for crafting engaging and informative content. They have a deep understanding of the content creation process and are able to adapt their writing style to suit the needs of the target audience. They are also knowledgeable about the latest trends and best practices in content creation and are able to adapt to changing circumstances.",
    tools=[
        google_search,
        website_scrapper,
        google_trends_tool,
        # SemrushTools.semrush_keyword_research,
        # SemrushTools.semrush_competitor_analysis,
        # SemrushTools.semrush_technical_seo,
    ],
    llm=llm,
    verbose=True
)

proofreader_agent = Agent(
    role="Proofreader Agent",
    goal="Ensure that the blog post is free of errors and typos. This includes checking for spelling, grammar, and punctuation errors, as well as ensuring that the content is consistent and coherent. The goal is to produce a polished and professional blog post that is easy to read and understand.",
    backstory="The Proofreader Agent is a detail-oriented individual with a keen eye for errors. They have a deep understanding of grammar and punctuation rules and are able to quickly identify and correct errors in written content. They are also knowledgeable about the latest trends and best practices in content creation and are able to adapt to changing circumstances.",
    tools=[
        google_search,
        website_scrapper,
        google_trends_tool,
        # SemrushTools.semrush_keyword_research,
        # SemrushTools.semrush_competitor_analysis,
        # SemrushTools.semrush_technical_seo,
    ],
    llm=llm,
    verbose=True
)

editor_agent = Agent(
    role="Editor Agent",
    goal="Review and refine the blog post for coherence and style. This includes ensuring that the content is well-organized and easy to follow, and that the writing style is consistent throughout. The goal is to produce a polished and professional blog post that is engaging and informative.",
    backstory="The Editor Agent is an experienced editor with a keen eye for detail. They have a deep understanding of the content creation process and are able to identify areas for improvement in written content. They are also knowledgeable about the latest trends and best practices in content creation and are able to adapt to changing circumstances.",
    tools=[
        google_search,
        website_scrapper,
        google_trends_tool,
        # SemrushTools.semrush_keyword_research,
        # SemrushTools.semrush_competitor_analysis,
        # SemrushTools.semrush_technical_seo,
    ],
    llm=llm,
    verbose=True
)

outreach_expert_agent = Agent(
    role="Outreach Expert Agent",
    goal="Develop and implement a content promotion and outreach strategy. This includes identifying relevant channels and platforms for promoting the blog post, as well as building relationships with influencers and other content creators. The goal is to increase the visibility and reach of the blog post and drive traffic to the client's website.",
    backstory="The Outreach Expert Agent is a skilled marketer with a talent for building relationships and driving content visibility. They have a deep understanding of the content promotion process and are able to quickly identify relevant channels and platforms for promoting content. They are also knowledgeable about the latest trends and best practices in content promotion and are able to adapt to changing circumstances.",
    tools=[
        google_search,
        website_scrapper,
        google_trends_tool,
        # SemrushTools.semrush_keyword_research,
        # SemrushTools.semrush_competitor_analysis,
        # SemrushTools.semrush_technical_seo,
    ],
    llm=llm,
    verbose=True
)


class StreamToExpander:
    def __init__(self, expander, buffer_limit=10000):
        self.expander = expander
        self.buffer = []
        self.buffer_limit = buffer_limit

    def write(self, data):
        cleaned_data = re.sub(r'\x1B\[\d+;?\d*m', '', data)
        if len(self.buffer) >= self.buffer_limit:
            self.buffer.pop(0)
        self.buffer.append(cleaned_data)

        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer.clear()

    def flush(self):
        if self.buffer:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer.clear()

with st.form("research_form"):
    focus_keyword = st.text_input("Enter a focus keyword:", "Renting trailers insurance")
    target_audience = st.text_input("Describe your target audience:", "Small business owners")
    tone = st.selectbox("Select the tone of the blog post:", ["Formal", "Informal", "Professional", "Conversational"])
    length = st.slider("Select the desired length of the blog post (in words):", min_value=300, max_value=3000, value=1000, step=100)
    key_points = st.text_area("Enter key points or topics you want to cover in the blog post:", "Benefits of renting trailers, insurance options, cost considerations, tips for renting")
    submit_button = st.form_submit_button("Generate SEO Briefing")

if submit_button:
    process_output_expander = st.expander("Processing Output:")
    sys.stdout = StreamToExpander(process_output_expander)
    
    try:
        # Update the agents and tasks with the user's inputs
        outliner_agent.goal += f" The blog post should be tailored to {target_audience} and have a {tone} tone."
        researcher_agent.goal += f" The research should focus on the key points provided: {key_points}."
        content_writer_agent.goal += f" The blog post should be around {length} words and cover the following key points: {key_points}. The tone should be {tone}."

        outline_task = Task(
            description=f"Create the initial outline for the blog post. This includes researching the topic, identifying key points, and structuring the content in a logical and engaging way. The blog post should be tailored to {target_audience} and have a {tone} tone. Focus on the key points: {key_points}.",
            expected_output="A detailed outline for the blog post, including the main points and subpoints, as well as any relevant research or data.",
            agent=outliner_agent,
            output_file=f"Results/outline-[{timestamp}].md"
        )

        keyword_research_task = Task(
            description=f"Conduct thorough keyword research to identify relevant keywords for the blog post focused on {focus_keyword}. This includes analyzing search volume, competition, and relevance to the topic. The blog post should be tailored to {target_audience} and have a {tone} tone. Focus on the key points: {key_points}.",
            expected_output="A list of relevant keywords, along with their search volume and competition metrics.",
            agent=technical_seo_agent,
            output_file=f"Results/keyword_research-[{timestamp}].md"
        )

        technical_seo_task = Task(
            description=f"Ensure that the blog post is optimized for search engines. This includes identifying relevant keywords, optimizing the meta tags and descriptions, and ensuring that the content is structured in a way that is easy for search engines to crawl and index. The blog post should be tailored to {target_audience} and have a {tone} tone. Focus on the key points: {key_points}.",
            expected_output="A technically optimized blog post with relevant keywords, meta tags, and descriptions.",
            agent=technical_seo_agent,
            output_file=f"Results/technical_seo-[{timestamp}].md"
        )

        content_writing_task = Task(
            description=f"Write the blog post based on the outline and research provided by the other agents. This includes crafting engaging and informative content that is tailored to {target_audience}. The blog post should be around {length} words and cover the following key points: {key_points}. The tone should be {tone}.",
            expected_output="A high-quality blog post that is both informative and entertaining.",
            agent=content_writer_agent,
            output_file=f"Results/content_writing-[{timestamp}].md"
        )

        proofreading_task = Task(
            description=f"Ensure that the blog post is free of errors and typos. This includes checking for spelling, grammar, and punctuation errors, as well as ensuring that the content is consistent and coherent. The blog post should be tailored to {target_audience} and have a {tone} tone. Focus on the key points: {key_points}.",
            expected_output="A blog post that is free of errors and typos, with consistent and coherent content.",
            agent=proofreader_agent,
            output_file=f"Results/proofreading-[{timestamp}].md"
        )

        editing_task = Task(
            description=f"Review and refine the blog post for coherence and style. This includes ensuring that the content is well-organized and easy to follow, and that the writing style is consistent throughout. The blog post should be tailored to {target_audience} and have a {tone} tone. Focus on the key points: {key_points}.",
            expected_output="A refined and coherent blog post with a consistent writing style and engaging content.",
            agent=editor_agent,
            output_file=f"Results/editing-[{timestamp}].md"
        )

        outreach_task = Task(
            description=f"Develop and implement a content promotion and outreach strategy for the blog post. This includes identifying relevant channels and platforms for promoting the content, as well as building relationships with influencers and other content creators. The goal is to increase the visibility and reach of the blog post and drive traffic to the client's website. The blog post should be tailored to {target_audience} and have a {tone} tone. Focus on the key points: {key_points}.",
            expected_output="A comprehensive content promotion and outreach strategy that includes specific tactics and timelines for implementation.",
            agent=outreach_expert_agent,
            output_file=f"Results/outreach-[{timestamp}].md"
        )

        # Define the Crew
        research_crew = Crew(
            agents=[
                boss_agent,
                outliner_agent,
                researcher_agent,
                technical_seo_agent,
                content_writer_agent,
                proofreader_agent,
                editor_agent,
                outreach_expert_agent
            ],
            tasks=[
                outline_task,
                keyword_research_task,
                technical_seo_task,
                content_writing_task,
                proofreading_task,
                editing_task,
                outreach_task
            ],
            process=Process.hierarchical,
            manager_llm=llm,
        )

        result = research_crew.kickoff()
        st.write(result)
    except Exception as e:
        st.error(f"Failed to process tasks: {e}")

