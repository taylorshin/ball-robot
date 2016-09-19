import environment

class RobotEnvironment(environment.Environment):
  def __init__(self, robot):
    self.robot = robot

    self.state = None

  def getCurrentState(self):
    return self.state

  def getPossibleActions(self, state):
    actions = list()

class Robot:
  def __init__(self, canvas, speed, color):
    self.canvas = canvas
    self.id = canvas.create_oval(10, 10, 50, 50, fill=color)
    # Sets x,y position of object
    self.canvas.move(self.id, 300, 300)
    self.speed = speed
    self.x = speed
    self.y = speed
    self.velocity_x = 0.1
    self.velocity_y = 0.5
    self.coef_restitution = 0.9
    self.time_scaling = 0.2
    self.canvas_height = self.canvas.winfo_reqheight()
    self.canvas_width = self.canvas.winfo_reqwidth()
    self.gravity = 0.1

  def draw(self):
    self.canvas.move(self.id, self.x, self.y)
    pos = self.canvas.coords(self.id)
    if pos[1] <= 0:
      # hits floor
      self.velocity_y = -self.velocity_y * self.coef_restitution
      #self.y = self.y * 1.1
      #self.y = abs(self.y)
    if pos[3] >= self.canvas_height:
      # hits ceiling
      self.velocity_y = -self.velocity_y * self.coef_restitution
      #self.y = self.y * 1.1
      #self.y = -self.speed
    if pos[0] <= 0:
      # hits left wall
      self.velocity_x = -self.velocity_x * self.coef_restitution
      #self.x = self.x * 1.1
      #self.x = 0
    if pos[2] >= self.canvas_width:
      # hits right wall
      self.velocity_x = -self.velocity_x * self.coef_restitution
      #self.x = self.x * 1.1
      #self.x = 0

    # Diff equation
    #self.y += self.gravity
    x_old = self.x
    y_old = self.y
    self.x = self.velocity_x * self.time_scaling
    self.velocity_y = self.velocity_y + self.gravity
    self.y = self.velocity_y * self.time_scaling
    #self.canvas.create_line(x_old, y_old, self.x, self.y, fill='black')

class Wall:
  def __init__(self, canvas, color):
    self.canvas = canvas
    # (x0, y0, x1, y1) are parameters for create_rectangle
    # (x0, y0) = top left point; (x1, y1) = bottom right point
    self.id = canvas.create_rectangle(400, 200, 425, 550, fill=color)
    #self.canvas.move(self.id, 200, 300)

  def draw(self):
    self.canvas.move(self.id, 0, 0)

if __name__ == '__main__':
    from robotDisplay import *
    run()
