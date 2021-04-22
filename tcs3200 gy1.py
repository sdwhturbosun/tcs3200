import RPi.GPIO as g
import time
from color import tcs3200

out=26
s2=19
s3=13
led=22
s0=27
s1=17
tcs=tcs3200(out,led,s0,s1,s2,s3)
tcs.openled()
tcs.getjizhunshijian()
while True:
    i=input("是否检测(y/n):")
    if i=='y':
        tcs.getrgbfangbo()
        
