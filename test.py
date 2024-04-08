import redis,requests
redis_client = redis.Redis(host='localhost', port=6379, db=0)
token = "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"
headers = {'Authorization': f'token {token}'}

if __name__ == "__main__":
    # 在名为 'myhash' 的哈希表中设置多个键值对
    redis_client.lpush('deadline_fighters','{"name":"project-group14","student":"KatashiLiu"}','{"name":"project-group14","student":"wumujie"}')
    # deadlineFighters = redis_client.lrange('free_riders',0,-1)
    # if deadlineFighters != None:
    #     print(json.loads(deadlineFighters[0]))