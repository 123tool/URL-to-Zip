import zipfile
import os

def create_zip(source_folder, output_filename):
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                # Menjaga struktur folder tetap benar di dalam ZIP
                zipf.write(file_path, os.path.relpath(file_path, os.path.join(source_folder, '..')))
    return output_filename
