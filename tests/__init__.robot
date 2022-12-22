
*** Settings ***
Library  SeleniumLibrary
Library  Process
Library  OperatingSystem
Library  DependencyLibrary

Variables    _test_variables.py

Suite Setup         Start the webserver
Suite Teardown      Stop the webserver


*** Keywords ***
Start the webserver
    Log To Console  start

    Remove File     _secret_auth_.json

    ${PROCESS_DEFAULT}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/_test_app.py    
        ...    --server.port    ${PORT_DEFAULT}    
        ...    --server.headless   true
        ...    env:ALT_AUTH_COOKIE_PREFIX=auth_cookie_2
    Set suite variable    ${PROCESS_DEFAULT}
    Log To Console     ${PROCESS_DEFAULT}

    ${PROCESS_HIDE_FOOTER}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/_test_app.py    
        ...    --server.port    ${PORT_HIDE_FOOTER}    
        ...    --server.headless   true
        ...    env:HIDE_FOOTER=true
    Set suite variable    ${PROCESS_HIDE_FOOTER}
    Log To Console     ${PROCESS_HIDE_FOOTER}

    ${PROCESS_HIDE_MENU}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/_test_app.py    
        ...    --server.port    ${PORT_HIDE_MENU}    
        ...    --server.headless   true
        ...    env:HIDE_MENU=true
    Set suite variable    ${PROCESS_HIDE_MENU}
    Log To Console     ${PROCESS_HIDE_MENU}

    ${PROCESS_LOGOUT_NAME}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/_test_app.py    
        ...    --server.port    ${PORT_LOGOUT_NAME_CHANGE}    
        ...    --server.headless   true
        ...    env:LOGOUT_BUTTON_NAME=Exit
    Set suite variable    ${PROCESS_LOGOUT_NAME}
    Log To Console     ${PROCESS_LOGOUT_NAME}

    ${PROCESS_HIDE_REGISTRATION}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/_test_app.py    
        ...    --server.port    ${PORT_HIDE_REGISTRATION}    
        ...    --server.headless   true
        ...    env:HIDE_REGISTRATION=true
    Set suite variable    ${PROCESS_HIDE_REGISTRATION}
    Log To Console     ${PROCESS_HIDE_REGISTRATION}

    ${PROCESS_HIDE_ACC_MGMT}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/_test_app.py    
        ...    --server.port    ${PORT_HIDE_ACCOUNT_MGMT}    
        ...    --server.headless   true
        ...    env:HIDE_ACCOUNT_MANAGEMENT=true
    Set suite variable    ${PROCESS_HIDE_ACC_MGMT}
    Log To Console     ${PROCESS_HIDE_ACC_MGMT}

    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/_test_app.py    
        ...    --server.port    ${PORT_CUSTOM_AUTH_NO_ACCOUNT_MGMT}    
        ...    --server.headless   true
        ...    env:CUSTOM_AUTH=true
        ...    env:HIDE_ACCOUNT_MANAGEMENT=true
    Set suite variable    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT}
    Log To Console     ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT}

    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT_LOGIN_NAME}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/_test_app.py    
        ...    --server.port    ${PORT_CUSTOM_AUTH_NO_ACCOUNT_MGMT_CUSTOM_NAME}    
        ...    --server.headless   true
        ...    env:CUSTOM_AUTH=Custom Login
        ...    env:HIDE_ACCOUNT_MANAGEMENT=true
    Set suite variable    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT_LOGIN_NAME}
    Log To Console     ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT_LOGIN_NAME}

    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT_LOGIN_NAME}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/_test_app.py    
        ...    --server.port    ${PORT_CUSTOM_USER_STORAGE}  
        ...    --server.headless   true
        ...    env:CUSTOM_USER_STORAGE=true
    Set suite variable    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT_LOGIN_NAME}
    Log To Console     ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT_LOGIN_NAME}

    ${PROCESS_CUSTOM_FORGOT_PASSWORD}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/_test_app.py    
        ...    --server.port    ${PORT_CUSTOM_FORGOT_PASSWORD}  
        ...    --server.headless   true
        ...    env:CUSTOM_FORGOT_PASSWORD=true
    Set suite variable    ${PROCESS_CUSTOM_FORGOT_PASSWORD}
    Log To Console     ${PROCESS_CUSTOM_FORGOT_PASSWORD}

    ${PROCESS_CUSTOM_AUTH_COOKIES}    Start Process    python3
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/_test_app.py    
        ...    --server.port    ${PORT_CUSTOM_AUTH_COOKIES} 
        ...    --server.headless   true
        ...    env:CUSTOM_AUTH_COOKIES=true
    Set suite variable    ${PROCESS_CUSTOM_AUTH_COOKIES}
    Log To Console     ${PROCESS_CUSTOM_AUTH_COOKIES}

    ${PROCESS_BACKWARDS_COMPATIBILITY}    Start Process    python3
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/_test_backwards_comp.py    
        ...    --server.port    ${PORT_BACKWARDS_COMPATIBILITY} 
        ...    --server.headless   true
    Set suite variable    ${PROCESS_BACKWARDS_COMPATIBILITY}
    Log To Console     ${PROCESS_BACKWARDS_COMPATIBILITY}

    sleep    2s

Stop the webserver
    Terminate All Processes
    Close All Browsers
    # Coverage Stop
    # ${RUN_PROCESS}    Run Process    coverage    html
    # ${RUN_PROCESS}    Run Process    coverage    xml
    Log To Console    end
