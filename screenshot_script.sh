#!/bin/bash

PICSDIR=/var/www/images

while true; do
  ffmpeg -y -i rtmp://localhost/mytv/$1 -an -vframes 1 "$PICSDIR/$1.jpg"
  sleep 5
done
