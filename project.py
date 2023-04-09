from OpenGL.GL import *
from OpenGL.GLUT import *
import math
import random
import numpy as np

WIDTH, HEIGHT = 600,600
window_width, window_height = 600, 600
window_pos_x, window_pos_y = 100, 100
def findZone(x0,y0,x1,y1):
  dx = x1-x0
  dy = y1-y0
  zone = 0
  if dx >= 0 and dy >= 0:
    if abs(dx) >= abs(dy):
      zone = 0
    else:
      zone = 1
  elif dx <= 0 and dy >= 0:
    if abs(dx) >= abs(dy):
      zone = 3
    else:
      zone = 2
  elif dx <= 0 and dy <= 0:
    if abs(dx) >= abs(dy):
      zone = 4
    else:
      zone = 5
  else:
    if abs(dx) >= abs(dy):
      zone = 7
    else:
      zone = 6
  return zone

def convertToZone0(x0,y0,x1,y1,zone):

  if zone == 0:
    return ([x0,y0,x1,y1])
  elif zone == 1:
    nx0 = y0
    ny0 = x0
    nx1 = y1
    ny1 = x1
    return([nx0,ny0,nx1,ny1])
  elif zone == 2:
    nx0 = y0
    ny0 = -x0
    nx1 = y1
    ny1 = -x1
    return([nx0,ny0,nx1,ny1])
  elif zone == 2:
    nx0 = y0
    ny0 = -x0
    nx1 = y1
    ny1 = -x1
    return([nx0,ny0,nx1,ny1])
  elif zone == 3:
    nx0 = -x0
    ny0 = y0
    nx1 = -x1
    ny1 = y1
    return([nx0,ny0,nx1,ny1])
  elif zone == 4:
    nx0 = -x0
    ny0 = -y0
    nx1 = -x1
    ny1 = -y1
    return([nx0,ny0,nx1,ny1])
  elif zone == 5:
    nx0 = -y0
    ny0 = -x0
    nx1 = -y1
    ny1 = -x1
    return([nx0,ny0,nx1,ny1])
  elif zone == 6:
    nx0 = -y0
    ny0 = x0
    nx1 = -y1
    ny1 = x1
    return([nx0,ny0,nx1,ny1])
  elif zone == 7:
    nx0 = x0
    ny0 = -y0
    nx1 = x1
    ny1 = -y1
    return([nx0,ny0,nx1,ny1])


def convertToOriginalZone(x, y, zone):
    if zone == 0:
        return [x, y]
    elif zone == 1:
        return [y, x]
    elif zone == 2:
        return [-y, x]
    elif zone == 3:
        return [-x, y]
    elif zone == 4:
        return [-x, -y]
    elif zone == 5:
        return [-y, -x]
    elif zone == 6:
        return [y, -x]
    elif zone == 7:
        return [x, -y]

def mlda(x0,y0,x1,y1): #Mid point line drawing algorithm function
  dx = x1 - x0
  dy = y1 - y0
  d = (2*dy)-dx
  incE = 2*dy
  incNE = 2*(dy-dx)

  points = []
  givenX0 = x0
  givenY0 = y0
  points.append([givenX0, givenY0])

  while givenX0<x1:
    if d > 0:
      givenX0 += 1
      givenY0 += 1
      d += incNE
    else:
      givenX0 += 1
      d += incE
    points.append([givenX0, givenY0])

  return points

def eightWaySymmetry(x0,y0,x1,y1):
  zone = findZone(x0,y0,x1,y1)
  convertedPoints = convertToZone0(x0,y0,x1,y1,zone)
  newZone = findZone(convertedPoints[0],convertedPoints[1],convertedPoints[2],convertedPoints[3])
  z0linePoints = mlda(convertedPoints[0],convertedPoints[1],convertedPoints[2],convertedPoints[3])


  originalZonePoints = []
  for i in z0linePoints:
    originalZonePoints.append(convertToOriginalZone(i[0],i[1],zone))

  for i in range(len(originalZonePoints)):
    originalZonePoints[i] = [(originalZonePoints[i][0]), (originalZonePoints[i][1])]

  return originalZonePoints

def midCircle(radius):
  d = 1-radius
  x = 0
  y = radius
  points = []
  points.append([x,y])
  while x<y:
    if d<0:
      d = d+(2*x)+3
      x += 1
    else:
      d = d+(2*x)-(2*y)+5
      x = x+1
      y = y-1
    points.append([x,y])
  return points

#making points for every Zone
def pointsAllZones(points, centerX, centerY, scalingFactor):
  scalingFactor = 1
  zone1Points = []
  zone2Points = []
  zone3Points = []
  zone4Points = []
  zone5Points = []
  zone6Points = []
  zone7Points = []
  zone0Points = []

  for each in points:
    zone1Points.append([((each[0]+centerX)/scalingFactor), ((each[1]+centerY)/scalingFactor)])
    zone6Points.append([((each[0]+centerX)/scalingFactor), ((-each[1]+centerY)/scalingFactor)])
    zone5Points.append([((-each[0]+centerX)/scalingFactor), ((-each[1]+centerY)/scalingFactor)])
    zone2Points.append([((-each[0]+centerX)/scalingFactor), ((each[1]+centerY)/scalingFactor)])
    zone0Points.append([((each[1]+centerX)/scalingFactor), ((each[0]+centerY)/scalingFactor)])
    zone3Points.append([((-each[1]+centerX)/scalingFactor), ((each[0]+centerY)/scalingFactor)])
    zone4Points.append([((-each[1]+centerX)/scalingFactor), ((-each[0]+centerY)/scalingFactor)])
    zone7Points.append([((each[1]+centerX)/scalingFactor), ((-each[0]+centerY)/scalingFactor)])
  return [zone1Points, zone2Points, zone3Points, zone4Points, zone5Points, zone6Points, zone7Points,zone0Points]

#for creating circle

def outerCircle(radius, centerPoints): #create circle calculating zone
  points = midCircle(radius)
  allZones = pointsAllZones(points,centerPoints[0],centerPoints[1], radius+10)
  allZonePoints = []
  for i in range(len(allZones[0])):
    allZonePoints.append([allZones[0][i][0],allZones[0] [i][1]])
    allZonePoints.append([allZones[1][i][0],allZones[1][i][1]])
    allZonePoints.append([allZones[2][i][0],allZones[2][i][1]])
    allZonePoints.append([allZones[3][i][0],allZones[3][i][1]])
    allZonePoints.append([allZones[4][i][0],allZones[4][i][1]])
    allZonePoints.append([allZones[5][i][0],allZones[5][i][1]])
    allZonePoints.append([allZones[6][i][0],allZones[6][i][1]])
    allZonePoints.append([allZones[7][i][0],allZones[7][i][1]])
  return allZonePoints

#making the circle function as a goal post

#Goal_bar
def goalBarP():
  left_bar = eightWaySymmetry(230, 450, 230, 350)
  top_bar = eightWaySymmetry(230, 450, 250, 450)
  right_bar = eightWaySymmetry(250, 450, 250, 350)
  bottom_bar = eightWaySymmetry(230, 350, 250, 350)

  centerPointsg = [240, 420 * 2]
  radiusg = 20
  allZonePoints = outerCircle(radiusg,centerPointsg)
  scale = np.array([[1, 0, 0],
             [0, 0.5, 0],
             [0, 0, 1]])
  transformedAllPoints = []
  for i in allZonePoints:
    v1 = np.array([[i[0]], [i[1]],[1]])
    transformedAllPoints.append(np.matmul(scale,v1))
  return [(left_bar+top_bar+right_bar+bottom_bar),transformedAllPoints]

def stickMan():
  leftLeg = eightWaySymmetry(0,0,10,10)
  rightLeg = eightWaySymmetry(10,10,20,0)
  middleBody = eightWaySymmetry(10,10,10,30)
  handsBody = eightWaySymmetry(0,25,20,25)
  wholeBody = leftLeg+rightLeg+middleBody+handsBody
  return wholeBody


# making everything on sceen functional

import math


def sceneTransform(scale, rot, mvX, mvY, throwPoint):
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(.5, .3, .7)
    glPointSize(3)

    # GoalBarStart
    glBegin(GL_POINTS)
    goalBarAllPoints = goalBarP()
    goalBar = goalBarAllPoints[0]
    goalCircle = goalBarAllPoints[1]
    for i in goalBar:
        glVertex2f(i[0], i[1])
    for i in goalCircle:
        glVertex2f(i[0], i[1])
    glEnd()
    # GoalBarEnd

    glColor3f(0, .5, 0)
    glBegin(GL_POINTS)

    scalingFactor = scale
    rotateAngle = rot
    moveX = mvX
    moveY = mvY
    a = math.cos(math.radians(rotateAngle))
    b = math.sin(math.radians(rotateAngle))

    r = np.array([[a, -b, 0],
                  [b, a, 0],
                  [0, 0, 1]])

    s = np.array([[scalingFactor, 0, 0],
                  [0, scalingFactor, 0],
                  [0, 0, 1]])

    trans = np.array([[1, 0, moveX],
                      [0, 1, moveY],
                      [0, 0, 0]])

    rotateScale = np.matmul(r, s)

    stickManBody = stickMan()

    for i in stickManBody:  # making stickman function with the system
        v1 = np.array([[i[0]], [i[1]], [1]])
        v11 = np.matmul(rotateScale, v1)
        v11 = np.matmul(trans, v11)
        glVertex2f(v11[0][0], v11[1][0])

    glEnd()

    centerPoints = [10, 35]
    radius = 5
    allZonePoints = outerCircle(radius, centerPoints)
    # print(allZonePoints)
    glBegin(GL_POINTS)

    for i in allZonePoints:
        v1 = np.array([[i[0]], [i[1]], [1]])
        v11 = np.matmul(rotateScale, v1)
        v11 = np.matmul(trans, v11)
        glVertex2f(v11[0][0], v11[1][0])

    glEnd()

    # BallStart              #ball throw point

    centerPoints = [22, 29]
    if throwPoint != 0:
        centerPoints = throwPoint
        rotateScale = np.array([[1, 0, 0],
                                [0, 1, 0],
                                [0, 0, 1]])
        trans = np.array([[1, 0, 0],
                          [0, 1, 0],
                          [0, 0, 0]])
    radius = 4
    allZonePoints = outerCircle(radius, centerPoints)
    glBegin(GL_POINTS)

    for i in allZonePoints:
        v1 = np.array([[i[0]], [i[1]], [1]])
        v11 = np.matmul(rotateScale, v1)
        v11 = np.matmul(trans, v11)
        glVertex2f(v11[0][0], v11[1][0])

    glEnd()
    # BallEnd                 #ball landing

# Everything that need to be inputed for the system


scene = 0
scale = 1
rotate = 0
mvX = 0
mvY = 0
score = 0
key_pressed = None
main_scene = 0
animate_flag = False
curr_x = 22
curr_y =29
path = []
path_index = 0
def keyboard_event(key, x, y):
    global scene, stepCount, scale, rotate, mvX, mvY, score, key_pressed, animate_flag, curr_x, curr_y
    if scene == 0:
        if key == b's':
            scene += 1
            animate_flag = True

    elif scene == 2:
        if key == b'w':
            animate_flag = True
            mvY += 2
            curr_y += 2
        elif key == b's':
            animate_flag = True
            mvY += -2
            curr_y += -2
        elif key == b'a':
            animate_flag = True
            mvX += -2
            curr_x += -2
        elif key == b'd':
            animate_flag = True
            mvX += 2
            curr_x += 2
        elif key == b't':
            scene += 1
            animate_flag = True


def animate():
    global scene, animate_flag, curr_x
    if scene == 1 and animate_flag:
        animate_flag = False
        glutPostRedisplay()
        scene += 1
    if scene == 2 and animate_flag:
        animate_flag = False
        glutPostRedisplay()
    if scene == 3 and animate_flag:
        animate_flag = False
        glutPostRedisplay()
    if scene == 4 and animate_flag:
        animate_flag = False

def animate2(step):
    global scale, rotate, mvX, mvY, curr_x, curr_y, mx, scene, my, path_index, score
    if curr_y > 500 or curr_x > 500:
        scene += 1
    if abs(curr_x - mx) < 5 and abs(curr_y - my) < 5:
        scene += 1
    else:
        curr_x, curr_y = path[path_index][0], path[path_index][1]
        path_index = min(path_index + 10, len(path) - 1)
    glutPostRedisplay()

timed_id = 0
def main():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    global scene, stepCount, scale, rotate, mvX, mvY, score, key_pressed, main_scene, curr_x, curr_y, mx,my, path, path_index, timed_id
    if scene == 0:

        points = []
        glPointSize(3)
        glColor3f(255, 255, 255)
        glBegin(GL_POINTS)
        points += eightWaySymmetry(50, 480, 50, 320)
        points += eightWaySymmetry(50, 480, 120, 480)
        points += eightWaySymmetry(120, 480, 120, 400)
        points += eightWaySymmetry(120, 400, 50, 400)

        points += eightWaySymmetry(140, 480, 140, 320)
        points += eightWaySymmetry(140, 480, 210, 480)
        points += eightWaySymmetry(210, 480, 210, 400)
        points += eightWaySymmetry(210, 400, 140, 400)
        points += eightWaySymmetry(140, 400, 210, 320)

        points += eightWaySymmetry(90 * 2 + 50, 480, 90 * 2 +50, 320)
        points += eightWaySymmetry(90 * 2 +50, 480, 90 * 2 +120, 480)
        points += eightWaySymmetry(90 * 2 +120, 400, 90 * 2 +50, 400)
        points += eightWaySymmetry(90 * 2 + 50, 320, 90 * 2 + 120, 320)

        points += eightWaySymmetry(90 * 3 +50, 480, 90 * 3 +50, 400)
        points += eightWaySymmetry(90 * 3 +50, 480, 90 * 3 +120, 480)
        points += eightWaySymmetry(90 * 3 +120, 400, 90 * 3 +50, 400)
        points += eightWaySymmetry(90 * 3 + 120, 400, 90 * 3 + 120, 320)
        points += eightWaySymmetry(90 * 3 + 50, 320, 90 * 3 + 120, 320)

        points += eightWaySymmetry(90 * 4 + 50, 480, 90 * 4 + 50, 400)
        points += eightWaySymmetry(90 * 4 + 50, 480, 90 * 4 + 120, 480)
        points += eightWaySymmetry(90 * 4 + 120, 400, 90 * 4 + 50, 400)
        points += eightWaySymmetry(90 * 4 + 120, 400, 90 * 4 + 120, 320)
        points += eightWaySymmetry(90 * 4 + 50, 320, 90 * 4 + 120, 320)

        points += eightWaySymmetry(90 * 2 + 30, 300- 50, 90 * 2 + 30, 280- 50)
        points += eightWaySymmetry(90 * 2 + 140, 300- 50, 90 * 2 + 140, 280- 50)
        points += eightWaySymmetry(90 * 2 + 50, 300 - 50, 90 * 2 + 50, 220 - 50)
        points += eightWaySymmetry(90 * 2 + 50, 300- 50, 90 * 2 + 120, 300- 50)
        points += eightWaySymmetry(90 * 2 + 120, 220- 50, 90 * 2 + 50, 220- 50)
        points += eightWaySymmetry(90 * 2 + 120, 220- 50, 90 * 2 + 120, 140- 50)
        points += eightWaySymmetry(90 * 2 + 50, 140- 50, 90 * 2 + 120, 140- 50)


        for p in points:
            glVertex2f(p[0], p[1])
        glEnd()

    if scene == 1:

        sceneTransform(scale, rotate, mvX, mvY, 0)

    if scene == 2:

        sceneTransform(scale, rotate, mvX, mvY, 0)

    if scene == 3:
        left_prob_cloud = min(220, curr_y)
        right_prob_cloud = max(260, 500 - curr_y)
        mx = random.randint(left_prob_cloud, right_prob_cloud) #240
        my = 420

        if (mx >= 220 and mx <= 260) and (my >= 410 and my <= 430):
            score = 420 - curr_y
        path = eightWaySymmetry(curr_x, curr_y, mx, my)
        scene += 1

    if scene == 4:
        timed_id = glutTimerFunc(100, animate2, 0)
        sceneTransform(scale, rotate, mvX, mvY, [curr_x, curr_y])

    if scene == 5:
        points = []
        glPointSize(3)
        glColor3f(255, 255, 255)
        glBegin(GL_POINTS)
        points += eightWaySymmetry(50, 480, 85, 400)
        points += eightWaySymmetry(120, 480, 85, 400)
        points += eightWaySymmetry(85, 400, 85, 320)

        points += eightWaySymmetry(50 + 90 * 1, 480, 120 + 90 * 1, 480)
        points += eightWaySymmetry(120 + 90 * 1, 480, 120 + 90 * 1, 320)
        points += eightWaySymmetry(120 + 90 * 1, 320, 50 + 90 * 1, 320)
        points += eightWaySymmetry(50 + 90 * 1, 320, 50 + 90 * 1, 480)

        points += eightWaySymmetry(120 + 90 * 2, 480, 120 + 90 * 2, 320)
        points += eightWaySymmetry(120 + 90 * 2, 320, 50 + 90 * 2, 320)
        points += eightWaySymmetry(50 + 90 * 2, 320, 50 + 90 * 2, 480)
        if score:
            points += eightWaySymmetry(50 + 90 * 0, 480 - 180, 67 + 90 * 0, 320 - 180)
            points += eightWaySymmetry(67 + 90 * 0, 320 - 180, 85 + 90 * 0, 480 - 180)
            points += eightWaySymmetry(85 + 90 * 0, 480 - 180, 102 + 90 * 0, 320 - 180)
            points += eightWaySymmetry(102 + 90 * 0, 320 - 180, 120 + 90 * 0, 480 - 180)

            points += eightWaySymmetry(90 * 1 + 85, 480 - 180, 90 * 1 + 85, 320 - 180)

            points += eightWaySymmetry(90 * 2 + 50, 480 - 180, 90 * 2 + 50, 320 - 180)
            points += eightWaySymmetry(90 * 2 + 50, 480 - 180, 90 * 2 + 120, 320 - 180)
            points += eightWaySymmetry(90 * 2 + 120, 480 - 180, 90 * 2 + 120, 320 - 180)

            points += eightWaySymmetry(90 * 3 + 50, 480 - 180, 90 * 3 + 50, 320 - 180)
        else:
            points += eightWaySymmetry(50 + 90 * 0, 480 - 180, 50 + 90 * 0, 320- 180)
            points += eightWaySymmetry(50 + 90 * 0, 320- 180, 120 + 90 * 0, 320- 180)

            points += eightWaySymmetry(50 + 90 * 1, 480- 180, 120 + 90 * 1, 480- 180)
            points += eightWaySymmetry(120 + 90 * 1, 480- 180, 120 + 90 * 1, 320- 180)
            points += eightWaySymmetry(120 + 90 * 1, 320- 180, 50 + 90 * 1, 320- 180)
            points += eightWaySymmetry(50 + 90 * 1, 320- 180, 50 + 90 * 1, 480- 180)

            points += eightWaySymmetry(90 * 2 + 50, 480- 180, 90 * 2 + 50, 400- 180)
            points += eightWaySymmetry(90 * 2 + 50, 480- 180, 90 * 2 + 120, 480- 180)
            points += eightWaySymmetry(90 * 2 + 120, 400- 180, 90 * 2 + 50, 400- 180)
            points += eightWaySymmetry(90 * 2 + 120, 400- 180, 90 * 2 + 120, 320- 180)
            points += eightWaySymmetry(90 * 2 + 50, 320- 180, 90 * 2 + 120, 320- 180)

            points += eightWaySymmetry(90 * 3 + 50, 480- 180, 90 * 3 + 50, 320- 180)
            points += eightWaySymmetry(90 * 3 + 50, 480- 180, 90 * 3 + 120, 480- 180)
            points += eightWaySymmetry(90 * 3 + 120, 400- 180, 90 * 3 + 50, 400- 180)
            points += eightWaySymmetry(90 * 3 + 50, 320- 180, 90 * 3 + 120, 320- 180)

            points += eightWaySymmetry(90 * 4 + 50, 480 - 180, 90 * 4 + 50, 320 - 180)



        for p in points:
            glVertex2f(p[0], p[1])
        glEnd()

        glPointSize(10)
        glColor3f(255, 255, 255)
        glBegin(GL_POINTS)
        if score:
            glVertex2f(90 * 3 + 50, 320 - 200)
        else:
            glVertex2f(90 * 4 + 50, 320 - 200)
        glEnd()

        print('+', '-' * 45, '+', sep='')
        print('| Game is over.', ' ' * 31, '|', sep='')
        print("Your score: ", score)
        print('+', '-' * 45, '+', sep='')


    glutSwapBuffers()


def iterate():
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(window_pos_x, window_pos_y)
window = glutCreateWindow("CSE423: Assignment 3")
glutDisplayFunc(main)
glutIdleFunc(animate)
glutKeyboardFunc(keyboard_event)
glutMainLoop()


