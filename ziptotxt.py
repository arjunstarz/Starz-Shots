import zipfile
from zipfile import ZipFile

zip_path = 'C:\\Users\\arjp\\Downloads\\10.zip'
output_file = '10.txt'
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    file_names = zip_ref.namelist()

with open(output_file, 'w') as f:
    for name in file_names:
        f.write(name + '\n')

print ("End of file")
