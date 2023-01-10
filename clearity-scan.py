import os
import re
import ast
import nltk
from textstat.textstat import textstat
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('vader_lexicon')

def score_documentation(documentation: str) -> float:
    # Split the documentation into sentences using NLTK's sent_tokenize() function
    sentences = nltk.sent_tokenize(documentation)
    num_sentences = len(sentences)
    
    # Split the documentation into words using NLTK's word_tokenize() function
    words = nltk.word_tokenize(documentation)
    num_words = len(words)
    
    # Compute the score as the ratio of the number of words to the number of sentences
    score = num_words / num_sentences
    
    return score

from textstat.textstat import textstat


def suggest_improvements(documentation: str):
    suggestions = []
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(documentation)
    for sentence in sentences:
        # Perform named entity recognition
        entities = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence)))
        for entity in entities:
            if hasattr(entity, 'label'):
                if entity.label() == 'PERSON':
                    suggestions.append("The use of proper names such as "+str(entity)+" can sometimes be confusing and can be replaced with more general terms.")
    return suggestions


def scan_documentation(path: str) -> float:
    # read the documentation file
    with open(path, 'r') as f:
        documentation = f.read()

    # # remove the --- character from the documentation string
    documentation = documentation.replace('---', '')

    # # remove any invalid characters from the documentation string
    documentation = re.sub(r'[^\x00-\x7F]+', '', documentation)

    # # remove links that starts with ( and ends with )
    documentation = re.sub(r'\([^)]*\)', '', documentation)

    # split the documentation string into a list of lines
    lines = documentation.split('\n')

    # join the remaining lines back into a single string
    documentation = '\n'.join(lines)
    
    # parse the documentation using AST
    # tree = ast.parse(documentation)

    # score the documentation
    score = score_documentation(documentation)
    suggestions = suggest_improvements(documentation)
    
    print("Score:",score)
    # Print the suggestions
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
