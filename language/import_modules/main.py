import sys, os, importlib.util

try:
    import current  # imports package, i.e. runs current/__init__.py
except ImportError:
    print("Can't import current module or package")
else:
    print(sys.modules['current'])

# the only way to import module is to use importlib
# otherwise content of the current.py should be moved to current/__init__.py
# see https://docs.python.org/3/library/importlib.html

# delete already imported package
del sys.modules['current']

# import module
module_name = 'current'
file_path = os.path.abspath(module_name + '.py')
spec = importlib.util.spec_from_file_location(module_name, file_path)
module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = module
spec.loader.exec_module(module)
print(sys.modules[module_name])
