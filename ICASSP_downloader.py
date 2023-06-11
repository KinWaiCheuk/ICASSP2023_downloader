import argparse
# import urllib.request
import requests
from pathlib import Path
import concurrent.futures
from tqdm.auto import tqdm
import os
import shutil


# https://confcats-event-sessions.s3.amazonaws.com/icassp23/videos/1615.mp4
# https://confcats-event-sessions.s3.amazonaws.com/icassp23/posters/1615.pdf

def append_id(filename, media):
    p = Path(filename)
    return "{0}_{2}{1}".format(p.stem, p.suffix, media)

def download_file(media, paperID, verbose, log_file):
    if media == "videos":
        url = f"https://confcats-event-sessions.s3.amazonaws.com/icassp23/{media}/{paperID}.mp4"
    else:
        url = f"https://confcats-event-sessions.s3.amazonaws.com/icassp23/{media}/{paperID}.pdf"
        

    # make an HTTP request within a context manager
    with requests.get(url, stream=True) as r:
        basename = os.path.basename(r.url)
        basename = append_id(basename, media)
        # check header to get content length, in bytes
        try:
            total_length = int(r.headers.get("Content-Length"))

            # implement progress bar via tqdm
            with tqdm.wrapattr(r.raw, "read", total=total_length, desc=f"{basename}")as raw:

                # save the output to a file
                with open(f"{basename}", 'wb')as output:
                    shutil.copyfileobj(raw, output)
        except Exception as e:
            with open(log_file, "a") as log:
                log.write(f"{basename} Not found. Probably the author did not upload it.\n")            

def main():
    parser = argparse.ArgumentParser(description="File Downloader")
    parser.add_argument("file", metavar="FILE", type=str,
                        help="Path to the text file containing URLs")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Display verbose output")
    parser.add_argument("-l", "--log", type=str, default="download.log",
                        help="Path to the log file (default: download_error.log)")
    parser.add_argument("-c", "--concurrent", type=int, default=5,
                        help="Number of concurrent downloads (default: 5)")
    args = parser.parse_args()
    
    if os.path.exists(args.log):
        os.remove(args.log)    

    with open(args.file, "r") as file:
        ID_list = file.read().splitlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrent) as executor:
        futures = []
        for paper_id in ID_list:
            for media in ['papers', 'posters', 'slides']: # remember to add videos
                future = executor.submit(download_file, media, paper_id, args.verbose, args.log)
                futures.append(future)

        # Wait for all downloads to complete
        concurrent.futures.wait(futures)
        
if __name__ == "__main__":
    main()