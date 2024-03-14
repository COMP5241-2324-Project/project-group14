from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run()