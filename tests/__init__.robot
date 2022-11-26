
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

    Remove File     _secret_auth_.json

    ${PROCESS_FULL}    Start Process   python3    
        ...    -m    coverage    run    --source    tests   
        ...    -m    streamlit    run    __test_app.py    
        ...    --server.port    8001    
        ...    --server.headless   true
        # ...    env:HIDE_FOOTER=true
    Set suite variable    ${PROCESS_FULL}
    Log To Console     ${PROCESS_FULL}

    ${PROCESS_HIDE_FOOTER}    Start Process   python3    
        ...    -m    coverage    run    --source    tests   
        ...    -m    streamlit    run    __test_app.py    
        ...    --server.port    8006    
        ...    --server.headless   true
        ...    env:HIDE_FOOTER=true
    Set suite variable    ${PROCESS_HIDE_FOOTER}
    Log To Console     ${PROCESS_HIDE_FOOTER}

    ${PROCESS_HIDE_MENU}    Start Process   python3    
        ...    -m    coverage    run    --source    tests   
        ...    -m    streamlit    run    __test_app.py    
        ...    --server.port    8007    
        ...    --server.headless   true
        ...    env:HIDE_MENU=true
    Set suite variable    ${PROCESS_HIDE_MENU}
    Log To Console     ${PROCESS_HIDE_MENU}

    ${PROCESS_LOGOUT_NAME}    Start Process   python3    
        ...    -m    coverage    run    --source    tests   
        ...    -m    streamlit    run    __test_app.py    
        ...    --server.port    8008    
        ...    --server.headless   true
        ...    env:LOGOUT_BUTTON_NAME=Exit
    Set suite variable    ${PROCESS_LOGOUT_NAME}
    Log To Console     ${PROCESS_LOGOUT_NAME}

    ${PROCESS_HIDE_REGISTRATION}    Start Process   python3    
        ...    -m    coverage    run    --source    tests   
        ...    -m    streamlit    run    __test_app.py    
        ...    --server.port    8002    
        ...    --server.headless   true
        ...    env:HIDE_REGISTRATION=true
    Set suite variable    ${PROCESS_HIDE_REGISTRATION}
    Log To Console     ${PROCESS_HIDE_REGISTRATION}

    ${PROCESS_HIDE_ACC_MGMT}    Start Process   python3    
        ...    -m    coverage    run    --source    tests   
        ...    -m    streamlit    run    __test_app.py    
        ...    --server.port    8003    
        ...    --server.headless   true
        ...    env:HIDE_ACCOUNT_MANAGEMENT=true
    Set suite variable    ${PROCESS_HIDE_ACC_MGMT}
    Log To Console     ${PROCESS_HIDE_ACC_MGMT}

    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT}    Start Process   python3    
        ...    -m    coverage    run    --source    tests   
        ...    -m    streamlit    run    __test_app.py    
        ...    --server.port    8004    
        ...    --server.headless   true
        ...    env:CUSTOM_AUTH=true
        ...    env:HIDE_ACCOUNT_MANAGEMENT=true
    Set suite variable    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT}
    Log To Console     ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT}

    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT_LOGIN_NAME}    Start Process   python3    
        ...    -m    coverage    run    --source    tests   
        ...    -m    streamlit    run    __test_app.py    
        ...    --server.port    8005    
        ...    --server.headless   true
        ...    env:CUSTOM_AUTH=Custom Login
        ...    env:HIDE_ACCOUNT_MANAGEMENT=true
    Set suite variable    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT_LOGIN_NAME}
    Log To Console     ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT_LOGIN_NAME}

    sleep    2s

Stop the webserver
    Log To Console    end
    Terminate Process    ${PROCESS_FULL}
    Terminate Process    ${PROCESS_HIDE_FOOTER}
    Terminate Process    ${PROCESS_HIDE_MENU}
    Terminate Process    ${PROCESS_LOGOUT_NAME}
    Terminate Process    ${PROCESS_HIDE_REGISTRATION}
    Terminate Process    ${PROCESS_HIDE_ACC_MGMT}
    Terminate Process    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT}
    Terminate Process    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT_LOGIN_NAME}
    Close All Browsers