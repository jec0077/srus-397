run:
	python ./yolo_alt.py 2 67 50

old:
	python ./main.py ./haarcascade_frontalface_default.xml 2 67 50

data:
	python ./data.py

sensors:
	python ./sensors.py

temphum:
	python ./TempHum.py

aqs:
	python ./AQsensor.py

testingcode:
	python ./TestingCode.py