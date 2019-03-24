__author__ = 'Nicolas Quiroz'


from RestrictedPython import compile_restricted, RestrictingNodeTransformer
from contextlib import redirect_stdout
from zipfile import ZipFile

import sys
import os
import shutil


class OwnRestrictingNodeTransformer(RestrictingNodeTransformer):
    pass


def exec_code(code: str):
    locals_: dict = {}
    result = compile_restricted(code, filename='<inline code>', mode='exec',
                                policy=None)
    exec(result, globals(), globals())
    return globals()


def gen_inputs(project_name: str, num: int = 10):
    path = os.path.join('resources', project_name)
    os.chdir(path)
    if os.path.exists('input'):
        shutil.rmtree('input')
    os.mkdir('input')
    if not os.path.exists('gen_flags.json'):
        print('No generation flags provided. Asumming None...')

        with open('gen_flags.txt', mode='w+'):
            pass

    for i in range(num):
        input_file = f'input{str(i).zfill(2)}.txt'
        input_file = os.path.join('input', input_file)
        execute_file('gen_flags.txt', 'gen.py', input_file,
                     project_name + f' _input{i}')

    os.chdir(os.path.join('..', '..'))


def execute_file(input_file: str, code_file: str, output_file: str, name: str):
    with open(input_file, encoding='utf-8') as in_file:
        sys.stdin = in_file
        message = f'Executing {name} with {input_file}'
        length = len(message)
        print('=' * (length // 2 - 1), message, '=' * (length // 2 - 1))

        with open(output_file, encoding='utf-8', mode='w+') as out_file:
            with redirect_stdout(out_file):
                with open(code_file, encoding='utf-8') as code:
                    exec_code(code.read())

        with open(output_file, encoding='utf-8') as f:
            txt = f.read()

        with open(output_file, encoding='utf-8', mode='w') as f:
            f.write(txt.rstrip())
        print('=' * 45, 'COMPLETE', '=' * 45)
        sys.stdin = sys.__stdin__


def run_code(project_name: str):
    print(f'{"/"*30}==> Project {repr(project_name)} starting...')
    os.chdir(os.path.join('resources', project_name))
    if os.path.exists('output'):
        shutil.rmtree('output')
    os.mkdir('output')
    for input_file_name in os.listdir('input'):
        start = input_file_name.find('input')
        out_file = 'output' + input_file_name[start + len('input'):]
        out_file = os.path.join('output',  out_file)
        input_file = os.path.join('input', input_file_name)
        execute_file(input_file, 'code.py', out_file, project_name)
    print(f'{"/"*30}==> Project {repr(project_name)} done. Compressing...')

    with ZipFile('tests_cases.zip', mode='w') as zip_:
        for folder in ['input', 'output']:
            for file_ in os.listdir(folder):
                zip_.write(os.path.join(folder, file_), os.path.join(folder,
                                                                     file_))
    os.chdir(os.path.join('..', '..'))
    print(f'----> Project {repr(project_name)} compressed.')


def create_proj(project: str, inputs: int):
    if ' ' in project:
        print('Invalid name, cannot contain spaces')
    else:
        path = os.path.join('resources', project)
        ovewrite = True
        if os.path.exists(path):
            msg = ('That project already exists, would you like to '
                   'overwrite it? [y/n]: ')
            if input(msg) != 'y':
                ovewrite = False
        if ovewrite:
            if os.path.exists(path):
                shutil.rmtree(path)
            os.mkdir(path)
            os.mkdir(os.path.join(path, 'input'))
            for i in range(inputs):
                with open(os.path.join(path, 'input', f'input{i:0>2}.txt'),
                          mode='w+'):
                    pass
            with open(os.path.join(path, 'gen.py'), mode='w+'):
                pass
            with open(os.path.join(path, 'code.py'), mode='w+'):
                pass
            with open(os.path.join(path, 'gen_flags.txt'), mode='w+'):
                pass
    print(f'{project!r} created.')


def main():
    cmd = sys.argv[1]
    if cmd == 'inputs':
        num = int(sys.argv[2])
        for project in sys.argv[3:]:
            gen_inputs(project, num)
    elif cmd == 'zip':
        for project in sys.argv[2:]:
            run_code(project)

    elif cmd == 'make':
        num = int(sys.argv[2])
        for project in sys.argv[3:]:
            gen_inputs(project, num)
        for project in sys.argv[3:]:
            run_code(project)
    elif cmd == 'create':
        create_proj(sys.argv[2], int(sys.argv[3]))
    else:
        print('Command not recognized:')
        print()
        print(f'{"inputs NUMBER [project_name, ...]": <50} generates NUMBER '
              'inputs for project_names, need a gen.py for each project_name. '
              'gen_flags.txt can be provided')
        print(f'{"zip [project_name, ...]": <50} generates a zip of testcases '
              'for each project_name')
        print(f'{"make NUMBER [project_name, ...]": <50} makes NUMBER '
              ' of compressed testcastes for each project_name, need a '
              'gen.py.  gen_flags.txt can be provided for altering generation')


if __name__ == "__main__":
    main()
