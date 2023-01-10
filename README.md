# Automation scripts

[check-dead-links.py](https://github.com/p1ng-request/automation-scripts-best-pracitces/blob/main/check-dead-links.py): A Python script to scan dead links from a given web domain.

[npl-scan.py](https://github.com/p1ng-request/automation-scripts/blob/main/nlp-scan.py): Basic Docs automation tool in Python. Features:
+ Scan all the .md files in a given directory and all the sub-directories.
+ Use machine learning models to classify the documentation and make suggestions based on the classification results.
+ Generate a Flesch-Kincaid readability test score for each doc.

[deeper-npl-scan.py](https://github.com/p1ng-request/automation-scripts/blob/main/deeper-nlp-scan.py): Scan docs using NLP
+ Utilizing natural language processing(NLP) techniques to determine complicated words by breaking down the text into individual sentences, followed by computing the Flesch-Kincaid Reading Ease score for each sentence to evaluate readability.

[deeper-ner-scan.py](https://github.com/p1ng-request/automation-scripts/blob/main/deeper-ner-scan.py): Scan docs using NER
+ Apply named entity recognition (NER) to identify specific entities within the text and make suggestions for improvements.

# Common best pracitces

## Compress an image
```bash
convert -strip -interlace Plane -resize 800x600 -gaussian-blur 0.05 -quality 85% source.png result.webp
```

## Convert a video to WebP/GIF
```bash
ffmpeg -filter_complex "[0:v] fps=12,scale=w=540:h=-1,split [a][b];[a] palettegen [p];[b][p] paletteuse" -i clip.mov clip.webp
```
