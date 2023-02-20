*** Settings ***
Library  SeleniumLibrary
Library  Process
Library  OperatingSystem
Library  DependencyLibrary

Variables    ../_test_variables.py


*** Variables ***
${URL}             http://localhost:${PORT_CUSTOM_FORGOT_PASSWORD}/


*** Test Cases ***
Custom Forgot Pwd Msg - Login Screen
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


Custom Forgot Pwd Msg - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Create Account')]
    Click Element                   //a[contains(text(),'Create Account')]
    Unselect Frame
    Wait Until Element Is Visible   //*[@placeholder="Please enter your first name"]
    Input Text      //*[@placeholder="Please enter your first name"]    Fname
    Wait Until Element Is Visible   //*[@placeholder="Please enter your last name"]
    Input Text      //*[@placeholder="Please enter your last name"]    Lname
    Wait Until Element Is Visible   //*[@placeholder="Please enter your email"]
    Input Text      //*[@placeholder="Please enter your email"]    forgot_password@email.com
    Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    Input Text      //*[@placeholder="Enter a unique username"]    forgot_password
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    forgot_password
    Click Element   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Registration Successful!")]
    Page Should Contain     Registration Successful!
    Close Browser


Custom Forgot Pwd Msg - Login, then Logout
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    forgot_password
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    forgot_password
    Click Element   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!
    Wait Until Element Is Visible   //*[contains(text(),"Logout")]
    Click Element    //*[contains(text(),'Logout')]
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain    Login
    Close Browser


Custom Forgot Pwd Msg - Reset Password
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Forgot Password')]
    Click Element                   //a[contains(text(),'Forgot Password')]
    Unselect Frame
    Wait Until Element Is Visible   //*[@placeholder="Please enter your email"]
    Input Text      //*[@placeholder="Please enter your email"]    forgot_password@email.com
    Click Element   //*[contains(text(),'Get Password')]
    Wait Until Element Is Visible   //*[contains(text(),"Secure Password Sent Successfully!")]
    Page Should Contain     Secure Password Sent Successfully!
    Wait Until Element Is Visible   //*[contains(text(),"Password via an insecure method:")]
    Page Should Contain     Password via an insecure method:
    Close Browser


Custom Forgot Pwd Msg - Reset Password - No Email Exists
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Forgot Password')]
    Click Element                   //a[contains(text(),'Forgot Password')]
    Unselect Frame
    Wait Until Element Is Visible   //*[@placeholder="Please enter your email"]
    Input Text      //*[@placeholder="Please enter your email"]    forgot_password_none@email.com
    Click Element   //*[contains(text(),'Get Password')]
    Wait Until Element Is Visible   //*[contains(text(),"No account with this email was found!")]
    Page Should Contain     No account with this email was found!
    Close Browser
