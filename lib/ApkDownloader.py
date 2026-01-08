import os
import zipfile
import cloudscraper
import shutil

from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

class FileDownloader:
    def __init__(self, url, download_dir, filename):
        self.url = url
        self.local_filepath = os.path.join(download_dir, filename)
        os.makedirs(download_dir, exist_ok=True)
        self.scraper = cloudscraper.create_scraper()
        
        cpu_threads = os.cpu_count() or 1
        if cpu_threads >= 4:
            self.thread_count = cpu_threads // 2
        else:
            self.thread_count = cpu_threads

    def download(self):
        try:
            head = self.scraper.head(self.url, allow_redirects=True, timeout=10)
            total_size = int(head.headers.get('content-length', 0))
            accept_ranges = head.headers.get('Accept-Ranges', '').lower()

            if total_size > 0 and 'bytes' in accept_ranges:
                return self._multi_threaded_download(total_size)
            else:
                return self._standard_download()
        except Exception as e:
            print(f"Setup failed, falling back: {e}")
            return self._standard_download()

    def _standard_download(self):
        r = self.scraper.get(self.url, stream=True, allow_redirects=True)
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))
        
        with tqdm.wrapattr(r.raw, "read", total=total, desc="Standard") as stream:
            with open(self.local_filepath, 'wb') as f:
                shutil.copyfileobj(stream, f)
        return True

    def _multi_threaded_download(self, total_size):
        with open(self.local_filepath, 'wb') as f:
            f.truncate(total_size)

        chunk_size = total_size // self.thread_count
        ranges = []
        for i in range(self.thread_count):
            start = i * chunk_size
            end = (i + 1) * chunk_size - 1 if i < self.thread_count - 1 else total_size - 1
            ranges.append((start, end))

        with tqdm(total=total_size, unit='B', unit_scale=True, desc="Fast") as pbar:
            with ThreadPoolExecutor(max_workers=self.thread_count) as executor:
                futures = [executor.submit(self._download_chunk, s, e, pbar) for s, e in ranges]
                for future in futures:
                    future.result()
        return True

    def _download_chunk(self, start, end, pbar):
        headers = {'Range': f'bytes={start}-{end}'}
        resp = self.scraper.get(self.url, headers=headers, stream=True)
        with open(self.local_filepath, 'rb+') as f:
            f.seek(start)
            for chunk in resp.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))

class FileExtractor:
    def __init__(self, file_path, extract_dir, version="jp"):
        self.file_path = file_path
        self.extract_dir = extract_dir
        self.apk_files = {
            'config.arm64_v8a.apk': os.path.join(self.extract_dir, 'config_arm64_v8a'),
        }
        if version == "global":
            pkg_filename = "com.nexon.bluearchive.apk"
        else:
            self.apk_files['UnityDataAssetPack.apk'] = os.path.join(self.extract_dir, 'UnityDataAssetPack')
            pkg_filename = "com.YostarJP.BlueArchive.apk"
        self.apk_files[pkg_filename] = os.path.join(self.extract_dir, 'BlueArchive_apk')
        os.makedirs(self.extract_dir, exist_ok=True)

    def extract_xapk(self):
        try:
            with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                zip_ref.extractall(self.extract_dir)
            print(f"Extracted {self.file_path} to {self.extract_dir}")
        except Exception as e:
            print(f"Error extracting {self.file_path}: {e}")
            return
        
        for apk_name, dest_dir in self.apk_files.items():
            print(apk_name, dest_dir)
            self.extract_apk(apk_name, dest_dir)
    
    def extract_il2cppData(self):
        destination_dir = os.path.join(self.extract_dir, 'Il2CppInspector')
        os.makedirs(destination_dir, exist_ok=True)
        
        try:
            with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                zip_ref.extractall(destination_dir)
            print(f"Extracted {self.file_path} to {destination_dir}")
        except Exception as e:
            print(f"Error extracting {self.file_path}: {e}")

    def extract_depotdownloader(self):
        destination_dir = os.path.join(self.extract_dir, 'DepotDownloader')
        os.makedirs(destination_dir, exist_ok=True)
        
        try:
            with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                zip_ref.extractall(destination_dir)
            print(f"Extracted {self.file_path} to {destination_dir}")
        except Exception as e:
            print(f"Error extracting {self.file_path}: {e}") 

    def extract_fbsdumper(self):
        destination_dir = os.path.join(self.extract_dir, 'FbsDumper')
        os.makedirs(destination_dir, exist_ok=True)
        
        try:
            with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                zip_ref.extractall(destination_dir)
            print(f"Extracted {self.file_path} to {destination_dir}")
        except Exception as e:
            print(f"Error extracting {self.file_path}: {e}") 

    def extract_apk(self, apk_filename, destination_dir):
        apk_path = os.path.join(self.extract_dir, apk_filename)
        if os.path.exists(apk_path):
            os.makedirs(destination_dir, exist_ok=True)
            try:
                with zipfile.ZipFile(apk_path, 'r') as apk_zip:
                    apk_zip.extractall(destination_dir)
                print(f"Extracted {apk_filename} to {destination_dir}")
            except Exception as e:
                print(f"Error extracting {apk_filename}: {e}")
        else:
            print(f"{apk_filename} not found in {self.extract_dir}")
