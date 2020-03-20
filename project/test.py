import time, random, string, datetime
orderid = ''.join(random.sample(string.ascii_letters+string.digits, 8))
print(orderid)

print(time.strftime("%Y%m%d%H%M", time.localtime()))
