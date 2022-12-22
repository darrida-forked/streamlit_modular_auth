*** Settings ***
Library  SeleniumLibrary
Library  Process
Library  OperatingSystem
Library  DependencyLibrary

Variables    ../_test_variables.py


*** Variables ***
${URL}             http://localhost:${PORT_LOGOUT_NAME_CHANGE}/


*** Test Cases ***
Logout Name - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Create Account')]
    Click Element                   //a[contains(text(),'Create Account')]
    Unselect Frame
    Wait Until Element Is Visible   //*[@placeholder="Please enter your name"]
    Input Text      //*[@placeholder="Please enter your name"]    Fname Lname
    Wait Until Element Is Visible   //*[@placeholder="Please enter your email"]
    Input Text      //*[@placeholder="Please enter your email"]    flname1@email.com
    Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    Input Text      //*[@placeholder="Enter a unique username"]    user6
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    password6
    Click Button   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Registration Successful!")]
    Page Should Contain     Registration Successful!
    Close Browser


Logout Name - Logout Button is Exit
    Depends on test     Logout Name - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user6
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password6
    Click Button   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!
    Wait Until Element Is Visible   //*[contains(text(),'Exit')]
    Click Button    //*[contains(text(),'Exit')]
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain     Login
    Close Browser

