import sys

from .main import *

if len(sys.argv) == 1:
    print("USAGE:")
    print("github_api <repository name> [<resository description>]\n")
    raise SystemExit("Repository name required")

token = os.environ["GITHUB_TOKEN"]
repository_name = sys.argv[1]
description = sys.argv[2] if len(sys.argv) == 3 else None
create_repo(token, repository_name, description)
