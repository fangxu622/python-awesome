import os 

path = "/media/fangxu/Segate3T/1-All-Sewer-Data/8-sewer-pipe"
out_path = "/media/fangxu/Segate3T/1-All-Sewer-Data/9-Sewer-video"

file_list = os.listdir(path)

for fname in file_list:
    input = os.path.join(path,fname)
    outp = os.path.join(out_path,fname.replace(".mkv",".mp4") )
    
    command =  "ffmpeg -i "+input+" -c:v copy " + outp
    output=os.system(command)
    print(output)
    
 # ffmpeg -i input.mkv -vcodec copy -acodec copy out.mp4
