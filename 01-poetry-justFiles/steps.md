# Steps

-  Start poetry for the project (needed only once) --> add a description, press enter to skip the others
poetry init
---> creates the pyproject.toml file (config file of the project)
---> Metadata about the project like name, version, description, authors, and dependencies.

-  Start venv created by poetry
poetry shell

-  Add pandas to venv
poetry add pandas

- Create the python script 'analyze_sales.py'

-  Test the script import in a python env
poetry shell
python
import analyze_sales
---> creates a compiled version of the python script inside __pychace__ folder
-> crtr+D to exit python
-> crtr+D to exit poetry

-  Create the justfile with 'analyze' rule that runs the script using poetry

-  Execute the script with the justfile rule
just analyze
