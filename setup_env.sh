#!/bin/sh
echo $PATH

VENV=lsmd
PYVER=3.5


DEPARRAY=(scipy pip configobj pandas dicttoxml ipython jupyter)

# turn off whatever other virtual environment user might be in
source deactivate

#remove any previous virtual environments called pager
CWD=`pwd`
cd $HOME;
conda remove --name $VENV --all -y
cd $CWD

conda create --name $VENV --yes --channel conda-forge python=$PYVER ${DEPARRAY[*]} -y

# activate the new environment
source activate $VENV

# tell the user they have to activate this environment
echo "Type 'source activate lsmd' to use this new virtual environment."
