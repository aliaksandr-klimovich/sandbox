namespace = dict(
    a=1,
)


def function_namespace():
    b = 2
    return locals()


def main():
    main.__globals__.update(namespace)
    print(a)
    main.__globals__.update(function_namespace())
    print(b)


if __name__ == '__main__':
    main()
