import os
import argparse

from lib.FileExtractor import FileExtractor
from lib.FileDownloader import FileDownloader
from lib.ApkProviderFetcher import get_apk_url

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download & extract Blue Archive Android Data"
    )
    parser.add_argument(
        "--client",
        choices=["global", "jp"],
        default="jp",
        help="Which game client to download (default: jp)",
    )
    args = parser.parse_args()
    
    client = args.client

    download_dir = os.path.join(os.getcwd(), f'apk_downloads')
    extract_dir = os.path.join(os.getcwd(), f'{client}_extracted')

    if client == "global":
        pkg = "com.nexon.bluearchive"
    else:
        pkg = "com.YostarJP.BlueArchive"

    # Download and Extract the Game XAPK
    print(f"Downloading {client} Data...")
    xapk_url = get_apk_url(pkg)
    downloader = FileDownloader(xapk_url, download_dir, f"{pkg}.xapk")
    downloader.download()
    FileExtractor(downloader.local_filepath, extract_dir, client).extract_xapk()
        
    print("Successfully downloaded and extracted files")