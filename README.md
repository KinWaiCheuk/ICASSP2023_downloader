# ICASSP 2023 paper/video/poster downloader
This code requires python 3.8.10 or above.

This script downloads the papers and the presentations published in ICASSP given the paper ID. The use is as easy as follows

## Step 1: Provide the paper IDs
Find the paper IDs that you are interested in [icassp-2023-program_22.pdf](icassp-2023-program_22.pdf), and then put it inside the [paper_ids.txt](paper_ids.txt). Each line of the [paper_ids.txt](paper_ids.txt) coressponds to one set of paper and its presentation materials.

## Step 2: Run the download script

Run the following script to download the papers and presentation materials:

```
python ICASSP_downloader.py paper_ids.txt -c 8
```

The argument `-c` controls how many downloads are allowed concurrently. The higher the values, the faster the download is. The default value is 8, whcih means that 8 files can be downloaded at the same time.

The output file `download_error.log` records the files failed to be downloaded. It fails mostly likely because the author did not upload the material.