# CHEM-240
 Python scripts for demonstrating key concepts used in the physical sciences

## Prerequisites

Before you can run the scripts, you need to install Python and set up some libraries. Follow these steps:

### Install Python

1. Download Python 3.12 from the official [Python website](https://www.python.org/downloads/).
2. During installation, ensure you check the option `Add Python 3.12 to PATH` to make Python accessible from the command line.

### Install Required Libraries

Open your command line interface by typing `cmd` in the searchbar (windows users) or by typing `Terminal` in Spotlight Search (press `Cmd + Space` to open Spotlight; Mac users) and install the necessary Python libraries by typing:

```bash
pip install numpy scipy matplotlib
```
## Module 1 scripts (Complex numbers)

1. Go to the GitHub repository containing the scripts.
2. Navigate to the Module1_PythonSupplements folder.
3. Download the desired scripts by clicking on each file and then clicking Download raw file (downwards arrow in the header of the code). The available scripts are:

    1. [Binomial Distribution coin flip simulator](https://github.com/ChristianIeritano/CHEM-240/blob/main/Module1_PythonSupplements/Binom_Dist_Coinflip.py). Download `Binom_Dist_Coinflip.py` and save the file somewhere accesible on your main wokring drive (like a Desktop folder). Execute the code the double clicking or running via your preferred Python environment. 
    2. [Particle on a ring wavefunctions (Rigid-Rotor)](https://github.com/ChristianIeritano/CHEM-240/blob/main/Module1_PythonSupplements/particle_on_a_ring_probDistrib.py). Download `particle_on_a_ring_probDistrib.py` and save the file somewhere accesible on your main wokring drive (like a Desktop folder). Execute the code the double clicking or running via your preferred Python environment. Execute the code the double clicking or running via your preferred Python environment. 
    3. [Hydrogen orbitals](https://github.com/ChristianIeritano/CHEM-240/tree/main/Module1_PythonSupplements/Hydrogen_orbitals). Download the `Hydrogen_orbitals` folder and save the file somewhere accesible on your main wokring drive (like a Desktop folder). Execute the code by double clicking [Launcher.py](https://github.com/ChristianIeritano/CHEM-240/blob/main/Module1_PythonSupplements/Hydrogen_orbitals/Launcher.py) (not hydrogen.py - this is where the math is done!) Launcher.py is found within \Hydrogen_orbitals. 

        1. For very large values of *n* and *l*, you may need to adjust the resolution by increasing the value of s located on line 54. 

        2. The math to plot the probability distributions was adapted from https://github.com/liam-ilan/electron-orbitals. Please cite accordindly if you use this in your teaching. 