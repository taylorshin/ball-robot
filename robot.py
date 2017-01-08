"""
The following link helped with the animation of a bouncing ball
https://pythongamegraphics.com/2015/04/05/animation-of-bouncing-balls/
"""

import environment

class RobotEnvironment(environment.Environment):
    def __init__(self, robot):
        self.robot = robot
        self.state = None
        self.nVelXStates = 11
        self.nVelYStates = 11
        self.velXBuckets = [i + 1 for i in range(10)]
        self.velYBuckets = [i + 1 for i in range(10)]
        # Reset
        self.reset()

    def getCurrentState(self):
        return self.state

    def getPossibleActions(self, state):
        actions = list()

        currVelXBucket, currVelYBucket = state
        if currVelXBucket > 0: actions.append('velX-down')
        if currVelXBucket < self.nVelXStates - 1: actions.append('velX-up')
        if currVelYBucket > 0: actions.append('velY-down')
        if currVelYBucket < self.nVelXStates - 1: actions.append('velY-up')

        return actions

    def doAction(self, action):
        nextState, reward =  None, None
        #oldY = get Y value of ball once it hits the right wall
        velXBucket, velYBucket = self.state
        if action == 'velX-up':
            newVelX = self.velXBuckets[velXBucket + 1]
            self.robot.velX = newVelX
            nextState = (velXBucket + 1, velYBucket)
        if action == 'velX-down':
            newVelX = self.velXBuckets[velXBucket - 1]
            self.robot.velX = newVelX
            nextState = (velXBucket - 1, velYBucket)
        if action == 'velY-up':
            newVelY = self.velYBuckets[velYBucket + 1]
            self.robot.velY = newVelY
            nextState = (velXBucket, velYBucket + 1)
        if action == 'velY-down':
            newVelY = self.velYBuckets[velYBucket - 1]
            self.robot.velY = newVelY
            nextState = (velXBucket, velYBucket - 1)

        #newX,newY = self.crawlingRobot.getRobotPosition()

        # a simple reward function
        #reward = newX - oldX

        self.state = nextState
        return nextState, reward

    def reset(self):
        # Resets the Environment to the initial state
        velState = self.nVelStates/2
        self.state = velState


class Robot:
    def __init__(self, canvas, x0, y0, x1, y1, color):
        self.canvas = canvas
        self.id = canvas.create_oval(x0, y0, x1, y1, fill=color)
        # Sets x,y position of object
        self.canvas.move(self.id, 100, 100)
        # Not sure what speed does...............lol
        # Seems like speed of 3 is good but 5 is not
        self.speed = 3
        self.x = self.speed
        self.y = self.speed
        self.velX = 5.0
        self.velY = 0.8
        # Proportion of elastic energy recovered after each bounce
        self.coef_restitution = 0.9
        # This determines the size of differential steps when calculating changes in position
        self.time_scaling = 0.2
        self.canvas_height = self.canvas.winfo_reqheight()
        self.canvas_width = self.canvas.winfo_reqwidth()
        self.gravity = 0.2

    def bounce(self):
        #self.velY *= 1.5
        #print "bounce! ", "velocity: ", self.velY
        print "x: ", self.pos[2], ", y: ", self.pos[3]
        print "xbox: ", self.canvas.bbox(self.id)[2], ", ybox: ", self.canvas.bbox(self.id)[3]

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        self.pos = self.canvas.coords(self.id)
        # Hits left boundary
        if self.pos[0] <= 0:
            self.velX = -self.velX * self.coef_restitution
        # Ball hits ceiling
        if self.pos[1] <= 0:
            self.velY = -self.velY * self.coef_restitution
        # Hits right boundary or hits the wall
        #if pos[2] >= self.canvas_width or pos[2] >= self.canvas.bbox(self.wall.id)[0]:
        if self.pos[2] >= self.canvas_width:
            # bbox returns (x1,y1,x2,y2) = bounding box where top left corner is (x1,y1)
            # and bottom right corner is (x2,y2)
            self.velX = -self.velX * self.coef_restitution
        # Hits floor
        if self.pos[3] >= self.canvas_height:
            self.velY = -self.velY * self.coef_restitution
            # If ball goes below floor automatically set its location to 0
            self.y = 0

        # Diff equation
        self.x = self.velX * self.time_scaling
        #self.gravity = self.gravity * self.time_scaling
        self.velY = self.velY + self.gravity
        self.y = self.velY * self.time_scaling

"""
class Wall:
    def __init__(self, canvas, color):
        self.canvas = canvas
        # (x0, y0, x1, y1) are parameters for create_rectangle
        # (x0, y0) = top left point; (x1, y1) = bottom right point
        self.id = canvas.create_rectangle(400, 150, 425, 550, fill=color)
        #self.canvas.move(self.id, 200, 300)

    def draw(self):
        self.canvas.move(self.id, 0, 0)
"""

class Basket:
    def __init__(self, canvas, x0, y0, x1, y1, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def draw(self):
        self.canvas.move(self.id, 0, 0)

if __name__ == '__main__':
    from robotDisplay import *
    run()
