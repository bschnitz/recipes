import setuptools

with open('requirements.txt', 'r') as f:
  install_requires = f.read().splitlines()

setuptools.setup(name='recipes',
                 packages=['recipes'],
                 install_requires=install_requires)
