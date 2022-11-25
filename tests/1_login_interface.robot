# MANUALLY SET GECKODRIVER IN PATH
# - Linux/MacOS: `export PATH=$PATH:$PWD/tests/utils/.`

*** Settings ***
Library  SeleniumLibrary
Library  Process
Library     OperatingSystem
Library  DependencyLibrary

Suite Setup         Start the webserver
Suite Teardown      Stop the webserver

*** Keywords ***
Start the webserver
    Log To Console  start
    
    # Clean up from previous test
    Remove File     _secret_auth_.json
    
    ${process}=     Start Process       python3     -m      coverage    run     --source    tests    -m      streamlit    run     __app.py     --server.port       8001    --server.headless   true

    Set suite variable    ${process}
    Log To Console     ${process}
    sleep  2s

Stop the webserver
    Log To Console  end
    Terminate Process    ${process}


*** Variables ***
${URL}             http://localhost:8001/
${BROWSER}         headlessfirefox
# ${BROWSER}         firefox
${DRIVER_LOGS}      .logs/geckodriver.log

*** Test Cases ***
Open Login Screen
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
    Close Browser


Check For Password File
    Depends on test     Open Login Screen
    File Should Exist   _secret_auth_.json


Open Reset Password Screen
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Reset Password')]
    Click Element                   //a[contains(text(),'Reset Password')]
    Unselect Frame
    Wait Until Page Contains    Reset Password
    Close Browser


Open Create Account Screen
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Create Account')]
    Click Element                   //a[contains(text(),'Create Account')]
    Unselect Frame
    Wait Until Page Contains    Name *
    Wait Until Page Contains    Email *
    Wait Until Page Contains    Username *
    Wait Until Page Contains    Password *
    Wait Until Page Contains    Register
    Close Browser


Open Forgot Password Screen
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Forgot Password?')]
    Click Element                   //a[contains(text(),'Forgot Password?')]
    Unselect Frame
    Wait Until Page Contains    Get Password
    Close Browser
