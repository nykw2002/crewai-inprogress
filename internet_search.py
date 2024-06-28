import os

try:
    from serpapi import GoogleSearch
except ImportError:
    print("SerpAPI not installed. Internet search functionality will not be available.")
    GoogleSearch = None

def search_internet(query):
    if GoogleSearch is None:
        return ["Internet search is not available due to missing SerpAPI package."]
    
    search = GoogleSearch({
        "q": query,
        "api_key": os.getenv("SERPAPI_API_KEY")
    })
    results = search.get_dict()
    
    if "organic_results" in results:
        return [result["snippet"] for result in results["organic_results"][:3]]
    else:
        return ["No results found."]