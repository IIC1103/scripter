__author__ = 'Nicolas Quiroz'


from RestrictedPython import compile_restricted, RestrictingNodeTransformer
from contextlib import redirect_stdout
import sys
import os
import shutil


class OwnRestrictingNodeTransformer(RestrictingNodeTransformer):
    pass


def exec_code(code: str):
    locals_: dict = {}
    result = compile_restricted(code, filename='<inline code>', mode='exec',
                                policy=None)
    exec(result, globals(), locals_)
    return locals_


def execute_file(input_file: str, code_file: str, output_file: str, name: str):
    with open(input_file, encoding='utf-8') as in_file:
        sys.stdin = in_file
        print('=' * 100)
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
            f.write(txt.strip())
        print('=' * 45, 'COMPLETE', '=' * 45)
        print('=' * 100)
        sys.stdin = sys.__stdin__


def run_code(project_name: str):
    print(f'----> Project {repr(project_name)} starting...')
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
    print('=' * 100)
    print(f'----> Project {repr(project_name)} done.')
    os.chdir(os.path.join('..', '..'))


def main():
    for project in sys.argv[1:]:
        run_code(project)


if __name__ == "__main__":
    main()