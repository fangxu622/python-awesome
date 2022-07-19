
#保存图像

import numpy as np
import cv2
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-i","--input_video", help="input path ", type=str)
parser.add_argument("-o","--out_video", help="outpath", type=str)
args = parser.parse_args()

#cap = cv2.VideoCapture(r"I:\20180129\1\20180129082515\1517214315489424063.h264")
#cap = cv2.VideoCapture(r"I:\20180129\0\20180129080032\1517212832974818707.h264")
cap = cv2.VideoCapture(args.input_video)


cc = cap.get(7)
print(cc)

c=0
while (cap.isOpened()):
    ret, frame = cap.read()
    c = c + 1
    if not ret:
        break
    if c % 1==0:#and c > 1800
    ##gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        gray=frame[:,300:1550,:].copy()

        #gray_re=cv2.resize(gray,(0,0),interpolation=cv2.INTER_LINEAR)
        #cv2.imshow('frame', gray)
        cv2.imwrite(args.out_video+"\\" + str(c) + '.jpg', gray)  # 存储为图像

        if c % 200 == 0:
            print(c)

        #print("已读完")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()