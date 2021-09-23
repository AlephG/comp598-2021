import argparse
import os, sys
from zipfile import ZipFile

parser = argparse.ArgumentParser()
parser.add_argument('-id', help='Student ID (only numbers)', required=True)
args = parser.parse_args()
STUDENTID = '{}'.format(args.id) 

def main():
    print("Preparing files to zip")
    src_folder = os.path.join('.', 'src')
    scripts_folder = os.path.join('.', 'scripts')
    output_file = os.path.join('.', 'output.json')
    to_zip = [src_folder, scripts_folder, output_file]
    final_zip_name = f"{STUDENTID}_submission_template.zip"
    with ZipFile(final_zip_name,'w') as zip:
        for file in to_zip:
            zip.write(file)
    print(f"{final_zip_name} file created successfully - submit it through myCourses <3")

    

if __name__ == "__main__":
    main()