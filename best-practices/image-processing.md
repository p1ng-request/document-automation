## Compress an image
```bash
convert -strip -interlace Plane -resize 800x600 -gaussian-blur 0.05 -quality 85% source.png result.webp
```

## Convert a video to WebP/GIF
```bash
ffmpeg -filter_complex "[0:v] fps=12,scale=w=540:h=-1,split [a][b];[a] palettegen [p];[b][p] paletteuse" -i clip.mov clip.webp
```
