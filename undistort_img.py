import cv2
import numpy as np
import sys
import glob

DIM=(1920, 1080)
K=np.array([[402.2979080929489, 0.0, 991.2069079274011], [0.0, 403.73598387954615, 620.0896074735731], [0.0, 0.0, 1.0]])
D=np.array([[0.14122685248115707], [-0.5609373445541239], [0.6898134489078499], [-0.2968557786411538]])
def undistort(img_path,out_path):
    img = cv2.imread(img_path)
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    outfilepath=out_path+img_path[img_path.rindex("\\"):]
    cv2.imwrite(outfilepath.replace(".jpg","_d.jpg"),undistorted_img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
if __name__ == '__main__':
    #for p in sys.argv[1:]:
    images = glob.glob(r'F:\SZU-Prj\jiaonang\camera-calibration\img3\*.jpg')
    out=r"F:\SZU-Prj\jiaonang\tools\calibr-fisheye\result"
    for p in  images:
        undistort(p,out)