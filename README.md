# Selenium for validation


## Development setup (for GNU/Linux OS)


Create a directory for source code

```sh
mkdir selenium-validation-test
cd selenium-validation-test
```

Install Virtual environment

```sh
sudo pip3 install virtualenv

# Create a virtual environment for project
virtualenv -p python3 venv

# Active
source venv/bin/activate
```

Install required packages

```sh
git checkout develop
pip install -r requirements.txt
```

Config configuration (setting)
```sh
cp settings/settings.sample.py settings.py
```

Run test

```sh
python selenium_test_suite.py
```