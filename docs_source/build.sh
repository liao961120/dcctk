rm -r img/ _build/
pandoc nb/dcctk_test.ipynb -f ipynb -t rst --extract-media img/ -s -o temp.rst

echo -e 'Quick Start\n================\n\n' > usage.rst
cat temp.rst >> usage.rst
rm temp.rst

make html

cp -r _build/html/* ../docs/
