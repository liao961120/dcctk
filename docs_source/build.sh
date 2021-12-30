pandoc nb/corpusSearch.ipynb -f ipynb -t rst --extract-media img/ -s -o temp.rst
pandoc nb/corpusAnalysis.ipynb -f ipynb -t rst --extract-media img/ -s -o temp2.rst

echo -e 'Query\n================\n\n' > query.rst
cat temp.rst >> query.rst
rm temp.rst

echo -e 'Stats\n================\n\n' > stats.rst
cat temp2.rst >> stats.rst
rm temp2.rst

make html

cp -r _build/html/* ../docs/
rm -r img/ _build/
