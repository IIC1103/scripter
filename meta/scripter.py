from os import mkdir, path, getcwd, listdir
from pathlib import Path
from shutil import rmtree
from json import load

root_path = Path(__file__).parent.parent.absolute()

class Generator:
    def __init__(self, project: str = None, sort: bool = True, root: str =  root_path) -> None:
        self.root = root
        self.sort = sort

        self.settings = {}
        self.projects_dir = None
        self.tests_dir = None
        
        self.load_settings()

        self.projects = self.load_projects()

    @staticmethod
    def request_confirmation():
        while (answer := input("¿Estás segur@? [Y/N] ").lower()) not in ['y', 'n']:
            print("Opción no válida, intente nuevamente:")
        return answer == 'y'

    def load_projects(self) -> dict:
        projects = {}
        for project in listdir(self.projects_dir):
            print(project)
            projects[project] = {"root": (project_root := path.join(self.projects_dir, project)),
                                 "tests": path.join(project_root, self.tests_dir),
                                 "gen.py": path.join(project_root, 'gen.py'),
                                 "code.py": path.join(project_root, 'code.py')}
        return projects

    def load_settings(self, settings_path: str = None):
        if settings_path is None:
            settings_path = path.join(self.root, 'settings.json')
        
        with open(settings_path, 'r') as file:
            self.settings = load(file)

        if not path.exists(projects_directory := path.join(self.root, self.settings["projects_dir"])):
            mkdir(projects_directory)
        self.projects_dir = projects_directory
        self.tests_dir = self.settings["tests_dir"]

    def new_project(self, name: str) -> None:
        if not path.exists(project_root := path.join(self.projects_dir, name)):
            mkdir(project_root)
            mkdir(tests_root := path.join(project_root, self.tests_dir))
            with open(genfile := path.join(project_root, 'gen.py'), "w") as file:
                pass
            with open(codefile := path.join(project_root, 'code.py'), "w") as file:
                pass
            self.projects[name] = {"root": project_root,
                                   "tests": tests_root,
                                   "gen.py": genfile,
                                   "code.py": codefile}
            print(f'Proyecto {name} creado exitosamente')
        else:
            print(f'El proyecto {name} ya existe')

    def delete_project(self, name: str) -> None:
        if path.exists(to_remove := path.join(self.tests_dir, name)):
            if self.request_confirmation():
                rmtree(to_remove)
