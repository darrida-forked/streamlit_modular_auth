
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
        ...    -m    streamlit    run    ${CURDIR}/tests_app/_app_1_full.py    
        ...    --server.port    ${PORT_DEFAULT}    
        ...    --server.headless   true
    Set suite variable    ${PROCESS_DEFAULT}
    Log To Console     ${PROCESS_DEFAULT}

    ${PROCESS_HIDE_FOOTER}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/tests_app/_app_hide_footer.py    
        ...    --server.port    ${PORT_HIDE_FOOTER}    
        ...    --server.headless   true
    Set suite variable    ${PROCESS_HIDE_FOOTER}
    Log To Console     ${PROCESS_HIDE_FOOTER}

    ${PROCESS_HIDE_MENU}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/tests_app/_app_hide_menu.py    
        ...    --server.port    ${PORT_HIDE_MENU}    
        ...    --server.headless   true
    Set suite variable    ${PROCESS_HIDE_MENU}
    Log To Console     ${PROCESS_HIDE_MENU}

    ${PROCESS_LOGOUT_NAME}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/tests_app/_app_custom_logout_name.py    
        ...    --server.port    ${PORT_LOGOUT_NAME_CHANGE}    
        ...    --server.headless   true
    Set suite variable    ${PROCESS_LOGOUT_NAME}
    Log To Console     ${PROCESS_LOGOUT_NAME}

    ${PROCESS_HIDE_REGISTRATION}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/tests_app/_app_2_hide_registration.py    
        ...    --server.port    ${PORT_HIDE_REGISTRATION}    
        ...    --server.headless   true
    Set suite variable    ${PROCESS_HIDE_REGISTRATION}
    Log To Console     ${PROCESS_HIDE_REGISTRATION}

    ${PROCESS_HIDE_ACC_MGMT}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/tests_app/_app_3_hide_account_mgmt.py    
        ...    --server.port    ${PORT_HIDE_ACCOUNT_MGMT}    
        ...    --server.headless   true
    Set suite variable    ${PROCESS_HIDE_ACC_MGMT}
    Log To Console     ${PROCESS_HIDE_ACC_MGMT}

    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/tests_app/_app_4_custom_auth_hide_account_mgmt.py    
        ...    --server.port    ${PORT_CUSTOM_AUTH_NO_ACCOUNT_MGMT}    
        ...    --server.headless   true
    Set suite variable    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT}
    Log To Console     ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT}

    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT_LOGIN_NAME}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/tests_app/_app_5_custom_auth_hide_acc_mgmt_custom_name.py    
        ...    --server.port    ${PORT_CUSTOM_AUTH_NO_ACCOUNT_MGMT_CUSTOM_NAME}    
        ...    --server.headless   true
    Set suite variable    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT_LOGIN_NAME}
    Log To Console     ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT_LOGIN_NAME}

    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT_LOGIN_NAME}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/tests_app/_app_6_custom_user_storage.py    
        ...    --server.port    ${PORT_CUSTOM_USER_STORAGE}  
        ...    --server.headless   true
    Set suite variable    ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT_LOGIN_NAME}
    Log To Console     ${PROCESS_CUSTOM_AUTH_HIDE_ACC_MGMT_LOGIN_NAME}

    ${PROCESS_CUSTOM_FORGOT_PASSWORD}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/tests_app/_app_7_custom_forgot_password.py    
        ...    --server.port    ${PORT_CUSTOM_FORGOT_PASSWORD}  
        ...    --server.headless   true
    Set suite variable    ${PROCESS_CUSTOM_FORGOT_PASSWORD}
    Log To Console     ${PROCESS_CUSTOM_FORGOT_PASSWORD}

    ${PROCESS_CUSTOM_AUTH_COOKIES}    Start Process    python3
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/tests_app/_app_8_custom_auth_cookies.py    
        ...    --server.port    ${PORT_CUSTOM_AUTH_COOKIES} 
        ...    --server.headless   true
    Set suite variable    ${PROCESS_CUSTOM_AUTH_COOKIES}
    Log To Console     ${PROCESS_CUSTOM_AUTH_COOKIES}

    ${PROCESS_BACKWARDS_COMPATIBILITY}    Start Process    python3
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/tests_app/_app_backwards_comp.py    
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
