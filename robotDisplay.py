import Tkinter
import qlearningAgents
import threading
import time
import sys
import random
import robot

class Application:

    def sigmoid(self, x):
        return 1.0 / (1.0 + 2.0 ** (-x))

    def incrementSpeed(self, inc):
        self.tickTime *= inc
        self.speed_label['text'] = 'Step Delay: %.5f' % (self.tickTime)

    def incrementEpsilon(self, inc):
        self.ep += inc
        self.epsilon = self.sigmoid(self.ep)
        self.learner.setEpsilon(self.epsilon)
        self.epsilon_label['text'] = 'Epsilon: %.3f' % (self.epsilon)

    def incrementGamma(self, inc):
        self.ga += inc
        self.gamma = self.sigmoid(self.ga)
        self.learner.setDiscount(self.gamma)
        self.gamma_label['text'] = 'Discount: %.3f' % (self.gamma)

    def incrementAlpha(self, inc):
        self.al += inc
        self.alpha = self.sigmoid(self.al)
        self.learner.setLearningRate(self.alpha)
        self.alpha_label['text'] = 'Learning Rate: %.3f' % (self.alpha)

    def initGUI(self, win):
        # Window
        self.win = win

        # Initialize frame
        win.grid()
        self.dec = -.5
        self.inc = .5
        self.tickTime = 0.1

        # Buttons and labels
        self.setupSpeedButtonAndLabel(win)
        self.setupEpsilonButtonAndLabel(win)
        self.setUpGammaButtonAndLabel(win)
        self.setupAlphaButtonAndLabel(win)
        #self.setupBounceButton(win)

        # Canvas
        self.canvas = Tkinter.Canvas(root, height=500, width=800)
        self.canvas.grid(row=3, columnspan=10)

    """
    def setupBounceButton(self, win):
        self.bounce = Tkinter.Button(win, text="BOUNCE", command=(lambda: self.robot.bounce()))
        self.bounce.grid(row=2, column=2, padx=10)
    """

    def setupAlphaButtonAndLabel(self, win):
        self.alpha_minus = Tkinter.Button(win,
        text="-",command=(lambda: self.incrementAlpha(self.dec)))
        self.alpha_minus.grid(row=1, column=3, padx=10)

        self.alpha = self.sigmoid(self.al)
        self.alpha_label = Tkinter.Label(win, text='Learning Rate: %.3f' % (self.alpha))
        self.alpha_label.grid(row=1, column=4)

        self.alpha_plus = Tkinter.Button(win,
        text="+",command=(lambda: self.incrementAlpha(self.inc)))
        self.alpha_plus.grid(row=1, column=5, padx=10)

    def setUpGammaButtonAndLabel(self, win):
        self.gamma_minus = Tkinter.Button(win,
        text="-",command=(lambda: self.incrementGamma(self.dec)))
        self.gamma_minus.grid(row=1, column=0, padx=10)

        self.gamma = self.sigmoid(self.ga)
        self.gamma_label = Tkinter.Label(win, text='Discount: %.3f' % (self.gamma))
        self.gamma_label.grid(row=1, column=1)

        self.gamma_plus = Tkinter.Button(win,
        text="+",command=(lambda: self.incrementGamma(self.inc)))
        self.gamma_plus.grid(row=1, column=2, padx=10)

    def setupEpsilonButtonAndLabel(self, win):
        self.epsilon_minus = Tkinter.Button(win,
        text="-",command=(lambda: self.incrementEpsilon(self.dec)))
        self.epsilon_minus.grid(row=0, column=3)

        self.epsilon = self.sigmoid(self.ep)
        self.epsilon_label = Tkinter.Label(win, text='Epsilon: %.3f' % (self.epsilon))
        self.epsilon_label.grid(row=0, column=4)

        self.epsilon_plus = Tkinter.Button(win,
        text="+",command=(lambda: self.incrementEpsilon(self.inc)))
        self.epsilon_plus.grid(row=0, column=5)

    def setupSpeedButtonAndLabel(self, win):
        self.speed_minus = Tkinter.Button(win,
        text="-",command=(lambda: self.incrementSpeed(.5)))
        self.speed_minus.grid(row=0, column=0)

        self.speed_label = Tkinter.Label(win, text='Step Delay: %.5f' % (self.tickTime))
        self.speed_label.grid(row=0, column=1)

        self.speed_plus = Tkinter.Button(win,
        text="+",command=(lambda: self.incrementSpeed(2)))
        self.speed_plus.grid(row=0, column=2)

    def skip5kSteps(self):
        self.stepsToSkip = 5000

    def __init__(self, win):
        self.ep = 0
        self.ga = 2
        self.al = 2
        self.stepCount = 0

        # Initialize GUI
        self.initGUI(win)

        # Initialize environment
        #self.wall = robot.Wall(self.canvas, 'black')
        self.basket = robot.Basket(self.canvas, self.canvas.winfo_reqwidth() - 5 - 50, 100, self.canvas.winfo_reqwidth() - 5, 150, 'red')
        self.robot = robot.Robot(self.canvas, 10, 10, 50, 50, 'blue', self.basket)
        self.robotEnvironment = robot.RobotEnvironment(self.robot)

        # Init Agent
        simulationFn = lambda agent: \
          simulation.SimulationEnvironment(self.robotEnvironment,agent)
        actionFn = lambda state: \
          self.robotEnvironment.getPossibleActions(state)
        self.learner = qlearningAgents.QLearningAgent(actionFn=actionFn)

        self.learner.setEpsilon(self.epsilon)
        self.learner.setLearningRate(self.alpha)
        self.learner.setDiscount(self.gamma)

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
        #self.stepCount += 1
        self.stepCount += 1
        state = self.robotEnvironment.getCurrentState()
        actions = self.robotEnvironment.getPossibleActions(state)
        if len(actions) == 0.0:
            self.robotEnvironment.reset()
            state = self.robotEnvironment.getCurrentState()
            actions = self.robotEnvironment.getPossibleActions(state)
            print 'Reset!'
        action = self.learner.getAction(state)
        if action == None:
            raise 'None action returned: Code Not Complete'
        nextState, reward = self.robotEnvironment.doAction(action)
        self.learner.observeTransition(state, action, nextState, reward)

    def run(self):
        self.stepCount = 0
        self.learner.startEpisode()
        while True:
            minSleep = .01
            tm = max(minSleep, self.tickTime)
            time.sleep(tm)
            self.stepsToSkip = int(tm / self.tickTime) - 1

            if not self.running:
                self.stopped = True
                return
            for i in range(self.stepsToSkip):
                self.step()
            self.stepsToSkip = 0
            if self.robot.getHitWall():
                self.step()
                print 'new VelX: ', self.robot.velX, ', new VelY: ', self.robot.velY
                self.robot.resetPosition()
                #self.robot = robot.Robot(self.canvas, 10, 10, 50, 50, 'blue', self.basket)
                self.robot.setHitWall(False)
        self.learner.stopEpisode()

    def start(self):
        self.win.mainloop()

""" MAIN LOOP STUFF """

def run():
    global root
    root = Tkinter.Tk()
    root.title('Something cool')
    root.resizable(0, 0)

    app = Application(root)

    def update_gui():
        app.robot.draw()
        #app.wall.draw()
        app.basket.draw()
        # this calls update_gui every 10 milliseconds without blocking Tkinter's main loop
        root.after(10, update_gui)
    update_gui()

    root.protocol('WM_DELETE_WINDOW', app.exit)
    try:
        app.start()
    except:
        app.exit()
