###!/usr/bin/env bash
#!/usr/bin/env expect
echo "ALL STOP First"
./STOP_Service.sh
sleep 2s
theIPaddress=$(ip addr show eth0 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1)
echo "########################################################"
echo "## Jenkins build for Thrive FW /Automation validation ##"
echo "########################################################"
echo ""
echo ""
echo "## Automation test run --- (1) Run BLE : Beacon_Scan / BLE BATT (2) Cloud API : Modify JSON / Upload to AWS ##"
python3 -m pytest -vv  test-1001_Beacon_Scan.py --alluredir=./allure-results && python3 -m pytest -vv test-1002_BLE_BATT.py --alluredir=./allure-results && python3 -m pytest -vv test-2001_Loadjson.py --alluredir=./allure-results && python3 -m pytest -vv test-2999_UploadFile.py --alluredir=./allure-results
sleep 30s
echo "## Automation test run --- (3) Postman Cloud API : FALLEvent test case ##"
python3 test-2888_Call_Postman.py
sleep 5s
echo "## Automation test run --- (4) Postman Cloud API : DailyReadinessInsightList test case ##"
python3 test-2881_Call_DailyReadinessInsightList.py
sleep 5s
echo "## Automation test run --- (5) Postman Cloud API : GetReadinessInsightSummary test case ##"
python3 test-2886_Call_GetReadinessInsightSummary.py
sleep 5s
echo "## Automation test run --- (5) Postman Cloud API : PWB_Activity-10baseday test case ##"
python3 test-2870_Call_PWB_Activity-10baseday.py
sleep 5s
echo "## Automation test run --- (6) Postman Cloud API : CheckRingRegistrationStatus ##"
python3 test-2927_Call_CheckRingRegistrationStatus.py
sleep 5s
echo "## Automation test run --- (7) Postman Cloud API : GetDeviceConfigurationProperties ##"
python3 test-2929_Call_GetDeviceConfigurationProperties.py
sleep 5s
echo "## Automation test run --- (8) Postman Cloud API : GetDeviceConfigurationProperties ##"
python3 test-2929_Call_GetDeviceConfigurationProperties.py
sleep 5s
echo "## Automation test run --- (9) Postman Cloud API : Diff_GetSleepSessionList_GetDailySleepInsightList ##"
python3 test-2931_Call_Diff_GetSleepSessionList_GetDailySleepInsightList.py
sleep 5s
echo "## Automation test run --- (10) Postman Cloud API : GetDailySleepInsightList ##"
python3 test-3020_Call_GetDailySleepInsightList.py
sleep 5s

echo ""
echo ""
echo "#-------------------------------------------------------"
echo "## Automation test run completed ##"
sleep 2s
echo ""
echo "#-------------------------------------------------------"
echo "## Prepare to generate Allure test report (Dashboard) ##"
allure generate --clean ./allure-results ./allure-results && allure serve -h $theIPaddress -p 5000 ./allure-results &
#yes | allure generate --clean ./allure-results ./allure-results && allure serve -h $theIPaddress -p 5000 ./allure-results &
##expect "Server started at" { send "\r" }
##interact 
#sleep 90s
#yes | ./STOP_Service.sh
#echo -ne '\n' | ls










