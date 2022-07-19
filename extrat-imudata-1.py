import struct
import os
import pandas as pd
from tqdm import tqdm
from scipy.ndimage import gaussian_filter1d
import numpy as np
from matplotlib import pyplot as plt

# first gen imu csv

def read_bigFile(str_path):
    src = open(str_path, 'rb')
    out = str_path[str_path.rindex("\\") + 1:str_path.rindex(".") + 1] + "csv"
    outdir=os.path.dirname(str_path)
    out_path=os.path.join(outdir,out)
    mag_path=str_path.replace(".ins","_mag.csv")
    our_file = open(out_path, "w")
    i=0
    cont = src.read(44)
    while len(cont) != 0:
        i=i+1
        l1 = struct.unpack("IIfffffffff", cont)
        l2 = list(l1)
        for x in range(2, 11):
            l2[x] = round(l2[x], 7)
        l3 = str(l2)[1:-1]
        l4 = l3.replace(", ", "\t")
        our_file.write(l4 + "\n")
        cont = src.read(44)
        print(str(i)) 
    src.close()
    our_file.close()
    return (out_path,mag_path)
    #print(l1)

# second gaussion filter 

def sensor_fliter(ins_path):
    #original csv path
    csv_path=ins_path.replace(".ins","_correct.csv")
    dfdata=pd.read_csv(csv_path,sep="\t",header=None)
    filter_csv_path=ins_path.replace(".ins","_filter.csv")

    mag_xl_path=path.replace(".ins","_filter_mag.xlsx")
    acc_xl_path=path.replace(".ins","_filter_acc.xlsx")

    writer_mag = pd.ExcelWriter(mag_xl_path)
    mag_value=dfdata.loc[:,8:10].values.transpose(1,0)
    mag_value_filter=gaussian_filter1d(mag_value,81)
    dfmag=pd.DataFrame(mag_value_filter.transpose(1,0))
    dfmag.to_excel(writer_mag,index = False,float_format='%.8f',header=False)
    writer_mag.save()

    writer_acc = pd.ExcelWriter(acc_xl_path)
    acc_value=dfdata.loc[:,2:4].values.transpose(1,0)
    acc_value_filter=gaussian_filter1d(acc_value,3)
    dfmag=pd.DataFrame(acc_value_filter.transpose(1,0))
    dfmag.to_excel(writer_acc,index = False,float_format='%.8f',header=False)
    writer_acc.save()

    #merge filter data
    time_index=dfdata.loc[:,0:1].values
    gyro=dfdata.loc[:,5:7].values
    merge_all_data=np.hstack([time_index,acc_value_filter.transpose(1,0),gyro,mag_value_filter.transpose(1,0)])
    fmt_params=['%d','%d','%.8f','%.8f','%.8f','%.8f','%.8f','%.8f','%.8f','%.8f','%.8f']
    np.savetxt(filter_csv_path,merge_all_data,fmt=fmt_params,delimiter='\t',newline='\n')
    
    axis=(dfdata.loc[:,0].values-dfdata.loc[:,0].values[0])/100000
    # plot
    plt.figure()
    plt.subplot(411)
    plt.title('acc_ori')
    plt.plot(axis,acc_value[0], color='green', label='x',linewidth=0.5)
    plt.plot(axis,acc_value[1], color='red', label='y',linewidth=0.5)
    plt.plot(axis,acc_value[2], color='blue', label='z',linewidth=0.5)
    plt.legend() # 显示图例
    plt.xlabel('acc')
    plt.ylabel('time(s)')

    plt.subplot(412)
    plt.title('acc_filter')
    plt.plot(axis,acc_value_filter[0], color='green', label='x',linewidth=0.5)
    plt.plot(axis,acc_value_filter[1], color='red', label='y',linewidth=0.5)
    plt.plot(axis,acc_value_filter[2], color='blue', label='z',linewidth=0.5)
    plt.legend() # 显示图例
    plt.xlabel('acc')
    plt.ylabel('time(s)')

    plt.subplot(413)
    plt.title('mag_ori')
    plt.plot(axis,mag_value[0], color='green', label='x',linewidth=0.5)
    plt.plot(axis,mag_value[1], color='red', label='y',linewidth=0.5)
    plt.plot(axis,mag_value[2], color='blue', label='z',linewidth=0.5)
    plt.legend() # 显示图例
    plt.xlabel('mag')
    plt.ylabel('time(s)')

    plt.subplot(414)
    plt.title('mag_filter')
    plt.plot(axis,mag_value_filter[0], color='green', label='x',linewidth=0.5)
    plt.plot(axis,mag_value_filter[1], color='red', label='y',linewidth=0.5)
    plt.plot(axis,mag_value_filter[2], color='blue', label='z',linewidth=0.5)
    plt.legend() # 显示图例
    plt.xlabel('mag')
    plt.ylabel('time(s)')

    plt.show()


# second

def mag_correct(ins_path,pb):
    #original csv path
    csv_path=ins_path.replace(".ins",".csv")
    dfdata=pd.read_csv(csv_path,sep="\t",header=None)

    correct_csv_path=ins_path.replace(".ins","_correct.csv")
    
    correct_path=ins_path.replace(".ins","_mag_correct.xlsx")

    writer = pd.ExcelWriter(correct_path)

    for i in tqdm(range(len(dfdata.loc[:,0]))):
        tmp3fx=dfdata.loc[i,8]/100-pb[6]
        tmp3fy=dfdata.loc[i,9]/100-pb[7]
        tmp3fz=dfdata.loc[i,10]/100-pb[8]
        dfdata.loc[i,8]=pb[0]*tmp3fx+pb[1]*tmp3fy+pb[2]*tmp3fz
        dfdata.loc[i,9]=pb[1]*tmp3fx+pb[3]*tmp3fy+pb[4]*tmp3fz
        dfdata.loc[i,10]=pb[2]*tmp3fx+pb[4]*tmp3fy+pb[5]*tmp3fz
    dfdata.to_csv(correct_csv_path,sep="\t",header=None,index=False,float_format='%.8f')

    dfdata.loc[:,8:10].to_excel(writer,index = False,float_format='%.8f',header=False)
    writer.save()

# third
def gen_xlsx(path):
    xl_path=path.replace(".ins","_mag.xlsx")
    csv_path=path.replace(".ins",".csv")
    
    dfdata=pd.read_csv(csv_path,sep="\t",header=None)
    writer = pd.ExcelWriter(xl_path)
    for i in tqdm(range(len(dfdata.loc[:,0]))):
        dfdata.loc[i,8]=dfdata.loc[i,8]/100
        dfdata.loc[i,9]=dfdata.loc[i,9]/100
        dfdata.loc[i,10]=dfdata.loc[i,10]/100
    dfdata.loc[:,8:10].to_excel(writer,index = False,float_format='%.8f',header=False)
    writer.save()



#path = r"F:\SZU-Prj\jiaonang\video-data\Ori-Video\camera_4\20180717_151601.ins"
#path="/media/fangxu/0F0510A00F0510A0/SZU-Prj/jiaonang/2019_310_capsule_prj/capsule_data/SL-VINS4/test-f4-x4-2019-07-02.ins"
#pb1
path=r"F:\SZU-Prj\jiaonang\2019_310_capsule_prj\IMU_PROCESS\capsule-imu\sz-fn4-fn4-2019-08-07.ins" 

#pb2
#path=r"F:\SZU-Prj\jiaonang\2019_310_capsule_prj\IMU_PROCESS\capsule-imu\sz-Xz1-Xz2-2019-08-08.ins" 
pb1=[1.085504171,-0.1596054,0.0733718378,1.452202268,-0.0368769996,0.6502236090,
            1.31647578076729,-0.46693767000554,0.30360859176764]
pb2=[1.10698652624115,-0.0146346862596,-0.00908552408071,1.337504412664,-0.024027693023,0.676010473413,
            1.306786060957,-0.461522530403,0.2388858011795]
pb3=[1.951829973843,
-0.6293990427481,
0.622595371178681,
1.21010502393173,
-0.941521054306247,
1.25212592530585,
1.29269300192224,
0.200966038179349,
1.01047273462001]
#first
read_bigFile(path)

#second
#sensor_fliter(path)

#second
#gen_xlsx(path)

#third
#mag_correct(path,pb3)