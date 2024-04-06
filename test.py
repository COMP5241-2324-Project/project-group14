import redis,requests
redis_client = redis.Redis(host='localhost', port=6379, db=0)
token = "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"
headers = {'Authorization': f'token {token}'}

if __name__ == "__main__":
    from datetime import datetime
    today = datetime.today()
    future_date = datetime(2024, 2, 6)
    difference = today - future_date
    days = difference.days
    print(days)
    # deadlineFighters = redis_client.lrange('free_riders',0,-1)
    # if deadlineFighters != None:
    #     print(json.loads(deadlineFighters[0]))