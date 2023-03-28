# MDO-Project-WEC-Arrays-SP-2023

Repository for project

Some scenarios 
https://tethys-engineering.pnnl.gov/publications/modelling-arrays-wave-energy-converters

-> This talks about creating a surrogate mechanical system and then doing control and design optimiziation of the system. We discussed create a surrogate empiricial model not the mechanical system but this is also interesting


how to set up Virtual environment with mamba via command line interface:

mamba create -n "venv_name" python
mamba activate venv_name
mamba install -c conda-forge capytaine
pip install https://github.com/LHEEA/meshmagick/archive/master.zip
mamba install numpy scipy matplotlib pandas notebook

can check venv list with :
mamba env list

can check active packages when env is active with:
mamba list
