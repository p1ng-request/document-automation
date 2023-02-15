## Resize an image
```bash
convert 0.png -resize 800x 1.png
```

## Compress an image
```bash
convert -strip -interlace Plane -resize 800x600 -gaussian-blur 0.05 -quality 85% 0.png 1.png
```

## Convert a video to WebP/GIF
```bash
ffmpeg -filter_complex "[0:v] fps=12,scale=w=800:h=-1,split [a][b];[a] palettegen [p];[b][p] paletteuse" -i 0.mov 1.webp
```

## Reduce Video Size
```bash
 ffmpeg -i 0.mov -vcodec libx265 -crf 28 1.mp4
```
