*** Settings ***
Documentation    Testing Automation Rest APIs
Library  Collections
Library  requests


*** Test Cases ***

Get Interface With No Interface Config
  ${result} =         get    http://localhost:5000/automation/ethernet-1
  Should Be Equal     ${result.status_code}    ${200}
  ${json} =           Set Variable    ${result.json()}
  ${info} =           Get From Dictionary   ${json}   info
  Should Be Equal     ${info}   interface not configured


Post Interface with Shutdown Yes

  &{body}=            Create Dictionary  device-name=test  ip-address=1.2.3.4  interface-name=ethernet-1  shutdown=yes
  ${result} =         post    http://localhost:5000/automation    json=${body}
  Should Be Equal     ${result.status_code}    ${201}


Get Interface With Admin And Oper Status as Down
  ${result} =         get    http://localhost:5000/automation/ethernet-1
  Should Be Equal     ${result.status_code}    ${200}
  ${json} =           Set Variable    ${result.json()}
  ${admin_state} =    Get From Dictionary   ${json}   admin-state
  ${oper_status} =    Get From Dictionary   ${json}   oper-status
  Should Be Equal     ${admin_state}   down
  Should Be Equal     ${oper_status}   down


Post Interface with Shutdown No

  &{body}=            Create Dictionary  device-name=test  ip-address=1.2.3.4  interface-name=ethernet-1  shutdown=no
  ${result} =         post    http://localhost:5000/automation    json=${body}
  Should Be Equal     ${result.status_code}    ${201}


Get Interface With Admin And Oper Status as Up
  ${result} =         get    http://localhost:5000/automation/ethernet-1
  Should Be Equal     ${result.status_code}    ${200}
  ${json} =           Set Variable    ${result.json()}
  ${admin_state} =    Get From Dictionary   ${json}   admin-state
  ${oper_status} =    Get From Dictionary   ${json}   oper-status
  Should Be Equal     ${admin_state}   up
  Should Be Equal     ${oper_status}   up
