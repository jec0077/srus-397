run:
	python ./main.py ./haarcascade_frontalface_default.xml 2

data:
	python ./data.py

sensors:
	python ./sensors.py

temphum:
	python ./TempHum.py

aqs:
	python ./AQsensor.py