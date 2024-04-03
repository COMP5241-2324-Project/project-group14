from flask import Flask, render_template
import requests
from flask import request
from flask import jsonify
import json

app = Flask(__name__)
token = "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"
headers = {"Authorization": f"Bearer {token}"}

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



if __name__ == '__main__':
    app.run(debug=True)