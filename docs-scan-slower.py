import os
import re
import nltk
from textstat.textstat import textstat
from typing import List
from pathlib import Path
import markdown
from nltk.sentiment import SentimentIntensityAnalyzer
from language_tool_python import LanguageTool
import language_tool_python
from textblob import TextBlob

nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
    
def clean_html(documentation: str):
    # use a regular expression to remove any HTML tags from the documentation
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', documentation)
    return cleantext

def parse_markdown(documentation: str):
    return markdown.markdown(documentation)

def remove_header(documentation: str):
    lines = documentation.split("\n")
    for i, line in enumerate(lines):
        if line.strip() == "---":
            start = i
            break
    for i, line in enumerate(lines[start+1:]):
        if line.strip() == "---":
            end = i + start + 1
            break
    return "\n".join(lines[end+1:])

def check_tone(documentation: str):
    # Create an instance of the sentiment intensity analyzer
    sentiment_analyzer = SentimentIntensityAnalyzer()
    # Get the sentiment score of the documentation
    sentiment_score = sentiment_analyzer.polarity_scores(documentation)
    print(sentiment_score)
    if sentiment_score['compound'] < -0.5:
        print("The documentation is written in a very negative tone.")
    elif sentiment_score['compound'] < 0:
        print("The documentation is written in a negative tone.")
    elif sentiment_score['compound'] == 0:
        print("The documentation is written in a neutral tone.")
    elif sentiment_score['compound'] > 0:
        print("The documentation is written in a positive tone.")
    elif sentiment_score['compound'] > 0.5:
        print("The documentation is written in a very positive tone.")

def score_documentation(documentation: str) -> float:
    """
    Compute the Flesch-Kincaid readability test
    """
    fk_score = textstat.flesch_kincaid_grade(documentation)
    return fk_score

def suggest_improvements(documentation: str):
    suggestions = []
    # create an instance of the LanguageTool class
    tool = language_tool_python.LanguageTool('en-US')
    # check for grammar errors
    grammar_errors = tool.check(documentation)
    for error in grammar_errors:
        context = error.context
        suggestions.append(f"Grammar Error: {error.message} in sentence: {context}")
    return suggestions


    # check for spelling errors
    textblob = TextBlob(documentation)
    for word in textblob.words:
        if word.spellcheck()[0][1] < 0.8:
            suggestions.append("Spelling Error: " + word)

    # Compute the Flesch-Kincaid readability test
    fk_score = textstat.flesch_kincaid_grade(documentation)
    coleman_score = textstat.coleman_liau_index(documentation)
    # Check if the documentation has an objective tone
    objective_score = textstat.automated_readability_index(documentation)
    clear_score = textstat.flesch_reading_ease(documentation)
    if fk_score > 18:
        suggestions.append("The document appears to be written at a higher reading level than the target audience. Consider simplifying the language.")
    elif fk_score < 10:
        suggestions.append("The document appears to be written at a lower reading level than the target audience. Consider using more complex vocabulary.")
    if coleman_score > 18:
        suggestions.append("The document appears to be written at a higher reading level than the target audience. Consider simplifying the language.")
    elif coleman_score < 12:
        suggestions.append("The document appears to be written at a lower reading level than the target audience. Consider using more complex vocabulary.")
    if objective_score > 14:
        suggestions.append("The document appears to be written in a more technical or advanced language. Consider simplifying the language.")
    if objective_score < 8:
        suggestions.append("The document appears to be written in a subjective or non-technical language. Consider changing the language.")

    if clear_score < 50:
        suggestions.append("The document appears not to be clear or direct. Consider using simpler words.")

    # Split the documentation into sentences
    sentences = nltk.sent_tokenize(documentation)
    for sentence in sentences:
        score = textstat.flesch_reading_ease(sentence)
        if score < 40:
            suggestions.append("The sentence: '{}' has a low readability score of {}. Consider simplifying the language.".format(sentence, score))
        # Perform named entity recognition
        entities = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence)))
        for entity in entities:
            if hasattr(entity, 'label'):
                if entity.label() == 'PERSON':
                    suggestions.append("The use of proper names such as "+str(entity)+" can sometimes be confusing and can be replaced with more general terms.")
    return suggestions

def scan_documentation(file: str) -> float:
    # read the documentation file
    with open(file, 'r') as f:
        documentation = f.read()

    # remove the header
    documentation = remove_header(documentation)
    
    # parse the markdown and get the plain text
    documentation = parse_markdown(documentation)
    
    # remove any HTML tags from the documentation
    documentation = clean_html(documentation)

    # remove any invalid characters from the documentation string
    documentation = re.sub(r'[^\x00-\x7F]+', '', documentation)

    # check the tone of the documentation
    check_tone(documentation)
   
    # score the documentation
    score = score_documentation(documentation)
    
    # get suggestions for improvement
    suggestions = suggest_improvements(documentation)
    
    # print the score and suggestions
    print("Score:",score)
    for suggestion in suggestions:
        print(suggestion)
    return score




def scan_all_documentations(root_dir: str):
    scores = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                score = scan_documentation(file_path)
                scores.append(score)
                print('File:', file)
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            scores.extend(scan_all_documentations(subdir_path))
    return scores


def main():
    root_dir = '/path'
    scores = scan_all_documentations(root_dir)
    # print(scores)

if __name__ == '__main__':
    main()
