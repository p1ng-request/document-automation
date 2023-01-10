# Common best pracitces

## Insert an image for Markdown
``` html
<center><img loading="lazy" src="/img/sample.webp" alt="desc" width="800" height="600"/></center>
```
## Image processing
```bash
convert -strip -interlace Plane -resize 800x600 -gaussian-blur 0.05 -quality 85% source.png result.webp
```

## Compress GIF
```bash
ffmpeg -i source.mov -vf "fps=10,scale=1000:-1:flags=lanczos" -c:v pam \
    -f image2pipe - | \
    convert -delay 10 - -loop 0 -layers optimize result.webp
```

# Handy scripts
+ [check-dead-links.py](https://github.com/p1ng-request/automation-scripts-best-pracitces/blob/main/check-dead-links.py): A Python script to scan dead links from a given web domain.
+ [npl-scan.py](https://github.com/p1ng-request/automation-scripts/blob/main/nlp-scan.py): Basic Docs automation tool in Python. Features:
++ Scan all the .md files in a given directory and all the sub-directories.
++ Use machine learning models to classify the documentation and make suggestions based on the classification results.
++ Generate a Flesch-Kincaid readability test score for each doc.
+ [deeper-npl-scan.py](https://github.com/p1ng-request/automation-scripts/blob/main/deeper-nlp-scan.py): Deeper scan of docs
+ + use readability statistics to identify specific areas of the document that are difficult to understand
+ + tokenize the text into sentences and then compute the Flesch-Kincaid Reading Ease score for each sentence. 
