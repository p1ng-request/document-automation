import os
import re
import nltk
import textstat
from typing import List, Tuple
from pathlib import Path
import markdown
from nltk.sentiment import SentimentIntensityAnalyzer
from language_tool_python import LanguageTool
import json

nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')

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
    cleanr = re.compile('```.*?```|<.*?>')
    cleantext = re.sub(cleanr, '', documentation, flags=re.DOTALL)
    return cleantext

def check_tone(documentation: str) -> str:
    # Check for Tone in the text
    # Create an instance of the sentiment intensity analyzer
    sentiment_analyzer = SentimentIntensityAnalyzer()
    # Get the sentiment score of the documentation
    sentiment_score = sentiment_analyzer.polarity_scores(documentation)
    if sentiment_score['compound'] < -0.5:
        print("\033[1;31;40m The documentation is written in a very negative tone. \033[0m")
    elif sentiment_score['compound'] < 0:
        print("\033[1;31;40m The documentation is written in a negative tone. \033[0m")
    elif sentiment_score['compound'] == 0:
        print("\033[1;33;40m The documentation is written in a neutral tone. \033[0m")
    elif sentiment_score['compound'] > 0:
        print("\033[1;32;40m The documentation is written in a positive tone. \033[0m")
    elif sentiment_score['compound'] > 0.5:
        print("\033[1;32;40m The documentation is written in a very positive tone. \033[0m")

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
        print("\033[1;31;47m ✗ There are grammatical and/or spelling errors in the document. \033[0m \033[1;31;47m Consider running the document through a grammar and spell checker. \033[0m")
        suggestions.append(("There are grammatical and/or spelling errors in the document. Consider running the document through a grammar and spell checker.", "Grammar and Spelling"))
    # Check if the documentation has an objective tone
    objective_score = textstat.automated_readability_index(documentation)
    clear_score = textstat.flesch_reading_ease(documentation)
    if fk_score > 18:
        print("\033[1;31;40m ✗ The document appears to be written at a higher reading level than the target audience. \033[0m \033[1;33;40m Consider simplifying the language. \033[0m")
        suggestions.append(("The document appears to be written at a higher reading level than the target audience. Consider simplifying the language.", "Readability"))
    elif fk_score < 10:
        print("\033[1;32;40m ✗ The document appears to be written at a lower reading level than the target audience. Consider using more complex vocabulary. \033[0m")
        suggestions.append(("The document appears to be written at a lower reading level than the target audience. Consider using more complex vocabulary.", "Readability"))
    if coleman_score > 18:
        print("\033[1;31;40m ✗ The document appears to be written at a higher reading level than the target audience. \033[0m \033[1;33;40m Consider simplifying the language. \033[0m")
        suggestions.append(("The document appears to be written at a higher reading level than the target audience. Consider simplifying the language.", "Readability"))
    elif coleman_score < 10:
        print("\033[1;32;40m ✗ The document appears to be written at a lower reading level than the target audience. \033[0m \033[1;33;40m Consider using more complex vocabulary. \033[0m")
        suggestions.append(("The document appears to be written at a lower reading level than the target audience. Consider using more complex vocabulary.", "Readability"))
    if objective_score > 18:
        print("\033[1;36;40m The document appears to be written in an objective tone. \033[0m")
        suggestions.append(("The document appears to be written in an objective tone.", "Objectivity"))
    elif objective_score < 10:
        print("\033[1;36;40m The document appears to be written in a subjective tone. \033[0m")
        suggestions.append(("The document appears to be written in a subjective tone.", "Objectivity"))
    if clear_score < 30:
        print("\033[1;31;40m ✗ The document appears to be difficult to read. Consider simplifying the language.\033[0m")
        suggestions.append(("The document appears to be difficult to read. Consider simplifying the language.", "Readability"))
    # Split the documentation into sentences
    sentences = nltk.sent_tokenize(documentation)
    for sentence in sentences:
        score = textstat.flesch_reading_ease(sentence)
        if score < 10:
            print("\033[1;31;40m ✗ The sentence: '{}' has a low readability score of {}. \033[0m \033[1;33;40m Consider simplifying the language. \033[0m".format(sentence, score))
            suggestions.append("The sentence: '{}' has a low readability score of {}. Consider simplifying the language.".format(sentence, score))
        # Perform named entity recognition
        # entities = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence)))
        # for entity in entities:
        #     if hasattr(entity, 'label'):
        #         if entity.label() == 'PERSON':
        #             suggestions.append("The use of proper names such as "+str(entity)+" can sometimes be confusing and can be replaced with more general terms.", "Clearity")
        # Import the terminology dictionary from a file
        with open('terminology_dict.json', 'r') as file:
            terms_dict = json.load(file)
        # Term/Terminology-Consistency checker
        try:
            with open("terminology_dict.txt", "r") as f:
                terms_dict = json.load(f)
        except FileNotFoundError:
            print("\033[1;31;47mTerminology dictionary file not found.\033[0m")
            return suggestions
        except json.decoder.JSONDecodeError as e:
            print("\033[1;31;47mError loading terminology dictionary file: {}\033[0m".format(e))
            return suggestions

        words = nltk.word_tokenize(documentation)
        # Check the consistency of the terms used in each sentence
        sentences = nltk.sent_tokenize(documentation)
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            for word in words:
                if word not in terms_dict:
                    print("\033[1;31;47m ✗ The word '{}' is not consistent with the terms found in the rest of the documentation.\033[0m".format(word))
                    suggestions.append(("The word '{}' is not consistent with the terms found in the rest of the documentation.".format(word), "Consistency"))
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
    root_dir = '/path/'
    scores = scan_all_documentations(root_dir)
    with open("output.txt", "w") as file:
        file.write(check_tone(scores))

if __name__ == '__main__':
    main()
