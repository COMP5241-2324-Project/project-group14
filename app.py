from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)
token = "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"
headers = {'Authorization': f'token {token}'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/issues')
def issues():
    url = "https://api.github.com/repos/{owner}/{repo}/issues"
    response = requests.get(url.format(owner="COMP5241-2324-Project", repo="project-group14"), headers = headers)
    issues = response.json()
    for issue in issues:
        print(f"Issue: {issue['title']}")
    return jsonify(response.json())

@app.route('/code_changes')
def code_changes():
    url_commits = "https://api.github.com/repos/{owner}/{repo}/commits"
    response_commits = requests.get(url_commits.format(owner="COMP5241-2324-Project", repo="project-group14"), headers = headers)
    commits = response_commits.json()
    if not commits:
        return jsonify({"error": "No commits found"}), 404
    
    for commit in commits:
        print(f"Commit: {commit['commit']['message']}, Author: {commit['commit']['author']['name']}")
    

    last_commit_sha = commits[0]['sha']

    url_commit = "https://api.github.com/repos/{owner}/{repo}/commits/{sha}"
    response_commit = requests.get(url_commit.format(owner="COMP5241-2324-Project", repo="project-group14", sha=last_commit_sha, headers = headers))
    return jsonify(response_commit.json())


if __name__ == '__main__':
    app.run(debug=True)