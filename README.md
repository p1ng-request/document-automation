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
++ Analyze the documentation's readability using a readability test such as the Flesch-Kincaid readability test and the Coleman-Liau index to evaluate the readability of the documentation and make suggestions for improvements.
