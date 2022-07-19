#export PYTHONPATH="/home/fangxu/anaconda3/lib/python3.6/site-packages:$PYTHONPATH"
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')

import numpy as np
import cv2
import os


mask_path="/media/fangxu/0F0510A00F0510A0/SZU-Prj/jiaonang/2019_310_capsule_prj/IMU_PROCESS/mask1.bmp"
path="/media/fangxu/Segate3T/Linux-Proj/SLAM/capsule-slam/1406-1405-2019-09-18.mp4"

#windows
#mask_path=r"F:\SZU-Prj\jiaonang\2019_310_capsule_prj\IMU_PROCESS\mask1.bmp"
#path=r"F:\Capsule-SLAM\Camera_params\Camera_params-1-1-2019-09-03.mp4"
cap = cv2.VideoCapture(path)
file1=path.split("/")[-1]
cc = cap.get(7)
print(cc)
mask=cv2.imread(mask_path)[:,:,1]/255
tem_dir=os.path.dirname(path)

root_dir=os.path.join(tem_dir,"cam0")
c=0
while (cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    if c % 1==0:#and c > 1800
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray=gray[20:,420:1590]*mask
        gray=gray.astype(np.uint8)#
        #gray_re=cv2.resize(gray,(670,600),interpolation=cv2.INTER_LINEAR)
        #cv2.imshow('frame', gray)
        filename=os.path.join(root_dir,str(c) + '.jpg')
        cv2.imwrite(filename, gray) 
        if c % 200 == 0:
            print(c)

        #print("已读完")
        #if cv2.waitKey(1) & 0xFF == ord('q'):
         #   break
        c = c + 1
cap.release()
#cv2.destroyAllWindows()