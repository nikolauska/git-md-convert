# Git markdown converter in python

Simple python script to converr markdown files from your repository to other formats.   
Also supports wiki documents with github!

## Currently supported format
- html

## Wanted supported format
- html
- pdf

## Usage
- run with console
    - python convert.py [options] [git clone url]
        - python convert.py -b stable-1.0 https://github.com/awesome/repo.git

## Arguments
- -b/--branch
    - Set different branch
    - Without this, master is used as default
