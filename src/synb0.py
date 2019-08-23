import os
from shutil import copyfile, rmtree
'''
The purpose of this script is to provide an outline for processing synthetic
b0s. The Synb0-DISCO method only requires a T1 image instead of fmap/phdiff
files, and uses deep learning to produce b0s.
To call Synb0-DISCO, there must be some prep beforehand:

Pull the repo https://github.com/MASILab/Synb0-DISCO.
Pull the repo https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix to
  Synb0-DISCO/src/python/. Revision 6d9e17390a4b2e186bc45427c37f4ff42409bb40
  works.
Pull the training data (or request it from Synb0-DISCO owners if link is dead)
  from https://drive.google.com/file/d/1W_gYAWzCluP3pS9l-4eoL1Q7i3uJqixY/view
  to Synb0-DISCO/src/checkpoints.
module load FSL/5.0.10 cuda/7.5 matlab/R2017b MRtrix3/20180123 AFNI/2017.07.17
Create a virtual environment for pix2pix. Requirements can be found in
  Synb0-DISCO/src/requirements.txt.
Activate the virtual environment.
Call this script as such:

  synb0(Dmprspace, mpr, name, root)

  <Dmprspace> - Directory where all the output files will be placed
  <mpr> - T1 path
  <name> - output file name (subject name typical)
  <root> - The path where the Synb0 repo was pulled to (for training data, etc.)

After calling the script, a Synb0 file will be generated in the given Dmprspace.
'''


def synb0(Dmprspace, mpr, name, root):
    # input:
    #   Dmprspace: directory where intermediate output will be stored
    #   mpr: T1 file
    #   name: output file name (subject name typical)
    #   dataset: output directory of RGB conversion

    # output:
    #   out_synb0: path of resulting synb0

    Dresults = os.path.join(Dmprspace, 'synb0_results')
    dataset = os.path.join(Dmprspace, 'synb0_dataset')

    # Build paths to specific scripts depending on the given root repo
    synb0_path = os.path.join(root, 'src')
    pix2pix_path = os.path.join(synb0_path, 'python/pytorch-CycleGAN-and-pix2pix')
    checkpoints_dir = os.path.join(synb0_path, "checkpoints")
    pix2pix_test_path = os.path.join(pix2pix_path, "test.py")

    # Call the matlab script that generates the images from the T1 for pix2pix to use
    mat_command = "matlab -nodisplay -nodesktop -r \"addpath(genpath('"+synb0_path+"')); datRGBtriDWMRI('" + \
        Dmprspace+"', '"+mpr+"', '"+name+"', '"+dataset+"', '"+root+"'); exit\""
    os.system(mat_command)

    # Prep the pix2pix commands for axi, sag, and cor
    pix2pix_commands = ["python " + pix2pix_test_path + " --dataroot " + dataset + "-axi --name b0ganRGB-axi_pix2pix --model pix2pix  --results_dir " + Dresults + " --which_direction AtoB  --how_many  10000000 --dataset_mode aligned --checkpoints_dir " + checkpoints_dir + "",
                        "python " + pix2pix_test_path + " --dataroot " + dataset + "-sag --name b0ganRGB-sag_pix2pix --model pix2pix  --results_dir " + Dresults + " --which_direction AtoB  --how_many  10000000 --dataset_mode aligned --checkpoints_dir " + checkpoints_dir + "",
                        "python " + pix2pix_test_path + " --dataroot " + dataset + "-cor --name b0ganRGB-cor_pix2pix --model pix2pix  --results_dir " + Dresults + " --which_direction AtoB  --how_many  10000000 --dataset_mode aligned --checkpoints_dir " + checkpoints_dir + ""]

    # Call the pix2pix commands that uses training data to build the Synb0 output
    for command in pix2pix_commands:
        os.system(command)

    # Call matlab that compiles the images back into a T1 format
    mat_command = "matlab -nodisplay -nodesktop -r \"addpath(genpath('"+synb0_path+"')); datRGBtriDWMRIrecon('" + \
        Dmprspace+"', '"+Dresults+"', '"+name+"', '" + \
        dataset+"', '"+mpr+"', '"+root+"'); exit\""
    os.system(mat_command)

    # Copy the final output into  "sub-XX_synb0_output.nii.gz"
    synb0_output = os.path.join(Dmprspace, name + "-r-mpr-ss-est-3--RGB-triplanar-mean-ORIG.nii.gz")
    output_file = os.path.join(Dmprspace, name + "_synb0_output.nii.gz")
    copyfile(synb0_output, output_file)
    return output_file
