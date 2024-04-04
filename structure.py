users = [user1, user2, user3, ...]
user1 = {
    'name': username1,       
    # the username of the first user
    'issue_num': 0,          
    # the number of issues created by this member in the repository
    'comment_num': 0,        
    # the number of comments made by this member in all issues in the repository
    'commit_num': 0, 
    # the number of commits submitted by this member in this repository
    'code_change': 0, 
    # calculate the amount of code changes made by this member in all his/her commits
    'deadline_change': 0, 
    # calculate the number of code changes made by this member close to the deadline
    'deadline_fighter': False, 
    # determine whether the member is a deadline fighter
    'free_rider': False,
    # determine whether the member is a free rider
    'score': 0
    # the contribution score of the member
}

repos = [repo1, repo2, repo3, ...]
repo1 = {
    'name': repo1name,       
    # the name of the first repo
    'issue_num': 0,          
    # the number of issues in this repository
    'comment_num': 0,        
    # the number of comments in all issues in the repo
    'commit_num': 0, 
    # the number of commits submitted by the contributors in this repo
    'code_change': 0, 
    # calculate the amount of code changes made by the contributors in this repo
    'deadline_change': 0, 
    # calculate the number of code changes made by the contributors in this repo
    'deadline_fighter': False, 
    # determine whether the contributors in this repo are deadline fighters
    'score': 0
    # the contribution score of the repo
}


issuePoint = 50
commitPoint = 20
commentPoint = 10
codeChangePoint = 1


deadline = '2024-04-07 00:00:00'