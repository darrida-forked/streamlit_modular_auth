# MANUALLY SET GECKODRIVER IN PATH
# - Linux/MacOS: `export PATH=$PATH:$PWD/tests/utils/.`

*** Settings ***
Library  SeleniumLibrary
Library  Process
Library  OperatingSystem
Library  DependencyLibrary


*** Variables ***
${URL}             http://localhost:8002/
${BROWSER}         headlessfirefox
# ${BROWSER}         firefox
${DRIVER_LOGS}      .logs/geckodriver.log


*** Test Cases ***
No Reg - Login Screen
    Open Browser  ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username
    Page Should Contain     Password
    Page Should Contain     Login
    Select Frame    tag:iframe
    Page Should Contain     Navigation
    Page Should Contain     Login
    Page Should Not Contain     Create Account
    Page Should Contain     Forgot Password?
    Page Should Contain     Reset Password
    Close Browser


No Reg - Reset Password Screen
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Reset Password')]
    Click Element                   //a[contains(text(),'Reset Password')]
    Unselect Frame
    Wait Until Page Contains    Reset Password
    Close Browser


No Reg - Forgot Password Screen
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Forgot Password?')]
    Click Element                   //a[contains(text(),'Forgot Password?')]
    Unselect Frame
    Wait Until Page Contains    Get Password
    Close Browser


No Reg - Create Account
    Open Browser    http://localhost:8001/  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Create Account')]
    Click Element                   //a[contains(text(),'Create Account')]
    Unselect Frame
    Wait Until Element Is Visible   //*[@placeholder="Please enter your name"]
    Input Text      //*[@placeholder="Please enter your name"]    Fname Lname
    Wait Until Element Is Visible   //*[@placeholder="Please enter your email"]
    Input Text      //*[@placeholder="Please enter your email"]    flname5@email.com
    Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    Input Text      //*[@placeholder="Enter a unique username"]    user5
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    password5
    Click Button   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Registration Successful!")]
    Page Should Contain     Registration Successful!
    Close Browser


No Reg - Login Successful
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user5
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password5
    Click Button   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!
    Close Browser


No Reg - Login, then Logout
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user5
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password5
    Click Button   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!
    Wait Until Element Is Visible   //*[contains(text(),'Logout')]
    Click Button    //*[contains(text(),'Logout')]
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain     Login
    Close Browser


No Reg - Login Failed - Invalid Password
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user5
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password2
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Click Button   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Invalid Username or Password!")]
    Page Should Contain     Invalid Username or Password!
    Close Browser


No Reg - Login Failed - Invalid Username
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user2
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password5
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Click Button   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Invalid Username or Password!")]
    Page Should Contain     Invalid Username or Password!
    Close Browser
