from time import time
import random
from objects import DataPoint, TimeSeries
from chart import plot
from model import AnomalyDetectionModel

data_points = []
for i in range(150):
    num = random.uniform(-20, 20)
    if i % 30 == 0:
        num = random.uniform(-150, 150)
    data_points.append(DataPoint(timestamp=int(time()) + i, value=num))


ts = TimeSeries(data=data_points)
#plot(ts)
model = AnomalyDetectionModel().fit(ts)

print(f"Model mean: {model.mean}, std:{model.std}")
toPredict = value=random.uniform(-150, 150)
print(f"Predict this {toPredict}")
res = model.predict(DataPoint(timestamp=int(time()), value=toPredict))
print(res)




