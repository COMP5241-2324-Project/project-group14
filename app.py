from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)
token = "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"
headers = {'Authorization': f'token {token}'}


token = "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"
headers = {'Authorization': f'token {token}'}
owner = 'microsoft'
repo = 'vscode'


@app.route('/')
def home():
    return render_template('index.html')



@app.route('/comments/<issueID>')
def comments(issueID):
    url = 'https://api.github.com/repos/%s/%s/issues/%s/comments' % (owner, repo, issueID)
    response = requests.get(url, headers = headers)
    comments = response.json()
    for comment in comments:
        print('\n\nComment from user %s:\n %s\n\n' % (comment['user']['login'], comment['body']))

    return jsonify(comments)


@app.route('/assignedIssues')
def assignedIssues():
    url = 'https://api.github.com/repos/%s/%s/issues' % (owner, repo)
    response = requests.get(url, headers = headers)
    issues = response.json()
    assigned_issue = []
    for issue in issues:
         if issue['labels'] != []:
            assigned_issue.append(issue)

    for issue in assigned_issue:
        print('Issue: %s' % issue['title'])
        cnt = 0
        for label in issue['labels']:
            cnt += 1
            print('Label %d: %s ' % (cnt, label['name']))
        print('')

    return assigned_issue

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
    app.run()