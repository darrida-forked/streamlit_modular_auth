# MANUALLY SET GECKODRIVER IN PATH
# - Linux/MacOS: `export PATH=$PATH:$PWD/tests/utils/.`

*** Settings ***
Library  SeleniumLibrary
Library  Process
Library  OperatingSystem
Library  DependencyLibrary

Variables    ../__test_variables.py


*** Variables ***
${URL}             http://localhost:${PORT_CUSTOM_FORGOT_PASSWORD}/


*** Test Cases ***
Custom Storage - Login Screen
    Open Browser  ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Page Should Contain     Password
    Page Should Contain     Login
    Select Frame    tag:iframe
    Wait Until Element Is Visible   //*[contains(text(),"Navigation")]
    Page Should Contain     Navigation
    Page Should Contain     Create Account
    Page Should Contain     Forgot Password?
    Page Should Contain     Reset Password
    Close Browser


Custom Storage - Create Account
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
    Input Text      //*[@placeholder="Please enter your email"]    forgot_password@email.com
    Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    Input Text      //*[@placeholder="Enter a unique username"]    forgot_password
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    forgot_password
    Click Button   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Registration Successful!")]
    Page Should Contain     Registration Successful!
    Close Browser


Custom Storage - Login Successful
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    forgot_password
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    forgot_password
    Click Button   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!
    Close Browser


Custom Storage - Reset Password
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Forgot Password')]
    Click Element                   //a[contains(text(),'Forgot Password')]
    Unselect Frame
    Wait Until Element Is Visible   //*[@placeholder="Please enter your email"]
    Input Text      //*[@placeholder="Please enter your email"]    forgot_password@email.com
    Click Button   //*[contains(text(),'Get Password')]
    Wait Until Element Is Visible   //*[contains(text(),"Secure Password Sent Successfully!")]
    Page Should Contain     Secure Password Sent Successfully!
    Wait Until Element Is Visible   //*[contains(text(),"Password via an insecure method:")]
    Page Should Contain     Password via an insecure method:
    Close Browser
