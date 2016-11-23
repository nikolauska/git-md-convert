#!/usr/bin/env python3

import sys

if sys.version_info[0] == 2:
    print("Python 3 is required!")
    sys.exit(1)

import os
import subprocess
import argparse
import shutil
import time

from library.color import print_red, print_green, print_blue, print_yellow
from library.git import git_pull, git_clone
from library.files import find_files, generate_folders

from library.pandoc_service import PandocPDFService, PandocHTMLService

def get_repo_name(url):
    splitted = url.split("/")
    return splitted[len(splitted) - 1].replace(".git", "")

def get_user_name(url):
    if "git@" in url:
        splitted = url.split(":")
        splitted = splitted[len(splitted) - 1].split("/")
        return splitted[0]
    else:
        splitted = url.split("/")
        return splitted[len(splitted) - 2]

def get_wiki_url(url):
    if "github.com" in url:
        return url.replace(".git", ".wiki.git");
    elif "gitlab.com" in url:
        return url.replace(".git", ".wiki.git");
    else:
        return None

def get_file_name(path):
    head, tail = os.path.split(path)
    splitted = tail.split(".")
    return splitted[0]

def pandoc_install():
    pandoc = shutil.which("pandoc")
    if pandoc == None:
        url = "http://pandoc.org/installing.html"
        print("Unable to find pandoc! See how to install it from {}".format(url))
    return 0

def load_data(repo_url, repo_path, wiki_url, wiki_path, branch):
    if os.path.isdir(repo_path):
        # Save current dir and mmove to found repo dir
        prevdir = os.getcwd()
        os.chdir(repo_path)

        print("Pulling new version from git")
        if not git_pull(branch, repo_path):
            # False means pull failed so we then want to reclone
            curr_dir = os.getcwd()
            os.chdir(prevdir)
            print_yellow("Removing folder \"{}\" to reclone it again".format(repo_path))
            try:
                shutil.rmtree(curr_dir, ignore_errors=True)
            except:
                print_red("Failed to delete folder \"{}\"".format(repo_path))
                return 1
            else:
                git_clone(repo_url, repo_path)

        # Move back to last dir
        os.chdir(prevdir)
    else:
        print("Cloning repository from {}...".format(repo_url))
        git_clone(repo_url, repo_path)

    if wiki_url != None:
        if os.path.isdir(wiki_path):
            # Save current dir and mmove to found repo dir
            prevdir = os.getcwd()
            os.chdir(wiki_path)

            print("Pulling new version from wiki")
            if not git_pull(branch, wiki_path):
                # False means pull failed so we then want to reclone
                curr_dir = os.getcwd()
                os.chdir(prevdir)
                print_yellow("Removing folder \"{}\" to reclone it again".format(wiki_path))
                try:
                    shutil.rmtree(curr_dir, ignore_errors=True)
                except:
                    print_red("Failed to delete folder \"{}\"".format(wiki_path))
                    return 1
                else:
                    git_clone(wiki_url, wiki_path)

            # Move back to last dir
            os.chdir(prevdir)
        else:
            print("Cloning wiki from {}...".format(wiki_url))
            git_clone(wiki_url, wiki_path)

def convert_files(repo_path, wiki_path, out_path, out_format):
    repo_output = os.path.join(out_path, "repository")
    wiki_output = os.path.join(out_path, "wiki")

    service = PandocHTMLService()
    if out_format == 'pdf':
        service = PandocPDFService()

    for repo_file in find_files(repo_path, ".md", start=repo_path):
        input_file = os.path.join(repo_path, repo_file)
        output_file = os.path.join(repo_output, repo_file.replace(".md", ".{}".format(out_format)))
        print("Generating file {}".format(output_file))
        generate_folders(output_file)
        service.generate(input_file, to_file=output_file)

    for wiki_file in find_files(wiki_path, ".md", start=repo_path):
        input_file = os.path.join(wiki_path, wiki_file)
        output_file = os.path.join(wiki_output, wiki_file.replace(".md", ".{}".format(out_format)))
        print("Generating file {}".format(output_file))
        generate_folders(output_file)
        service.generate(input_file, to_file=output_file)


    return 0

def main(repo_url, branch, out_format):
    repo = get_repo_name(repo_url)
    user = get_user_name(repo_url)
    wiki_url = get_wiki_url(repo_url)

    base_path = os.path.abspath("./")
    repo_path = os.path.join(base_path, "cache", user, repo, "repository")
    wiki_path = os.path.join(base_path, "cache", user, repo, "wiki")
    out_path = os.path.join(base_path, "converted", user, repo, out_format)

    if wiki_url != None:
        print_blue("\n############################################\n")
        print_blue("URL: {}".format(repo_url))
        print_blue("Wiki: {}".format(wiki_url))
        print_blue("User: {}".format(user))
        print_blue("Name: {}".format(repo))
        print_blue("\n############################################\n")
    else:
        print_blue("\n############################################\n")
        print_blue("URL: {}".format(repo_url))
        print_blue("User: {}".format(user))
        print_blue("Name: {}".format(repo))
        print_blue("\n############################################\n")

    load_data(repo_url, repo_path, wiki_url, wiki_path, branch)
    convert_files(repo_path, wiki_path, out_path, out_format)

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("url", help="Url to git reposity where to convert markdown from")
    parser.add_argument("-b", "--branch", help="Change which branch to pull documentation from", default="master")
    parser.add_argument("-f", "--format", help="Change format you want to export file to", default="html")

    args = parser.parse_args()

    pandoc_install()

    main(args.url, args.branch, args.format)


