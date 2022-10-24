from pathlib import Path
import shutil
import sys
from normalize import normalize

# folder_for_scan = "D:\Sort"
def main(folder_for_scan):
    REGISTER_EXTENSIONS = {
        'IMAGES' : ['JPEG', 'PNG', 'JPG', 'SVG'],
        'TXT_DOCUMENTS' : ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
        'MUSIC' : ['MP3', 'OGG', 'WAV', 'AMR'],
        'VIDEO' : ['AVI', 'MP4', 'MOV', 'MKV'],
        'ARCHIVES' : ['ZIP', 'GZ', 'TAR']
    }

    FILES = {
        'IMAGES' : [],
        'TXT_DOCUMENTS' : [],
        'MUSIC' : [],
        'VIDEO' : [],
        'ARCHIVES' : [],
        'UNKN' : []
    }
    FOLDERS = []

    def parser(folder: Path) -> None:
        for item in folder.iterdir():
            if item.is_dir():
                if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'unknown'):
                    FOLDERS.append(item)
                    parser(item)
                continue
            ext = Path(item.name).suffix[1:].upper()
            fullname = folder / item.name
            if not ext:
                FILES['UNKN'].append(fullname)
            else:
                try:
                    for key, val in REGISTER_EXTENSIONS.items():
                        if ext in val:
                            FILES[key].append(fullname)
                except KeyError:
                    UNKNOWN.add(ext)
                    FILES['UNKN'].append(fullname)

    def handle_media(filename: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / normalize(filename.name))
    def handle_archive(filename: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
        folder_for_file.mkdir(exist_ok=True, parents=True)
        try:
            shutil.unpack_archive(str(filename.resolve()), str(folder_for_file.resolve()))
        except shutil.ReadError:
            print(f'Це не архів {filename}!')
            folder_for_file.rmdir()
            return None
        filename.unlink()
    def handle_folder(folder: Path):
        try:
            folder.rmdir()
        except OSError:
            print(f'Помилка видалення папки {folder}')
    def scan(folder):
        for file in FILES['IMAGES']:
            handle_media(file, folder / 'images')
        for file in FILES['TXT_DOCUMENTS']:
            handle_media(file, folder / 'documents')
        for file in FILES['MUSIC']:
            handle_media(file, folder / 'audio')
        for file in FILES['VIDEO']:
            handle_media(file, folder / 'video')
        for file in FILES['UNKN']:
            handle_media(file, folder / 'unknown')
        for file in FILES['ARCHIVES']:
            handle_archive(file, folder / 'archives')
        for folder in FOLDERS[::-1]:
            handle_folder(folder)
    parser(Path(folder_for_scan))
    scan(Path(folder_for_scan))

if __name__ == '__main__':
    try:
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder {folder_for_scan.resolve()}')
    except IndexError:
        print(f'Enter link to folder')
    else:
        main(folder_for_scan.resolve())