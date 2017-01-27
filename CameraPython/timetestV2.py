import datetime
import time

while True:
	start = time.time()
	print(datetime.datetime.now())
	while time.time()-start < 0.001:
		continue

