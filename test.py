import sys

if sys.version_info[0] == 2:
    print("Python 3 is required!")
    sys.exit(1)

import os

import convert

class tester:
    def __init__(self, url, user, repo, has_wiki, branch):
        self.failed = []
        self.success = []
        self.url = url
        self.user = user
        self.repo = repo
        self.has_wiki = has_wiki
        self.branch = branch

        if convert.main(url, branch) == 0:
            self.test_downloaded()
            self.test_converted()
        else:
            self.failed.append("Unable to run convert script for {}!".format(self.url))

    def test_downloaded(self):
        base_path = os.path.join(os.path.abspath("./downloaded"), self.user, self.repo)
        if os.path.exists(os.path.join(base_path, "repository")):
            self.success.append("Downloaded repository folder found for {}!".format(self.url))
        else:
            self.failed.append("Downloaded repository folder not found for {}!".format(self.url))
        if self.has_wiki:
            if os.path.exists(os.path.join(base_path, "wiki")):
                self.success.append("Downloaded wiki folder found for {}!".format(self.url))
            else:
                self.failed.append("Downloaded wiki folder not found for {}!".format(self.url))

    def test_converted(self):
        base_path = os.path.join(os.path.abspath("./converted"), self.user, self.repo)
        if os.path.exists(os.path.join(base_path, "html")):
            self.success.append("Converted html folder found for {}!".format(self.url))
        else:
            self.failed.append("Converted html folder not found for {}!".format(self.url))

def main():
    failed = []
    success = []

    # url: https://github.com/nikolauska/KGE.git
    # user: nikolauska
    # repo: KGE
    test = tester("https://github.com/nikolauska/KGE.git", "nikolauska", "KGE", True, "master")
    failed.extend(test.failed)
    success.extend(test.success)

    print("\nResult:")
    print("Failed: {}".format(len(failed)))
    for fail in failed:
        print("    - {}".format(fail))
    print("Succcess: {}".format(len(success)))
    for value in success:
        print("    - {}".format(value))

    return len(failed)



if __name__ == "__main__":
    sys.exit(main())
