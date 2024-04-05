import redis,json
redis_client = redis.Redis(host='localhost', port=6379, db=0)

if __name__ == "__main__":
    totalCommit = redis_client.get('totalCommit').decode('utf-8')
    print(totalCommit)
    # deadlineFighters = redis_client.lrange('free_riders',0,-1)
    # if deadlineFighters != None:
    #     print(json.loads(deadlineFighters[0]))