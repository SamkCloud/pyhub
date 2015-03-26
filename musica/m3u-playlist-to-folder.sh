#!/bin/sh

# copia tutti i file musicali in una playlist m3u in una cartella

IN_FILE=$1
OUT_DIR=$2

grep -v -E '(^#|^$)' $IN_FILE | while read -r line ; do
    echo "Processing $line"
	cp "$line" "$OUT_DIR"
  
done