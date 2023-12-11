# pyLife-PragTic
pyLife WS @ Prague, 14-15th of December 2023

## Preperation

#### Install miniconda or anaconda

Install [miniconda](https://conda.io/miniconda.html) or [anaconda](http://anaconda.com) on your computer. See the instructions on the pages how to do that.

### Clone the repo
To use all notebooks and apps, please clone the repo. As an alternative, you can download the *.zip file directly.
### Your python environment
1. Go to the working directory
2. Open a cli prompt
3. create a new conda env:
   ```console
   conda env create -p ./.env --file environment.yaml
   ```
4. activate the env:
   ```console
   conda activate ./.env
   ```
5. start the streamlit app
   ```console
   cd use_cases/damage_calc
   streamlit run streamlit_damage_calc.py  
   ```
