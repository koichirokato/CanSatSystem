#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

def find_rect_of_target_color(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    mask = np.zeros(h.shape, dtype=np.uint8)
    mask[((h < 20) | (h > 200)) & (s > 128)] = 255
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    # rects : [x,y,width,height]
    for contour in contours:
        approx = cv2.convexHull(contour)
        rect = cv2.boundingRect(approx)
        rects.append(np.array(rect))
    return rects

def camera_system():
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # while cv2.waitKey(30) < 0:
    _, frame = capture.read()
    rects = find_rect_of_target_color(frame)
    capture.release()
    cv2.destroyAllWindows()
    return rects

if __name__ == "__main__":
    capture = cv2.VideoCapture(0)
    while cv2.waitKey(30) < 0:
        _, frame = capture.read()
        rects = find_rect_of_target_color(frame)
        if len(rects) > 0:
            rect = max(rects, key=(lambda x: x[2] * x[3]))
            cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2)
            circle_point = np.array(rect[0:2] + (rect[2:4])/2, dtype=int)
            circle_point = np.round(circle_point)
            print(circle_point)
            cv2.circle(frame,tuple(circle_point),10,(0,0,255),-1)
        cv2.imshow('red', frame)
        print(rect)
    capture.release()
    cv2.destroyAllWindows()
