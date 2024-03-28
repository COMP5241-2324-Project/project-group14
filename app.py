from flask import Flask, render_template, jsonify
import requests, datetime
import AnalysisBot


app = Flask(__name__)
token = "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"
headers = {'Authorization': f'token {token}'}


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
    issue_response = requests.get(url, headers = headers)
    issues = issue_response.json()
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

@app.route('/code_changes')
def code_changes():
    # 初始化一个列表来存储所有的提交
    all_commits = []
    page = 1
    while True:
        url_commits = "https://api.github.com/repos/{owner}/{repo}/commits?page={page}&per_page=100"
        response_commits = requests.get(url_commits.format(owner="COMP5241-2324-Project", repo="project-group14", page=page), headers = headers)
        commits = response_commits.json()
        if not commits:
            break

        for commit in commits:
            url_commit = "https://api.github.com/repos/{owner}/{repo}/commits/{sha}"
            response_commit = requests.get(url_commit.format(owner="COMP5241-2324-Project", repo="project-group14", sha=commit['sha'], headers = headers))
            commit_data = response_commit.json()
            all_commits.append(commit_data)

        page += 1

    return jsonify(all_commits)
