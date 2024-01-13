from Classes.button import Button
from Classes.mouse import Mouse
import tkinter
import cv2
from pynput.keyboard import Key, Controller as kc
from pynput.mouse import Button as bt, Controller as mc
import mediapipe as mp
import numpy as np

dimensions = (1280, 720)
boardheight = 600
boardwidth = 300
clicklag = 5
tolerance = 30

'''
dimensions: screen x, y
boardheight, boardwidth makes key dimension
clicklag: time between each input
tolerance: distance needed in hand to click
'''

vid = cv2.VideoCapture(0)
vid.set(3, dimensions[0])
vid.set(4, dimensions[1])
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
buttonlist = []
buttonlower = []
mode = True
qwerty = [["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"], ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"], ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":"], ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"], ["SHIFT", "ENTER", "SPACE", "MOUSE", "SHOW", "TAB", "DEL", "ESC"]]
qwertyl = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"], ["a", "s", "d", "f", "g", "h", "j", "k", "l", ":"], ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"], ["SHIFT", "ENTER", "SPACE", "MOUSE", "SHOW", "TAB", "DEL", "ESC"]]
escape = True
press = tolerance
leftt = 0
rightt = 0
caps = False
time = clicklag
board = (int(dimensions[0]/2), int(dimensions[1]/2))
show = True
shows = False
lefttoggle = True
root = tkinter.Tk()
root.withdraw()
sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
righttoggle = True
key = kc()
mouse = mc()
mouses = Mouse(clicklag)

def make(startpos, endpos):
    x1, y1 = startpos
    x2, y2 = endpos
    x = (x2 - x1)/len(qwerty[0])
    y = (y2 - y1)/len(qwerty)
    l = int(x*8/10), int(y*8/10)
    for i in range(len(qwerty)):
        for j in range(len(qwerty[i])):
            if i + 1 == len(qwerty):
                length = (len(qwerty[0]) - 2)*x+l[0]
                kl = length / (len(qwerty[-1]) - 1)
                buttonlist.append(Button((int(kl*j)+x1, int(y*i)+y1), (int(kl*8/10), l[1]), qwerty[i][j]))
            else:
                buttonlist.append(Button((int(x*j)+x1, int(y*i)+y1), l, qwerty[i][j]))
    for i in range(len(qwertyl)):
        for j in range(len(qwertyl[i])):
            if i + 1 == len(qwertyl):
                length = (len(qwertyl[0]) - 2)*x+l[0]
                kl = length / (len(qwertyl[-1]) - 1)
                buttonlower.append(Button((int(kl*j)+x1, int(y*i)+y1), (int(kl*8/10), l[1]), qwertyl[i][j]))
            else:
                buttonlower.append(Button((int(x*j)+x1, int(y*i)+y1), l, qwertyl[i][j]))

def det(frame, hands):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    return results

def keys(b):
    global escape
    global mode
    global shows
    if b.text == "SHIFT":
        return True
    elif b.text == "ENTER":
        key.press(Key.enter)
    elif b.text == "SPACE":
        key.press(Key.space)
    elif b.text == "MOUSE":
        mode = True
    elif b.text == "SHOW":
        buttonlist[44].text = "HIDE"
        buttonlower[44].text = "HIDE"
        shows = not shows
    elif b.text == "TAB":
        key.press(Key.tab)
    elif b.text == "DEL":
        key.press(Key.backspace)
    elif b.text == "ESC":
        escape = False
    elif b.text == "HIDE":
        shows = not shows
        buttonlist[44].text = "SHOW"
        buttonlower[44].text = "SHOW"
    else:
        key.press(b.text)
    return False

def clicks(n):

    global mode
    global shows

    if n == 1:
        mouse.click(bt.left)
    elif n == 3:
        mouse.click(bt.right)
    elif n == 7:
        shows = not shows
    elif n == 15:
        mouse.press(bt.left)
    elif n >= 8 and n % 2 == 0:
        mode = False
    if n == 0:
        mouse.release(bt.left)

def dist(x, y):
    return ((y[0]-x[0])**2+(y[1]-x[1])**2)**(1/2)

make((board[0]-boardheight, board[1]-boardwidth), (board[0]+boardheight,  board[1]+boardwidth))

with mp_hands.Hands(max_num_hands = 2, min_detection_confidence = 0.8, min_tracking_confidence = 0.5) as hands:

    while escape:
        leftt = leftt + 1
        rightt = rightt + 1
        if leftt == time:
            leftt = leftt % time
            lefttoggle = True
        if rightt == time:
            rightt = rightt % time
            righttoggle = True
    

        ret, frame = vid.read()
        if ret:
            frame = cv2.flip(frame, 1)
            results = det(frame, hands)
            points = results.multi_hand_landmarks
            if points:
                left = np.array([[res.x*vid.get(3), res.y*vid.get(4), res.z] for res in points[0].landmark])
                if len(points) == 2:
                    right = np.array([[res.x*vid.get(3), res.y*vid.get(4), res.z] for res in points[1].landmark])
                if mode:
                    Mouse.handNum(mouses, left)
                    if mouses.click:
                        clicks(mouses.past)
                        mouses.click = False
                    if mouses.gesture % 2 == 1 or (mouses.past == 15 and mouses.gesture == 0):
                        mouse.position = int(left[0][0]*sw/dimensions[0]), int(left[0][1]*sh/dimensions[1])
                if shows:
                    for hand in points:
                        mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            if not mode:
                if shows:
                    buttonlist[44].text = "HIDE"
                    buttonlower[44].text = "HIDE"
                else:
                    buttonlist[44].text = "SHOW"
                    buttonlower[44].text = "SHOW"
                if caps:
                    button = buttonlist
                else:
                    button = buttonlower
                for b in button:
                    if points:
                        if b.check(left[8][:2]):
                            if press > dist(left[8][:2], left[4][:2]) and lefttoggle:
                                leftt = 0
                                lefttoggle = False
                                if keys(b):
                                    caps = not caps
                        elif len(points)==2 and press<dist(left[8][:2], right[8][:2]):
                            if b.check(right[8][:2]):
                                if press > dist(right[8][:2], right[4][:2]) and righttoggle:
                                    rightt = 0
                                    righttoggle = False
                                    if keys(b):
                                        caps = not caps
                    b.draw(frame)
            cv2.imshow("Video", frame)
        if cv2.waitKey(1) == ord("-"):
            break
vid.release
cv2.destroyAllWindows


