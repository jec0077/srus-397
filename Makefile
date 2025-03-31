test-yolo:
	python ./yolo_alt.py 2 67 50

test-data:
	python ./data.py

test-temphum:
	python ./TempHum.py

test-aqs:
	python ./AQsensor.py

test-relay:
	python ./relay.py

test-display:
	python ./display.py

test-intsys:
	python ./intergrated_system.py

run:
	python ./main.py 2 67 50
