# mri2fem

Original repostiory is found at https://github.com/kent-and/mri2fem. This repository is a fork of the original repository where we have made the code into an installable package with the command `mri2fem`.
We have also added a CI to ensure the code is working.

Source code for the command line tool `mri2fem` is found in the folder `src`, while the scripts to reproduce for each chapter in the book is found in the folder `reproduce-book`.

The `mri2fem` command has several subcommands

```
$ mri2fem --help
usage: __main__.py [-h] [--dry-run] [-v] {download-data,svmtk,freesurfer} ...

positional arguments:
  {download-data,svmtk,freesurfer}
    download-data       Download the sample data
    svmtk               Surface and volume meshing toolkit
    freesurfer          Run freesurfer

options:
  -h, --help            show this help message and exit
  --dry-run             Just print the command and do not run it (default: False)
  -v, --verbose         Print more information (default: False)
```

and some of these subcommands have their own subcommands. For example, the `svmtk` subcommand has the following subcommands

```
$ mri2fem svmtk --help

usage: mri2fem svmtk [-h] {surface-to-mesh,remesh-surface,smooth-surface,repair,create-gw-mesh,create-brain-mesh} ...

positional arguments:
  {surface-to-mesh,remesh-surface,smooth-surface,repair,create-gw-mesh,create-brain-mesh}
    surface-to-mesh     Convert a surface to a mesh
    remesh-surface      Remesh a surface
    smooth-surface      Smooth a surface
    repair              Repair a surface
    create-gw-mesh      Create a mesh for groundwater flow
    create-brain-mesh   Create a mesh for brain

options:
  -h, --help            show this help message and exit
```


## Environment setup

## FEniCS + SVMTK

We will use `conda` to create an environment for FEniCS and SVMTK.

### Conda installation
First install [Miniforge](https://github.com/conda-forge/miniforge?tab=readme-ov-file) and make sure to update `conda`:
```bash
conda update -n base -c conda-forge conda
```


### Create environment for FEniCS+SVMTK
To create an isolated environment for FEniCS and SVMTK, run the following command:
```bash
conda env create --file conda-env/svmtk_fenics.yml
```
Now activate the environment with the following command:
```bash
conda activate svmtk-fenics
```

## FreeSurfer

We will use docker to run FreeSurfer. First, install docker by following the instructions [here](https://docs.docker.com/get-docker/).

One main disadvantage with using FreeSurfer is that it is not build for Arm64 architecture (i.e Mac OS Apple Silicon). So, even if you can install FreeSurfer on your machine, you will you might encounter issues when running the code. Therefore, we recommend using docker if you are on an Apple Silicon machine.

If you are not running Mac OS Apple Silicon, you can still use docker to run FreeSurfer.

### FreeSurfer license

One thing to note is that you need first [register](https://surfer.nmr.mgh.harvard.edu/registration.html) to get access to the FreeSurfer license. Freesusfer will then send you an email with a file called `license.txt`.
Create a new folder in your home directory called `.freesurfer` and save the `license.txt` file in this folder, i.e
```bash
mkdir ~/.freesurfer
mv ~/Downloads/license.txt ~/.freesurfer/license.txt
```

### Build docker image
To build the docker image, run the following command if you are on an Apple Silicon machine:
```bash
docker build -t freesurfer -f docker/freesurfer741_arm.Dockerfile .
```
and the following command if you are on a non-Apple Silicon machine:
```bash
docker build -t freesurfer -f docker/freesurfer741.Dockerfile .
```
