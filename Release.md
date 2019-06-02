### Release Steps
Create 2 virtualenv to generate package for both python 2 & 3 


```bash
virtualenv -p /usr/bin/python3 venv
virtualenv -p /usr/bin/python2 venv2
# activate python3 venv
 source venv/bin/activate
 pip install -r requirements.txt
 python3 setup.py sdist bdist_wheel
 deactivate
  # switch to python2  venv2
 source venv2/bin/activate
 pip install -r requirements.txt
 python2.7 setup.py sdist bdist_wheel
 # Check for Markdown  error
 twine check dist/*
 # Replace the 0.5 with current version
 twine upload dist/superhooks-0.5.tar.gz
 twine upload dist/superhooks-0.5-py2-none-any.whl 
 twine upload dist/superhooks-0.5-py3-none-any.whl
 ```
 