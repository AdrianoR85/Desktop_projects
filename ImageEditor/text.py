import os

path = os.path.join(os.path.expanduser("~"), 'Pictures', 'ImagesEditor')

file_name = os.path.basename(path)
destination_path = os.path.join(path, file_name)

