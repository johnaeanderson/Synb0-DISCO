import os
import sys
from synb0 import synb0
from shutil import rmtree, copy

def gen_synb0_single(in_file, root, output_folder):
    print("gen single synb0")
    # Generate tmp_folder
    temp_folder = os.path.join(output_folder, "synb0_tmp")

    # Grab the base name of the file
    name = (os.path.basename(in_file)).split("_T1")[0]

    # Call the function to generate the Synb0
    output_file = synb0(temp_folder, in_file, name, root)

    # Copy the synb0 out of the temp file
    copy(output_file, output_folder)

    # Clear all other files
    rmtree(temp_folder)

def gen_synb0_bids(bids_dir, synb0_root, output_folder):
    from bids import BIDSLayout
    bids = os.listdir(bids_dir)
    bids.sort()

    for sub in bids:
        if sub.startswith("sub-"):
            # Get subject path
            sub_path = os.path.join(bids_dir, sub)
            sessions = os.listdir(sub_path)
            # Loop over sessions for this subject
            for ses in sessions:
                # Get session path
                ses_path = os.path.join(sub_path,ses)
                anat_folder = os.path.join(ses_path, "anat")
                if not(os.path.exists(anat_folder)):
                    print("anat folder doesnt exist for " + sub + ", skipping...")
                    break
                sub_output_folder = os.path.join(output_folder,sub,ses)
                # Get T1 for subject
                t1 = ""
                anat_files = os.listdir(anat_folder)
                # Grab the newest T1 file
                anat_files.sort()
                anat_files.reverse()
                for anat_file in anat_files:
                    if "T1" in anat_file and "json" in anat_file:
                        t1 = os.path.splitext(anat_file)[0]
                        t1_path = os.path.join(anat_folder, t1)
                        break
                # Output folder
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                # Call the single synb0 script
                gen_synb0_single(t1_path, synb0_root, sub_output_folder)

def main():
    bids_dir = sys.argv[1]
    synb0_root = sys.argv[2]
    output_folder = sys.argv[3]

    gen_synb0_bids(bids_dir, synb0_root, output_folder)

if __name__== "__main__":
    main()
