# Git markdown converter in python

Simple python script to converr markdown files from your repository to other formats.
Also supports wiki documents with github!

## Setup
- `python -m venv myvenv`
- Start virtual environment
    - cmd `.\myvenv\Scripts\activate.bat`
    - powershell `.\myvenv\Scripts\activate.ps1`
    - bash/zsh `source ./bin/activate`
    - fish `source ./bin/activate.fish`
    - chs/tcsh `source ./bin/activate.csh`
- `pip install -r requirements.txt`

## Usage
- `python convert.py [options] [git clone url]`
    - `python convert.py -b 1.0 -f pdf https://github.com/nikolauska/git-md-convert`
    - `python convert.py --branch=1.0 --format=pdf https://github.com/nikolauska/git-md-convert`

## Options
- `-b` or `--branch`
  - Change to this branch before converting
- `-f` or `--format`
  - Change to another format (default `html`)
  - Supported:
    - `html`
    - `pdf`
    - `rst`
