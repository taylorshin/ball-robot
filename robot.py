"""
The following link helped with the animation of a bouncing ball
https://pythongamegraphics.com/2015/04/05/animation-of-bouncing-balls/
"""

import environment

class RobotEnvironment(environment.Environment):
    def __init__(self, robot):
        self.robot = robot
        self.state = None
        self.nVelocityStates = 11
        self.velocityBuckets = [-5,-4,-3,-2,-1,0,1,2,3,4,5]
        # Reset
        self.reset()

    def getCurrentState(self):
        return self.state

    def getPossibleActions(self, state):
        actions = list()
        currVelocityBucket = state
        if currVelocityBucket > 0:
            actions.append('faster')
        if currVelocityBucket < self.nVelocityStates - 1:
            actions.append('slower')
        return actions

    def reset(self):
        # Resets the Environment to the initial state
        velocityState = self.nVelocityStates/2
        self.state = velocityState


class Robot:
    def __init__(self, canvas, speed, color, wall):
        self.canvas = canvas
        self.id = canvas.create_oval(10, 10, 50, 50, fill=color)
        # Sets x,y position of object
        self.canvas.move(self.id, 100, 100)
        self.speed = speed
        self.x = speed
        self.y = speed
        self.velocity_x = 1.5
        self.velocity_y = 0.8
        # Proportion of elastic energy recovered after each bounce
        self.coef_restitution = 0.9
        # This determines the size of differential steps when calculating changes in position
        self.time_scaling = 0.2
        self.canvas_height = self.canvas.winfo_reqheight()
        self.canvas_width = self.canvas.winfo_reqwidth()
        self.gravity = 0.2
        self.wall = wall

    def bounce(self):
        self.velocity_y *= 1.5
        print "bounce! ", "velocity: ", self.velocity_y

    #def detectWallCollision(self):
        # TODO

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        # Hits left boundary
        if pos[0] <= 0:
            self.velocity_x = -self.velocity_x * self.coef_restitution
        # Ball hits ceiling
        if pos[1] <= 0:
            self.velocity_y = -self.velocity_y * self.coef_restitution
        # Hits right boundary or hits the wall
        if pos[2] >= self.canvas_width or pos[2] >= self.canvas.bbox(self.wall.id)[0]:
            # bbox returns (x1,y1,x2,y2) = bounding box where top left corner is (x1,y1)
            # and bottom right corner is (x2,y2)
            self.velocity_x = -self.velocity_x * self.coef_restitution
        # Hits floor
        if pos[3] >= self.canvas_height:
            self.velocity_y = -self.velocity_y * self.coef_restitution
            # If ball goes below floor automatically set its location to 0
            self.y = 0

        # Diff equation
        self.x = self.velocity_x * self.time_scaling
        #self.gravity = self.gravity * self.time_scaling
        self.velocity_y = self.velocity_y + self.gravity
        self.y = self.velocity_y * self.time_scaling

class Wall:
    def __init__(self, canvas, color):
        self.canvas = canvas
        # (x0, y0, x1, y1) are parameters for create_rectangle
        # (x0, y0) = top left point; (x1, y1) = bottom right point
        self.id = canvas.create_rectangle(400, 150, 425, 550, fill=color)
        #self.canvas.move(self.id, 200, 300)

    def draw(self):
        self.canvas.move(self.id, 0, 0)

if __name__ == '__main__':
    from robotDisplay import *
    run()
