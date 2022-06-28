from itertools import cycle
from model import Model
from simulator import Simulator
import numpy as np
import matplotlib.pyplot as plt

distance = np.array([[320.0e3]])
unloading_time = np.array([[4 * 3600.0]])
loading_time = np.array([[8 * 3600.0]])
train_speed = np.array([40 / 3.6])
train_load = np.array([5.0e6])
maximum_number_of_trains = 8

cycle_time = unloading_time[0][0] + loading_time[0][0] + 2 * distance[0][0] / train_speed[0]
ntm = cycle_time / loading_time[0][0]

time_horizon = 50 * 24 * 3600

numerical_productivity = [0]
analytical_productivity = [0]
queue_time = [0]
number_of_trains = [0]
for i in range(1, maximum_number_of_trains):
  train_count = np.array([i], dtype=int)

  model = Model(distance, unloading_time, loading_time, train_count, train_speed, train_load)
  
  simulator = Simulator()
  simulator.simulate(model, time_horizon)
  productivity, production, time = model.productivity()
  queue_time.append(model.queue_time())

  number_of_trains.append(i)
  numerical_productivity.append(productivity[-1])
  analytical_productivity.append(min(train_count[0], ntm) * train_load[0] / cycle_time)
  print(f" Numerical productivity - {numerical_productivity[-1] * 3.6:.0f}")
  print(f"Analytical productivity - {analytical_productivity[-1] * 3.6:.0f}")

hf, ha = plt.subplots()
plt.plot(number_of_trains, np.array(numerical_productivity) * 3.6, label="numerical")
plt.plot(number_of_trains, np.array(analytical_productivity) * 3.6, label="analytical")
plt.xlabel("number of trains")
plt.ylabel("productivity (ton / hours)")
plt.title(f"{i} trains")
plt.legend()

hf, ha = plt.subplots()
plt.plot(number_of_trains, np.array(queue_time) / 3600, label="numerical")
plt.plot(number_of_trains, np.array(queue_time) / 3600, label="analytical")
plt.xlabel("number of trains")
plt.ylabel("queue time (hours)")
plt.title(f"{i} trains")

plt.show()
