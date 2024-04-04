from flask import Flask, render_template, jsonify
import requests, datetime
import AnalysisBot

from flask import request
from flask import jsonify
import json

app = Flask(__name__)
token = "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"
headers = {'Authorization': f'token {token}'}


@app.route('/')
def home():
    return render_template('index.html') 

# 获取所有group的commit数量，一共有多少group，一共有多少成员
@app.route('/getTotalInfo')
def getTotalInfo():
    data ={'totalCommit':30,'totalGroups':40,'totalNumbers':50}
    return jsonify(data)

@app.route('/getGroupInfo')
def getGroupInfo():
    group = request.args.get('group')
    data ={'issues':20,'comments':30,'codeChanges':40}
    return jsonify(data)

@app.route('/getGroupCommitFrequency')
def getGroupCommitFrequency():
    group = request.args.get('group')
    data ={
        'group':group,
        'commitFrequency':[35, 50, 55, 75, 95, 125, 145]
        }
    return jsonify(data)

@app.route('/getGroupMemberContributor')
def getGroupMemberContributor():
    group = request.args.get('group')
    data ={
        'group':group,
        'labels':["student 1", "student 2", "student 3", "student 4", "student 5"],
        'memberContributor':[55, 49, 44, 24, 15]
        }
    return jsonify(data)

@app.route('/getDeadlineFighters')
def getDeadlineFighters():
    data =[{'name':'group1','student':'Bob'},{'name':'group2','student':'Alicy'},{'name':'group3','student':'niko'}]
    return jsonify(data)

@app.route('/getFreeRiders')
def getFreeRiders():
    data =[{'name':'group4','student':'Bob'},{'name':'group5','student':'Alicy'},{'name':'group6','student':'niko'}]
    return jsonify(data)

@app.route('/getInfoFromAi', methods=['POST'])
def getInfoFromAi():
    data = request.get_json()
    group_name, group_owner, function_select = data.get('group_name'), data.get('group_owner'), data.get('function_select')
    response_data = {}
    if function_select == 'Member contribution':
        response_data = {'answer':'this is Member contribution function '+group_name+' '+group_owner}
    else:
        response_data = {'answer':'this is Group progress function '+group_name+' '+group_owner}
    return jsonify(response_data)

@app.route('/projects-list/<string:org>')
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

@app.route('/commit-frequency', methods=['POST'])
def commit_frequency():
    owner = request.form.get('owner')
    repo = request.form.get('reporisty')
    branch = request.form.get('branch')
    committer = request.form.get('committer')

    if(committer == None or committer == ''):
        url = f"https://api.github.com/repos/{owner}/{repo}/commits?sha={branch}"
    else:
        url = f"https://api.github.com/repos/{owner}/{repo}/commits?sha={branch}&committer={committer}"
    response = requests.get(url)
    data = response.json()
    commit_frequency = len(data)
    return render_template('index.html', commit_frequency=commit_frequency)





@app.route('/comments/<issueID>', methods=['POST'])
def comments():
    issueID = request.args.get('issueID')
    owner = request.args.get('owner')
    repo = request.args.get('repo')
    url = 'https://api.github.com/repos/%s/%s/issues/%s/comments' % (owner, repo, issueID)
    response = requests.get(url, headers = headers)
    comments = response.json()
    for comment in comments:
        print('\n\nComment from user %s:\n %s\n\n' % (comment['user']['login'], comment['body']))

    return jsonify(comments)


@app.route('/assignedIssues', methods=['POST'])
def assignedIssues():
    owner = request.args.get('owner')
    repo = request.args.get('repo')
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

if __name__ == '__main__':
    app.run(debug=True)