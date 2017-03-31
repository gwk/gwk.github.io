#!/usr/bin/env python3

import os
from subprocess import Popen
from time import sleep


# ANSI console colors.
RST = '\x1b[0m'
TXT_R = '\x1b[31m'

def log(*items):
  print(TXT_R, 'parent: ', *items, RST, sep='')


p_to_c_r, p_to_c_w = os.pipe() # parent-to-child.
c_to_p_r, c_to_p_w = os.pipe() # child-to-parent.

parent_pair = (c_to_p_r, p_to_c_w) # used by parent.
child_pair  = (p_to_c_r, c_to_p_w) # used by child.

env = os.environ.copy()
env.update({
  'CHILD_RECV' : str(child_pair[0]),
  'CHILD_SEND' : str(child_pair[1]),
})

proc  = Popen('./child.py', env=env, pass_fds=child_pair)

for fd in child_pair:
  os.close(fd) # crucial; otherwise parent cannot tell when child has closed its pipe or otherwise terminated.

recv = open(parent_pair[0], 'r')
send = open(parent_pair[1], 'w')

while True:
  log('waiting...')
  line = recv.readline()
  if not line: break
  msg = line.rstrip('\n')
  log('read: ', repr(msg))
  sleep(0.1)
  response = 'ack ' + msg
  log('resp: ', repr(response))
  print(response, file=send, flush=True)

log('stopped. cleanup...')

for fd in parent_pair:
  os.close(fd)

proc.wait()
log(f'done; child exit code: {proc.returncode}')
