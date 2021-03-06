import sys
import requests
import time

"""
Use: single command line arg must be the filename to parse
"""

input_file = sys.argv[1]
f = open(input_file, "r")

lines = f.read()

commands = []

for line in lines.split('\n'):
    split_line = [x for x in line.split(' ') if x != '']
    print(split_line)
    command = split_line[1]
    tokens = command.split(',')
    action = tokens[0]
    args = tokens[1:]

    if action == "ADD":
        #userid, amount
        cmd = {
            'id': args[0],
            'amount': float(args[1])
        }

    elif action in ["QUOTE", "CANCEL_SET_BUY", "CANCEL_SET_SELL"]:
        #userid, StockSymbol
        cmd = {
            'id': args[0],
            'stock': args[1]
        }

    elif action in ["BUY", "SELL", "SET_BUY_AMOUNT", "SET_BUY_TRIGGER", "SET_SELL_AMOUNT", "SET_SELL_TRIGGER"]:
        #userid, StockSymbol, amount
        cmd = {
            'id': args[0],
            'stock': args[1],
            'amount': float(args[2])
        }
    
    elif action in ["COMMIT_BUY", "CANCEL_BUY", "COMMIT_SELL", "CANCEL_SELL", "DISPLAY_SUMMARY"]:
        #userid
        cmd = {
            'id': args[0]
        }

    elif action == "DUMPLOG":
        if len(args) == 2:
            action = "USER_DUMPLOG"
            cmd = {
                'id': args[0],
                'filename': args[1]
            }
        else:
            cmd = {
                'filename': args[0]
            }

    else:
        print("invalid action")

    commands.append(cmd)
    time.sleep(5)
    req = requests.post("http://localhost:5000/{}".format(action), json=cmd)