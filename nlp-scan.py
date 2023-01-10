import os
import re
import ast
import nltk
from textstat.textstat import textstat
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

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

def suggest_improvements(documentation: str):
    # suggestions for improvement
    suggestions = []
    
    # Use the Flesch–Kincaid readability test
    score = textstat.flesch_kincaid_grade(documentation)
    if score > 12:
        suggestions.append("The document appears to be written at a higher reading level than the target audience. Consider simplifying the language.")
    elif score < 6:
        suggestions.append("The document appears to be written at a lower reading level than the target audience. Consider using more complex vocabulary.")
    
    # Prepare the classification model
    tfidf = TfidfVectorizer()
    clf = LinearSVC()
    
    # Train the model on a set of labeled documents
    X_train = ["This is a positive document", "This is a negative document", "This document is neutral"]
    y_train = ["positive", "negative", "neutral"]
    X_train = tfidf.fit_transform(X_train)
    clf.fit(X_train, y_train)
    
    # Vectorize and classify the new document
    X_new = tfidf.transform([documentation])
    y_pred = clf.predict(X_new)[0]
    
    # Make suggestions based on the classification results
    if y_pred == "positive":
        suggestions.append("The document appears to be positive. Keep up the good work!")
    elif y_pred == "negative":
        suggestions.append("The document appears to be negative. Consider revising it to be more positive.")
    elif y_pred == "neutral":
        suggestions.append("The document appears to be neutral. Consider adding more opinion or emotion to it.")
    
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
    root_dir = '/Users/kanariesdev04/kanaries-docs/docs/rath'
    scores = scan_all_documentations(root_dir)
    # print(scores)

if __name__ == '__main__':
    main()
