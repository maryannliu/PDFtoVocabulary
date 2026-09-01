import pymupdf 
import re 
import nltk 
from nltk.corpus import words

doc = pymupdf.open('114P_English.pdf') 
print("Pages:", len(doc)) 
vocabulary = set() 

# downloard nltk corpus once 
# nltk.download('words')


english_words = set(w.lower() for w in words.words())


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

# Filter against NLTK's English word list 
valid_vocab = { w.lower() for w in vocabulary if w.lower() in english_words }
removed = vocabulary - valid_vocab

print(f"Kept {len(valid_vocab)} words, removed {len(removed)} non-English/unknown tokens")
print(removed)
print(sorted(valid_vocab))