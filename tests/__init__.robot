
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
    Remove File    sqlmodel_storage.sqlite

    # REQUIRES postgres docker container running | password="easypass" | ports 5432:5432
    # docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=easypass -d postgres
    ${PROCESS_INIT_POSTGRES_STORAGE}    Start Process   python3    
        ...    -m    streamlit    run    ${CURDIR}/tests_app/multipage_app_admin_pg/Home.py
        ...    --server.port    ${PORT_INIT_POSTGRES_STORAGE}
        ...    init_storage
    Set suite variable    ${PROCESS_INIT_POSTGRES_STORAGE}
    Log To Console     ${PROCESS_INIT_POSTGRES_STORAGE}

    ${PROCESS_DEFAULT_POSTGRES}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/tests_app/multipage_app_admin_pg/Home.py
        ...    --server.port    ${PORT_DEFAULT_POSTGRES}    
        ...    --server.headless   true
    Set suite variable    ${PROCESS_DEFAULT_POSTGRES}
    Log To Console     ${PROCESS_DEFAULT_POSTGRES}

    ${PROCESS_DEFAULT}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/tests_app/_app_1_full.py    
        ...    --server.port    ${PORT_DEFAULT_JSON}    
        ...    --server.headless   true
    Set suite variable    ${PROCESS_DEFAULT}
    Log To Console     ${PROCESS_DEFAULT}

    ${PROCESS_INIT_SQLITE_STORAGE}    Start Process   python3    
        ...    -m    streamlit    run    ${CURDIR}/tests_app/_app_1_full_sqlite.py
        ...    --server.port    ${PORT_INIT_SQLITE_STORAGE}
        ...    init_storage
    Set suite variable    ${PROCESS_INIT_SQLITE_STORAGE}
    Log To Console     ${PROCESS_INIT_SQLITE_STORAGE}

    ${PROCESS_DEFAULT_SQLITE}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/tests_app/_app_1_full_sqlite.py    
        ...    --server.port    ${PORT_DEFAULT_SQLITE}    
        ...    --server.headless   true
    Set suite variable    ${PROCESS_DEFAULT_SQLITE}
    Log To Console     ${PROCESS_DEFAULT_SQLITE}

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

    ${PROCESS_CUSTOM_LOGIN_NAME}    Start Process   python3    
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/tests_app/_app_custom_login_name.py   
        ...    --server.port    ${PORT_CUSTOM_LOGIN_NAME}    
        ...    --server.headless   true
    Set suite variable    ${PROCESS_CUSTOM_LOGIN_NAME}
    Log To Console     ${PROCESS_CUSTOM_LOGIN_NAME}

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

    ${PROCESS_MULTIPAGE_AUTH}    Start Process    python3
        ...    -m    coverage    run    -a    --source    tests   
        ...    -m    streamlit    run    ${CURDIR}/tests_app/multipage_app/Home.py    
        ...    --server.port    ${PORT_MULTIPAGE_AUTH} 
        ...    --server.headless   true
    Set suite variable    ${PROCESS_MULTIPAGE_AUTH}
    Log To Console     ${PROCESS_MULTIPAGE_AUTH}

    sleep    2s

Stop the webserver
    Terminate All Processes
    Close All Browsers
    # Coverage Stop
    # ${RUN_PROCESS}    Run Process    coverage    html
    # ${RUN_PROCESS}    Run Process    coverage    xml
    Log To Console    end
