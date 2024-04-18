import bridge_service
import argparse

argparser = argparse.ArgumentParser(description='Bridge Service')
argparser.add_argument('-p', type=int, default=None, help='Port to run the service on')
args = argparser.parse_args()
if args.p is not None:
    bridge_service.run(args.p)
else:
    bridge_service.run()