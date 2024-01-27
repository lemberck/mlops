# Steps

### Install Poetry
- Install poetry (Ubuntu - terminal)
 - `curl -sSL https://install.python-poetry.org | python3 -`

- Add to Path
    - `echo "export PATH=\"$HOME/.local/bin:$PATH\"" >> $HOME/.profile`
    - `source $HOME/.profile`

- Check installation
    - `poetry --version`

### Initiate Poetry for the project
-  Start poetry for the project (needed only once) --> add a description, press enter to skip the others :

    - `poetry init`

> Creates the pyproject.toml file (config file of the project).

> Metadata about the project like name, version, description, authors, and dependencies.

-  Start venv created by poetry :

    - `poetry shell`

-  Add project dependencies to the venv :

    - `poetry add pandas`

> Creates the poetry.lock file when the first dependency is added.

> Locks the versions of your project's dependencies (including sub-dependencies) to ensure consistency and reproducibility of your environment.

- Create the python script 'analyze_sales.py'

-  Test the script import in a python env :

    - `poetry shell`

    - `python`

    - `import analyze_sales`

>  Creates a compiled version of the python script inside __ pychace __ folder.


    - ctrl+D to exit python
    - ctrl+D to exit poetry

### Install just
- Install just (Ubuntu - terminal)
    - `sudo apt install just`
    - Note: You must have the Prebuilt-MPR set up on your system in order to run this command.


-  Create the justfile with 'analyze' rule that runs the script using poetry

-  Execute the script with the justfile rule

    - `just analyze`
