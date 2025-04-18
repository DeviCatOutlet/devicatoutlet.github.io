#!/bin/sh

# Check if magick and cwebp are installed
if ! command -v magick >/dev/null 2>&1; then
    echo "Error: ImageMagick (magick) is not installed."
    exit 1
fi
if ! command -v cwebp >/dev/null 2>&1; then
    echo "Error: cwebp is not installed."
    exit 1
fi

# Use find to locate .jpg, .jpeg, and .png files
for file in *.jpg *.jpeg *.png; do
    # Check if file exists and is a regular file
    if [ -f "$file" ]; then
        echo "Processing $file..."

        # Extract base filename
        base=$(echo "$file" | sed 's/\.[^.]*$//')

        # Resize with magick: height 1080, strip metadata, denoise
        magick "$file" -strip "${base}_magick.jpg"
        if [ $? -ne 0 ]; then
            echo "Error: magick failed for $file"
            continue
        fi

        # Compress to WebP with cwebp
        cwebp -q 50 -m 6 -preset photo -low_memory -af -sharp_yuv -pass 10 -segments 3 -metadata none "${base}_magick.jpg" -o "${base}.webp"
        if [ $? -ne 0 ]; then
            echo "Error: cwebp failed for $file"
            rm -f "${base}_magick.jpg"
            continue
        fi

        # Clean up intermediate file
        rm -f "${base}_magick.jpg"
        echo "Created ${base}.webp"
    fi
done

# Check if any files were processed
if ! ls *.webp >/dev/null 2>&1; then
    echo "No .jpg, .jpeg, or .png images were found or processed."
fi