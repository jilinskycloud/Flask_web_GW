import redis

r1 = redis.StrictRedis(host='localhost', port=6370, db=1, charset="utf-8", decode_responses=True)


data = r1.lrange('ac233f211b2a', 0, -1)
print(data)