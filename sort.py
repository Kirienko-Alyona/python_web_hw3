import os 
import shutil
from pathlib import Path
import sys
from concurrent.futures import ThreadPoolExecutor


list_extensions = []
unknown_files = []
path = Path(r".\\can_sorted\\")
archives = Path(path, "archives")
images = Path(path, "images")
documents = Path(path, "documents")
video = Path(path, "video")
audio = Path(path, "audio")
unknown_extension = Path(path, "unknown_extension")

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

def main(folder: Path):
    sorted(folder)
    return

def sorted(path: Path):   
    for element in path.iterdir():
        if element.is_dir():
            with ThreadPoolExecutor(max_workers = 5) as executor:
                executor.submit(sorted, element)  
            
            if element == images or element == video or element == archives or element == documents or element == audio or element == unknown_extension:
                continue
            else:
                try:
                    os.rmdir(element)
                except:
                    sorted(element)
        else:
            rename_element = normalize(element)
            sorted_files(rename_element)        
    return

def sorted_files(file: Path):      
    file_extension = file.suffix
    file_extension = file_extension.casefold()         
    if file_extension == ".zip" or file_extension == ".gz" or file_extension == ".tar":
        archives.mkdir(parents=True, exist_ok=True)
        name_folder = file.name 
        name_folder = name_folder.removesuffix(file_extension)
        new_path = archives / name_folder
        new_path.mkdir(parents=True, exist_ok=True)
        shutil.unpack_archive(file, new_path)
        shutil.move(file, archives)
        list_extensions.append(file_extension)  
    elif file_extension == ".png" or file_extension == ".jpeg" or file_extension == ".jpg" or file_extension == ".svg":
        images.mkdir(parents=True, exist_ok=True)
        shutil.move(file, images)   
        list_extensions.append(file_extension)
    elif file_extension ==".doc" or file_extension == ".docx" or file_extension == ".txt" or file_extension == ".pdf" or file_extension == ".xlsx" or file_extension == ".pptx":
        documents.mkdir(parents=True, exist_ok=True)
        shutil.move(file, documents) 
        list_extensions.append(file_extension)
    elif file_extension == ".avi" or file_extension == ".mp4" or file_extension == ".mov" or file_extension == ".mkv":
        video.mkdir(parents=True, exist_ok=True)
        shutil.move(file, video) 
        list_extensions.append(file_extension)
    elif file_extension == ".mp3" or file_extension == ".ogg" or file_extension == ".wav" or file_extension == ".amr":
        audio.mkdir(parents=True, exist_ok=True)
        shutil.move(file, audio) 
        list_extensions.append(file_extension)
    else:
        unknown_extension.mkdir(parents = True, exist_ok = True)
        shutil.move(file, unknown_extension) 
        unknown_files.append(file_extension)             
    return list_extensions, unknown_files


def delete_dublicate_extensions(extensions):    
    new_list_extensions = []
    for elem in extensions:
        if elem not in new_list_extensions:
            new_list_extensions.append(elem)
    return new_list_extensions


def normalize(file):
    file_name = file.name
    new_name = file_name.translate(TRANS)        
    file_name_path = Path(file)
    l = os.path.split(file)
    new_name_path = Path(l[0], new_name)
    os.rename(file_name_path, new_name_path)    
    return new_name_path   

def start_terminal(path):
    
    try:
        
        folder_for_scan = Path(sys.argv[1])
        main(folder_for_scan.resolve())
        known_extensions = delete_dublicate_extensions(list_extensions)
        unknown_extensions = delete_dublicate_extensions(unknown_files)
        print(f"Список відомих розширень файлів: {known_extensions}")
        print(f"Список невідомих розширень файлів: {unknown_extensions}")
    except IndexError:
        print(f"Введіть шлях до папки - змінна path")   
    return 


if __name__ == '__main__':        
    start_terminal(path)
    