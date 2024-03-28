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

groups = [group1, group2, group3, ...]
group1 = {
    'name': groupname1,       
    # the group name of the first group
    'issue_num': 0,          
    # the number of issues created by this group in the repository
    'comment_num': 0,        
    # the number of comments made by this group in all issues in the repository
    'commit_num': 0, 
    # the number of commits submitted by this group in this repository
    'code_change': 0, 
    # calculate the amount of code changes made by this group in all their commits
    'deadline_change': 0, 
    # calculate the number of code changes made by this group close to the deadline
    'deadline_fighter': False, 
    # determine whether the member of this group are deadline fighters
    'score': 0
    # the contribution score of the group
}


issuePoint = 50
commitPoint = 20
commentPoint = 10
codeChangePoint = 1


deadline = '2024-04-07 00:00:00'