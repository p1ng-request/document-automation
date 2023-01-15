![Banner](https://raw.githubusercontent.com/p1ng-request/p1ng-request/main/banner.gif)
## Something I have been working on 🎯

[broken-links-checker.py](https://github.com/p1ng-request/document-automation/blob/main/broken-links-checker.py): A Python script to scan broken links from a given web domain.

:sparkles::sparkles:[ml-docs-scanner.py](https://github.com/p1ng-request/document-automation/blob/main/ml-docs-scanner.py):sparkles::sparkles:: The udpated version of NLP Docs Scanner.
+ Using machine learning techniques to train models on the cleaned data, make predictions on the data, score the documentation based on the criteria you specified.
+ Use supervised learning techniques to train a model to predict the quality of a document based on a set of labeled examples. For example, you can use grammatical error correction models, spell checker models, readability metrics such as the Flesch-Kincaid readability test, sentiment analysis models to measure the objectivity and tone of a document.
+ (Not Open Sourced) Utilize AI models to check for consistency and coherence in style, tone, and terminology throughout the text, and give improved readability scores.
+ Screenshot:
![machine learning scanner screenshot](https://github.com/p1ng-request/document-automation/blob/main/screenshot.png?raw=true)
+ Dependenceis:
```bash
## prereq: python3, jre
## Install dependenceis:
pip3 install nltk textstat markdown textblob language-tool-python pyfiglet textblob
```

[nlp-docs-scanner.py](https://github.com/p1ng-request/document-automation/blob/main/nlp-docs-scanner.py): Automated Documentation Scanner. Features:
+ Scan all .md files in a given directory and all the sub-directories and use natural language processing(NLP) techniques to determine complicated words by breaking down the text into individual sentences.
+ Grammar and Spelling checker.
+ Evaluate **readability**: the Flesch-Kincaid Reading Ease score.
+ Evalute the **objectivity**: by computing the Automated Readability Index (ARI) and Flesch-Kincaid Grade Level.
+ Evalute **clearity**: Apply named entity recognition (NER) to identify specific words within the text and make suggestions for improvements.
+ Evalue the **tone**: Apply Sentiment analysis using Machine learning (ML) techniques.
+ Evalute the **consistency**: Analyze the text based on NLP and ML, which, detects terms and check consistency.
> Note 1: You are obligated to [create a *terminology_dict.json* file](https://github.com/p1ng-request/document-automation/blob/main/create-term-dic.py) in the following format:
```json
{
    "word1": count1,
    "word2": count2,
    ...
}
```
> Note 2: Grammar check, spelling check & clearity check on a word-based level proven to be unreliable for generating too many false positives. Best pracitce: use grammarly instead.
