# Testing

## **Robot Test Framework**
- Official Website: https://robotframework.org

### **Dependencies**
- Create and activate Python virtual environment (recommended)
- Package editable installed
  ```shell
  # from project root directory
  pip install -e .
  ```
- Python libraries
  - robotframework
  - robotframework-SeleniumLibrary
  - robotframework-dependencylibrary
  - robotframework-stacktrace
  - extra-streamlit-components
  - selenium
  - coverage
  - seleniumbase
  - watchdog (generally recommended by all things streamlit related)
- Browser Drivers
  - Located in: `streamlit_login_auth_ui/tests/utils`
    - if adding other drivers, model their child directory after the driver directories currently available
  - Driver for relevant operating system and chipset architecture must be added to system path
  - Examples:
    - Firefox, MacOS, Apple Silicon: `export PATH=$PATH:$PWD/tests/utils/geckodriver_macos_arm64/.`
    - Firefox, Windows, x86, via Powershell: `$ENV:PATH += ";.\tests\util\chromedriver_win32"`
  - Download other drivers:
    - geckdriver: https://github.com/mozilla/geckodriver/releases
    - chromedriver: https://chromedriver.chromium.org/downloads


### **Running Tests**
- basic execution
  ```shell
  cd tests
  robot .
  ```

- rerun failed tests (note that doing it this way overwrites output.xml with only the failed tests)
  ```shell
  robot --rerunfiled output.xml .
  ```
  - Article about re-running tests without overwriting original results: https://medium.com/@manish.pandey65/re-run-rf-tests-15d41e154572

### **Manual Tests Pass/Fail Badge**
```shell
pip install anybadget
anybadge --label=tests --value=passing --file=testing.svg passing=green failing=red
```
- Source: https://tryexceptpass.org/article/conveying-info-with-repository-badges/
- Official website: https://github.com/jongracecox/anybadge

### **Tests Notes**
- Global Variables: `tests/_test_variables.py`
  - BROWSER OPTIONS:
    - `BROWSER`: captures value passed into `robot` cli statment (i.e., `robot --variable BROWSER:headlesschrome .`) or set separately as an environment variable
      - "firefox": Runs tests in Firefox, and opens a visible browser for each
      - "headlessfirefox" (default): Runs tests in Firefox, but in headless mode
      - "chrome": Runs tests in Chrome/Chromium, and opens a visible browser for each
      - "headlesschrome": Runs tests in Chrome/Chromium, but in headless mode
    - `DRIVER_LOGS`: Exists mostly to direct "geckodriver" logs to a subfolder when firefox is used (otherwise they clutter up the tests directory with numerous log files)
    - `TIMEOUT`: How long a test is attempted before it fails. Default is 20 (seconds). Pass `--variable TIMEOUT:<int>` to "robot" cli statment to change this.
  - PORTS:
    - Each test webserver (representing different `streamlit_login_auth_ui.__login__` initialization settings) needs to run on a different port number. The associated tests for each `__login__` setting type need to make calls to the correct port. These variables provide a central location to set the port for both a test webserver and it's associated sets file.
- Main Test App File: `tests/_test_app.py`
  - All of the tests webservers launched from `tests/__init__.robot` execute this file.
  - It allows running `__login__` under many different configuration scenarios through the use of environment variables. Different environment variables are used with each test webserver in `tests/__init__.robot`.
  - Example: One test webserver can run the app in default mode, while another can hide the Streamlit footer, another can hide account management information, and yet another can run the app with a custom user storage bolt-on.

## **Coverage**
- Official Docs: https://coverage.readthedocs.io
- ***There is no separate execution step*** (coverage runs with Robot Test Framework execution)

### **Basic Results**
```shell
coverage report
```

### **HTML Page for Results**
```shell
coverage html
```
- Open `htmlcov/index.html` in web browser

### **XML File for Plugins**
```shell
coverage xml
```
- Use a coverage plugin that supports coverage.xml
  - Example: "Coverage Gutters" for VS Code (when enabled and on a file that coverage exists for it will show green and red indicators shows which lines are covered by tests)

### **Manul Coverage Percentage Badge**
```shell
pip install anybadge
anybadge --value=98 --overwrite --file=coverage.svg coverage
```
...or...
```shell
pip install coverage-badge
coverage-badge -o coverage.svg
```

### **Coverage Configuration Notes**
- Two items result in coverage results:
  1. `coverage    run    -a    --source    tests` statement in each of the webserver "Start Process" steps in `tests/__init__.robot`
    - A separate "coverage" process is run for each webserver instance (different processes represent different start up settings passed to `streamlit_login_auth_ui.__login__`)
    - `-a` results in each coverage process appending it's results to the existing `.coverage` file rather than overwriting it.
  2. `tests/.coveragerc` configuration file
    - Omitting "." prevents coverage from including `.py` test related files in the report
    - Including the "source_pkgs" name of "streamlit_login_auth_ui" instructs coverage to include the library files (located in a different parent directory) in the report

## **Troubleshooting**

### **Leftover Processes**
Sometimes if a test run fails or is cancelled in the middle it can result in processes left running in the background. This uses up resources and can render ports unusable by processes attempting to start testing webservers, which results in failed tests.

- Identify processes using ports
  - MacOS (and probably linux)
    ```shell
    sudo lsof -i -n -P | grep TCP
    ```
- End "python" processes
  - MacOS (and probably linux)
    ```shell
    kill -9 $(ps -x | grep python)
    ```
- End "firefox" processes
  - MacOS (and probably linux)
    ```shell
    kill -9 $(ps -x | grep firefox)
    ```
- End "chrome" processes
  - MacOS (and probably linux)
    ```shell
    kill -9 $(ps -x | grep chrome)
    ```
