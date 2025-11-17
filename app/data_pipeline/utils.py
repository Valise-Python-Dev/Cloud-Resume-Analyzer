import re

def remove_email(text):
    return re.sub(r'\S+@\S+', '', text)

def remove_url(text):
    return re.sub(r'http\S+|www.\S+', '', text)

def remove_special_chars(text):
    return re.sub(r'[^A-Za-z0-9\s.,]', ' ', text)

def remove_extra_spaces(text):
    return " ".join(text.split())
