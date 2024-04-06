from flask import Flask, render_template, jsonify
import requests
import AnalysisBot
import CalcGroupContribution
from flask import request
from flask import jsonify
import json, redis
from datetime import datetime


app = Flask(__name__)
token = "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"
headers = {'Authorization': f'token {token}'}
deadline = '2024-04-07 00:00:00'
free_ratio = 0.3
ddl_ratio = 0.8

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def home():
    return render_template('index.html') 

# 获取所有group的commit数量，一共有多少group，一共有多少成员
@app.route('/getTotalInfo')
def getTotalInfo():
    owner = "COMP5241-2324-Project"
    repo = "project-group14"
    # 第一次要调接口，把数据写reids。 以后先判断需不需要调接口，
    # totalCommit = redis_client.get('totalCommit').decode('utf-8')
    totalCommit = None
    if  totalCommit == None:
        totalCommit = get_commit_count(owner, repo)
        totalNumbers =get_contributor_count(owner, repo)

        users = CalcGroupContribution.Getusers(owner, repo)
        users = CalcGroupContribution.CountIssueAndComment(owner, repo, users)
        totalIssues = 0
        for use in users:
            totalIssues += use['issue_num']
        today = datetime.today()
        future_date = datetime(2024, 2, 6)
        difference = today - future_date
        days = difference.days
        data ={'totalCommit':totalCommit, 'totalGroups': totalIssues,'totalNumbers':totalNumbers, 'totalDays':days}

        # redis_client.set('totalCommit', totalCommit)
        # redis_client.set('totalNumbers', totalNumbers)
        # redis_client.set('totalGroups', 20)
        return jsonify(data)
    else:
        totalNumbers = redis_client.get('totalNumbers').decode('utf-8')
        totalGroups = redis_client.get('totalGroups').decode('utf-8')
        data ={'totalCommit':totalCommit, 'totalGroups': totalGroups,'totalNumbers':totalNumbers}
        return jsonify(data)

def get_commit_count(owner, repo):
    page = 1
    count = 0
    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/commits?page={page}"
        response = requests.get(url, headers=headers)
        commits = response.json()
        if not commits:
            break
        count += len(commits)
        page += 1
        if count > 100:
            return count
    return count

def get_contributor_count(owner, repo):
    page = 1
    count = 0
    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/contributors?page={page}"
        response = requests.get(url, headers=headers)
        contributors = response.json()
        if not contributors:
            break
        count += len(contributors)
        page += 1
        if count > 100:
            return count
    return count

# 获取group的信息，包括issues数量，comments数量，code changes数量
@app.route('/getGroupInfo')
def getGroupInfo():
    owner = "COMP5241-2324-Project"
    repo = request.args.get('group')

    users = CalcGroupContribution.Getusers(owner, repo)
    users = CalcGroupContribution.CountIssueAndComment(owner, repo, users)
    issues_count = 0
    comments_count = 0
    for use in users:
        issues_count += use['issue_num']
        comments_count += use['comment_num']

    data ={'issues':issues_count,'comments':comments_count}
    return jsonify(data)

def get_issues_count(owner, repo):
    url = 'https://api.github.com/repos/%s/%s/issues' % (owner, repo)
    issue_response = requests.get(url, headers = headers)
    issues = issue_response.json()
    assigned_issue = []
    issue_id = []
    for issue in issues:
         if issue['labels'] != []:
            assigned_issue.append(issue)
            issue_id.append(issue['id'])
    for issue in assigned_issue:
        print('Issue: %s' % issue['title'])
        cnt = 0
        for label in issue['labels']:
            cnt += 1
            print('Label %d: %s ' % (cnt, label['name']))
        print('')

    return len(assigned_issue),issue_id

def get_comments_count(owner, repo, issue_id):
    count = 0
    for id in issue_id:
        url = 'https://api.github.com/repos/%s/%s/issues/%s/comments' % (owner, repo, id)
        response = requests.get(url, headers = headers)
        comments = response.json()
        count += len(comments)
    return count


@app.route('/getGroupCommitFrequency')
def getGroupCommitFrequency():
    group = request.args.get('group')
    owner = "COMP5241-2324-Project"
    commits = get_commits(owner, group)
    commit_frequency = [0,0,0,0,0,0,0]
    for commit in commits:
        date = commit['commit']['author']['date']
        date = datetime.strptime(commit['commit']['author']['date'],"%Y-%m-%dT%H:%M:%SZ")
        days = (date.month-1)*30 + date.day
        index = (days-57)//7
        print(days)
        commit_frequency[index] += 1
    count = 0
    for i in range(len(commit_frequency)):
        count += commit_frequency[i]
        commit_frequency[i] = count
    data ={
        'group':group,
        'commitFrequency':commit_frequency
        }
    return jsonify(data)

def get_commits(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits?page=1&per_page=100"
    response = requests.get(url, headers=headers)
    commits = response.json()
    return commits

@app.route('/getGroupMemberContributor')
def getGroupMemberContributor():
    group = request.args.get('group')
    data ={
        'group':group,
        'labels':["student 1", "student 2", "student 3", "student 4", "student 5"],
        'memberContributor':[55, 49, 44, 24, 15]
        }
    return jsonify(data)


@app.route('/getMemberContributor')
def getMemberContributor():
    group_name = 'project-group14'
    group_owner = 'COMP5241-2324-Project'
    users = CalcGroupContribution.Getusers(group_owner, group_name)
    users = CalcGroupContribution.CountIssueAndComment(group_owner, group_name, users)
    users = CalcGroupContribution.code_changes_stats(group_owner, group_name, users, deadline)
    data = []
    for user in users:
        data.append({'group_name':group_name ,'member':user['name'],'commits':user['commit_num'],'issues':user['issue_num'],'code_changes':user['code_change']})
    return jsonify(data)

@app.route('/getDeadlineFighters')
def getDeadlineFighters():
    group_name = 'project-group14'
    group_owner = 'COMP5241-2324-Project'
    deadlineFighters = redis_client.lrange('deadline_fighters',0,-1)
    if deadlineFighters != None:
        data = []
        for fighter in deadlineFighters:
            data.append(json.loads(fighter))
        return jsonify(data)
    data = []
    users = CalcGroupContribution.Getusers(group_owner, group_name)
    users = CalcGroupContribution.CountIssueAndComment(group_owner, group_name, users)
    users = CalcGroupContribution.code_changes_stats(group_owner, group_name, users, deadline)
    users = CalcGroupContribution.Deadline_fighter_judge(users, ddl_ratio)
    for user in users:
        if user['deadline_fighter'] == True:
            data.append({'name':group_name,'student':user['name']})
    return jsonify(data)

@app.route('/getFreeRiders')
def getFreeRiders():
    group_name = 'project-group14'
    group_owner = 'COMP5241-2324-Project'
    data = []
    deadlineFighters = redis_client.lrange('free_riders',0,-1)
    if deadlineFighters != None:
        data = []
        for fighter in deadlineFighters:
            data.append(json.loads(fighter))
        return jsonify(data)
    users = CalcGroupContribution.Getusers(group_owner, group_name)
    users = CalcGroupContribution.CountIssueAndComment(group_owner, group_name, users)
    users = CalcGroupContribution.code_changes_stats(group_owner, group_name, users, deadline)
    users = CalcGroupContribution.Deadline_fighter_judge(users, ddl_ratio)
    for user in users:
        if user['free_rider'] == True:
            data.append({'name':group_name,'student':user['name']})
    return jsonify(data)



@app.route('/getInfoFromAi', methods=['POST'])
def getInfoFromAi():
    data = request.get_json()
    group_name, group_owner = data.get('group_name'), data.get('group_owner')
    users = CalcGroupContribution.Getusers(group_owner, group_name)
    users = CalcGroupContribution.CountIssueAndComment(group_owner, group_name, users)
    users = CalcGroupContribution.code_changes_stats(group_owner, group_name, users, deadline)
    users = CalcGroupContribution.Free_rider_judge(users, free_ratio)
    users = CalcGroupContribution.Deadline_fighter_judge(users, ddl_ratio)
    resp = AnalysisBot.chat(CalcGroupContribution.CreateUserStringForAI(users))
    response_data = {'answer':resp}
    return jsonify(response_data)

@app.route('/getGroupInfoFromAi', methods=['POST'])
def getGroupInfoFromAi():
    data = request.get_json()
    group_name1, group_name2, group_owner = data.get('group_name1'), data.get('group_name2'),data.get('group_owner')
    repo1 = CreateNewRepoInfo(group_owner, group_name1)
    repo1 = CalcGroupContribution.CalcGroupContribution(repo1, group_owner, group_name1, deadline, free_ratio, ddl_ratio, needAI = False)
    repo2 = CreateNewRepoInfo(group_owner, group_name2)
    repo2 = CalcGroupContribution.CalcGroupContribution(repo2, group_owner, group_name2, deadline, free_ratio, ddl_ratio, needAI = False)
    repos = []
    repos.append(repo1)
    repos.append(repo2)
    resp = AnalysisBot.chat(CreateRepoStringForAI(repos))
    response_data = {'answer':resp}
    return jsonify(response_data)

def CreateNewRepoInfo(owner, name):
    return {'name': owner + '/' + name, 'issue_num': 0, 'comment_num': 0, 'commit_num': 0, 'code_change': 0, 'deadline_change': 0, 'deadline_fighter': False, 'score': 0}


def CreateRepoStringForAI(repos):
    n = len(repos)
    ans = 'There are %d github repositories in total. The workload of these repositories to the repository are as follows: \n' % n
    
    for i in range(n):
        str = 'repository %s had %d issues, %d comments, a total of %d commits, and made %d lines of code changes;\n' % (repos[i]['name'], repos[i]['issue_num'], repos[i]['comment_num'], repos[i]['commit_num'], repos[i]['code_change'])
        ans += str

    ans += 'Please sort the above repositories in descending order of their workload.'
    print(ans)
    return ans


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
def code_changes(owner, repo):
    # 初始化一个列表来存储所有的提交
    all_commits = []
    page = 1
    while True:
        url_commits = "https://api.github.com/repos/{owner}/{repo}/commits?page={page}&per_page=100"
        response_commits = requests.get(url_commits.format(owner, repo, page=page), headers = headers)
        commits = response_commits.json()
        if not commits:
            break

        for commit in commits:
            url_commit = "https://api.github.com/repos/{owner}/{repo}/commits/{sha}"
            response_commit = requests.get(url_commit.format(owner, repo, sha=commit['sha'], headers = headers))
            commit_data = response_commit.json()
            all_commits.append(commit_data)

        page += 1

    return jsonify(all_commits)

if __name__ == '__main__':
    app.run(debug=True)