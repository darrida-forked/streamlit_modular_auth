# MANUALLY SET GECKODRIVER IN PATH
# - Linux/MacOS: `export PATH=$PATH:$PWD/tests/utils/.`

*** Settings ***
Library  SeleniumLibrary
Library  Process
Library  OperatingSystem
Library  DependencyLibrary

Suite Setup         Start the webserver
Suite Teardown      Stop the webserver


*** Keywords ***
Start the webserver
    Log To Console  start
    
    ${PROCESS}    Start Process   python3    
        ...    -m    coverage    run    --source    tests   
        ...    -m    streamlit    run    __test_app.py    
        ...    --server.port    8001    
        ...    --server.headless   true
        ...    env:HIDE_MENU=true

    Set suite variable    ${PROCESS}
    Log To Console     ${PROCESS}
    sleep    2s

Stop the webserver
    Log To Console    end
    Terminate Process


*** Variables ***
${URL}             http://localhost:8001/
${BROWSER}         headlessfirefox
# ${BROWSER}         firefox
${DRIVER_LOGS}      .logs/geckodriver.log


*** Test Cases ***
Login Screen
    Open Browser  ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username
    Page Should Contain     Password
    Page Should Contain     Login
    Select Frame    tag:iframe
    Page Should Contain     Navigation
    Page Should Contain     Login
    Page Should Contain     Create Account
    Page Should Contain     Forgot Password?
    Page Should Contain     Reset Password
    Unselect Frame
    Page Should Not Contain    //*[@id="MainMenu"]
    Close Browser
