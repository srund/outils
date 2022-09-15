# outils
Utilities to help manage an Odoo installation

The general state of this project is very much "Work in progess.".
The functionality is tested to the extent the test suite states, which at the
time of writing this covers almost all written code.

## Dev notes:

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
