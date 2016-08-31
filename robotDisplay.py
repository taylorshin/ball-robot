import Tkinter
import threading
import time
import sys
import random

class Robot:

  def __init__(self, canvas, speed, color):
    self.canvas = canvas
    self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
    # Sets x,y position of object
    self.canvas.move(self.id, 300, 300)
    self.speed = speed
    self.x = 0
    self.y = speed
    self.canvas_height = self.canvas.winfo_reqheight()
    self.canvas_width = self.canvas.winfo_reqwidth()

  def draw(self):
    self.canvas.move(self.id, self.x, self.y)
    pos = self.canvas.coords(self.id)
    if pos[1] <= 0:
      self.y = self.speed
    if pos[3] >= self.canvas_height:
    #if pos[3] >= 500:
      self.y = -self.speed
    if pos[0] <= 0:
      self.x = 0
    if pos[2] >= self.canvas_width:
      self.x = 0

class Wall:

  def __init__(self, canvas, color):
    self.canvas = canvas
    # (x0, y0, x1, y1) are parameters for create_rectangle
    # (x0, y0) = top left point; (x1, y1) = bottom right point
    self.id = canvas.create_rectangle(400, 200, 450, 550, fill=color)
    #self.canvas.move(self.id, 200, 300)
    
  def draw(self):
    self.canvas.move(self.id, 0, 0)

class Application:

  def initGUI(self, win):
    # Window
    self.win = win

    # Initialize frame
    win.grid()
    self.dec = -.5
    self.inc = .5
    self.tickTime = 0.1

    # Canvas
    self.canvas = Tkinter.Canvas(root, height=500, width=800)
    self.canvas.grid(row=2, columnspan=10)

  def __init__(self, win):
    self.stepCount = 0

    # Initialize GUI
    self.initGUI(win)

    # Initialize environment
    self.robot = Robot(self.canvas, 3, 'blue')
    self.wall = Wall(self.canvas, 'black')

    # Start GUI
    self.running = True
    self.stopped = False
    self.stepsToSkip = 0
    self.thread = threading.Thread(target=self.run)
    self.thread.start()

  def exit(self):
    self.running = False
    for i in range(5):
      if not self.stopped:
        time.sleep(0.1)
    try:
      self.win.destroy()
    except:
      pass
    sys.exit(0)

  def step(self):
    self.stepCount += 1


  def run(self):
    self.stepCount = 0 

    while True:
      minSleep = .01
      tm = max(minSleep, self.tickTime)
      time.sleep(tm)
      self.stepsToSkip = int(tm / self.tickTime) - 1

      if not self.running:
        self.stopped = True
        return

  def start(self):
    self.win.mainloop()

"""--------------------------------------------------------------"""

def run():
  global root
  root = Tkinter.Tk()
  root.title('Something cool')
  root.resizable(0, 0)

  app = Application(root)
  
  def update_gui():
    app.robot.draw()
    app.wall.draw()
    root.after(10, update_gui)
  update_gui()

  root.protocol('WM_DELETE_WINDOW', app.exit)
  try:
    app.start()
  except:
    app.exit()
