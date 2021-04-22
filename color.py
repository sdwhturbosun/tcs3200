import RPi.GPIO as g
import time
class tcs3200:
    def __init__(self,out,led,s0,s1,s2,s3):
        self.out=out
        self.led=led
        self.s0=s0
        self.s1=s1
        self.s2=s2
        self.s3=s3
        self.t1=0
        self.t2=0
        self.fangbo=0#记录当前检测方波个数
        self.shijian=0#
        self.jizhunshijian=[0,0,0]#以255个方波为基准，将rgb的基准时间分别保存
        self.rgbfangbo=[0,0,0]#r,g,b方波数量，基准时间内测的的3个方波个数就表示此刻rgb的值
        g.setmode(g.BCM)
        g.setwarnings(False)
        g.setup((self.led,self.s0,self.s1,self.s2,self.s3),g.OUT)
        g.setup(out,g.IN,pull_up_down=g.PUD_UP)
    def fangbojisuan(self,channel):
        if g.event.detected(self.out):
            self.fangbo+=1
        if self.fangbo==255:
            self.t2=time.time()
            g.remove_event_detect(self.out)
    def openled(self):
        g.output(self.led,1)
    def closeled(self):
        g.output(self.led,0)
    def redfilter(self):
        g.output(self.s2,0)
        g.output(self.s3,0)
    def bluefilter(self):
        g.output(self.s2,0)
        g.output(self.s3,1)
    def nofilter(self):
        g.output(self.s2,1)
        g.output(self.s3,0)
    def greenfilter(self):
        g.output(self.s2,1)
        g.output(self.s3,1)
    #内部震荡方波频率与光强成正比，OUT引脚输出方波频率与震荡器成比例关系，比例因子通过s0,s1设置
    def nopower(self):
        g.output(self.s0,0)
        g.output(self.s1,0)
    def out1than50(self):
        g.output(self.s0,0)
        g.output(self.s1,1)
    def out1than5(self):
        g.output(self.s0,1)
        g.output(self.s1,0)
    def out1than1(self):
        g.output(self.s0,1)
        g.output(self.s1,1)
    def getjizhunshijian(self):#使用1：50的输出比例，以白色255个方波为基准
        fangbo=0
        jizhunshijian=0
        
        self.out1than50()
        self.redfilter()#time for red
        self.t1=time.time()
        while self.fangbo<255:
            g.wait_for_edge(self.out,g.RISING)
            self.fangbo+=1
        self.t2=time.time()
        self.fangbo=0
        rt=self.t2-self.t1
        
        self.jizhunshijian[0]=rt
       
        self.t1=0
        self.t2=0
        self.greenfilter()#time for green
        self.t1=time.time()
        while self.fangbo<255:
            g.wait_for_edge(self.out,g.RISING)
            self.fangbo+=1
        self.t2=time.time()
        self.fangbo=0
        gt=self.t2-self.t1
        
        self.jizhunshijian[1]=gt
        
        self.t1=0
        self.t2=0
        self.bluefilter()#time for blue
        self.t1=time.time()
        while self.fangbo<255:
            g.wait_for_edge(self.out,g.RISING)
            self.fangbo+=1
        self.t2=time.time()
        self.fangbo=0
        bt=self.t2-self.t1
        
        self.jizhunshijian[2]=bt
        
        self.t1=0
        self.t2=0
        print(self.jizhunshijian)
    def getrgbfangbo(self):
        rshijian=self.jizhunshijian[0]
        gshijian=self.jizhunshijian[1]
        bshijian=self.jizhunshijian[2]
        self.out1than50()#out:震荡器频率=1:5
        self.redfilter()#检测红色
        fangbo=0
        t1=time.time() 
        while time.time()-t1<rshijian:
            g.wait_for_edge(self.out,g.RISING)#等待边缘检测，发现了fangbo就+1
            fangbo+=1
        self.rgbfangbo[0]=fangbo
        self.greenfilter()#检测绿色
        fangbo=0
        t1=time.time() 
        while time.time()-t1<gshijian:
            g.wait_for_edge(self.out,g.RISING)
            fangbo+=1
        self.rgbfangbo[1]=fangbo
        self.bluefilter()#检测蓝色
        fangbo=0
        t1=time.time() 
        while time.time()-t1<bshijian:
            g.wait_for_edge(self.out,g.RISING)
            fangbo+=1
        self.rgbfangbo[2]=fangbo
        print(self.rgbfangbo)
        
        