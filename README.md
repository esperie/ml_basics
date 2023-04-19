# ML Basics

SMU MBA ML/AI Workshop

## Setup

1. Install PyCharm
2. Setup a Github account: https://github.com/
3. Download the Github Desktop app for your OS
    - Click on the top left tab that says "Current Repository"
    - Click add and clone the
      repository: https://github.com/esperie/ml_basics.git
    - Organize all your repositories into a folder
4. Install PyCharm
5. Create New Project in PyCharm and point to the local repository folder
    - Under Python interpreter, select "New Virtual Environment"
6. (Optional) Some settings to consider
    - Settings > Tools > Actions on Save > Check "Reformat Code"
    - Settings > Build, Execution, Deployment > Console > Uncheck "Show Console
      Variables by Default"
7. Our data is shared
   in: https://www.dropbox.com/sh/2fju8lxw7fk2hzc/AABulJvzPjnzzk7S2iOHczCra?dl=0
    - Copy the files to your current project folder under store

## Package installation

1. Open the terminal in PyCharm.

### If you are not on an ARM based Mac (i.e. 2019 and before):

2. Install the packages using the following
   command: `pip3 install -U pip pandas colorama tqdm numpy matplotlib scikit-learn scipy plotly
   pycaret"[full]" ydata-profiling django fastapi"[all]" httpx openpyxl
   passlib psycopg2-binary pyarrow requests s3fs transformers`
3. Go to https://pytorch.org/get-started/locally/ and follow the instructions
   to install pytorch on your OS (and whether your machine comes with a GPU or
   not).

### If you are on an ARM based Mac:

1. Install XCode command line tools using the following command: `xcode-select
   --install`
2. Install homebrew with: `/bin/bash -c "$(curl -fsSL
   https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
3. Install miniforge with: `brew install miniforge`
4. Go to settings > Project > Project Interpreter > Click on Add Interpreter >
   Click Add Local Interpreter > Choose Conda Environment and key in the
   following in the box: `/opt/homebrew/bin/conda`
5. Create new environment.
6. Install the packages using the following
   command: `conda install pip pandas colorama tqdm numpy matplotlib scikit-learn scipy plotly
   ydata-profiling django httpx openpyxl
   passlib psycopg2-binary pyarrow requests s3fs transformers pycaret`
7. Run: `pip3 install fastapi"[all]"`

## Folder Structure

1. All functionalities are now consolidated under the applications folder.
2. Each applications folder should have the following structure.
   > data: all data etl and wrangling codes
   >
   > algo: logic, analytics, ML, DL, AI codes
   >
   > models (if created): Django data models
   >
   > other django files (if created.)
   >
   > views: to serve the data and algo models
3. logs: All log files are kept here.
4. store: All data files are kept here. Model files too.
4. tools: All tools that are not applications specific are kept here.
5. config: All configuration files are kept here.

## Every script should follow the following layout

```

# All imports on the top

# Setup and global variables section

# Functions section

# Classes section

if __name__ == "__main__':

# execution code

# test code

```