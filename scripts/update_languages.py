import os
import requests

TOKEN = os.environ["GH_TOKEN"]
USERNAME = "nagakei713"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

QUERY = """
{
  user(login: "%s") {
    repositories(first: 100, ownerAffiliations: [OWNER, ORGANIZATION_MEMBER], isFork: false) {
      nodes {
        languages(first: 10) {
          edges { size node { name } }
        }
      }
    }
  }
}
""" % USERNAME

res = requests.post("https://api.github.com/graphql", json={"query": QUERY}, headers=HEADERS)
data = res.json()

lang_sizes = {}
for repo in data["data"]["user"]["repositories"]["nodes"]:
    for edge in repo["languages"]["edges"]:
        lang = edge["node"]["name"]
        size = edge["size"]
        lang_sizes[lang] = lang_sizes.get(lang, 0) + size

total = sum(lang_sizes.values())
table = "| Language | % |\n|----------|---|\n"
for lang, size in sorted(lang_sizes.items(), key=lambda x: x[1], reverse=True):
    table += f"| {lang} | {size/total*100:.1f}% |\n"

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

start_marker = "<!--LANGUAGES_START-->"
end_marker = "<!--LANGUAGES_END-->"
new_readme = readme.split(start_marker)[0] + start_marker + "\n" + table + end_marker + readme.split(end_marker)[1]

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

print("README.md updated successfully!")
