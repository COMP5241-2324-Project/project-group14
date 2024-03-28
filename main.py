import CalcGroupContribution


def CreateNewRepoInfo(owner, name):
    return {'name': owner + '/' + name, 'issue_num': 0, 'comment_num': 0, 'commit_num': 0, 'code_change': 0, 'deadline_change': 0, 'deadline_fighter': False, 'score': 0}


def 


if __name__ == '__main__':
    filePath = 'groups.txt'
    deadline = '2024-03-27 00:00:00'
    free_ratio = 0.3
    ddl_ratio = 0.8

    repos = []

    with open(filePath, 'r') as f:
        line = f.readline()             
        while line:            
            owner = line.split()[0]
            name = line.split()[1]
            print('Now handle %s/%s ' % (owner, name))
            repo = CreateNewRepoInfo(owner, name)
            repo = CalcGroupContribution.CalcGroupContribution(repo, owner, name, deadline, free_ratio, ddl_ratio, needAI = False)
            print('The info of the whole repo:')
            print(repo)
            repos.append(repo)
            line = f.readline() 
                
        

