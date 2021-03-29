from os import chdir, mkdir, path, listdir
from itertools import count
import subprocess

class Subcontext:
    def __init__(self, root:str, project: dict) -> None:
        self.root = root
        self.project_root = project["root"]
        self.code = project["code.py"]
        self.gen = project["gen.py"]
        self.project_tests = project["tests"]
        self.testcase = count(start= len(listdir(self.project_tests)))

    def excecute(self):
        pass

    def __enter__(self):
        if not path.exists(testcase_path := path.join(self.project_tests, 
                            f'test{str(self.testcase_number).zfill(2)}')):
            mkdir(testcase_path)

        chdir(testcase_path)

    def __exit__(self):
        chdir(self.root)