from pathlib import Path

from setuptools import setup, find_packages

dir_path = Path(__file__).resolve().parent

with dir_path.joinpath('easyrl').joinpath('version.py').open('r') as fp:
    exec(fp.read())


def read_requirements_file(filename):
    req_file = dir_path.joinpath(filename)
    with req_file.open('r') as f:
        return [line.strip() for line in f]


from IPython import embed

embed()
packages = find_packages()
# Ensure that we don't pollute the global namespace.
easyrl_pkgs = []
for p in packages:
    if p == 'easyrl' or p.startswith('easyrl.'):
        easyrl_pkgs.append(p)

setup(
    name='easyrl',
    version=__version__,
    author='Tao Chen',
    url='https://github.com/taochenshh/easyrl.git',
    license='MIT',
    packages=packages,
    package_dir={'': '.'},
    install_requires=read_requirements_file('requirements.txt'),
)