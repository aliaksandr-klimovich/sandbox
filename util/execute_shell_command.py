from subprocess import Popen, PIPE


def run(command, input_, fail=True):
    """
    Run a shell command in the subprocess.

    command: string representation of the command

    Example:
        r, out, err = run("ls -l")
        print(out)
    """

    print('-' * 80)
    print('Run: {}'.format(command))

    p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate(input=input_)

    rc = p.poll()
    out = out.strip()
    err = err.strip()

    print('rc:  {}'.format(rc))
    print('out: {}'.format(out))
    print('err: {}'.format(err))

    if rc != 0 and fail and getattr(run, 'failed', False):
        run.failed = True
        exit(1)

    return rc, out, err


# todo add example
if __name__ == '__main__':
    pass
