#/bin/sh
# riconverte un'immagine jpg per ridurre la qualità e la dimensione

#convert -strip -interlace Plane -gaussian-blur 0.05 -quality 85% src.jpg dst.jpg

convert -strip -interlace Plane -gaussian-blur 0.05 -quality 85% $1 $1