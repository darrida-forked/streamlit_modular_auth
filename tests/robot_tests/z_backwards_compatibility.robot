*** Settings ***
Library  SeleniumLibrary
Library  Process
Library  OperatingSystem
Library  DependencyLibrary

Variables    ../_test_variables.py


*** Variables ***
${URL}            http://localhost:${PORT_BACKWARDS_COMPATIBILITY}/


*** Test Cases ***
Backwards Compatible - Login Screen
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


Backwards Compatible - Check For Password File
    Depends on test     Backwards Compatible - Login Screen
    File Should Exist   _secret_auth_.json


Backwards Compatible - Reset Password Screen
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Reset Password')]
    Click Element                   //a[contains(text(),'Reset Password')]
    Unselect Frame
    Wait Until Page Contains    Reset Password
    Close Browser


Backwards Compatible - Create Account Screen
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


Backwards Compatible - Forgot Password Screen
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Forgot Password?')]
    Click Element                   //a[contains(text(),'Forgot Password?')]
    Unselect Frame
    Wait Until Page Contains    Get Password
    Close Browser


Backwards Compatible - Create Account
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
    Input Text      //*[@placeholder="Please enter your email"]    legacy@email.com
    Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    Input Text      //*[@placeholder="Enter a unique username"]    legacy1
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    password1
    Click Button   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Registration Successful!")]
    Page Should Contain     Registration Successful!
    Close Browser


Backwards Compatible - Login, then Logout
    Depends on test     Backwards Compatible - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    legacy1
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password1
    Click Button   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!
    Wait Until Element Is Visible   //*[contains(text(),'Logout')]
    Click Button    //*[contains(text(),'Logout')]
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain     Login
    Close Browser


Backwards Compatible - Login, Refresh, Logout, Refresh (check auth cookies)
    Depends on test     Backwards Compatible - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    legacy1
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password1
    Click Button   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!
    Wait Until Element Is Visible   //*[contains(text(),'Logout')]
    Page Should Contain    Logout
    Reload Page
    Wait Until Element Is Visible   //*[contains(text(),'Logout')]
    Page Should Contain    Logout
    Click Button    //*[contains(text(),'Logout')]
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain    Login
    Reload Page
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain    Login
    Close Browser


Backwards Compatible - Login, Close Browser, Open (check auth cookies)
    Depends on test     Backwards Compatible - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    legacy1
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password1
    Click Button   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!
    Wait Until Element Is Visible   //*[contains(text(),'Logout')]
    Page Should Contain    Logout
    Close Browser
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Element Is Visible   //*[contains(text(),'Logout')]
    Page Should Contain    Logout
    Click Button    //*[contains(text(),'Logout')]
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain    Login
    Close Browser


Backwards Compatible - Invalid Password
    Depends on test     Backwards Compatible - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    legacy1
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password2
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Click Button   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Invalid Username or Password!")]
    Page Should Contain     Invalid Username or Password!
    Close Browser


Backwards Compatible - Invalid Username - Special First
    Depends on test     Backwards Compatible - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    legacy2
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password1
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Click Button   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Invalid Username or Password!")]
    Page Should Contain     Invalid Username or Password!
    Close Browser


Backwards Compatible - Reset Password
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Reset Password')]
    Click Element                   //a[contains(text(),'Reset Password')]
    Unselect Frame
    Wait Until Element Is Visible   //*[@placeholder="Please enter your email"]
    Input Text      //*[@placeholder="Please enter your email"]    legacy@email.com
    Wait Until Element Is Visible   //*[@placeholder="Please enter your current password"]
    Input Text      //*[@placeholder="Please enter your current password"]    password1
    Wait Until Element Is Visible   //*[@placeholder="Please enter a new, strong password"]
    Input Text      //*[@placeholder="Please enter a new, strong password"]    password1_new
    Wait Until Element Is Visible   //*[@placeholder="Please re- enter the new password"]
    Input Text      //*[@placeholder="Please re- enter the new password"]    password1_new
    Click Button   //*[contains(text(),'Reset Password')]
    Wait Until Element Is Visible   //*[contains(text(),"Password Reset Successfully!")]
    Page Should Contain     Password Reset Successfully!
    Close Browser


Backwards Compatible - Reset Password Re-Login Successful
    Depends on test     Backwards Compatible - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    legacy1
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password1_new
    Click Button   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!
    Wait Until Element Is Visible   //*[contains(text(),"Logout")]
    Click Button    //*[contains(text(),'Logout')]
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain    Login
    Close Browser


Backwards Compatible - Reset Password - Wrong Password
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Reset Password')]
    Click Element                   //a[contains(text(),'Reset Password')]
    Unselect Frame
    Wait Until Element Is Visible   //*[@placeholder="Please enter your email"]
    Input Text      //*[@placeholder="Please enter your email"]    legacy@email.com
    Wait Until Element Is Visible   //*[@placeholder="Please enter your current password"]
    Input Text      //*[@placeholder="Please enter your current password"]    password_wrong
    Wait Until Element Is Visible   //*[@placeholder="Please enter a new, strong password"]
    Input Text      //*[@placeholder="Please enter a new, strong password"]    password1_new
    Wait Until Element Is Visible   //*[@placeholder="Please re- enter the new password"]
    Input Text      //*[@placeholder="Please re- enter the new password"]    password1_new
    Click Button   //*[contains(text(),'Reset Password')]
    Wait Until Element Is Visible   //*[contains(text(),"Incorrect password!")]
    Page Should Contain     Incorrect password!
    Close Browser


Backwards Compatible - Reset Password - Don't Match
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   tag:iframe
    Select Frame    tag:iframe
    Wait Until Element Is Visible      //a[contains(text(),'Reset Password')]
    Click Element                   //a[contains(text(),'Reset Password')]
    Unselect Frame
    Wait Until Element Is Visible   //*[@placeholder="Please enter your email"]
    Input Text      //*[@placeholder="Please enter your email"]    legacy@email.com
    Wait Until Element Is Visible   //*[@placeholder="Please enter your current password"]
    Input Text      //*[@placeholder="Please enter your current password"]    password1_new
    Wait Until Element Is Visible   //*[@placeholder="Please enter a new, strong password"]
    Input Text      //*[@placeholder="Please enter a new, strong password"]    password1_match1
    Wait Until Element Is Visible   //*[@placeholder="Please re- enter the new password"]
    Input Text      //*[@placeholder="Please re- enter the new password"]    password1_match2
    Click Button   //*[contains(text(),'Reset Password')]
    Wait Until Element Is Visible   //*[contains(text(),"Passwords don't match!")]
    Page Should Contain     Passwords don't match!
    Close Browser


Backwards Compatible - Reset Password - Email Doesn't Exist
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
    Click Button   //*[contains(text(),'Reset Password')]
    Wait Until Element Is Visible   //*[contains(text(),"Email does not exist!")]
    Page Should Contain     Email does not exist!
    Close Browser


Backwards Compatible - Create Account - No Username
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
    # Input Text      //*[@placeholder="Enter a unique username"]    legacy1
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    password1
    Click Button   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Please enter a valid Username! (no space characters)")]
    Page Should Contain     Please enter a valid Username! (no space characters)
    Close Browser


Backwards Compatible - Create Account - Invalid Username
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
    Click Button   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Please enter a valid Username! (no space characters)")]
    Page Should Contain     Please enter a valid Username! (no space characters)
    Close Browser


Backwards Compatible - Create Account - Invalid Email
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
    Input Text      //*[@placeholder="Please enter your email"]    legacy2@email.com
    Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    Input Text      //*[@placeholder="Enter a unique username"]    legacy2
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    password1
    Click Button   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Please enter a valid Email!")]
    Page Should Contain     Please enter a valid Email!
    Close Browser


Backwards Compatible - Create Account - Invalid Name
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
    Input Text      //*[@placeholder="Please enter your email"]    legacy2@email
    Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    Input Text      //*[@placeholder="Enter a unique username"]    legacy2
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    password1
    Click Button   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Please enter a valid name!")]
    Page Should Contain     Please enter a valid name!
    Close Browser


Backwards Compatible - Create Account - Username Exists
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
    Input Text      //*[@placeholder="Please enter your email"]    legacy5@email.com
    Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    Input Text      //*[@placeholder="Enter a unique username"]    legacy1
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    password1
    Click Button   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Sorry, username already exists!")]
    Page Should Contain     Sorry, username already exists!
    Close Browser


Backwards Compatible - Create Account - Email Exists
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
    Input Text      //*[@placeholder="Please enter your email"]    legacy@email.com
    Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    Input Text      //*[@placeholder="Enter a unique username"]    legacy12
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    password1
    Click Button   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Email already exists!")]
    Page Should Contain     Email already exists!
    Close Browser
