import numpy as np
from numpy import random 

people_cnt = 25
max_iter = 300000
success_cnt = 0

for i in range(max_iter):
	days = []
	for j in range(people_cnt):
		days.append(np.random.randint(365))
	if len(set(days)) < people_cnt:
		success_cnt+=1

print(round(1 - success_cnt / max_iter, 4))