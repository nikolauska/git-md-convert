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
from library.files import find_files
from library.markdown2 import markdown_path

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
    else:
        return None

def get_file_name(path):
    head, tail = os.path.split(path)
    splitted = tail.split(".")
    return splitted[0]

def load_data(repo_url, repo_path, wiki_url, wiki_path, branch):
    if os.path.isdir(repo_path):
        print("\n############################################\n")
        print("Git folder found on \"{}\"".format(repo_path))

        # Save current dir and mmove to found repo dir
        prevdir = os.getcwd()
        os.chdir(repo_path)

        print("Trying to pull newest information...")
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
        print("\n############################################\n")
    else:
        print("\n############################################\n")
        print("No git folder found on \"{}\"".format(repo_path))
        print("Trying to clone repository from {}...".format(repo_url))
        git_clone(repo_url, repo_path)
        print("\n############################################\n")

    if wiki_url != None:
        if os.path.isdir(wiki_path):
            print("\n############################################\n")
            print("\nWiki folder found on \"{}\"".format(wiki_path))

            # Save current dir and mmove to found repo dir
            prevdir = os.getcwd()
            os.chdir(wiki_path)

            print("Trying to pull newest information...")
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
            print("\n############################################\n")
        else:
            print("\n############################################\n")
            print("\nNo git folder found on \"{}\"".format(wiki_path))
            print("Trying to clone wiki from {}...".format(wiki_url))
            git_clone(wiki_url, wiki_path)
            print("\n############################################\n")

def markdown_convert(user, repo):
    repo_path = os.path.abspath("./downloaded/{}/{}".format(user, repo))
    convert_path = os.path.abspath("./converted/{}/{}/html".format(user, repo))

    if not os.path.exists(os.path.abspath("./converted/")):
        os.mkdir(os.path.abspath("./converted/"))

    if not os.path.exists(os.path.abspath("./converted/{}/".format(user))):
        os.mkdir(os.path.abspath("./converted/{}/".format(user)))

    if not os.path.exists(os.path.abspath("./converted/{}/{}".format(user, repo))):
        os.mkdir(os.path.abspath("./converted/{}/{}".format(user, repo)))

    if not os.path.exists(convert_path):
        os.mkdir(convert_path)

    files = find_files(os.path.join(repo_path, "repository"), ".md")
    files.extend(find_files(os.path.join(repo_path, "wiki"), ".md"))

    html_files = []

    for file in files:
        temp = file.replace(repo_path, "").split("\\")
        file_path = convert_path

        for asd in temp:
            if not ".md" in asd:
                file_path = os.path.join(file_path, asd)
                if not os.path.exists(file_path):
                    os.mkdir(file_path)
            else:
                file_path = os.path.join(file_path, asd.replace(".md",".html"))

        html_files.append(file_path)
        try:
            fp = open(file_path)
            fp.write(markdown_path(file, encoding="utf-8",
                                            html4tags=False, tab_width=4,
                                            safe_mode=None,
                                            extras=["code-friendly", "fenced-code-blocks", "tables", "cuddled-lists"]))
            fp.close()
        except IOError:
            # If not exists, create the file
            fp = open(file_path, 'w+')
            fp.write(markdown_path(file, encoding="utf-8",
                                            html4tags=False, tab_width=4,
                                            safe_mode=None,
                                            extras=["code-friendly", "fenced-code-blocks", "tables", "cuddled-lists"]))
            fp.close()

    return html_files

def pdf_convert(path, md_files):
    if not os.path.exists(path):
        os.mkdir(path)

    for md in md_files:
        pdf()

def main(repo_url, branch):
    repo = get_repo_name(repo_url)
    user = get_user_name(repo_url)
    wiki_url = get_wiki_url(repo_url)

    repo_path = "downloaded/{}/{}/repository".format(user, repo)
    wiki_path = "downloaded/{}/{}/wiki".format(user, repo)

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
    md_files = markdown_convert(user, repo)

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("url", help="Url to git reposity where to convert markdown to pdf")
    parser.add_argument("-b", "--branch", help="Change which branch to pull documentation from")

    args = parser.parse_args()

    branch = "master";

    if args.branch:
        branch = args.branch

    sys.exit(main(args.url, branch))
