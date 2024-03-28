import requests, datetime
import AnalysisBot

token = "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"
headers = {'Authorization': f'token {token}'}

def code_changes_stats(owner, repo, users, deadline):
    new_users = users
    page = 1
    while True:
        url_commits = "https://api.github.com/repos/{owner}/{repo}/commits?page={page}&per_page=100"
        response_commits = requests.get(url_commits.format(owner=owner, repo=repo, page=page), headers = headers)
        commits = response_commits.json()
        if not commits:
            break
            
        for commit in commits:
            author = commit['author']['login']
            for user in new_users:
                if user['name'] == author:
                    user['commit_num'] += 1

                    url_commit = "https://api.github.com/repos/{owner}/{repo}/commits/{sha}"
                    response_commit = requests.get(url_commit.format(owner=owner, repo=repo, sha=commit['sha'], headers = headers))
                    commit_data = response_commit.json()
                    if 'stats' in commit_data:
                        user['code_change'] += commit_data['stats']['total']
                        
                        commit_time = commit_data['commit']['author']['date']
                        date = datetime.datetime.strptime(commit_time, '%Y-%m-%dT%H:%M:%SZ')
                        deadline_time = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
                        three_day_ago = deadline_time - datetime.timedelta(days=3)
                        if date > three_day_ago and date < deadline_time:
                            user['deadline_change'] += commit_data['stats']['total']

        page += 1

    return new_users


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
        
        #print(issue_id)
        comment_url = 'https://api.github.com/repos/%s/%s/issues/%s/comments' % (owner, repo, issue_id)
        comment_response = requests.get(comment_url, headers = headers)
        comments = comment_response.json()
        for comment in comments:
            comment_user_name = comment['user']['login']
            for user in new_users:
                if user['name'] == comment_user_name:
                    user['comment_num'] += 1

    return new_users


def Getusers(owner, repo):
    url = 'https://api.github.com/repos/%s/%s/contributors' % (owner, repo)
    response = requests.get(url, headers = headers)
    all_users = response.json()

    users = []
    for user in all_users:
        new_user = {'name': user['login'], 'issue_num': 0, 'comment_num': 0, 'commit_num': 0, 'code_change': 0, 'deadline_change': 0, 'deadline_fighter': False, 'free_rider': False, 'score': 0}
        users.append(new_user)
    return users


def Free_rider_judge(users, free_ratio):
    # 初始化一个字典来存储每个用户的总分
    scores = []

    # 计算每个用户的总分
    for user in users:
        score = user['code_change'] * 1 + user['issue_num'] * 50 + user['comment_num'] * 10 + user['commit_num'] * 20
        user['score'] = score
        scores.append(score)

    # 计算平均分
    average_score = sum(scores) / len(scores)

    # 判断每个用户是否是free rider
    for user in users:
        if user['score'] < average_score * free_ratio:
            user['free_rider'] = True

    return users


def Deadline_fighter_judge(users, ddl_ratio):
    for user in users:
        if user['deadline_change'] > user['code_change'] * ddl_ratio:
            user['deadline_fighter'] = True
    return users


def CreateStringForAI(users):
    n = len(users)
    ans = 'A certain github repository has a total of %d contributors. The contributions of these contributors to the repository are as follows: \n' % n
    
    for i in range(n):
        str = 'Contributor %s published %d issues in the repository, commented %d times, submitted a total of %d commits, and made %d lines of code changes;\n' % (users[i]['name'], users[i]['issue_num'], users[i]['comment_num'], users[i]['commit_num'], users[i]['code_change'])
        ans += str

    ans += 'Please sort the above contributors in descending order of their contribution.'
    print(ans)
    return ans


def CalcGroupContribution(oldRepoInfo, owner, repo, deadline, free_ratio, ddl_ratio, needAI = False):
    users = Getusers(owner, repo)
    users = CountIssueAndComment(owner, repo, users)
    users = code_changes_stats(owner, repo, users, deadline)
    users = Free_rider_judge(users, free_ratio)
    users = Deadline_fighter_judge(users, ddl_ratio)
    if needAI == True:
        AnalysisBot.chat(CreateStringForAI(users))

    n = len(users)
    deadline_fighter_num = 0
    repoInfo = oldRepoInfo
    
    for i in range(n):
        repoInfo['issue_num'] += users[i]['issue_num']
        repoInfo['comment_num'] += users[i]['comment_num']
        repoInfo['commit_num'] += users[i]['commit_num']
        repoInfo['code_change'] += users[i]['code_change']
        repoInfo['deadline_change'] += users[i]['deadline_change']
        repoInfo['score'] += users[i]['score']
        if users[i]['deadline_fighter'] == True:
            deadline_fighter_num += 1


    if deadline_fighter_num / n > 0.5:
        repoInfo['deadline_fighter'] = True

    return users
