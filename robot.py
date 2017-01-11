"""
The following link helped with the animation of a bouncing ball in python
https://pythongamegraphics.com/2015/04/05/animation-of-bouncing-balls/
"""

import environment

class RobotEnvironment(environment.Environment):
    def __init__(self, robot):
        self.robot = robot
        self.state = None
        self.nVelXStates = 10
        self.nVelYStates = 10
        self.velXBuckets = [i for i in range(1, 11)]
        self.velYBuckets = []
        for i in range(-5, 0):
            self.velYBuckets.append(i)
        for i in range(1, 6):
            self.velYBuckets.append(i)
        # Reset
        self.reset()
        print 'OG VelX: ', self.robot.velX, ', OG VelY: ', self.robot.velY

    def getCurrentState(self):
        return self.state

    def getPossibleActions(self, state):
        actions = list()

        # Maybe actions should differ based on +/- distance from basket
        currVelXBucket, currVelYBucket = state
        if currVelXBucket > 0: actions.append('velX-up')
        if currVelXBucket < self.nVelXStates - 1: actions.append('velX-down')
        if currVelYBucket > 0: actions.append('velY-up')
        if currVelYBucket < self.nVelXStates - 1: actions.append('velY-down')

        return actions

    def doAction(self, action):
        nextState, reward =  None, None

        oldY = self.robot.getDistanceToBasket()

        print 'Action: ', action

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

        newY = self.robot.getDistanceToBasket()

        # a simple reward function
        reward = newY - oldY

        self.state = nextState
        return nextState, reward

    def reset(self):
        # Resets the Environment to the initial state
        velXState = self.nVelXStates / 2
        velYState = self.nVelYStates / 2
        self.state = velXState, velYState
        #self.robot.resetPosition()


class Robot:
    def __init__(self, canvas, x0, y0, x1, y1, color, basket):
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
        self.velY = 5.0
        # Proportion of elastic energy recovered after each bounce
        self.coef_restitution = 0.9
        # This determines the size of differential steps when calculating changes in position
        self.time_scaling = 0.2
        self.canvas_height = self.canvas.winfo_reqheight()
        self.canvas_width = self.canvas.winfo_reqwidth()
        self.gravity = 0.2
        # Set up basket
        self.basket = basket
        # Not sure if this should be initialized to None
        # There would be an edge case at the beginning where it would subtract an int with None
        self.distToBasket = -1000
        self.hitWall = False

    def bounce(self):
        self.velY *= 1.5
        #print "bounce! ", "velocity: ", self.velY
        print "x: ", self.pos[2], ", y: ", self.pos[3]
        print "xbox: ", self.canvas.bbox(self.id)[2], ", ybox: ", self.canvas.bbox(self.id)[3]

    # Returns the distance from the ball to the basket
    def getDistanceToBasket(self):
        return self.distToBasket

    def getHitWall(self):
        return self.hitWall

    def setHitWall(self, hit):
        self.hitWall = hit

    def resetPosition(self):
        #tempVelX = self.velX
        #tempVelY = self.velY
        #self.velX = 0
        #self.velY = 0
        self.canvas.coords(self.id, 110, 110, 150, 150)
        #self.velX = tempVelX
        #self.velY = tempVelY

    def draw(self):
        # Original skeleton code had move at the beginning of this function
        #self.canvas.move(self.id, self.x, self.y)
        self.pos = self.canvas.coords(self.id)

        oldX = self.pos[0]
        oldY = self.pos[1]

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
            self.distToBasket = abs(self.canvas.bbox(self.basket.id)[3] - self.canvas.bbox(self.id)[3])
            self.hitWall = True
        # Hits floor
        if self.pos[3] >= self.canvas_height:
            self.velY = -self.velY * self.coef_restitution
            # If ball goes below floor automatically set its location to 0
            #self.y = 0
            self.canvas.move(self.id, 0, -5)

        # Diff equation
        self.x = self.velX * self.time_scaling
        #self.gravity = self.gravity * self.time_scaling
        self.velY = self.velY + self.gravity
        self.y = self.velY * self.time_scaling

        # Move the ball after calculating the physics
        self.canvas.move(self.id, self.x, self.y)

        # Draw line to show ball path
        self.pos = self.canvas.coords(self.id)
        self.canvas.create_line(oldX, oldY, self.pos[0], self.pos[1], fill='black')

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
