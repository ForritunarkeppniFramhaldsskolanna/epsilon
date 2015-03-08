import sys
import re

assert re.match('^[0-9]+\n$', sys.stdin.readline())

assert sys.stdin.read() == ''
sys.exit(42)
