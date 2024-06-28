import difflib

def compare_documents(doc1, doc2):
    diff = difflib.unified_diff(doc1.splitlines(), doc2.splitlines())
    return '\n'.join(diff)