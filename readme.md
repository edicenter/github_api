# GITHUB API

The code in `gut_gui.py` demonstrates how to list, create, or delete repositories from within Python
using GitHub's REST API: https://docs.github.com/en/rest/repos

You need your own GitHub `Personal Access Token` to make all requests.
You can create it in your GitHub account under `Settings` -> `Deveoper Settings` -> `Personal Access Tokens` -> `Tokens (classic)`.

The program expects to find the `Github Token` in the environment variable `GITHUB_TOKEN`.

Tested with Python version 12.4

Required Python packages: `requests`, `pyside6`

https://pypi.org/project/requests/

`githu_gui.pyw` is a GUI where you can create new and list existing Github repositories.

## GITHUB TOKENS

The programs expects two environment variables:

- `GITHUB_TOKEN` to create new repositories
- `GITHUB_TOTP` to generate TOTPs (time based one-time passwords)

## INITIALIZE YOUR DEVELOPMENNT ENVIRONMENT

PySide6 is very big Python package. We want to install it system-wide (not in our virtual environment directory)

Install PySide6 on your system:

> pip install pyside6 -U

Create virtual environment directory:

> mkdir .venv

Create virutal environment in the directory `.venv`.
The option `--site-packages` enables system-wide Python packages.

> pipenv install --site-packages

> pipenv shell

## RUN GUI APPLICATION

> (github_api) python github_gui.pyw
