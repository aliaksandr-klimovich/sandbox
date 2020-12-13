import os
import sys

r, w = os.pipe()
pid = os.fork()

if pid:
    # This is a parent process
    # Close write fd because parent is not going to write to pipe
    os.close(w)
    r = os.fdopen(r)
    # Read from pipe
    text = r.read()
    print(f'text = "{text}", pid = {pid}')
    sys.exit(0)
else:
    # This is the child process
    # Close read fd because child is not going to read from pipe
    os.close(r)
    w = os.fdopen(w, 'w')
    # Write to pipe
    w.write('Some text...')
    w.close()
    sys.exit(0)
