import os
import re
import ast
import nltk
from textstat.textstat import textstat

def score_documentation(documentation: str) -> float:
    # Compute the Flesch-Kincaid readability test
    fk_score = textstat.flesch_kincaid_grade(documentation)
    return fk_score
    # Compute the Gunning Fog Index
    # fog_index = textstat.gunning_fog(documentation)
    # return fog_index
    # Compute the Automated Readability Index
    # ari = textstat.automated_readability_index(documentation)
    # return ari

def suggest_improvements(documentation: str):
    suggestions = []
    
    # Split the documentation into sentences
    sentences = nltk.sent_tokenize(documentation)
    
    for sentence in sentences:
        score = textstat.flesch_reading_ease(sentence)
        if score < 40:
            suggestions.append("The sentence: '{}' has a low readability score of {}. Consider simplifying the language.".format(sentence, score))
    
    # Compute the Flesch-Kincaid readability test
    fk_score = textstat.flesch_kincaid_grade(documentation)
    coleman_score = textstat.coleman_liau_index(documentation)
    if fk_score > 18:
        suggestions.append("The document appears to be written at a higher reading level than the target audience. Consider simplifying the language.")
    elif fk_score < 10:
        suggestions.append("The document appears to be written at a lower reading level than the target audience. Consider using more complex vocabulary.")
    if coleman_score > 18:
        suggestions.append("The document appears to be written at a higher reading level than the target audience. Consider simplifying the language.")
    elif coleman_score < 12:
        suggestions.append("The document appears to be written at a lower reading level than the target audience. Consider using more complex vocabulary.")
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
