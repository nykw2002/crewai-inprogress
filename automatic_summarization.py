from gensim.summarization import summarize

def summarize_text(text, ratio=0.2):
    return summarize(text, ratio=ratio)