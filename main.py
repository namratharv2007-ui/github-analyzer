import requests

username = input("Enter GitHub username: ")

url = f"https://api.github.com/users/{username}"

response = requests.get(url)

data = response.json()
if data.get("message") == "Not Found":
    print("User not found!")
    exit()

print("\n----- GitHub Profile -----")
print("Name:", data.get("name"))
print("Followers:", data.get("followers"))
print("Public Repos:", data.get("public_repos"))
print("Bio:", data.get("bio"))
print("Account Created:", data.get("created_at"))

repos_url = f"https://api.github.com/users/{username}/repos"

repos = requests.get(repos_url).json()

print("\nRepositories:")

for repo in repos:
    print("-", repo["name"])
    
most_starred = None

for repo in repos:
    if most_starred is None or repo["stargazers_count"] > most_starred["stargazers_count"]:
        most_starred = repo

print("\nMost Starred Repository:")
print("Name:", most_starred["name"])
print("Stars:", most_starred["stargazers_count"])

language_count = {}

for repo in repos:
    language = repo["language"]

    if language:
        if language in language_count:
            language_count[language] += 1
        else:
            language_count[language] = 1

print("\nLanguages Used:")

for language, count in language_count.items():
    print(language, ":", count)

top_language = max(language_count, key=language_count.get)

print("\nTop Language:")
print(top_language)