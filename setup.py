from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
      long_description = f.read().strip()

setup(name='dcctk',
      version='0.0.1',
      description="Diachronic Character-based Corpus toolkit",
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/liao961120/dcctk',
      author='Yongfu Liao',
      author_email='liao961120@github.com',
      license='MIT',
      packages=find_packages("dcctk", exclude=["test"]),
      install_requires=['pyyaml'],
      # tests_require=['deepdiff'],
      zip_safe=False)
