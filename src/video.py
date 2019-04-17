#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit as Die
try:
    import sys
    import cv2
    from colordetection import ColorDetector
except ImportError as err:
    Die(err)
string1 = ""

class Webcam:
    def __init__(self):
        self.cam              = cv2.VideoCapture(0)
        self.stickers         = self.get_sticker_coordinates('main')
        self.current_stickers = self.get_sticker_coordinates('current')
        self.preview_stickers = self.get_sticker_coordinates('preview')

    def get_sticker_coordinates(self, name):
        """
        Every array has 2 values: x and y.
        Grouped per 3 since on the cam will be
        3 rows of 3 stickers.

        :param name: the requested color type
        :returns: list
        """
        stickers = {
            'main': [
                [200, 120], [300, 120], [400, 120],
                [200, 220], [300, 220], [400, 220],
                [200, 320], [300, 320], [400, 320]
            ],
            'current': [
                [20, 20], [54, 20], [88, 20],
                [20, 54], [54, 54], [88, 54],
                [20, 88], [54, 88], [88, 88]
            ],
            'preview': [
                [20, 130], [54, 130], [88, 130],
                [20, 164], [54, 164], [88, 164],
                [20, 198], [54, 198], [88, 198]
            ]
        }
        return stickers[name]


    def draw_main_stickers(self, frame):
        """Draws the 9 stickers in the frame."""
        for x,y in self.stickers:
            cv2.rectangle(frame, (x,y), (x+30, y+30), (255,255,255), 2)

    def draw_current_stickers(self, frame, state):
        """Draws the 9 current stickers in the frame."""
        for index,(x,y) in enumerate(self.current_stickers):
            cv2.rectangle(frame, (x,y), (x+32, y+32), ColorDetector.name_to_rgb(state[index]), -1)

    def draw_preview_stickers(self, frame, state):
        """Draws the 9 preview stickers in the frame."""
        for index,(x,y) in enumerate(self.preview_stickers):
            cv2.rectangle(frame, (x,y), (x+32, y+32), ColorDetector.name_to_rgb(state[index]), -1)

    def color_to_notation(self, color):
        """
        Return the notation from a specific color.
        We want a user to have green in front, white on top,
        which is the usual.

        :param color: the requested color
        """
        notation = {
            'green'  : 'F',
            'white'  : 'U',
            'blue'   : 'B',
            'red'    : 'R',
            'orange' : 'L',
            'yellow' : 'D'
        }
        return notation[color]

    def scan(self):
        """
        Open up the webcam and scans the 9 regions in the center
        and show a preview in the left upper corner.

        After hitting the space bar to confirm, the block below the
        current stickers shows the current state that you have.
        This is show every user can see what the computer toke as input.

        :returns: dictionary
        """
        mf = 0
        sides   = {}
        preview = ['white','white','white',
                   'white','white','white',
                   'white','white','white']
        state   = [0,0,0,
                   0,0,0,
                   0,0,0]
       # string1 = "" 
        while True:
            _, frame = self.cam.read()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            key = cv2.waitKey(10) & 0xff

            # init certain stickers.
            self.draw_main_stickers(frame)
            self.draw_preview_stickers(frame, preview)
            flage=1
            for index,(x,y) in enumerate(self.stickers):
                roi          = hsv[y:y+32, x:x+32]
                avg_hsv      = ColorDetector.average_hsv(roi)
                color_name   = ColorDetector.get_color_name(avg_hsv)
                state[index] = color_name

                # update when space bar is pressed.
                if key == 32:
                    if flage ==1:
                       # print state
                        mf+=1
                        str_(state,mf)
                        flage=0
                    preview = list(state)
                    self.draw_preview_stickers(frame, state)
                    face = self.color_to_notation(state[4])
                    notation = [self.color_to_notation(color) for color in state]
                    sides[face] = notation
            
            # show the new stickers
            self.draw_current_stickers(frame, state)

            # append amount of scanned sides
            text = 'scanned sides: {}/6'.format(len(sides))
            cv2.putText(frame, text, (20, 460), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 1, cv2.CV_AA)

            # quit on escape.
            if key == 27:
                break

            # show result
            cv2.imshow("default", frame)

        self.cam.release()
        cv2.destroyAllWindows()
        return sides if len(sides) == 6 else False
def zh(Color1):
    if Color1=="blue":
        return "B"
    elif Color1=="orange":
        return "O"
    elif Color1=="white":
        return "W"
    elif Color1=="yellow":
        return "Y"
    elif Color1=="green":
        return "G"
    else:
        return "R"
def  str_(list_,m):
    global string1
    str1 = ""
    for i in range(9):
        str2=list_[i]
        if m==1:
            if i==4:
                str1+="G"
                continue
            if i%3 == 0:
                str1+="\n"
            str1+=zh(str2)
        elif m==2:
            if i==4:
                str1+="W"#ROBY
                continue
            if i%3 == 0:
                str1+="\n"
            str1+=zh(str2)
        elif m==3:
            if i==4:
                str1+="R"
                continue
            if i%3 == 0:
                str1+="\n"
            str1+=zh(str2)
        elif m==4:
            if i==4:
                str1+="O"
                continue
            if i%3 == 0:
                str1+="\n"
            str1+=zh(str2)
        elif m==5:
            if i==4:
                str1+="B"
                continue
            if i%3 == 0:
                str1+="\n"
            str1+=zh(str2)
        elif m==6:
            if i==4:
                str1+="Y"
                continue
            if i%3 == 0:
                str1+="\n"
            str1+=zh(str2)
    str1+="\n"
    string1=string1+str1
    if m == 6:
        makefile()
    print str1
def makefile():
    global string1
    input_=open("CUBE_STATE.txt",'w')
    input_.write(string1)
    input_.close()
webcam = Webcam()
