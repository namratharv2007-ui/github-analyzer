from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route("/")
def home():

    username = request.args.get("username")

    profile = None
    repos = []
    language_percentages = {}
    summary = ""

    if username:

        url = f"https://api.github.com/users/{username}"

        response = requests.get(url)

        data = response.json()

        if data.get("message") != "Not Found":

            repos_url = f"https://api.github.com/users/{username}/repos"
            repos = requests.get(repos_url).json()

            most_starred = None

            for repo in repos:
                if most_starred is None or repo["stargazers_count"] > most_starred["stargazers_count"]:
                    most_starred = repo

            language_count = {}

            for repo in repos:

                language = repo["language"]

                if language:

                    if language in language_count:
                        language_count[language] += 1
                    else:
                        language_count[language] = 1

            total = sum(language_count.values())

            for language, count in language_count.items():
                language_percentages[language] = round((count / total) * 100, 1)

            top_language = "None"

            if language_count:
                top_language = max(language_count, key=language_count.get)

            summary = (
                f"{data.get('name')} has {data.get('public_repos')} public repositories. "
                f"Their primary language is {top_language}. "
                f"The most popular repository is {most_starred['name']} with "
                f"{most_starred['stargazers_count']} stars."
            )

            profile = {
                "avatar": data.get("avatar_url"),
                "name": data.get("name"),
                "followers": data.get("followers"),
                "repos": data.get("public_repos"),
                "bio": data.get("bio"),
                "created": data.get("created_at"),
                "top_language": top_language,
                "most_starred_name": most_starred["name"],
                "most_starred_stars": most_starred["stargazers_count"],
                "github_url": data.get("html_url")
            }

    return render_template(
    "index.html",
    profile=profile,
    repos=repos[:5],
    language_percentages=language_percentages,
    summary=summary,
    chart_labels=list(language_percentages.keys()),
    chart_values=list(language_percentages.values())
)

if __name__ == "__main__":
    app.run(debug=True)