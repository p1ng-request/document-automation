import os
import re
import nltk
import textstat
from typing import List, Tuple
from pathlib import Path
import markdown
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from nltk.sentiment import SentimentIntensityAnalyzer
from language_tool_python import LanguageTool
import json
from pyfiglet import Figlet
from textblob import TextBlob

nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('vader_lexicon')

def print_banner():
    custom_fig = Figlet(font='slant')
    print(custom_fig.renderText('Automated Docs-Scanner'))

def clean_html(documentation: str) -> str:
    # Removes any HTML tags from the documentation
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', documentation)
    return cleantext

def parse_markdown(documentation: str) -> str:
    # Convert markdown to html
    return markdown.markdown(documentation)

def remove_header(documentation: str) -> str:
    # Remove YAML front matter
    lines = documentation.split("\n")
    start = 0
    end = len(lines)
    for i, line in enumerate(lines):
        if line.strip() == "---":
            start = i
            break
    for i, line in enumerate(lines[start+1:]):
        if line.strip() == "---":
            end = i + start + 1
            break
    return "\n".join(lines[end+1:])

def remove_code_blocks(documentation: str) -> str:
    # Removes any code blocks from the documentation
    cleanr = re.compile('```.*?```|<.*?>', re.DOTALL)
    cleantext = re.sub(cleanr, '', documentation)
    return cleantext

def check_tone(documentation: str) -> str:
    # Check for Tone in the text
    # Create an instance of the sentiment intensity analyzer
    sentiment_analyzer = SentimentIntensityAnalyzer()
    # Get the sentiment score of the documentation
    sentiment_score = sentiment_analyzer.polarity_scores(documentation)
    if sentiment_score['compound'] < 0:
        print("\033[1;35;40m The documentation is written in a subjective tone. \033[0m")
    elif sentiment_score['compound'] == 0:
        print("\033[1;33;40m The documentation is written in a neutral tone. \033[0m")
    elif sentiment_score['compound'] > 0:
        print("\033[1;32;40m The documentation is written in a objective tone. \033[0m")

def score_documentation(documentation: str) -> float:
    # Compute the Flesch-Kincaid readability test
    fk_score = textstat.flesch_kincaid_grade(documentation)
    return fk_score

def suggest_improvements(documentation: str) -> List[Tuple[str, str]]:
    suggestions = []
    # create an instance of the LanguageTool class
    tool = LanguageTool('en-US')
    # Compute the Flesch-Kincaid readability test
    fk_score = score_documentation(documentation)
    coleman_score = textstat.coleman_liau_index(documentation)
    # Check for grammar and spelling errors
    grammar_errors = tool.check(documentation)
    if grammar_errors:
        print("\033[1;31;47m There are grammatical and/or spelling errors in the document. \033[0m \033[1;31;47m Consider running the document through a grammar and spell checker. \033[0m")
        for error in grammar_errors:
            suggestions.append((error.message, error.context))

    if fk_score > 12:
        print("\033[1;31;47m The document is quite difficult to read. \033[0m \033[1;31;47m Consider simplifying the sentence structure and using shorter sentences. \033[0m")
        # suggestions.append(("Readability", "The document is quite difficult to read"))
    elif coleman_score > 14:
        print("\033[1;31;47m The document is quite difficult to read. \033[0m \033[1;31;47m Consider simplifying the sentence structure and using shorter sentences. \033[0m")
        # suggestions.append(("Readability", "The document is quite difficult to read"))

    return suggestions

def evaluate_documentation(docs: List[str], labels: List[str]) -> None:
    for i, doc in enumerate(docs):
        print(f"Evaluating {labels[i]}...")
        print("-"*50)
        print("Cleaning and preprocessing...")
        doc = clean_html(doc)
        doc = remove_code_blocks(doc)
        check_tone(doc)
        score = score_documentation(doc)
        print(f"Flesch-Kincaid Readability Score: {score}")
        if score > 12:
            print("\033[1;31;47m The document is quite difficult to read. \033[0m \033[1;31;47m Consider simplifying the sentence structure and using shorter sentences. \033[0m")
        suggestions = suggest_improvements(doc)
        print("\n".join([f"{suggestion[0]}: {suggestion[1]}" for suggestion in suggestions]))
        print()

def get_md_files(root_dir: str) -> List[str]:
    md_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".md"):
                md_files.append(os.path.join(dirpath, filename))
    return md_files

if __name__ == '__main__':
    print_banner()
    root_dir = '/path/'
    md_files = get_md_files(root_dir)
    documents = []
    labels = []
    for file in md_files:
        print("\033[1;33;47m Processing document: {} \033[0m".format(os.path.basename(file)))
        with open(file, "r") as f:
            contents = f.read()
        # Get the label of the document, you need to set it based on your use case.
        file_label = 'your label'
        labels.append(file_label)
        contents = remove_header(contents)
        contents = remove_code_blocks(contents)
        contents = clean_html(contents)
        check_tone(contents)
        score = score_documentation(contents)
        print("\033[1;34;47m The Flesch-Kincaid readability score is {} \033[0m".format(score))
        suggestions = suggest_improvements(contents)
        if suggestions:
            print("The following suggestions can improve the documentation:")
            for suggestion in suggestions:
                print(f"{suggestion[0]} - {suggestion[1]}")
        documents.append(contents)
 
