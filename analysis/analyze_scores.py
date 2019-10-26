import sys
import json
import numpy as np

data = None
with open(sys.argv[1], 'r') as score_data:
    parsed = json.load(score_data)
    data = list(map(lambda d: float(d), parsed))

if score_data is None:
    sys.exit(1)

print('Data points loaded: ' + str(data))

gradients = np.gradient(data)
print('Gradients:          ' + str(gradients))

average = np.average(data)
print('Average:            ' + str(average))
