import CalcGroupContribution
import AnalysisBot

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


if __name__ == '__main__':
    filePath = 'groups.txt'
    deadline = '2024-04-07 00:00:00'
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
    
    AnalysisBot.chat(CreateRepoStringForAI(repos))
                
        

