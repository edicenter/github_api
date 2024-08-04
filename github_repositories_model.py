"""

.columns_label(0) --> "Name"
.columns_label(1) --> "Private?"

.column_count() --> 8

.row_count() --> 53

.get_data(row:int, column:int)
.get_data(0,10)  --> "Webedifact"
.get_data(4,10)  --> datetime('2024-10-02 10:01:00')

"""
from dataclasses import dataclass, field, fields
from datetime import datetime
from importlib import metadata
from os import name


@dataclass
class GithubRepo:
    name: str = field(metadata={'label': "Name"})
    private: bool = field(metadata={'label': "Private?"})
    size: int = field(metadata={'label': "Size"})
    owner: str = field(metadata={'label': "Owner"})
    url: str = field(metadata={'label': "URL"})
    clone_url: str = field(metadata={'label': "Clone URL"})
    date_created: datetime = field(metadata={'label': "Date Created"})
    date_pushed: datetime = field(metadata={'label': "Last Pushed?"})
    description: str = field(metadata={'label': "Description"})

    @classmethod
    def create(cls, repo):
        return cls(
            name=repo['name'],
            private=repo['private'],
            size=int(repo['size']),
            owner=repo['owner']['login'],
            url=repo['html_url'],
            clone_url=repo['clone_url'],
            date_created=datetime.fromisoformat(repo['created_at']),
            date_pushed=datetime.fromisoformat(repo['pushed_at']),
            description=repo['description']
        )


class GithubRepositoriesModel():

    repo_fields = fields(GithubRepo)

    def __init__(self, repos: list[dict]):
        """
        'repos' is a dictionary of dictionaries as returned by Github REST API. All values are strings.
        """
        self._repos = [GithubRepo.create(r) for r in repos]

    def column_label(self, column: int):
        return self.repo_fields[column].metadata['label']

    def column_count(self):
        return len(self.repo_fields)

    def row_count(self):
        return len(self._repos)

    def get_data(self, row: int, column: int):
        repo = self._repos[row]
        return repo.__getattribute__(self.repo_fields[column].name)

    def get_repo(self, row: int) -> GithubRepo:
        return self._repos[row]

    def sort(self, column: int, descending=False):
        self._repos.sort(key=lambda repo: repo.__getattribute__(self.repo_fields[column].name),
                         reverse=descending)

    def sort_by(self, key_fn, descending=True):
        self._repos.sort(key=key_fn, reverse=descending)

    def __len__(self):
        return len(self._repos)


if __name__ == "__main__":

    repos = [
        {'allow_forking': True,
         'archive_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/{archive_format}{/ref}',
         'archived': False,
         'assignees_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/assignees{/user}',
         'blobs_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/git/blobs{/sha}',
         'branches_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/branches{/branch}',
         'clone_url': 'https://github.com/nklkli/dotnet-mailmessage-to-internet-message.git',
         'collaborators_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/collaborators{/collaborator}',
         'comments_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/comments{/number}',
         'commits_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/commits{/sha}',
         'compare_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/compare/{base}...{head}',
         'contents_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/contents/{+path}',
         'contributors_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/contributors',
         'created_at': '2024-05-02T12:18:52Z',
         'default_branch': 'main',
         'deployments_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/deployments',
         'description': 'Converts System.Net.Mail.MailMessage to the Internet Message '
         'Format which can be save to an EML file.',
         'disabled': False,
         'downloads_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/downloads',
         'events_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/events',
         'fork': False,
         'forks': 0,
         'forks_count': 0,
         'forks_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/forks',
         'full_name': 'nklkli/dotnet-mailmessage-to-internet-message',
         'git_commits_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/git/commits{/sha}',
         'git_refs_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/git/refs{/sha}',
         'git_tags_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/git/tags{/sha}',
         'git_url': 'git://github.com/nklkli/dotnet-mailmessage-to-internet-message.git',
         'has_discussions': False,
         'has_downloads': True,
         'has_issues': True,
         'has_pages': False,
         'has_projects': True,
         'has_wiki': True,
         'homepage': None,
         'hooks_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/hooks',
         'html_url': 'https://github.com/nklkli/dotnet-mailmessage-to-internet-message',
         'id': 795014923,
         'is_template': False,
         'issue_comment_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/issues/comments{/number}',
         'issue_events_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/issues/events{/number}',
         'issues_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/issues{/number}',
         'keys_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/keys{/key_id}',
         'labels_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/labels{/name}',
         'language': 'C#',
         'languages_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/languages',
         'license': None,
         'merges_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/merges',
         'milestones_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/milestones{/number}',
         'mirror_url': None,
         'name': 'dotnet-mailmessage-to-internet-message',
         'node_id': 'R_kgDOL2L3Cw',
         'notifications_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/notifications{?since,all,participating}',
         'open_issues': 0,
         'open_issues_count': 0,
         'owner': {'avatar_url': 'https://avatars.githubusercontent.com/u/91247496?v=4',
                    'events_url': 'https://api.github.com/users/nklkli/events{/privacy}',
                    'followers_url': 'https://api.github.com/users/nklkli/followers',
                    'following_url': 'https://api.github.com/users/nklkli/following{/other_user}',
                    'gists_url': 'https://api.github.com/users/nklkli/gists{/gist_id}',
                    'gravatar_id': '',
                    'html_url': 'https://github.com/nklkli',
                    'id': 91247496,
                    'login': 'nklkli',
                    'node_id': 'MDQ6VXNlcjkxMjQ3NDk2',
                    'organizations_url': 'https://api.github.com/users/nklkli/orgs',
                    'received_events_url': 'https://api.github.com/users/nklkli/received_events',
                    'repos_url': 'https://api.github.com/users/nklkli/repos',
                    'site_admin': False,
                    'starred_url': 'https://api.github.com/users/nklkli/starred{/owner}{/repo}',
                    'subscriptions_url': 'https://api.github.com/users/nklkli/subscriptions',
                    'type': 'User',
                    'url': 'https://api.github.com/users/nklkli'},
         'permissions': {'admin': True,
                         'maintain': True,
                         'pull': True,
                         'push': True,
                         'triage': True},
         'private': False,
         'pulls_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/pulls{/number}',
         'pushed_at': '2024-05-02T12:57:49Z',
         'releases_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/releases{/id}',
         'size': 8,
         'ssh_url': 'git@github.com:nklkli/dotnet-mailmessage-to-internet-message.git',
         'stargazers_count': 0,
         'stargazers_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/stargazers',
         'statuses_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/statuses/{sha}',
         'subscribers_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/subscribers',
         'subscription_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/subscription',
         'svn_url': 'https://github.com/nklkli/dotnet-mailmessage-to-internet-message',
         'tags_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/tags',
         'teams_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/teams',
         'topics': [],
         'trees_url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message/git/trees{/sha}',
         'updated_at': '2024-05-02T12:57:53Z',
         'url': 'https://api.github.com/repos/nklkli/dotnet-mailmessage-to-internet-message',
         'visibility': 'public',
         'watchers': 0,
         'watchers_count': 0,
         'web_commit_signoff_required': False},


        {'allow_forking': True,
         'archive_url': 'https://api.github.com/repos/nklkli/django_tutorital/{archive_format}{/ref}',
         'archived': False,
         'assignees_url': 'https://api.github.com/repos/nklkli/django_tutorital/assignees{/user}',
         'blobs_url': 'https://api.github.com/repos/nklkli/django_tutorital/git/blobs{/sha}',
         'branches_url': 'https://api.github.com/repos/nklkli/django_tutorital/branches{/branch}',
         'clone_url': 'https://github.com/nklkli/django_tutorital.git',
         'collaborators_url': 'https://api.github.com/repos/nklkli/django_tutorital/collaborators{/collaborator}',
         'comments_url': 'https://api.github.com/repos/nklkli/django_tutorital/comments{/number}',
         'commits_url': 'https://api.github.com/repos/nklkli/django_tutorital/commits{/sha}',
         'compare_url': 'https://api.github.com/repos/nklkli/django_tutorital/compare/{base}...{head}',
         'contents_url': 'https://api.github.com/repos/nklkli/django_tutorital/contents/{+path}',
         'contributors_url': 'https://api.github.com/repos/nklkli/django_tutorital/contributors',
         'created_at': '2024-07-28T10:13:36Z',
         'default_branch': 'master',
         'deployments_url': 'https://api.github.com/repos/nklkli/django_tutorital/deployments',
         'description': 'https://docs.djangoproject.com/en/5.0/intro/',
         'disabled': False,
         'downloads_url': 'https://api.github.com/repos/nklkli/django_tutorital/downloads',
         'events_url': 'https://api.github.com/repos/nklkli/django_tutorital/events',
         'fork': False,
         'forks': 0,
         'forks_count': 0,
         'forks_url': 'https://api.github.com/repos/nklkli/django_tutorital/forks',
         'full_name': 'nklkli/django_tutorital',
         'git_commits_url': 'https://api.github.com/repos/nklkli/django_tutorital/git/commits{/sha}',
         'git_refs_url': 'https://api.github.com/repos/nklkli/django_tutorital/git/refs{/sha}',
         'git_tags_url': 'https://api.github.com/repos/nklkli/django_tutorital/git/tags{/sha}',
         'git_url': 'git://github.com/nklkli/django_tutorital.git',
         'has_discussions': False,
         'has_downloads': True,
         'has_issues': True,
         'has_pages': False,
         'has_projects': True,
         'has_wiki': True,
         'homepage': None,
         'hooks_url': 'https://api.github.com/repos/nklkli/django_tutorital/hooks',
         'html_url': 'https://github.com/nklkli/django_tutorital',
         'id': 834773230,
         'is_template': False,
         'issue_comment_url': 'https://api.github.com/repos/nklkli/django_tutorital/issues/comments{/number}',
         'issue_events_url': 'https://api.github.com/repos/nklkli/django_tutorital/issues/events{/number}',
         'issues_url': 'https://api.github.com/repos/nklkli/django_tutorital/issues{/number}',
         'keys_url': 'https://api.github.com/repos/nklkli/django_tutorital/keys{/key_id}',
         'labels_url': 'https://api.github.com/repos/nklkli/django_tutorital/labels{/name}',
         'language': 'Python',
         'languages_url': 'https://api.github.com/repos/nklkli/django_tutorital/languages',
         'license': None,
         'merges_url': 'https://api.github.com/repos/nklkli/django_tutorital/merges',
         'milestones_url': 'https://api.github.com/repos/nklkli/django_tutorital/milestones{/number}',
         'mirror_url': None,
         'name': 'django_tutorital',
         'node_id': 'R_kgDOMcGg7g',
         'notifications_url': 'https://api.github.com/repos/nklkli/django_tutorital/notifications{?since,all,participating}',
         'open_issues': 0,
         'open_issues_count': 0,
         'owner': {'avatar_url': 'https://avatars.githubusercontent.com/u/91247496?v=4',
                       'events_url': 'https://api.github.com/users/nklkli/events{/privacy}',
                       'followers_url': 'https://api.github.com/users/nklkli/followers',
                       'following_url': 'https://api.github.com/users/nklkli/following{/other_user}',
                       'gists_url': 'https://api.github.com/users/nklkli/gists{/gist_id}',
                       'gravatar_id': '',
                       'html_url': 'https://github.com/nklkli',
                       'id': 91247496,
                       'login': 'nklkli',
                       'node_id': 'MDQ6VXNlcjkxMjQ3NDk2',
                       'organizations_url': 'https://api.github.com/users/nklkli/orgs',
                       'received_events_url': 'https://api.github.com/users/nklkli/received_events',
                       'repos_url': 'https://api.github.com/users/nklkli/repos',
                       'site_admin': False,
                       'starred_url': 'https://api.github.com/users/nklkli/starred{/owner}{/repo}',
                       'subscriptions_url': 'https://api.github.com/users/nklkli/subscriptions',
                       'type': 'User',
                       'url': 'https://api.github.com/users/nklkli'},
         'permissions': {'admin': True,
                         'maintain': True,
                         'pull': True,
                         'push': True,
                         'triage': True},
         'private': False,
         'pulls_url': 'https://api.github.com/repos/nklkli/django_tutorital/pulls{/number}',
         'pushed_at': '2024-07-28T10:27:33Z',
         'releases_url': 'https://api.github.com/repos/nklkli/django_tutorital/releases{/id}',
         'size': 24,
         'ssh_url': 'git@github.com:nklkli/django_tutorital.git',
         'stargazers_count': 0,
         'stargazers_url': 'https://api.github.com/repos/nklkli/django_tutorital/stargazers',
         'statuses_url': 'https://api.github.com/repos/nklkli/django_tutorital/statuses/{sha}',
         'subscribers_url': 'https://api.github.com/repos/nklkli/django_tutorital/subscribers',
         'subscription_url': 'https://api.github.com/repos/nklkli/django_tutorital/subscription',
         'svn_url': 'https://github.com/nklkli/django_tutorital',
         'tags_url': 'https://api.github.com/repos/nklkli/django_tutorital/tags',
         'teams_url': 'https://api.github.com/repos/nklkli/django_tutorital/teams',
         'topics': [],
         'trees_url': 'https://api.github.com/repos/nklkli/django_tutorital/git/trees{/sha}',
         'updated_at': '2024-07-28T10:27:36Z',
         'url': 'https://api.github.com/repos/nklkli/django_tutorital',
         'visibility': 'public',
         'watchers': 0,
         'watchers_count': 0,
         'web_commit_signoff_required': False},




        {'allow_forking': True,
         'archive_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/{archive_format}{/ref}',
         'archived': False,
         'assignees_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/assignees{/user}',
         'blobs_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/git/blobs{/sha}',
         'branches_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/branches{/branch}',
         'clone_url': 'https://github.com/nklkli/fdating_webscraper.git',
         'collaborators_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/collaborators{/collaborator}',
         'comments_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/comments{/number}',
         'commits_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/commits{/sha}',
         'compare_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/compare/{base}...{head}',
         'contents_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/contents/{+path}',
         'contributors_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/contributors',
         'created_at': '2024-07-28T13:10:40Z',
         'default_branch': 'main',
         'deployments_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/deployments',
         'description': 'FDating webscraper using Playwright',
         'disabled': False,
         'downloads_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/downloads',
         'events_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/events',
         'fork': False,
         'forks': 0,
         'forks_count': 0,
         'forks_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/forks',
         'full_name': 'nklkli/fdating_webscraper',
         'git_commits_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/git/commits{/sha}',
         'git_refs_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/git/refs{/sha}',
         'git_tags_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/git/tags{/sha}',
         'git_url': 'git://github.com/nklkli/fdating_webscraper.git',
         'has_discussions': False,
         'has_downloads': True,
         'has_issues': True,
         'has_pages': False,
         'has_projects': True,
         'has_wiki': False,
         'homepage': None,
         'hooks_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/hooks',
         'html_url': 'https://github.com/nklkli/fdating_webscraper',
         'id': 834819320,
         'is_template': False,
         'issue_comment_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/issues/comments{/number}',
         'issue_events_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/issues/events{/number}',
         'issues_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/issues{/number}',
         'keys_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/keys{/key_id}',
         'labels_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/labels{/name}',
         'language': 'Python',
         'languages_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/languages',
         'license': None,
         'merges_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/merges',
         'milestones_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/milestones{/number}',
         'mirror_url': None,
         'name': 'fdating_webscraper',
         'node_id': 'R_kgDOMcJU-A',
         'notifications_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/notifications{?since,all,participating}',
         'open_issues': 0,
         'open_issues_count': 0,
         'owner': {'avatar_url': 'https://avatars.githubusercontent.com/u/91247496?v=4',
                       'events_url': 'https://api.github.com/users/nklkli/events{/privacy}',
                       'followers_url': 'https://api.github.com/users/nklkli/followers',
                       'following_url': 'https://api.github.com/users/nklkli/following{/other_user}',
                       'gists_url': 'https://api.github.com/users/nklkli/gists{/gist_id}',
                       'gravatar_id': '',
                       'html_url': 'https://github.com/nklkli',
                       'id': 91247496,
                       'login': 'nklkli',
                       'node_id': 'MDQ6VXNlcjkxMjQ3NDk2',
                       'organizations_url': 'https://api.github.com/users/nklkli/orgs',
                       'received_events_url': 'https://api.github.com/users/nklkli/received_events',
                       'repos_url': 'https://api.github.com/users/nklkli/repos',
                       'site_admin': False,
                       'starred_url': 'https://api.github.com/users/nklkli/starred{/owner}{/repo}',
                       'subscriptions_url': 'https://api.github.com/users/nklkli/subscriptions',
                       'type': 'User',
                       'url': 'https://api.github.com/users/nklkli'},
         'permissions': {'admin': True,
                         'maintain': True,
                         'pull': True,
                         'push': True,
                         'triage': True},
         'private': True,
         'pulls_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/pulls{/number}',
         'pushed_at': '2024-07-28T13:11:36Z',
         'releases_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/releases{/id}',
         'size': 4,
         'ssh_url': 'git@github.com:nklkli/fdating_webscraper.git',
         'stargazers_count': 0,
         'stargazers_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/stargazers',
         'statuses_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/statuses/{sha}',
         'subscribers_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/subscribers',
         'subscription_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/subscription',
         'svn_url': 'https://github.com/nklkli/fdating_webscraper',
         'tags_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/tags',
         'teams_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/teams',
         'topics': [],
         'trees_url': 'https://api.github.com/repos/nklkli/fdating_webscraper/git/trees{/sha}',
         'updated_at': '2024-07-28T13:11:39Z',
         'url': 'https://api.github.com/repos/nklkli/fdating_webscraper',
         'visibility': 'private',
         'watchers': 0,
         'watchers_count': 0,
         'web_commit_signoff_required': False},
    ]

    repos = GithubRepositoriesModel(repos)

    print(f"{repos.column_count()=}")
    print(f"{repos.row_count()=}")
    print(f"{repos.get_data(0, 0)=}")
    print(f"{repos.get_data(1, 0)=}")
    print(f"{repos.get_data(2, 0)=}")
    print(f"{repos.get_data(2, 2)=}")
    print(f"{repos.get_data(2, 7)=}")
    print(f"{repos.column_label(0)=}")
    print(f"{repos.column_label(1)=}")
    print(f"{repos.column_label(2)=}")

    print("NOT SORTED")
    for row in range(len(repos)):
        print("\t", repos.get_data(row, 0))

    print("SORTED ASC")
    repos.sort(0)
    for row in range(len(repos)):
        print("\t", repos.get_data(row, 0))

    print("SORTED DESC")
    repos.sort(0, descending=True)
    for row in range(len(repos)):
        print("\t", repos.get_data(row, 0))
