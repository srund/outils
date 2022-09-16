# outils
Utilities to help manage an Odoo installation

The general state of this project is very much "Work in progess.".
The functionality is tested to the extent the test suite states, which at the
time of writing this covers almost all written code.

## Dev notes:

### Modules

The projects end-goal is provide as good base for Python scripting on Odoo
modules and installations. Such as de-entangling dependencies or finding
manifests with the wrong values.


#### odootools

    `odootools` provides base functionality for the rest of the modules within
    this project.

    The `odootools` modules is expected to consist of file/system related
    operations. Odoo, other programs such as Postgresql or non standard
    Python-modules (including `odoo`) are not expected to be installed.

    The OdooToolsHandle contain references to an Odoo-installation, by default
    assumed to be the nightly deb-package.
    Functionality that reference an Odoo installation such as including core
    modules should be able to run in an Odoo-free environment using the
    appropriate arguments.

    A possible and valid use case should be unzipping a set of odoo modules
    on a computer without Odoo installed and start querying the folder for
    information.

#### graph

    This modules provides functionality from the `networkx` modue.

    Networkx is expected to be installed. Other than that the same assumptions
    as `odootools` apply. This might change in the future as it is useful to
    construct DiGraphs from individual Odoo databases.

#### db

Database related queries and operations. Assumes `psycopg2` is installed and is
able to connect to an Odoo database.

#### cli

Click client. Assumes `click` is installed.

Scope is a work in progress. The general assumption is that it should be able
to provide the same functionality as the bash-based odootools at some point.


### Testing

The repository include functionality tests of the code. Please write tests when
adding to this project.

Run the tests from the project root with for example:
```
python3 -m unittest discover .
```
To include code coverage install the `coverage` module and run:
```
python3 -m coverage run --source=. -m unittest discover .
python3 -m coverage report
```
