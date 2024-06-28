import re
from datetime import datetime

def extract_dates(text):
    date_pattern = r'\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}'
    dates = re.findall(date_pattern, text)
    return [datetime.strptime(date, '%d/%m/%Y' if '/' in date else '%Y-%m-%d') for date in dates]

def generate_timeline(text):
    dates = extract_dates(text)
    return sorted(dates)