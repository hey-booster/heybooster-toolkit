git pull
rm -rf dist
python3 version_update.py
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install --upgrade twine
python3 -m twine upload --repository pypi dist/*
git add .
git commit -m "New Version Publish"
git push -f
