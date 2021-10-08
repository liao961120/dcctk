from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
      long_description = f.read().strip()

setup(name='dcctk',
      version='0.0.10',
      description="Diachronic Character-based Corpus toolkit",
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/liao961120/dcctk',
      author='Yongfu Liao',
      author_email='liao961120@github.com',
      license='MIT',
      packages=['dcctk'],
      install_requires=['pyyaml', 'cqls', 'gdown>=3.10.2', 'opencc', 'transformers', 'scipy'],
      # tests_require=['deepdiff'],
      zip_safe=False)
