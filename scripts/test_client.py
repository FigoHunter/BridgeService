from bridge_service_client import BridgeServiceClient
import time
import random

client = BridgeServiceClient('First')

@client.action()
def test(*args):
    print('execute test action')
    print(args)

while True:
    client.send_action('Second','test', ['arg1', 'arg2'])
    time.sleep(random.randint(1,5))