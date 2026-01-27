import os
import zipfile

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
