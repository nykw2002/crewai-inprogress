import re

def extract_citations(text):
    citation_pattern = r'\(([^)]+, \d{4})\)'
    return re.findall(citation_pattern, text)

def track_sources(agent_outputs):
    sources = {}
    for agent, output in agent_outputs.items():
        sources[agent] = extract_citations(output)
    return sources