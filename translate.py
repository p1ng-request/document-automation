import os
import re
from transformers import pipeline

# Define the source and target directories
source_dir = "/input-path"
target_dir = "/output-path"

# Define the translator
translator = pipeline("translation_en_to_zh", model="Helsinki-NLP/opus-mt-en-zh")

# Iterate through the files in the source directory
if not os.path.exists(target_dir):
    os.makedirs(target_dir)
for file in os.listdir(source_dir):
    if file.endswith(".md"):
        print(f'Processing file {file}')
        with open(os.path.join(source_dir, file), "r") as f:
            source_text = f.read()
            
        # Split the text into smaller parts
        parts = source_text.split("\n")
        
        # Translate the title and description fields
        title_match = re.search(r"title: \"(.+)\"", source_text, re.IGNORECASE)
        description_match = re.search(r"description: (.+)", source_text, re.IGNORECASE)
        
        for i in range(len(parts)):
            if not (re.match(r"id:", parts[i]) or re.match(r"slug:", parts[i]) or re.match(r"keywords:", parts[i]) or re.search(r"!\[.+\]\(.+\)", parts[i])):
                if parts[i].startswith("#"):
                    parts[i] = "#"+translator(parts[i][1:])[0]["translation_text"]
                elif parts[i].startswith("title:") or parts[i].startswith("description:"):
                    title_desc = parts[i].split(':',1)
                    parts[i] = title_desc[0] + ":" + translator(title_desc[1])[0]["translation_text"]
                elif not re.search(r"^<.+>$", parts[i]):
                    parts[i] = translator(parts[i])[0]["translation_text"]
            
        # Join the translated parts back together
        target_text = "\n".join(parts)
        
        # Save the translated text to the target directory
        with open(os.path.join(target_dir, file), "w") as f:
            f.write(target_text)

# os.chdir(target_dir)
# os.system("git add .")
# os.system('git commit -m "Translation of files complete"')
# os.system("git push myrepourl")
# print("All files pushed to Github repository")
