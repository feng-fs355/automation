
for i in {1..1}

do
    echo "## THRIV-1322  : Generate / upload material to AWS ##"
    echo "$i : iterations"

	python3 -m pytest -vv test-2001_Loadjson.py --alluredir=./allure-results && python3 -m pytest -vv test-2999_UploadFile.py --alluredir=./allure-results
    sleep 5s
	python3 -m pytest -vv test-2002_Timeshift.py --alluredir=./allure-results && python3 -m pytest -vv test-2999_UploadFile.py --alluredir=./allure-results
	sleep 5s
	python3 -m pytest -vv test-2001_Loadjson.py --alluredir=./allure-results && python3 -m pytest -vv test-2999_UploadFile.py --alluredir=./allure-results
	sleep 5s
	python3 -m pytest -vv test-2005_Filename-updatetime.py --alluredir=./allure-results && python3 -m pytest -vv test-2999_UploadFile.py --alluredir=./allure-results
	sleep 5s
	python3 -m pytest -vv test-2006_Timeshift_date.py --alluredir=./allure-results && python3 -m pytest -vv test-2999_UploadFile.py --alluredir=./allure-results
	sleep 5s
	
done
