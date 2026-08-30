import pymupdf 
import re 
doc = pymupdf.open('114P_English.pdf') 
print("Pages:", len(doc)) 
vocabulary = set() 



for page in doc:
    text = page.get_text('words') 
    for item in text: 
        word = item[4] 
        parts = re.split(r'\s+', word) 
        for part in parts:
            part = re.sub(r'\d', '', part)
            part = re.sub(r'^\([A-Z]\)$', '', part)
            part = re.sub(r'[.!?]', '', part)
            vocabulary.add(part)

print(vocabulary)