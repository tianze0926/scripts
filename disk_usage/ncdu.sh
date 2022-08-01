# scan
sudo ncdu -1xo- / | gzip >export.gz

# view
zcat export.gz | ncdu -f-