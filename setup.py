from setuptools import find_packages, setup

requirements_lines = [line.strip() for line in open("requirements.txt").readlines()]
install_requires = list(filter(None, requirements_lines))

setup(
    name='pyfbad',
    packages=find_packages(where="src"),
    version='0.1.4',
    description='anomaly detector',
    author='teknasyon',
    license='',
    install_requires = install_requires,
    package_dir={"": "src"},
)
