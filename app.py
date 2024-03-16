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

@app.route('/code_changes_stats')
def code_changes_stats():
    # 初始化一个字典来存储每个用户的提交次数和代码修改总数
    user_stats = {}
    page = 1
    while True:
        url_commits = "https://api.github.com/repos/{owner}/{repo}/commits?page={page}&per_page=100"
        response_commits = requests.get(url_commits.format(owner="COMP5241-2324-Project", repo="Simpsyber", page=page), headers = headers)
        commits = response_commits.json()
        if not commits:
            break

        for commit in commits:
            author = commit['commit']['author']['name']
            if author not in user_stats:
                user_stats[author] = {'commit_count': 0, 'total_changes': 0}

            user_stats[author]['commit_count'] += 1

            url_commit = "https://api.github.com/repos/{owner}/{repo}/commits/{sha}"
            response_commit = requests.get(url_commit.format(owner="COMP5241-2324-Project", repo="Simpsyber", sha=commit['sha'], headers = headers))
            commit_data = response_commit.json()
            if 'stats' in commit_data:
                user_stats[author]['total_changes'] += commit_data['stats']['total']

        page += 1

    return jsonify(user_stats)


if __name__ == '__main__':
    app.run(debug=True)