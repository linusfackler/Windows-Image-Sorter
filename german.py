import os
import datetime
import locale
from PIL import Image

# Set the locale to German
locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

def get_file_creation_date(file_path):
    try:
        # Attempt to get date from EXIF data if the file is an image
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            with Image.open(file_path) as img:
                exif_data = img._getexif()
                if exif_data:
                    date_string = exif_data.get(36867, 'Unknown')  # 36867 corresponds to DateTimeOriginal
                    if date_string != 'Unknown':
                        return datetime.datetime.strptime(date_string, '%Y:%m:%d %H:%M:%S').date()
    except Exception as e:
        print(f"Failed to retrieve EXIF creation date for {file_path} due to {e}")

    # Fallback to file modification date for all files (including .mov and .mp4)
    try:
        mod_time = os.path.getmtime(file_path)
        return datetime.datetime.fromtimestamp(mod_time).date()
    except Exception as e:
        print(f"Failed to retrieve file modification date for {file_path} due to {e}")

    return None

def main():
    current_directory = os.getcwd()
    file_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mov', '.mp4']

    for filename in os.listdir(current_directory):
        if filename.lower().endswith(tuple(file_extensions)):
            file_date = get_file_creation_date(filename)
            
            if file_date:
                folder_name = f"{file_date.year} - {file_date.strftime('%B')}"
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                os.rename(filename, os.path.join(folder_name, filename))

if __name__ == "__main__":
    main()
