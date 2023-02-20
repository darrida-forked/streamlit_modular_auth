*** Settings ***
Library  SeleniumLibrary
Library  Process
Library  OperatingSystem
Library  DependencyLibrary

Variables    ../_test_variables.py


*** Variables ***
${URL}             http://localhost:${PORT_MULTIPAGE_AUTH}/


*** Test Cases ***
Multipage - Create Account
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
    Input Text      //*[@placeholder="Please enter your email"]    user93@email.com
    Wait Until Element Is Visible   //*[@placeholder="Enter a unique username"]
    Input Text      //*[@placeholder="Enter a unique username"]    user93
    Wait Until Element Is Visible   //*[@placeholder="Create a strong password"]
    Input Text      //*[@placeholder="Create a strong password"]    password11
    Click Element   //*[contains(text(),'Register')]
    Wait Until Element Is Visible   //*[contains(text(),"Registration Successful!")]
    Page Should Contain     Registration Successful!
    Close Browser


Multipage - Login, then Logout
    # Depends on test     Multipage - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user93
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password11
    Click Element   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!
    Wait Until Element Is Visible   //*[contains(text(),'Logout')]
    Click Element    //*[contains(text(),'Logout')]
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain     Login
    Close Browser


Multipage - Login, Refresh, Logout, Refresh
    # Depends on test     Multipage - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user93
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password11
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


Multipage - Login, Close Browser, Open
    # Depends on test     Multipage - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user93
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password11
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


Multipage - Session Expire (15s)
    # Depends on test     Multipage - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user93
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password11
    Click Element   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!
    Wait Until Element Is Visible   //*[contains(text(),'Logout')]
    Page Should Contain    Logout
    sleep    16s
    Reload Page
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain    Login
    Reload Page
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain    Login
    Close Browser


Multipage - Login, Change Page, Refresh, Logout
    # Depends on test     Multipage - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user93
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password11
    Click Element   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!

    Page Should Contain    Pictures
    Click Element    //*[contains(text(), 'Pictures')]

    Wait Until Element Is Visible    //*[contains(text(), '[pictures here]')]
    Page Should Contain    [pictures here]
    Reload Page
    Wait Until Element Is Visible    //*[contains(text(), '[pictures here]')]
    Page Should Contain    [pictures here]

    Wait Until Element Is Visible   //*[contains(text(),'Home')]
    Click Element    //*[contains(text(),'Home')]
    Wait Until Element Is Visible   //*[contains(text(),'Logout')]
    Click Element    //*[contains(text(),'Logout')]
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain    Login
    Reload Page
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain    Login
    Close Browser


Multipage - Confirm Page State Cleared on Change Page
    # Depends on test     Multipage - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user93
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password11
    Click Element   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!

    # Check State Is Pages "home"
    Wait Until Element Is Visible    //*[contains(text(), 'Home page state set')]
    Page Should Contain    Home page state set
    
    # Change Pictures, Check State
    Page Should Contain    Pictures
    Click Element    //*[contains(text(), 'Pictures')]
    Wait Until Element Is Visible    //*[contains(text(), 'Picture page state set')]
    Page Should Contain    Picture page state set
    
    # Change Pictures, Check State
    Page Should Contain    Home
    Click Element    //*[contains(text(), 'Home')]
    Wait Until Element Is Visible    //*[contains(text(), 'Home page state set')]
    Page Should Contain    Home page state set

    # Logout
    Wait Until Element Is Visible   //*[contains(text(),'Logout')]
    Click Element    //*[contains(text(),'Logout')]
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain    Login
    Reload Page
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain    Login
    Close Browser


Multipage - Test Auth Failed and Succeed
    # Depends on test     Multipage - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    
    # LOGIN
    Wait Until Page Contains    Username    timeout=${TIMEOUT}
    Wait Until Element Is Visible   //*[@placeholder="Your unique username"]
    Input Text      //*[@placeholder="Your unique username"]    user93
    Wait Until Element Is Visible   //*[@placeholder="Your password"]
    Input Text      //*[@placeholder="Your password"]    password11
    Click Element   //*[contains(text(),'Login')]
    Wait Until Element Is Visible   //*[contains(text(),"Your Streamlit Application Begins here!")]
    Page Should Contain     Your Streamlit Application Begins here!

    # OPEN "POEMS" PAGE WITHOUT GROUP AUTHORIZATION
    # - Should result in "Insufficient permissions" message
    Page Should Contain    Poems
    Click Element    //*[contains(text(), 'Poems')]
    Wait Until Element Is Visible    //*[contains(text(), 'Insufficient permissions')]
    Page Should Contain    Insufficient permissions
    Reload Page
    Wait Until Element Is Visible    //*[contains(text(), 'Insufficient permissions')]
    Page Should Contain    Insufficient permissions

    # NAVIGATE BACK HOME AND CLICK TEST BUTTON TO ADD "poems" GROUP
    Wait Until Element Is Visible   //*[contains(text(),'Home')]
    Click Element    //*[contains(text(), 'Home')]
    Wait Until Element Is Visible   //*[contains(text(),'Add Poems')]
    Click Element    //*[contains(text(),'Add Poems')]
    Wait Until Element Is Visible   //*[contains(text(),'Permissions for poems group added')]
    
    # OPEN "POEMS" PAGE AGAIN **WITH** GROUP AUTH
    # - Should show page content ("[poems here]")
    Page Should Contain    Poems
    Click Element    //*[contains(text(), 'Poems')]
    Wait Until Element Is Visible    //*[contains(text(), '[poems here]')]
    Page Should Contain    [poems here]
    Reload Page
    Wait Until Element Is Visible    //*[contains(text(), '[poems here]')]
    Page Should Contain    [poems here]
    
    # LOGOUT
    Wait Until Element Is Visible   //*[contains(text(),'Home')]
    Click Element    //*[contains(text(), 'Home')]
    Wait Until Element Is Visible   //*[contains(text(),'Logout')]
    Click Element    //*[contains(text(),'Logout')]
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain    Login
    Reload Page
    Wait Until Element Is Visible   //*[contains(text(),'Login')]
    Page Should Contain    Login
    Close Browser


Multipage - Redirect When Not Logged In
    # Depends on test     Multipage - Create Account
    Open Browser    ${URL}  browser=${BROWSER}  service_log_path=${DRIVER_LOGS}
    
    # LAUNCH
    Wait Until Page Contains    Username    timeout=${TIMEOUT}

    # OPEN "POEMS" PAGE WITHOUT GROUP AUTHORIZATION
    # - Should result in "Insufficient permissions" message
    Page Should Contain    Poems
    Click Element    //*[contains(text(), 'Poems')]
    Wait Until Element Is Visible    //*[contains(text(), 'Not logged in...')]
    Wait Until Element Is Visible    //*[contains(text(), 'Redirecting...')]
    Wait Until Element Is Visible    //*[contains(text(), 'Login')]
    Page Should Contain    Login

    # REFRESH TO ENSURE
    Reload Page
    Wait Until Element Is Visible    //*[contains(text(), 'Login')]
    Page Should Contain    Login

    Close Browser
