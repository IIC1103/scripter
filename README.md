# Scripter

A python sandbox for making testcases

Requirements:

* Python 3.8.\*
* Pipenv

On command line:

``` bash
python3 -m pip install pipenv
```

Then

``` bash
pipenv install --dev
```

And you are ready to start!

## Usage

Before using, make sure the virtual environment is activated:

`pipenv shell`

Then, for any command just run

`python main.py [command] [params][...]`

Each exercise on which you expect you generate set of inputs and outputs is considered a *project*. Each project must be created with the main file.

For creating a project run

`python main.py create project_name`

This will generate a set of files and folders inside `resources/project_name` :

-`input` folder: This is where the input files will be inserted, when generated. If you rather wish to make your own custom input files, please follow the format `inputXX.txt` where XX is a number bigger that the range of tests create (i.e: if you generate 10 tests, make it input10.txt or bigger).

-`output` folder: This is where your output files will be created.
-`code.py`: This is the file on which you must place the code thay will generate the output files. Expect input to be passed as input, so use:

```python
sample_input = input()
```

For the output to be written on the text file, use:

```python
print(sample_input)
```

-`gen.py`: This is the file that is run for generating the input text files. Use `print()` for the text to be written on the input file.

**All projects must me stored under the folder `Resources` and created**

For all the commands, run `python main.py help`
