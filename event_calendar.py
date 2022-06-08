import math

class EventCalendar:
  """
  Class for handling an event calendar.
  """
  def __init__(self):
    """
    Constructs an event calendar.
    """
    self.calendar = []

  def push(self, time: float, function, data):
    """
    Add event to calendar.

    Args:
      time (float): fire time.
      function (function): callback function.
      data: custome callback data.
    """
    i = [0, len(self.calendar)]
    while i[0] != i[1]:
      im = math.floor((i[0] + i[1]) / 2)
      if time >= self.calendar[im][0]:
        i[0] = im + 1
      else:
        i[1] = im
    self.calendar.insert(i[0], (time, function, data))

  def pop(self):
    """
    Get the nearest time event.

    Returns:
      (tuple): fire time and callback data.
    """
    return self.calendar.pop(0)

  def is_empty(self):
    """
    Check whether calendar is empty.

    Returns:
      (boolean): true if calendar is empty.
    """
    return len(self.calendar) == 0
