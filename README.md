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

Install chromedriver
```sh
The latest drivers can be found at:

https://sites.google.com/a/chromium.org/chromedriver/downloads

Download and copy to correct directory
For windows: C:\Windows
For mac/ubuntu: /usr/local/bin
```

Run test

```sh
python selenium_test_suite.py
```