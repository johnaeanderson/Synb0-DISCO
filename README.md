# Synb0-DISCO (TIGRLab)

Synb0-DISCO is a tool used for generating synthetic b0s using deep learning using only a T1. This is useful when doing diffusion imaging without fieldmap/phasediff files. Find more about this tool at the [original repo](https://github.com/MASILab/Synb0-DISCO) or the [paper](https://www.sciencedirect.com/science/article/abs/pii/S0730725X18306179). 

The TIGRLab version of the repo has modifications to make it easier to run on our system.

## Installation

Pull this repo.

```bash
git clone https://github.com/TIGRLab/Synb0-DISCO
```

Pull the pix2pix repo to Synb0-DISCO/src/python. To be safe, switch to revision 6d9e17390a4b2e186bc45427c37f4ff42409bb40 which is confirmed to work.

```bash
git clone https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix Synb0-DISCO/src/python/pytorch-CycleGAN-and-pix2pix/
git -C Synb0-DISCO/src/python/pytorch-CycleGAN-and-pix2pix/ checkout 6d9e1739
```

Copy the training data from smansour's projects folder.
```bash
mkdir -p Synb0-DISCO/src/checkpoints
cp -r /projects/smansour/Synb0_DISCO_checkpoints/* Synb0-DISCO/src/checkpoints/
```

Load FSL 6.0.1, matlab R2017b.
```bash
module load FSL/6.0.1 matlab/R2017b
```

Create a python (3.5.5) environment with the dependencies from Synb0-DISCO/src/requirements.txt.

*note, install python environments from here: https://github.com/pyenv/pyenv, then install the software for virtual environments from here https://github.com/pyenv/pyenv-virtualenv

Note: Always activate your python environment after loading the modules from the previous step. This is because loading those modules sometimes override the python environments.
```bash
pyenv virtualenv 3.5.5 synb0
pyenv activate synb0
pip install -r Synb0-DISCO/src/requirements.txt
```

Congrats! You are now ready to generate synthetic b0s.

## Usage

*Note, prior to running this command, make sure your T1 images are oriented correctly (fslreorient2std) and de-biased N4BiasFieldCorrection

In the following commands, <synb0_root> should always point to the folder where you pulled the repo, Synb0-DISCO. This is required to import all the scripts in it and the training data. 

To generate a b0 given a single T1:
```bash
python Synb0-DISCO/src/gen_synb0_single.py <t1_file> <synb0_root> <output_folder>
```

To generate a b0 given a bids directory:
```bash
python Synb0-DISCO/src/gen_synb0_bids.py <bids_dir> <synb0_root> <output_folder>
```
