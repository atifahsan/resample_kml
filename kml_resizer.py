import os
import glob

FOLDER_NAME = "kmls"
script_dir = os.path.abspath(os.path.dirname(__file__))
kml_folder = os.path.join(script_dir, FOLDER_NAME)


def kml_resizer():
    resize_factor = input("Enter KML sample points reduction factor (e.g., 2, 4, 8)? ")
    file_list = get_kml_file_list(kml_folder)
    for file in file_list:
        resize_kml_files(file, int(resize_factor))
    print('Processed {} files'.format(len(file_list)))
    input("Press enter key to exit")

def get_kml_file_list(path):
    kml_files = []
    for filename in glob.glob(os.path.join(path, "*.kml")):
        kml_files.append(filename)
    return kml_files

def resize_kml_files(kml_file, factor):
    output_kml = kml_file[:-4] + ' - Resized' + kml_file[-4:]
    print('Saving {}'.format(output_kml))
    with open(kml_file, "r") as f, open(output_kml,'w') as g:
        count = 0
        check = False
        for line in f:
            if line.startswith("<Placemark>"):
                count += 1
                check = True
            if count % factor != 0 and check == True:
                pass
            if count % factor == 0 or check == False:
                g.write(line)
            if line.startswith("</Placemark>"):
                check = False

if __name__ == "__main__":
    kml_resizer()
