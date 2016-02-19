import subprocess

from library.color import print_red, print_green

def parse_error(err):
    return str(err).replace("\\n", "\n").replace("\\r", "\r").replace("b\"", "")

def git_pull(branch, location):
    try:
        subprocess.check_output(["git", "pull", "origin", branch], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print_red("Failed to pull newest version to \"{}\"".format(location))
        print_red("{}\n".format(parse_error(e.output)))
        return False
    else:
        print_green("New data pulled")
        return True

def git_clone(url, location):
    try:
        subprocess.check_output(["git", "clone", url, location], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print_red("Failed to clone from".format(url))
        print_red("{}\n".format(parse_error(e.output)))
        return False
    else:
        print_green("Repository cloned to \"{}\"".format(location))
        return True
