from main import redis_conn, Order
import time

key = 'refund_order'
group = 'payment-group'

try:
    redis_conn.xgroup_create(key, group, mkstream=True)
except:
    print('Group already exists')

while True:
    try:
        results = redis_conn.xreadgroup(group, key, {key: '>'}, None)
        
        if results != []:
            for result in results:
                obj = result[1][0][1]
                order = Order.get(obj['pk'])
                order.status = 'refunded'
                order.save()

    except Exception as e:
        print(f'Error reading from Redis: {str(e)}')
        continue

    time.sleep(1)