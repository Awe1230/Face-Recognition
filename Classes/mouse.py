class Mouse:

    def __init__(self, lag):
        self.gesture = 0
        self.history = [0]*lag
        self.past = 0
        self.click = False

    def handNum(self, landmarks):
        gesture = 0
        for i in range(4):
            j = 8 + 4*i
            if landmarks[j][1] < landmarks[j-3][1]:
                gesture = 2**i + gesture
        
        for i in range(len(self.history) + 1):
            if i != len(self.history):
                if gesture != self.history[i]:
                    self.history[i] = gesture
                    break
            elif gesture != self.gesture:
                if gesture == 0 or (self.gesture == 0 and self.past == 15):
                    self.click = True
                self.past = self.gesture
                self.gesture = gesture

        
        

