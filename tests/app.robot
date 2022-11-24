*** Settings ***
Library  SeleniumLibrary
Library  Process

Suite Setup         Start the webserver
Suite Teardown      Stop the webserver

*** Keywords ***
# Setup geckodriver
    # Set Environment Variable  webdriver.geckodriver.driver  ${EXECDIR}tests/utils/geckodriver
    # export PATH=$PATH:$PWD/tests/utils/.

Start the webserver
    Log To Console  start
    ${process}=     Start Process       python3     -m      coverage    run     --source    tests    -m      streamlit    run     __app.py     --server.port       8000    --server.headless   true

    Set suite variable    ${process}
    Log To Console     ${process}
    sleep  2s

Stop the webserver
    Log To Console  end
    Terminate Process    ${process}


*** Variables ***
${URL}             http://localhost:8000/
${BROWSER}         headlessfirefox
# ${BROWSER}         firefox

*** Test Cases ***
Open Login Screen
    Open Browser  ${URL}  browser=${BROWSER}
    Wait Until Page Contains    Username
    Page Should Contain     Password
    Page Should Contain     Reset Password
    Page Should Contain     Forgot Password?
    Page Should Contain     Create Account
    Page Should Contain     Navigation
    Close Browser


Open Reset Password Screen
    Open Browser    ${URL}  browser=${BROWSER}
    Wait Until Page Contains    Username
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Reset Password')]
    Click Element                   //a[contains(text(),'Reset Password')]
    Unselect Frame
    Wait Until Page Contains    Reset Password
    Close Browser


Open Create Account Screen
    Open Browser    ${URL}  browser=${BROWSER}
    Wait Until Page Contains    Username
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Create Account')]
    Click Element                   //a[contains(text(),'Create Account')]
    Unselect Frame
    Wait Until Page Contains    Register
    Close Browser


Open Forgot Password Screen
    Open Browser    ${URL}  browser=${BROWSER}
    Wait Until Page Contains    Username
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Forgot Password?')]
    Click Element                   //a[contains(text(),'Forgot Password?')]
    Unselect Frame
    Wait Until Page Contains    Get Password
    Close Browser


    #<a href="#" class="nav-link" aria-current="page" data-v-4323f8ce="" style="font-size: 14px; text-align: left; margin: 0px;"><i class="icon bi-x-circle" data-v-4323f8ce=""></i> Forgot Password?</a>