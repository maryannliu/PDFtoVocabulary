# PDF Vocabulary Extractor

## Purpose

These PDFs are **Taiwanese high school entrance English exams**.

As an English tutor, I want to turn past entrance exams into a reusable vocabulary resource for my students. Instead of asking students to repeatedly study vocabulary from scattered exam papers, this project extracts the vocabulary that actually appears in entrance exams and creates a focused list they can memorize.

The longer-term goal is to turn this into a vocabulary learning tool that can provide students with:

* A list of vocabulary frequently appearing in entrance exams
* Definitions
* Example sentences
* Synonyms and antonyms
* Vocabulary grouped into meaningful categories

This makes the project not just a PDF text-extraction exercise, but a way of **using programming to automate part of my teaching workflow**.

---

## Key Skills Demonstrated

* Does not blindly trust AI-generated code
* Uses official documentation to verify Python libraries and APIs
* Debugs unexpected program behaviour systematically
* Uses regular expressions for text processing
* Applies programming to solve a real-world teaching problem

---

## Initial Approach

I first asked ChatGPT how to extract words from a PDF.

It suggested two approaches:

* Extract selectable text directly from the PDF
* Use Optical Character Recognition (OCR) for scanned PDFs

I chose **direct text extraction** because the PDFs I was working with contained selectable text.

Before copying and pasting the suggested code, I searched online to verify that the Python library was legitimate and checked its documentation.

I also discovered that ChatGPT's initial suggestion used an older import name for PyMuPDF.

Instead of blindly following the generated code, I followed the current PyMuPDF documentation and used:

```python
import pymupdf
```

I then used `get_text("words")` to extract individual text elements.

---

# Problem 1: Unicode Characters Mixed With Words

My initial code was:

```python
import pymupdf

doc = pymupdf.open('114P_English.pdf')

print("Pages:", len(doc))

vocabulary = []

for page in doc:
    text = page.get_text('words')

    for item in text:
        word = item[4]

        if word not in vocabulary:
            vocabulary.append(item[4])

print(vocabulary)
```

The extracted text contained unexpected Unicode characters mixed into words:

```text
'that\u2006\u300042\u3000\u2006.'
'Now,'
'makes'
'mother'
'thank'
'giving'
'Cameron\u2006\u300043\u3000\u2006his'
```

## Solution

I initially tried filtering the extracted text by allowing only English letters, hyphens and apostrophes.

However, this introduced another problem, which led to further investigation.

---

# Problem 2: Words That Were Not Actually English Words

The output contained strange words such as:

```text
'bhiking'
'familys'
'dask'
'cservice'
'cmaking'
'bto'
'experiencewe'
'athe'
'cjeff'
'dthe'
'cmade'
'andis'
```

Instead of immediately adding more filtering rules, I needed to understand what PyMuPDF was actually extracting.

## Solution

I printed the raw extracted strings using `repr()`:

```python
for item in text:
    word = item[4]
    print(repr(word))
```

Using `repr()` made invisible Unicode characters visible and allowed me to inspect the actual strings returned by PyMuPDF.

---

# Problem 3: Multiple-Choice Options Were Being Parsed With Words

The raw output revealed that multiple-choice options were being extracted as strings containing both the option label and the word.

For example:

```text
'(A)\u2006blow'
'(B)\u2006build'
'(C)\u2006follow'
```

Visually, these were:

```text
(A) blow
(B) build
(C) follow
```

My filtering was removing the parentheses and whitespace, which could turn:

```text
(A) blow
```

into:

```text
Ablow
```

## Solution

I tried removing the multiple-choice labels before applying the other filtering.

---

# Problem 4: Apostrophes Were Being Removed

I then noticed that contractions such as:

```text
it’ll
```

were becoming:

```text
itll
```

The PDF was using a **curly apostrophe** (`’`) rather than the standard ASCII apostrophe (`'`).

I therefore modified the filtering to recognise both types of apostrophe.

This successfully preserved words such as:

```text
it’s
it’ll
doesn’t
```

However, I was still seeing unexpected combinations of words.

---

# Problem 5: Words That Appeared to Be Combined

I found outputs such as:

```text
'is'
'hard'
'for'
'trees'
'toalong'
'this'
```

At this point, I realised that simply filtering characters was potentially hiding the original structure of the PDF.

I decided to go back to the raw extracted text rather than continuing to add filtering rules.

---

# Problem 6: Blanks Were Being Removed

I eventually found the underlying problem.

The PDF contained questions such as:

```text
Dad is busy cooking in the kitchen.
Dinner will be _____ in ten minutes.
```

The blank was represented using special Unicode spacing characters.

PyMuPDF could return something similar to:

```text
'be\u2006\u3000\u3000\u3000\u2006in'
```

When I removed all non-English characters, the blank disappeared:

```text
be + blank + in
```

became:

```text
bein
```

This explained many of the apparently nonsensical vocabulary items.

## Solution

Instead of removing Unicode whitespace, I first separated the string wherever whitespace occurred:

```python
parts = re.split(r'\s+', word)
```

For example:

```text
'(A)\u2006blow'
```

became:

```python
['(A)', 'blow']
```

This preserved the separation between the option label and the vocabulary.

---

# Problem 7: Losing My Mind

After several rounds of modifying regex filters, I realised I was approaching the problem in the wrong order.

I had been trying to clean the text before understanding its structure.

The important lesson was:

> **Don't blindly filter data before understanding what the raw data actually looks like.**

I decided to determine the filtering process myself.

The new approach was:

1. Extract the raw text
2. Split strings containing Unicode whitespace
3. Inspect the result
4. Remove numbers
5. Remove multiple-choice labels such as `(A)` and `(B)`
6. Remove punctuation
7. Validate the remaining words against an English vocabulary resource

After applying the filtering in this order, the first page produced a much cleaner vocabulary list.

I then tested the process against the rest of the document.

---

# Next Step: Vocabulary Validation

The next step is to use the **NLTK English corpus** to determine whether an extracted string is an actual English word.

This will help distinguish legitimate vocabulary from PDF extraction artifacts.

The planned pipeline is:

```text
PDF
 ↓
PyMuPDF
 ↓
Extract words
 ↓
Split Unicode whitespace
 ↓
Remove numbers
 ↓
Remove multiple-choice labels
 ↓
Remove punctuation
 ↓
Validate against English vocabulary
 ↓
Remove duplicates
 ↓
Vocabulary list
```

---

# Future Development

Once reliable vocabulary extraction is working, I want to turn the vocabulary list into a useful study resource for my students.

### 1. Definitions

Use a dictionary API or library to automatically retrieve definitions for each vocabulary word.

### 2. Example Sentences

Generate an example sentence for each word so students can learn the word **in context**, rather than memorising an isolated definition.

For example:

```text
Vocabulary: prepare

Definition:
To make something ready.

Example:
I need to prepare for my English exam tomorrow.
```

### 3. Synonyms and Antonyms

Provide related words to help students build connections between vocabulary.

```text
happy

Synonyms:
glad, cheerful, joyful

Antonyms:
sad, unhappy
```

### 4. Vocabulary Categories

Group vocabulary into meaningful categories to make memorisation easier.

Possible categories include:

* People and relationships
* School and education
* Food and cooking
* Places
* Nature
* Emotions
* Actions
* Daily life
* Transportation
* Technology
* Health
* Describing people
* Describing things


The ultimate goal is to transform **past exam papers into a structured, reusable vocabulary database**.

---

## Final Goal

The final version of this project could turn:

```text
Past exam PDFs
       ↓
Vocabulary extraction
       ↓
English validation
       ↓
Definitions
       ↓
Example sentences
       ↓
Synonyms / antonyms
       ↓
Vocabulary categories
       ↓
Student study resource
```

This would allow me to spend less time manually preparing vocabulary lists and more time helping students actually learn the vocabulary.
