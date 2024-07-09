# GITHUB API

The code in `gut_gui.py` demonstrates how to list, create, or delete repositories from within Python
using GitHub's REST API: https://docs.github.com/en/rest/repos

You need your own GitHub `Personal Access Token` to make all requests.
You can create it in your GitHub account under `Settings` -> `Deveoper Settings` -> `Personal Access Tokens` -> `Tokens (classic)`.

The program expects to find the `Github Token` in the environment variable `GITHUB_TOKEN`.

Tested with Python version 12.4

Required Python package: `requests`

        python -m pip install requests

https://pypi.org/project/requests/

`githu_gui.pyw` is a GUI where you can create new and list existing Github repositories.

## CREATE AND ACTIVATE VIRTUAL ENVIRONMENT

> cd c:\github_api

> python -m venv .venv --prompt github_api

> .venv\Scripts\activate

## INSTALL PYTHON PACKAGES

> (github_api) pip install -r requirements.txt

## RUN GUI APPLICATION

> c:\github_api\.venv\Scripts\python.exe c:\github_api\github_gui.pyw
