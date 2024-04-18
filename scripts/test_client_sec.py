from bridge_service_client import BridgeServiceClient
import time
import random

client = BridgeServiceClient('Second')

@client.action()
def test(*args):
    print('execute test action')
    print(args)

while True:
    client.send_action('First','test', ['arg2', 'arg1'])
    time.sleep(random.randint(1,5))

