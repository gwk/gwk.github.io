#!/usr/bin/env python3

import os
from time import sleep


# ANSI console colors.
RST = '\x1b[0m'
TXT_G = '\x1b[32m'

def log(*items):
  print(TXT_G, 'child: ', *items, RST, sep='')


recv = open(int(os.environ['CHILD_RECV']), 'r')
send = open(int(os.environ['CHILD_SEND']), 'w')

def request(msg):
  log('send: ', repr(msg))
  print(msg, file=send, flush=True)
  log('waiting...')
  response = recv.readline().rstrip('\n')
  log('recv: ', repr(response))

for msg in 'abc':
  request(msg)

log('done.')
