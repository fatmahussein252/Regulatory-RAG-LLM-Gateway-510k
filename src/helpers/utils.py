import re

def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s:/]", "", text)
    text = re.sub(r"_", " ", text)
    # Remove lines that contain only spaces/tabs 
    text = re.sub(r'^[ \t]+$', '', text, flags=re.MULTILINE) 
    # Replace multiple blank lines with a maximum of two 
    text = re.sub(r'\n{2,}', '\n', text) 
    # Strip trailing spaces on each line 
    text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE) 
    # Remove excessive internal spacing (but keep single spaces) 
    text = re.sub(r'[ \t]{2,}', ' ', text) 

    return text.strip()