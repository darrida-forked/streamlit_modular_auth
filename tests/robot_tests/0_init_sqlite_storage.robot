*** Settings ***
Library  SeleniumLibrary
Library  Process
Library  OperatingSystem
Library  DependencyLibrary

Variables    ../_test_variables.py


*** Variables ***
${URL}            http://localhost:${PORT_INIT_SQLITE_STORAGE}/


*** Test Cases ***
Setup - Init SQLITE Database Storage
    Open Browser  ${URL}  browser=${BROWSER}
        ...    service_log_path=${DRIVER_LOGS}
    Close Browser
