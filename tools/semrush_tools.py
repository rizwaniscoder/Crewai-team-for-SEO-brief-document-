import requests
import json
import os

from langchain.tools import tool
from langchain_community.document_loaders import WebBaseLoader

class SemrushTools:
  
  @tool('semrush keyword research')
  def semrush_keyword_research(query: str) -> str:
    """
    Use this tool to perform keyword research using Semrush.
    """
    return SemrushTools.sermush_keyword_research(query)
  
  @tool('semrush competitor analysis')
  def semrush_competitor_analysis(query: str) -> str:
    """
    Use this tool to perform competitor analysis using Semrush.
    """
    return SemrushTools.sermush_competitor_analysis(query)
    
  @tool('semrush technical seo')
  def semrush_technical_seo(query: str) -> str:
    """
    Use this tool to perform technical SEO analysis using Semrush.
    """
    return SemrushTools.sermush_technical_seo(query)
    
  def semrush_keyword_research(query):
    url = "https://api.semrush.com/analytics/ta/api/v3/sources"
    payload = json.dumps({
      "target": query,
      "device_type": "desktop",
      "display_limit": 10,
      "display_offset": 0,
      "country": "us",
      "sort_order": "traffic_share",
      "traffic_channel": "referral",
      "traffic_type": "organic",
      "display_date": "2023-06-01",
      "export_columns": "target,from_target,display_date,country,traffic_share,traffic,channel"
    })
    headers = {
      'X-API-KEY': os.getenv("SEMRUSH_API_KEY"),
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()['data']['rows']
    
    string = []
    for result in results:
      string.append(f"{result[0]}\n{result[1]}\n{result[2]}\n{result[3]}\n{result[4]}\n{result[5]}\n{result[6]}\n\n")
      
    return f"Keyword research results for '{query}':\n\n" + "\n".join(string)
  
  def semrush_competitor_analysis(query):
    url = "https://api.semrush.com/analytics/ta/api/v3/competitors"
    payload = json.dumps({
      "target": query,
      "device_type": "desktop",
      "display_limit": 10,
      "display_offset": 0,
      "country": "us",
      "sort_order": "traffic_share",
      "traffic_channel": "referral",
      "traffic_type": "organic",
      "display_date": "2023-06-01",
      "export_columns": "target,from_target,display_date,country,traffic_share,traffic,channel"
    })
    headers = {
      'X-API-KEY': os.getenv("SEMRUSH_API_KEY"),
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()['data']['rows']
    
    string = []
    for result in results:
      string.append(f"{result[0]}\n{result[1]}\n{result[2]}\n{result[3]}\n{result[4]}\n{result[5]}\n{result[6]}\n\n")
      
    return f"Competitor analysis results for '{query}':\n\n" + "\n".join(string)
  
  def semrush_technical_seo(query):
    url = "https://api.semrush.com/analytics/ta/api/v3/technical-seo"
    payload = json.dumps({
      "target": query,
      "device_type": "desktop",
      "display_limit": 10,
      "display_offset": 0,
      "country": "us",
      "sort_order": "traffic_share",
      "traffic_channel": "referral",
      "traffic_type": "organic",
      "display_date": "2023-06-01",
      "export_columns": "target,from_target,display_date,country,traffic_share,traffic,channel"
    })
    headers = {
      'X-API-KEY': os.getenv("SEMRUSH_API_KEY"),
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()['data']['rows']
    
    string = []
    for result in results:
      string.append(f"{result[0]}\n{result[1]}\n{result[2]}\n{result[3]}\n{result[4]}\n{result[5]}\n{result[6]}\n\n")
      
    return f"Technical SEO analysis results for '{query}':\n\n" + "\n".join(string)
  
if __name__ == "__main__":
  print(SemrushTools.sermush_keyword_research("example.com"))
