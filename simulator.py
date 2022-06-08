from json import load
import event_calendar


class Simulator:
  """Discrete event system simulator."""
  
  def __init__(self):
    """Construct an event system simulator."""

    self.time = 0
    self.calendar = event_calendar.EventCalendar()
  
  def add_event(self, time, function, data):
    """
    Add event to calendar.

    Args:
      time (float): fire time.
      function (function): callback function.
      data: custome callback data.
    """

    self.calendar.push(time, function, data)

  def simulate(self, model, fire_time: float=24 * 3600):
    """
    Simulate discrete event system.

    Args:
      model (:obj:model): discrete event system model.
      fire_time (float): time horizon.
    """
    model.clear()
    model.starting_events(self)
    while not self.calendar.is_empty() and self.time <= fire_time:
      self.time, function, data = self.calendar.pop()
      function(self, data)