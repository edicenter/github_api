"""
Make HTTP requests to the Github API to list, create or delete repositories.
"""
from urllib.parse import urlparse
import os
import re
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


def create_clone_url_with_owner(owner: str, clone_url: str) -> str:
    parse_result = urlparse(clone_url)
    return parse_result._replace(netloc=f"{owner}@{parse_result.netloc}").geturl()


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
        result = f"OK. GITHUB RESOSITORY '{repo}' CREATED.\n"
        result += f"HTML URL: {repo['html_url']}\n"
        result += "-"*50 + "\n\n"
        result += "git init\n"
        result += "git add .\n"
        result += "git commit -m \"first commit\"\n"
        clone_url = json_response["clone_url"]
        owner = json_response["owner"]["login"]
        clone_url = create_clone_url_with_owner(owner, clone_url)
        result += f"git remote add github {clone_url}\n"
        result += "git push -u github main\n\n"
        result += "-"*50 + "\n"
        return result
    else:
        raise Exception(f"Could not create Github repository '{repo}"
                        f"Response status code: {response.status_code}"
                        f"Response: \n{response.json()}")


def list_repositories(token, organisation=None):
    """
    List repositories for the authenticated user.

    https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repositories-for-the-authenticated-user
    """

    # Pattern to match a value in the HTTP  header 'link'.
    # Example: <https://api.github.com/repositories/1300192/issues?page=4>; rel="next"
    nextPattern = "(?<=<)([\\S]*)(?=>; rel=\"next\")"

    if organisation:
        url = baseurl + f"/orgs/{organisation}/repos"
    else:
        url = baseurl + "/user/repos"

    while True:
        response: requests.Response = requests.get(
            url, headers={"Authorization": f"Bearer {token}"})

        if response.status_code != 200:
            err_msg = ("Github-API Request fehlgeschlagen;\n\n"
                       "Erwartet status code 200;\n\n"
                       f"Github-API '{url=}' antwortet  mit {response.status_code=}\n\n"
                       f"{response.text=} ")
            raise Exception(err_msg)

        for repo in response.json():
            yield repo

        if (m := re.search(nextPattern, response.headers.get('Link', ""), re.IGNORECASE)) and \
                m is not None:
            url = m.group(0)
        else:
            break


def update_repository(token: str,
                      owner: str,
                      repo: str,
                      clone_url: str,
                      new_name: str,
                      new_description: str,
                      new_private: bool
                      ):
    """
    https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#update-a-repository
    """
    url = f"{baseurl}/repos/{owner}/{repo}"
    response = requests.patch(url,

                              headers={"Authorization": "Bearer " + token},

                              json={'name': new_name,
                                    'description': new_description,
                                    'private': new_private,
                                    })

    if response.status_code != 200:
        raise Exception(f"'Update a repository' request to Github-API failed.\n"
                        f"{url=}; {owner=}; {repo=}\n"
                        f"{response.status_code=}\n"
                        f"{response.text=}")

    new_repo = response.json()
    new_clone_url = create_clone_url_with_owner(owner, new_repo['clone_url'])
    git_command = ("Repository updated.\n"
                   "Don't forget to update the URL of your local repository if necessary:\n\n"
                   f"git remote set-url github {new_clone_url}")
    return git_command


if __name__ == "__main__":
    import os
    token = os.environ['GITHUB_TOKEN']
    owner = os.environ['GITHUB_OWNER']
    # repo_count = 0
    # all_repos = list(list_repositories(token))
    # for repo in all_repos[:3]:
    #     repo_count += 1
    #     pprint(repo)
    #     print(",")
    # print(f"{repo_count} repositories found.")

    result = update_repository(token,
                               owner,
                               clone_url="https://github.com/nklkli/Windows10RemoveAppsPSCommands.git",
                               repo="Windows10RemoveAppsPSCommands",
                               new_name="Windows10RemoveApps",
                               new_description="new descri...",
                               new_private=False)
    print(result)
