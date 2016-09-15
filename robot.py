class Robot:
  def __init__(self, canvas, speed, color):
    self.canvas = canvas
    self.id = canvas.create_oval(10, 10, 50, 50, fill=color)
    # Sets x,y position of object
    self.canvas.move(self.id, 300, 300)
    self.speed = speed
    self.x = 0
    self.y = speed
    self.canvas_height = self.canvas.winfo_reqheight()
    self.canvas_width = self.canvas.winfo_reqwidth()
    self.gravity = 0.05

  def draw(self):
    self.canvas.move(self.id, self.x, self.y)
    pos = self.canvas.coords(self.id)
    if pos[1] <= 0:
      #self.y = self.speed
      self.y = abs(self.y)
    if pos[3] >= self.canvas_height:
      self.y = -self.speed
    if pos[0] <= 0:
      self.x = 0
    if pos[2] >= self.canvas_width:
      self.x = 0
    self.y += self.gravity

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
