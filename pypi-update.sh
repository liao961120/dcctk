[[ -d build/ ]] && rm -r build/ 
[[ -d build/ ]] && rm -r build/ 
[[ -d dist/ ]] && rm -r dist/
[[ -d dcctk.egg-info/ ]] && rm -r dcctk.egg-info/
python3 setup.py sdist bdist_wheel &&
twine upload dist/*
