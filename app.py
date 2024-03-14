from flask import Flask, render_template
import requests
from flask import jsonify
import json

app = Flask(__name__)
token = "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"
headers = {"Authorization": f"Bearer {token}"}

@app.route('/')
def home():
    return render_template('index.html') 


@app.route('/projects-list/<string:org')
def test(org):
    url = f"https://api.github.com/orgs/{org}/projects"
    response = requests.get(url, headers=headers)
    print(response.json())
    data = response.json()
    return jsonify({'data': data})
'''
org: The organization name. The name is not case sensitive.
获取组织为COMP5241-2324-Project，仓库为project-group14，名称为Group 14 Project design的board信息
'''
@app.route('/project-id')
def list_projects_id():
    query = """
    query {
    organization(login: "COMP5241-2324-Project") {
        repository(name: "project-group14") {
        projects(first: 100) {
            edges {
            node {
                name
            }
            }
        }
        }
    }
    }
    """
    response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    print(json.dumps(response.json(), indent=4))
    return render_template('index.html') 

'''
owner: The account owner of the repository. The name is not case sensitive.
repo: The name of the repository without the .git extension. The name is not case sensitive.
branch: SHA or branch to start listing commits from. Default: the repository's default branch (usually main).
committer: GitHub username or email address to use to filter by commit committer.

Example:https://api.github.com/repos/Flyraty/weekly_travel/commits?sha=main
'''
@app.route('/commit-frequency/<string:owner>/<string:repo>/<string:branch>', defaults={'committer': None})
@app.route('/commit-frequency/<string:owner>/<string:repo>/<string:branch>/<string:committer>')
def commit_frequency(owner, repo, branch, committer):
    if(committer == None):
        url = f"https://api.github.com/repos/{owner}/{repo}/commits?sha={branch}"
    else:
        url = f"https://api.github.com/repos/{owner}/{repo}/commits?sha={branch}&committer={committer}"
    response = requests.get(url)
    data = response.json()
    commit_frequency = len(data)
    return jsonify({'commit_frequency': commit_frequency})



if __name__ == '__main__':
    app.run(debug=True)