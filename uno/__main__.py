import argparse
import os

from .Client import Player
from .server import start_server

parser = argparse.ArgumentParser(description='Basic UNO card game using XMLRPC, written in python')
parser.add_argument('-s', '--server', action="store_true", help='start a server')
parser.add_argument('-c', '--client', action="store_true", help='start a client')
parser.add_argument('-p', '--port', dest='port', default=8000, help='Port to serve on / connect to')
parser.add_argument('-H', '--host', dest='host', default='localhost', help='Hostname to host on / connect to')
parser.add_argument('player_name', nargs='?', default='player%s' % os.getpid(), help='Your player name')

args = parser.parse_args()
if args.server:
    start_server(args.host, args.port)
if args.client:
    Player(f'http://{args.host}:{args.port}/', args.player_name)
