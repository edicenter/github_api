"""
Make HTTP requests to the Github API to list, create or delete repositories.
"""
import os
from pprint import pprint

import requests

baseurl = "https://api.github.com"


def delete_repo(token, repo, owner, owner_is_organisation=False):
    """
    Deletes a Github repository.

    https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#delete-a-repository
    """

    response = requests.delete(url=baseurl + f"/repos/{owner}/{repo}",
                               headers={"Authorization": "Bearer " +
                                        token})
    print("Request URL:", response.url)
    print("Delete Repository Response:")
    print("Response Status:", response.status_code)
    pprint(response.text)
    if response.status_code == 204:
        print(f"OK. Github repository '{repo}' deleted.")


def create_organization_repo(token, repo, organization, description, private=True):
    """
    Create an organization repository

    https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#create-an-organization-repository
    """
    url = f"/orgs/{organization}/repos"
    fullurl = baseurl + url
    response = requests.post(fullurl,
                             headers={"Authorization": f"Bearer {token}"},
                             json={"name": repo,
                                   "description": description,
                                   "private": private})
    print("Create Repository Response:")
    print("Request URL:", response.url)
    print("Response Status:", response.status_code)
    if response.status_code == 201:
        json_response = response.json()
        pprint(json_response)
        clone_url = json_response["clone_url"]
        print(f"OK. Github repository '{repo}' created.")
        print(f"Clone-URL: {clone_url}")


def create_repo(token, repo, description=None, private=True, organization=None):
    """
    Creates a new repository for the authenticated user.

    https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#create-a-repository-for-the-authenticated-user
    """
    if organization:
        url = baseurl + f"/orgs/{organization}/repos"
    else:
        url = baseurl + "/user/repos"

    response = requests.post(url,
                             headers={"Authorization": "Bearer " +
                                      token},
                             json={"name": repo,
                                   "description": description,
                                   "private": private})
    print("Create Repository Response:")
    print("Request URL:", response.url)
    print("Response Status:", response.status_code)
    if response.status_code == 201:
        from urllib.parse import urlparse
        json_response = response.json()
        pprint(json_response)
        clone_url = json_response["clone_url"]
        print(f"OK. GITHUB RESOSITORY '{repo}' CREATED.")
        print(
            "Create a new repository and push an existing repository from the command line:")
        print("-"*50)
        print("git init")
        print("git add .")
        print("git commit -m \"first commit\"")
        clone_url = urlparse(clone_url)
        owner = json_response["owner"]["login"]
        clone_url = clone_url._replace(
            netloc=f"{owner}@{clone_url.netloc}").geturl()
        print(f"git remote add github {clone_url}")
        print("git push -u github main")
        print("")
        print("-"*50)


def list_repositories(token, organisation=None):
    """
    List repositories for the authenticated user.

    https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repositories-for-the-authenticated-user
    """

    if organisation:
        url = baseurl + f"/orgs/{organisation}/repos"
    else:
        url = baseurl + "/user/repos"

    response = requests.get(url,
                            headers={"Authorization": f"Bearer {token}"})

    pad = 10

    def print_repo_property(repo, property):
        print(f"{property:<{pad}}:", repo[property])

    for repo in response.json():
        print_repo_property(repo, "name")
        print_repo_property(repo, "description")
        print_repo_property(repo, "private")
        print_repo_property(repo, "size")
        print_repo_property(repo, "clone_url")
        print_repo_property(repo, "language")
        print()

    print("List Repositories Response:")
    print("Request URL:", response.url)
    print("Response Status:", response.status_code)
