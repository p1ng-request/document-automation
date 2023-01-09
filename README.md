## Common best pracitces

### Insert an image for Markdown
``` html
<center><img loading="lazy" src="/img/view-modes-rath.webp" alt="View modes in RATH" width="800" height="600"/></center>
```
### Image processing
```bash
convert -strip -interlace Plane -resize 800x600 -gaussian-blur 0.05 -quality 85% source.png result.webp
```

### Compress GIF
```bash
ffmpeg -i source.mov -vf "fps=10,scale=1000:-1:flags=lanczos" -c:v pam \
    -f image2pipe - | \
    convert -delay 10 - -loop 0 -layers optimize result.webp
```

## Handy scripts
+ check-dead-links.py: A python script to check the dead links of a given web domain.
