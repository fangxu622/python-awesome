import struct
import os

# first gen imu csv

def read_bigFile(str_path):
    src = open(str_path, 'rb')
    out = str_path[str_path.rindex("/") + 1:str_path.rindex(".") + 1] + "csv"
    outdir=os.path.dirname(str_path)
    out_path=os.path.join(outdir,out)
    #mag_path=str_path.replace(".ins","_mag.csv")
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
    #return (out_path,mag_path)

path="/media/fangxu/Segate3T/Linux-Proj/SLAM/capsule-slam/1406-1405-2019-09-18.ins" 
read_bigFile(path)
