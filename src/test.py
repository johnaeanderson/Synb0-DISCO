from synb0 import synb0
import os
import sys

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

  python test.py <t1_path> <output_dir> <name> <synb0_root>

  <t1_path> - T1 path
  <output_dir> - Directory where all the output files will be placed
  <name> - output file name (subject name typical)
  <synb0_root> - The path where the Synb0 repo was pulled to (for training data, etc.)

After calling the script, a Synb0 file will be generated in the given Dmprspace.
'''

# mpr is t1 file
mpr=sys.argv[1]
# output_root is where you want all generated files to go
Dmprspace=sys.argv[2]
# name of output files
name=sys.argv[3]
# root is where you have all the src files and data (git checkout Synb0-DISCO)
root = sys.argv[4]

synb0(Dmprspace, mpr, name, root)
