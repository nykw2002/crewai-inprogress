from serpapi import GoogleSearch
import os

def search_internet(query):
    search = GoogleSearch({
        "q": query,
        "api_key": os.getenv("SERPAPI_API_KEY")
    })
    results = search.get_dict()
    
    if "organic_results" in results:
        return [result["snippet"] for result in results["organic_results"][:3]]
    else:
        return ["No results found."]