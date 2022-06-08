import simulator
import numpy as np

class Model:
  """Discrete event system model."""
  def __init__(self, distance: np.array, unload_time: np.array,
                load_time: np.array, train_count: np.array,
                train_velocity: list, train_load: int) -> None:
    """
    Construct a discrete event system model.

    Args:
      distance (numpy.array): distance from port to terminal.
      unload_time (numpy.array): unloading time.
      load_time (numpy.array): loading time.
      train_count (numpy.array): train count.
      train_velocity (numpy.array): train speed.
      train_load (numpy.array): train load.
    """
    self.distance = distance
    self.unload_time = unload_time
    self.load_time = load_time
    self.train_count = train_count
    self.train_velocity = train_velocity
    self.train_load = train_load
    self.clear()
  
  def clear(self):
    port_count = self.distance.shape[0]
    terminal_count = self.distance.shape[1]
    self.terminal_queue = self.terminal_queue_forecast = [[0] for _ in range(terminal_count)]
    self.port_queue = self.port_queue_forecast = [[0] for _ in range(port_count)]

  def starting_events(self, simulator: simulator.Simulator):
    """
    Add starting events to simulator calendar.

    Args:
      simulator (:obj:Simulator): Simulator.
    """
    id = 0
    for train_model_index in range(len(self.train_count)):
      for _ in range(self.train_count[train_model_index]):
        port_index = 0
        terminal_index = self.dispatch_to_terminal(simulator.time, port_index, train_model_index)
        time = simulator.time + self.distance[port_index, terminal_index] / self.train_velocity[train_model_index]
        data = [port_index, terminal_index, train_model_index, id]
        simulator.add_event(time, self.on_finish_unloaded_path, data)
        id += 1
  
  
  def on_finish_unloaded_path(self, simulator: simulator.Simulator, data):
    """
    Callback function for finishing unloaded path.

    Args:
      simulator (:obj:Simulator): Simulator.
      data (list): port, terminal and train model indexes.
    """
    print(f'{simulator.time // 3600:02.0f}:{simulator.time % 3600:02.0f} Train {data[3]} arrived at terminal {data[1]} to unload')

    terminal_index = data[1]
    train_model_index = data[2]
    terminal_unloading_time = np.maximum(simulator.time, self.terminal_queue[terminal_index][-1]) + self.load_time[terminal_index, train_model_index]
    self.terminal_queue[terminal_index].append(terminal_unloading_time)
    simulator.add_event(terminal_unloading_time, self.on_finish_loading, data)
  

  def on_finish_loading(self, simulator: simulator.Simulator, data: list):
    """
    Callback function for finishing loading.

    Args:
      simulator (:obj:Simulator): Simulator.
      data (list): port, terminal and train model indexes.
    """
    print(f'{simulator.time // 3600:02.0f}:{simulator.time % 3600:02.0f} Train {data[3]} going from terminal {data[1]} to port {data[0]}')
    terminal_index = data[1]
    train_model_index = data[2]
    port_index = self.dispatch_to_port(simulator.time, terminal_index, train_model_index)
    data[0] = port_index
    port_unloading_time = simulator.time + self.distance[port_index, terminal_index] / self.train_velocity[train_model_index]
    simulator.add_event(port_unloading_time, self.on_finish_loaded_path, data)
    

  def on_finish_loaded_path(self, simulator: simulator.Simulator, data: list):
    """
    Callback function for finishing loaded path.

    Args:
      simulator (:obj:Simulator): Simulator.
      data (list): port, terminal and train model indexes.
    """
    print(f'{simulator.time // 3600:02.0f}:{simulator.time % 3600:02.0f} Train {data[3]} arrived at port {data[0]} to load')
  
    port_index = data[0]
    train_model_index = data[2]
    port_loading_time = np.maximum(simulator.time, self.port_queue[port_index][-1]) + self.load_time[port_index, train_model_index]
    self.port_queue[port_index].append(port_loading_time)
    simulator.add_event(port_loading_time, self.on_finish_unloading, data)


  def on_finish_unloading(self, simulator: simulator.Simulator, data):
    """
    Callback function for finishing unloading.

    Args:
      simulator (:obj:Simulator): Simulator.
      data (list): port, terminal and train model indexes.
    """
    print(f'{simulator.time // 3600:02.0f}:{simulator.time % 3600:02.0f} Train {data[3]} going from port {data[0]} to terminal {data[1]}')

    port_index = data[0]
    train_model_index = data[2]
    terminal_index = self.dispatch_to_terminal(simulator.time, port_index, train_model_index)
    data[1] = terminal_index
    terminal_loading_time = simulator.time + self.distance[port_index, terminal_index] / self.train_velocity[train_model_index]
    simulator.add_event(terminal_loading_time, self.on_finish_unloaded_path, data)

  def dispatch_to_terminal(self, current_time, port_index, train_model):
    """Route train to terminal."""
    queue_time = np.array([q[-1] for q in self.terminal_queue_forecast])
    transport_time = self.distance[port_index, :] / self.train_velocity[train_model]
    load_time = self.load_time[:, train_model]
    final_time = np.maximum(queue_time, current_time + transport_time) + load_time
    terminal_index = np.argmin(final_time)
    self.terminal_queue_forecast[terminal_index].append(final_time[terminal_index])
    return terminal_index
  
  def dispatch_to_port(self, current_time, terminal_index, train_model):
    """Route train to port."""
    queue_time = np.array([q[-1] for q in self.port_queue_forecast])
    transport_time = self.distance[:, terminal_index] / self.train_velocity[train_model]
    unload_time = self.unload_time[:, train_model]
    final_time = np.maximum(queue_time, current_time + transport_time) + unload_time
    port_index = np.argmin(final_time)
    self.port_queue_forecast[port_index].append(final_time[port_index])
    return port_index