from model import Model
from simulator import Simulator
import numpy as np

distance = np.array([[320.0e3, 800.0e3]])
unloading_time = np.array([[4 * 3600.0]])
loading_time = np.array([[8 * 3600.0], [8 * 3600.0]])
train_count = np.array([2], dtype=int)
train_speed = np.array([40 / 3.6])
train_load = np.array([5.0e6])

model = Model(distance, unloading_time, loading_time, train_count, train_speed, train_load)

simulator = Simulator()
time_horizon = 4 * 24 * 3600
simulator.simulate(model, time_horizon)
