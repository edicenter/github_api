from dataclasses import asdict
from dataclasses import fields
from dataclasses import dataclass, field


@dataclass
class GithubRepo:
    name: str = field(metadata={"label": "Name"})
    private: bool = field(metadata={"label": "Private?"})

    @classmethod
    def create(cls, n, p):
        return cls(private=p, name=n)


print("Number of fields: ", len(fields(GithubRepo)))
print(fields(GithubRepo)[0])
print()
print("name:", fields(GithubRepo)[0].name)
print("label:", fields(GithubRepo)[0].metadata['label'])
print("label:", fields(GithubRepo)[1].metadata['label'])

r = GithubRepo("Kola", True)


print("asdict:", asdict(r))
