from flask import Flask, render_template, jsonify
import requests

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



def CountIssueAndComment(owner, repo, users):
    new_users = users

    issue_url = 'https://api.github.com/repos/%s/%s/issues' % (owner, repo)
    issue_response = requests.get(issue_url, headers = headers)
    issues = issue_response.json()

    for issue in issues:
        issue_id = issue['number']
        issue_user_name = issue['user']['login']
        for user in new_users:
            if user['name'] == issue_user_name:
                user['issue_num'] += 1
        
        print(issue_id)
        comment_url = 'https://api.github.com/repos/%s/%s/issues/%s/comments' % (owner, repo, issue_id)
        comment_response = requests.get(comment_url, headers = headers)
        comments = comment_response.json()
        for comment in comments:
            comment_user_name = comment['user']['login']
            for user in new_users:
                if user['name'] == comment_user_name:
                    user['comment_num'] += 1

    return new_users


if __name__ == '__main__':
    user1 = {'name': 'zerg', 'issue_num': 0, 'comment_num': 0}
    user2 = {'name': 'Nimbid04', 'issue_num': 0, 'comment_num': 0}
    user3 = {'name': 'VSCodeTriageBot', 'issue_num': 0, 'comment_num': 0}
    users = [user1, user2, user3]
    owner = 'microsoft'
    repo = 'vscode'
    print(CountIssueAndComment(owner, repo, users))