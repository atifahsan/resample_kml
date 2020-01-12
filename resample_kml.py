'''
zipped = [placemark[i:i+2] for i in range(0, len(placemark), 2)] # To convert 1D list to 2D list
del zipped[k-1::k] # Delete every k-th element from list
'''
import os
import glob
from lxml import etree

FOLDER_NAME = "kmls"
script_dir = os.path.abspath(os.path.dirname(__file__))
kml_folder = os.path.join(script_dir, FOLDER_NAME)


def resample_kml():
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

def resize_kml_files(kml_file, resize_factor):
    output_kml = kml_file[:-4] + ' - Resized' + kml_file[-4:]
    tree = etree.parse(kml_file)
    root = tree.getroot()
    doc_node = root.getchildren()
    export_tool = check_export_tool(root)

    if export_tool == 'tems':
        placemark = doc_node[0].getchildren()[-1]
        count = 0
        for elem in placemark:
            if elem.tag == '{http://earth.google.com/kml/2.2}Placemark':
                count += 1
                if count % resize_factor != 0:
                    placemark.remove(elem)
        tree.write(output_kml, pretty_print=True)

    elif export_tool == 'actix':
        count = 0
        for elem in doc_node[0].getchildren():
            if elem.tag == 'Style':
                count += 1
            if count % resize_factor != 0:
                doc_node[0].remove(elem)
        tree.write(output_kml, pretty_print=True)

    else:
        print('Could not process {}'.format(kml_file))

def check_export_tool(root):
    if root.tag == '{http://www.opengis.net/kml/2.2}kml': # Actix Analyzer Export
        return 'actix'
    elif root.tag == '{http://earth.google.com/kml/2.2}kml': # TEMS Discovery Export
        return 'tems'

if __name__ == "__main__":
    resample_kml()
