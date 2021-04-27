from random import random, uniform
from math import sin, cos
from math import radians , sqrt
import csv
import os

print(os.curdir)
def shift2d_kp(kp):
    '''kp - 1D list of keypoints [X1,Y1,X2,Y2,...]'''
    minx=min([kp[i] for i in range(len(kp)) if i%2==0])
    miny=min([kp[i] for i in range(len(kp)) if i%2==1])
    maxx=max([kp[i] for i in range(len(kp)) if i%2==0])
    maxy=max([kp[i] for i in range(len(kp)) if i%2==1])

    print(maxx)
    print(maxy)

    print(minx)
    print(miny)
    
    #aug_kp=kp.copy()
    
    disp = [uniform(-minx, 1 - maxx), uniform(-miny, 1 - maxy)]
    print(disp)
    aug_kp=[kp[i]+disp[0] if i%2==0 else kp[i]+disp[1] for i in range(len(kp))]
    return aug_kp


def rotate_kp(kp,center =[0.5,0.5],max_angle = 30):
    '''Currently available data has the signer well centered hence there will be no issure in small rotations'''
    angle = uniform(-1*max_angle,max_angle)
    #angle = max_angle
    new_kp = kp.copy()
    for i in range(0,len(kp)-1,2):
        x = kp[i]
        y = kp[i+1]
        new_x = center[0] + cos(radians(angle)) * (x-center[0]) - sin(radians(angle)) * (y-center[1])
        new_y = center[1] + sin(radians(angle)) * (x-center[0]) - cos(radians(angle)) * (y-center[1])
        new_kp[i],new_kp[i+1] = new_x , new_y
    return new_kp



def scalekp(kp,max_range=1.4,min_range=0.8):
    rand_scale = 1 + (max_range - min_range) * (random() - (1 - min_range))
    center = [0.5,0.5]
    scaled_list = [center[0] + (kp[i] - center[0]) * rand_scale for i in range(len(kp))]
    return scaled_list


print(rotate_kp([1,1]))
'''with open("./csv_data/all_raw_csv_data.csv") as f:
    w = open("./csv_data/all_aug_csv_data.csv",'a')
    reader = csv.reader(f)
    for row in reader:
        print(row)
        if row == []:
            continue
        if row[0] == "letter":
            continue
        w.write(",".join(row) +"\n")
        letter =  row.pop(0)
        kp = list(map(float,row))
        
        s=""
        for k in range(6):
            rotated  =  list(map(str,[letter] + rotate_kp(kp)))
            shifted  =  list(map(str,[letter] + shift2d_kp(kp)))
            scaled   =  list(map(str,[letter] + scalekp(kp)))
            s += ",".join(rotated) +"\n"
            s += ",".join(shifted) +"\n"
            s += ",".join(scaled) +"\n"
        w.write(s)'''
