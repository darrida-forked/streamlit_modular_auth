*** Settings ***
Library  SeleniumLibrary
Library  Process
Library  OperatingSystem
Library  DependencyLibrary

Variables    ../_test_variables.py


*** Variables ***
${URL}            http://localhost:${PORT_DEFAULT}/


*** Test Cases ***
Default - Login Screen
    Open Browser  ${URL}  browser=${BROWSER}
        ...    service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Page Should Contain     Password
    Page Should Contain     Login
    Select Frame    tag:iframe
    Wait Until Element Is Visible   //*[contains(text(),"Navigation")]
    Page Should Contain     Navigation
    Page Should Contain     Login
    Page Should Contain     Create Account
    Page Should Contain     Forgot Password?
    Page Should Contain     Reset Password
    Unselect Frame
    Page Should Not Contain    //a[contains(text(),'Made with')]
    Page Should Not Contain    //*[@id="MainMenu"]
    Close Browser


Default - Check For Password File
    Depends on test     Default - Login Screen
    File Should Exist   _secret_auth_.json


Default - Reset Password Screen
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Reset Password')]
    Click Element                   //a[contains(text(),'Reset Password')]
    Unselect Frame
    Wait Until Page Contains    Reset Password
    Close Browser


Default - Create Account Screen
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Create Account')]
    Click Element                   //a[contains(text(),'Create Account')]
    Unselect Frame
    Wait Until Page Contains    Name *
    Wait Until Page Contains    Email *
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Page Contains    Password *
    Wait Until Page Contains    Register
    Close Browser


Default - Forgot Password Screen
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Forgot Password?')]
    Click Element                   //a[contains(text(),'Forgot Password?')]
    Unselect Frame
    Wait Until Page Contains    Get Password
    Close Browser


Default - Create Account
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
    Input Text      //*[@placeholder="Please enter your email"]    flname@email.com
    Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    Input Text      //*[@placeholder="Enter a unique username"]    user1
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    password1
    Wait Until Element Is Visible    //*[contains(text(),'Register')]
    Click Element   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Registration Successful!")]
    Page Should Contain     Registration Successful!
    Close Browser


Default - Login, then Logout
    Depends on test     Default - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user1
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password1
    Click Element   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!
    Wait Until Element Is Visible   //*[contains(text(),'Logout')]
    Click Element    //*[contains(text(),'Logout')]
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain     Login
    Close Browser


Default - Login, Refresh, Logout, Refresh (check auth cookies)
    Depends on test     Default - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user1
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password1
    Click Element   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!
    Wait Until Element Is Visible   //*[contains(text(),'Logout')]
    Page Should Contain    Logout
    Reload Page
    Wait Until Element Is Visible   //*[contains(text(),'Logout')]
    Page Should Contain    Logout
    Click Element    //*[contains(text(),'Logout')]
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain    Login
    Reload Page
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain    Login
    Close Browser


Default - Login, Close Browser, Open (check auth cookies)
    Depends on test     Default - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user1
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password1
    Click Element   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!
    Wait Until Element Is Visible   //*[contains(text(),'Logout')]
    Page Should Contain    Logout
    Close Browser
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Element Is Visible   //*[contains(text(),'Logout')]
    Page Should Contain    Logout
    Click Element    //*[contains(text(),'Logout')]
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain    Login
    Close Browser


Default - Invalid Password
    Depends on test     Default - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user1
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password2
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Click Element   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Invalid Username or Password!")]
    Page Should Contain     Invalid Username or Password!
    Close Browser


Default - Invalid Username - Special First
    Depends on test     Default - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user2
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password1
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Click Element   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Invalid Username or Password!")]
    Page Should Contain     Invalid Username or Password!
    Close Browser


Default - Reset Password
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Reset Password')]
    Click Element                   //a[contains(text(),'Reset Password')]
    Unselect Frame
    Wait Until Element Is Visible   //*[@placeholder="Please enter your email"]
    Input Text      //*[@placeholder="Please enter your email"]    flname@email.com
    Wait Until Element Is Visible   //*[@placeholder="Please enter your current password"]
    Input Text      //*[@placeholder="Please enter your current password"]    password1
    Wait Until Element Is Visible   //*[@placeholder="Please enter a new, strong password"]
    Input Text      //*[@placeholder="Please enter a new, strong password"]    password1_new
    Wait Until Element Is Visible   //*[@placeholder="Please re- enter the new password"]
    Input Text      //*[@placeholder="Please re- enter the new password"]    password1_new
    Click Element   //*[contains(text(),'Reset Password')]
    Wait Until Element Is Visible   //*[contains(text(),"Password Reset Successfully!")]
    Page Should Contain     Password Reset Successfully!
    Close Browser


Default - Reset Password Re-Login Successful
    Depends on test     Default - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user1
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password1_new
    Click Element   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!
    Wait Until Element Is Visible   //*[contains(text(),"Logout")]
    Click Element    //*[contains(text(),'Logout')]
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain    Login
    Close Browser


Default - Reset Password - Wrong Password
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Reset Password')]
    Click Element                   //a[contains(text(),'Reset Password')]
    Unselect Frame
    Wait Until Element Is Visible   //*[@placeholder="Please enter your email"]
    Input Text      //*[@placeholder="Please enter your email"]    flname@email.com
    Wait Until Element Is Visible   //*[@placeholder="Please enter your current password"]
    Input Text      //*[@placeholder="Please enter your current password"]    password_wrong
    Wait Until Element Is Visible   //*[@placeholder="Please enter a new, strong password"]
    Input Text      //*[@placeholder="Please enter a new, strong password"]    password1_new
    Wait Until Element Is Visible   //*[@placeholder="Please re- enter the new password"]
    Input Text      //*[@placeholder="Please re- enter the new password"]    password1_new
    Click Element   //*[contains(text(),'Reset Password')]
    Wait Until Element Is Visible   //*[contains(text(),"Incorrect password!")]
    Page Should Contain     Incorrect password!
    Close Browser


Default - Reset Password - Don't Match
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Reset Password')]
    Click Element                   //a[contains(text(),'Reset Password')]
    Unselect Frame
    Wait Until Element Is Visible   //*[@placeholder="Please enter your email"]
    Input Text      //*[@placeholder="Please enter your email"]    flname@email.com
    Wait Until Element Is Visible   //*[@placeholder="Please enter your current password"]
    Input Text      //*[@placeholder="Please enter your current password"]    password1_new
    Wait Until Element Is Visible   //*[@placeholder="Please enter a new, strong password"]
    Input Text      //*[@placeholder="Please enter a new, strong password"]    password1_match1
    Wait Until Element Is Visible   //*[@placeholder="Please re- enter the new password"]
    Input Text      //*[@placeholder="Please re- enter the new password"]    password1_match2
    Click Element   //*[contains(text(),'Reset Password')]
    Wait Until Element Is Visible   //*[contains(text(),"Passwords don't match!")]
    Page Should Contain     Passwords don't match!
    Close Browser


Default - Reset Password - Email Doesn't Exist
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Reset Password')]
    Click Element                   //a[contains(text(),'Reset Password')]
    Unselect Frame
    Wait Until Element Is Visible   //*[@placeholder="Please enter your email"]
    Input Text      //*[@placeholder="Please enter your email"]    flname99999@email.com
    Wait Until Element Is Visible   //*[@placeholder="Please enter your current password"]
    Input Text      //*[@placeholder="Please enter your current password"]    password1_new
    Wait Until Element Is Visible   //*[@placeholder="Please enter a new, strong password"]
    Input Text      //*[@placeholder="Please enter a new, strong password"]    password1_new2
    Wait Until Element Is Visible   //*[@placeholder="Please re- enter the new password"]
    Input Text      //*[@placeholder="Please re- enter the new password"]    password1_new2
    Click Element   //*[contains(text(),'Reset Password')]
    Wait Until Element Is Visible   //*[contains(text(),"Email does not exist!")]
    Page Should Contain     Email does not exist!
    Close Browser


Default - Create Account - No Username
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
    Input Text      //*[@placeholder="Please enter your email"]    flname111@email.com
    # Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    # Input Text      //*[@placeholder="Enter a unique username"]    user1
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    password1
    Click Element   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Please enter a valid Username! (no space characters)")]
    Page Should Contain     Please enter a valid Username! (no space characters)
    Close Browser


Default - Create Account - Invalid Username
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
    Input Text      //*[@placeholder="Please enter your email"]    flname111@email.com
    Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    Input Text      //*[@placeholder="Enter a unique username"]    userwith space
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    password1
    Click Element   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Please enter a valid Username! (no space characters)")]
    Page Should Contain     Please enter a valid Username! (no space characters)
    Close Browser


Default - Create Account - Invalid Email
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
    Input Text      //*[@placeholder="Please enter your email"]    flname@email
    Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    Input Text      //*[@placeholder="Enter a unique username"]    user2
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    password1
    Click Element   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Please enter a valid Email!")]
    Page Should Contain     Please enter a valid Email!
    Close Browser


Default - Create Account - Invalid Name
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Create Account')]
    Click Element                   //a[contains(text(),'Create Account')]
    Unselect Frame
    Wait Until Element Is Visible   //*[@placeholder="Please enter your name"]
    Input Text      //*[@placeholder="Please enter your name"]    .starts with period
    Wait Until Element Is Visible   //*[@placeholder="Please enter your email"]
    Input Text      //*[@placeholder="Please enter your email"]    flname@email
    Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    Input Text      //*[@placeholder="Enter a unique username"]    user2
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    password1
    Click Element   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Please enter a valid name!")]
    Page Should Contain     Please enter a valid name!
    Close Browser


Default - Create Account - Username Exists
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
    Input Text      //*[@placeholder="Please enter your email"]    flname5@email.com
    Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    Input Text      //*[@placeholder="Enter a unique username"]    user1
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    password1
    Click Element   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Sorry, username already exists!")]
    Page Should Contain     Sorry, username already exists!
    Close Browser


Default - Create Account - Email Exists
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
    Input Text      //*[@placeholder="Please enter your email"]    flname@email.com
    Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    Input Text      //*[@placeholder="Enter a unique username"]    user12
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    password1
    Click Element   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Email already exists!")]
    Page Should Contain     Email already exists!
    Close Browser