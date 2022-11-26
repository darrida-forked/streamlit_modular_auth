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
        ...    env:LOGOUT_BUTTON_NAME=Exit

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
Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Create Account')]
    Click Element                   //a[contains(text(),'Create Account')]
    Unselect Frame
    Wait Until Element Is Visible   //*[@placeholder="Please enter your name"]
    Input Text      //*[@placeholder="Please enter your name"]    Fname Lname
    Wait Until Element Is Visible   //*[@placeholder="Please enter your email"]
    Input Text      //*[@placeholder="Please enter your email"]    flname@email.com
    Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    Input Text      //*[@placeholder="Enter a unique username"]    user5
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    password5
    Click Button   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Registration Successful!")]
    Page Should Contain     Registration Successful!
    Close Browser


Logout Button is Exit
    Depends on test     Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user5
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password5
    Click Button   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!
    Wait Until Element Is Visible   //*[contains(text(),'Exit')]
    Click Button    //*[contains(text(),'Exit')]
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain     Login
    Close Browser

