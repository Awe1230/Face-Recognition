import cv2
class Button:
    def __init__(self, pos1, length, text):
        self.pos1 = pos1
        self.length = length
        self.text = text
        self.default = (112, 112, 112)
        self.color = self.default
        self.caps = False
    def draw(self, frame):
        cv2.rectangle(frame, self.pos1, (self.pos1[0]+self.length[0], self.pos1[1]+self.length[1]), self.color, cv2.FILLED)
        i = self.text in ["I", "i", "J", "j", ":", ",", ".", "^", "ENTER", "SPACE", "SHOW"]
        j = self.text in ["m", "TAB", "DEL", "ESC"]
        cv2.putText(frame, self.text, (self.pos1[0]+15+10*i-10*j, self.pos1[1]+60), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 5)
    def check(self, point):
        if self.pos1[0] < point[0] and point[0] < self.pos1[0]+self.length[0]:
            if self.pos1[1] < point[1] and point[1] < self.pos1[1]+self.length[1]:
                self.color = (0, 0, 0)
                return True
        else:
            self.color = (112, 112, 112)
            return False