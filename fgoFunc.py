###################################################################################################################################################
#                                                                                                                                                 #
#                                                                                                                                                 #
#    YYYYYYY       YYYYYYY     LLLLLLLLLLL                     SSSSSSSSSSSSSSS      FFFFFFFFFFFFFFFFFFFFFF     MMMMMMMM               MMMMMMMM    #
#    Y:::::Y       Y:::::Y     L:::::::::L                   SS:::::::::::::::S     F::::::::::::::::::::F     M:::::::M             M:::::::M    #
#    Y:::::Y       Y:::::Y     L:::::::::L                  S:::::SSSSSS::::::S     F::::::::::::::::::::F     M::::::::M           M::::::::M    #
#    Y::::::Y     Y::::::Y     LL:::::::LL                  S:::::S     SSSSSSS     FF::::::FFFFFFFFF::::F     M:::::::::M         M:::::::::M    #
#    YYY:::::Y   Y:::::YYY       L:::::L                    S:::::S                   F:::::F       FFFFFF     M::::::::::M       M::::::::::M    #
#       Y:::::Y Y:::::Y          L:::::L                    S:::::S                   F:::::F                  M:::::::::::M     M:::::::::::M    #
#        Y:::::Y:::::Y           L:::::L                     S::::SSSS                F::::::FFFFFFFFFF        M:::::::M::::M   M::::M:::::::M    #
#         Y:::::::::Y            L:::::L                      SS::::::SSSSS           F:::::::::::::::F        M::::::M M::::M M::::M M::::::M    #
#          Y:::::::Y             L:::::L                        SSS::::::::SS         F:::::::::::::::F        M::::::M  M::::M::::M  M::::::M    #
#           Y:::::Y              L:::::L                           SSSSSS::::S        F::::::FFFFFFFFFF        M::::::M   M:::::::M   M::::::M    #
#           Y:::::Y              L:::::L                                S:::::S       F:::::F                  M::::::M    M:::::M    M::::::M    #
#           Y:::::Y              L:::::L         LLLLLL                 S:::::S       F:::::F                  M::::::M     MMMMM     M::::::M    #
#           Y:::::Y            LL:::::::LLLLLLLLL:::::L     SSSSSSS     S:::::S     FF:::::::FF                M::::::M               M::::::M    #
#        YYYY:::::YYYY         L::::::::::::::::::::::L     S::::::SSSSSS:::::S     F::::::::FF                M::::::M               M::::::M    #
#        Y:::::::::::Y         L::::::::::::::::::::::L     S:::::::::::::::SS      F::::::::FF                M::::::M               M::::::M    #
#        YYYYYYYYYYYYY         LLLLLLLLLLLLLLLLLLLLLLLL      SSSSSSSSSSSSSSS        FFFFFFFFFFF                MMMMMMMM               MMMMMMMM    #
#                                                                                                                                                 #
#                                                                                                                                                 #
###################################################################################################################################################
'Full-automatic FGO Script'
__author__='hgjazhgj'
import time,os,numpy,cv2,re,logging
from airtest.core.android.android import Android
from airtest.core.android.constant import CAP_METHOD,ORI_METHOD,TOUCH_METHOD
logging.getLogger('airtest').handlers[0].formatter.datefmt='%H:%M:%S'
logger=(lambda logger:(logger.setLevel(logging.DEBUG),logger.addHandler((lambda handler:(handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s]<%(name)s> %(message)s','%H:%M:%S')),handler)[1])(logging.StreamHandler())),logger)[2])(logging.getLogger('fgoFunc'))
IMG_APEMPTY=cv2.imread('image/apempty.png')
IMG_ATTACK=cv2.imread('image/attack.png')
IMG_BEGIN=cv2.imread('image/begin.png')
IMG_BATTLEBEGIN=cv2.imread('image/battlebegin.png')
IMG_BATTLECONTINUE=cv2.imread('image/battlecontinue.png')
IMG_BOUND=cv2.imread('image/bound.png')
IMG_BOUNDUP=cv2.imread('image/boundup.png')
IMG_CARDSEALED=cv2.imread('image/cardsealed.png')
IMG_CHOOSEFRIEND=cv2.imread('image/choosefriend.png')
IMG_END=cv2.imread('image/end.png')
IMG_FAILED=cv2.imread('image/failed.png')
IMG_FRIEND=[[file[:-4],cv2.imread('image/friend/'+file)]for file in os.listdir('image/friend')if file.endswith('.png')]
IMG_GACHA=cv2.imread('image/gacha.png')
IMG_HOUGUSEALED=cv2.imread('image/hougusealed.png')
IMG_LISTEND=cv2.imread('image/listend.png')
IMG_LISTNONE=cv2.imread('image/listnone.png')
IMG_NOFRIEND=cv2.imread('image/nofriend.png')
IMG_PARTYINDEX=cv2.imread('imagse/partyindex.png')
IMG_STAGE=[cv2.imread(f'image/stage{i}.png')for i in range(1,4)]
IMG_STAGETOTAL=[cv2.imread(f'image/total{i}.png')for i in range(1,4)]
IMG_STILL=cv2.imread('image/still.png')
IMG_JACKPOT=cv2.imread('image/jackpot.png')
partyIndex=0
skillInfo=[[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]
houguInfo=[[1,1],[1,1],[1,1],[1,1],[1,1],[1,1]]
dangerPos=[0,0,1]
friendPos=4
masterSkill=[[0,0,0],[0,0,0],[0,0,0,0]]
terminateFlag=False
suspendFlag=False
def verifyFlag():
    while suspendFlag and not terminateFlag:time.sleep(.1)
    if terminateFlag:exit(0)
def sleep(x,part=.1):
    timer=time.time()+x-part
    while time.time()<timer:
        verifyFlag()
        time.sleep(part)
    time.sleep(max(0,timer+part-time.time()))
def show(img):cv2.imshow('imshow',img),cv2.waitKey(),cv2.destroyAllWindows()
class Fuse:
    def __init__(self,fv=300):
        self.__value=0
        self.__max=fv
    @property
    def value(self):return self.__value
    @property
    def max(self):return self.__max
    def inc(self):
        if self.__value>self.__max:
            logger.warning('Fused')
            exit(0)
        self.__value+=1
        return self
    def reset(self):
        logger.debug(f'Fuse {self.__value}')
        self.__value=0
        return self
fuse=Fuse()
def acquireLock(func):
    def wrapper(self,*args,**kwargs):
        while self.lock:time.sleep(.05)
        verifyFlag()
        self.lock=True
        try:return func(self,*args,**kwargs)
        finally:self.lock=False
    return wrapper
class Base(Android):
    def __init__(self,serialno=None):
        if serialno is None:
            self.serialno=None
            return
        self.lock=False
        try:super().__init__(serialno,cap_method=CAP_METHOD.JAVACAP,ori_method=ORI_METHOD.ADB)#,touch_method=TOUCH_METHOD.ADBTOUCH)
        except:self.serialno=None
        else:
            self.render=[round(i)for i in self.get_render_resolution(True)]
            if self.render[2]*9>self.render[3]*16:
                self.scale=1080/self.render[3]
                self.border=(round(self.render[2]-self.render[3]*16/9)>>1,0)
            else:
                self.scale=1920/self.render[2]
                self.border=(0,round(self.render[3]-self.render[2]*9/16)>>1)
            self.key={c:[round(p[i]/self.scale+self.border[i]+self.render[i])for i in range(2)]for c,p in{
                '\x70':(790,74),'\x71':(828,74),'\x72':(866,74),'\x73':(903,74),'\x74':(940,74),'\x75':(978,74),'\x76':(1016,74),'\x77':(1053,74),'\x78':(1091,74),'\x79':(1128,74),#VK_F1..10
                '1':(277,640),'2':(648,640),'3':(974,640),'4':(1262,640),'5':(1651,640),'6':(646,304),'7':(976,304),'8':(1267,304),'0':(1819,367),
                'Q':(1800,475),'W':(1360,475),'E':(1493,475),'R':(1626,475),'T':(210,540),'Y':(510,540),'U':(810,540),'I':(1110,540),'O':(1410,540),'P':(1710,540),'\xDC':(1880,40),#\ VK_OEM_5
                'A':(109,860),'S':(244,860),'D':(385,860),'F':(582,860),'G':(724,860),'H':(861,860),'J':(1056,860),'K':(1201,860),'L':(1336,860),'\xBA':(1247,197),#; VK_OEM_1
                'Z':(960,943),'X':(259,932),'B':(495,480),'N':(248,1041),'M':(1200,1000),
                ' ':(1820,1030),
                '\x64':(70,221),'\x65':(427,221),'\x66':(791,221),'\x67':(70,69),'\x68':(427,69),'\x69':(791,69),#VK-NUMPAD4..9
                }.items()}
    @acquireLock
    def touch(self,p):super().touch([round(p[i]/self.scale+self.border[i]+self.render[i])for i in range(2)])
    @acquireLock
    #def swipe(self,rect,duration=.15,steps=2,fingers=1):super().swipe(*[[round(rect[i<<1|j]/self.scale)+self.border[j]+self.render[j]for j in range(2)]for i in range(2)],duration,steps,fingers)
    def swipe(self,rect):#if this dosen't work, use the above one instead
        p1,p2=[numpy.array(self._touch_point_by_orientation([rect[i<<1|j]/self.scale+self.border[j]+self.render[j]for j in range(2)]))for i in range(2)]
        vd=p2-p1
        lvd=numpy.linalg.norm(vd)
        vd*=5/lvd/self.scale
        vx=numpy.array([0.,0.])
        getPos=lambda x:' '.join([str(int(i))for i in self.minitouch.transform_xy(*x)])
        self.minitouch.safe_send('d 0 '+getPos(p1)+' 50\nc\n')
        time.sleep(.01)
        for _ in range(2):
            self.minitouch.safe_send('m 0 '+getPos(p1+vx)+' 50\nc\n')
            vx+=vd
            time.sleep(.02)
        vd*=5
        while numpy.linalg.norm(vx)<lvd:
            self.minitouch.safe_send('m 0 '+getPos(p1+vx)+' 50\nc\n')
            vx+=vd
            time.sleep(.008)
        self.minitouch.safe_send('m 0 '+getPos(p2)+' 50\nc\n')
        time.sleep(.35)
        self.minitouch.safe_send('u 0\nc\n')
        time.sleep(.02)
    @acquireLock
    def press(self,c):super().touch(self.key[c])
    @acquireLock
    def snapshot(self):return cv2.resize(super().snapshot()[self.render[1]+self.border[1]:self.render[1]+self.render[3]-self.border[1],self.render[0]+self.border[0]:self.render[0]+self.render[2]-self.border[0]],(1920,1080),interpolation=cv2.INTER_CUBIC)
base=Base()
def doit(pos,wait):[(base.press(i),sleep(j*.001))for i,j in zip(pos,wait)]
class Check:
    def __init__(self,forwordLagency=.01,backwordLagency=0):
        sleep(forwordLagency)
        fuse.inc()
        self.im=base.snapshot()
        global check
        check=self
        sleep(backwordLagency)
    def compare(self,img,rect=(0,0,1920,1080),delta=.05):return cv2.minMaxLoc(cv2.matchTemplate(self.im[rect[1]:rect[3],rect[0]:rect[2]],img,cv2.TM_SQDIFF_NORMED))[0]<delta and fuse.reset()
    def select(self,img,rect=(0,0,1920,1080)):return(lambda x:x.index(min(x)))([cv2.minMaxLoc(cv2.matchTemplate(self.im[rect[1]:rect[3],rect[0]:rect[2]],i,cv2.TM_SQDIFF_NORMED))[0]for i in img])
    def tapOnCmp(self,img,rect=(0,0,1920,1080),delta=.05):return(lambda loc:loc[0]<delta and(base.touch((rect[0]+loc[2][0]+(img.shape[1]>>1),rect[1]+loc[2][1]+(img.shape[0]>>1))),fuse.reset())[1])(cv2.minMaxLoc(cv2.matchTemplate(self.im[rect[1]:rect[3],rect[0]:rect[2]],img,cv2.TM_SQDIFF_NORMED)))
    def save(self,name=''):cv2.imwrite(time.strftime('%Y-%m-%d_%H.%M.%S',time.localtime())+'.jpg'if name==''else name,self.im);return self
    def show(self):show(cv2.resize(self.im,(0,0),None,.4,.4,cv2.INTER_NEAREST));return self
    def isAddFriend(self):return self.compare(IMG_END,(243,863,745,982))
    def isApEmpty(self):return self.compare(IMG_APEMPTY,(906,897,1017,967))
    def isBattleBegin(self):return self.compare(IMG_BATTLEBEGIN,(1673,959,1899,1069))
    def isBattleContinue(self):return self.compare(IMG_BATTLECONTINUE,(1072,805,1441,895))
    def isBattleFailed(self):return self.compare(IMG_FAILED,(277,406,712,553))
    def isBattleFinished(self):return(self.compare(IMG_BOUND,(112,250,454,313))or self.compare(IMG_BOUNDUP,(987,485,1468,594)))
    def isBegin(self):return self.compare(IMG_BEGIN,(1630,950,1919,1079))
    def isChooseFriend(self):return self.compare(IMG_CHOOSEFRIEND,(1628,314,1772,390))
    def isGacha(self):return self.compare(IMG_GACHA,(973,960,1312,1052))
    def isHouguReady(self):return(lambda im:[not any(self.compare(j,(470+346*i,258,768+346*i,387),.3)for j in(IMG_HOUGUSEALED,IMG_CARDSEALED))and(numpy.mean(self.im[1014:1021,217+480*i:235+480*i])>90or numpy.mean(im[1014:1021,217+480*i:235+480*i])>90)for i in range(3)])(Check(.7).im)
    def isListEnd(self,pos):return any(self.compare(i,(pos[0]-35,pos[1]-29,pos[0]+35,pos[1]+10),.15)for i in(IMG_LISTEND,IMG_LISTNONE))
    def isNoFriend(self):return self.compare(IMG_NOFRIEND,(369,545,1552,797),.1)
    def isSkillReady(self):return[[not self.compare(IMG_STILL,(65+480*i+141*j,895,107+480*i+141*j,927),.1)for j in range(3)]for i in range(3)]
    def isTurnBegin(self):return self.compare(IMG_ATTACK,(1567,932,1835,1064))
    def getABQ(self):return[-1if self.compare(IMG_CARDSEALED,(43+386*i,667,345+386*i,845),.3)else(lambda x:x.index(max(x)))([numpy.mean(self.im[771:919,108+386*i:318+386*i,j])for j in(2,1,0)])for i in range(5)]
    def getPartyIndex(self):return cv2.minMaxLoc(cv2.matchTemplate(self.im[58:92,768:1152],IMG_PARTYINDEX,cv2.TM_SQDIFF_NORMED))[2][0]//37+1
    def getPortrait(self):return[self.im[640:740,195+480*i:296+480*i]for i in range(3)]
    def getStage(self):return self.select(IMG_STAGE,(1296,20,1342,56))+1
    def getStageTotal(self):return self.select(IMG_STAGETOTAL,(1325,20,1372,56))+1
    def isNextJackpot(self):return self.compare(IMG_JACKPOT,(1556,336,1859,397))
def gacha():
    while fuse.value<30:
        if Check(.1).isGacha():doit('MK',(200,2700))
        base.press('\xDC')
def jackpot():
    while fuse.value<130:
        if Check().isNextJackpot():doit('0JJ',(600,1800,0))
        for _ in range(40):base.press('2')
def chooseFriend():
    refresh=False
    while not Check(.2).isChooseFriend():
        if check.isNoFriend():
            if refresh:sleep(10)
            doit('\xBAJ',(500,1000))
            refresh=True
    if len(IMG_FRIEND)==0:
        time.sleep(.2)
        return base.press('8')
    while True:
        timer=time.time()
        while not Check(.2,.1).isListEnd((1860,1064)):
            for i,_ in(i for i in IMG_FRIEND if check.tapOnCmp(i[1],delta=.015)):
                logger.info(f'Friend {i}')
                try:p=re.search('[0-9x]{11}$',i).group()
                except AttributeError:pass
                else:
                    skillInfo[friendPos]=[[skillInfo[friendPos][i][j]if p[i*3+j]=='x'else int(p[i*3+j])for j in range(3)]for i in range(3)]
                    houguInfo[friendPos]=[houguInfo[friendPos][i]if p[i]=='x'else int(p[i])for i in range(9,11)]
                return
            base.swipe((800,900,800,300))
        if refresh:sleep(max(0,timer+10-time.time()))
        doit('\xBAJ',(500,1000))
        refresh=True
        while not Check(.2).isChooseFriend():
            if check.isNoFriend():
                sleep(10)
                doit('\xBAJ',(500,1000))
def battle():
    turn,stage,stageTurn,servant=0,0,0,[0,1,2]
    while True:
        if Check(.1).isTurnBegin():
            turn+=1
            stage,stageTurn,skill,newPortrait=(lambda chk:(lambda x:[x,stageTurn+1if stage==x else 1])(chk.getStage())+[chk.isSkillReady(),chk.getPortrait()])(Check(.35))
            if turn==1:stageTotal=check.getStageTotal()
            else:servant=(lambda m,p:[m+p.index(i)+1if i in p else servant[i]for i in range(3)])(max(servant),[i for i in range(3)if servant[i]<6and cv2.matchTemplate(newPortrait[i],portrait[i],cv2.TM_SQDIFF_NORMED)[0][0]>=.04])
            if stageTurn==1and dangerPos[stage-1]:doit(('\x69\x68\x67\x66\x65\x64'[dangerPos[stage-1]-1],'\xDC'),(250,500))
            portrait=newPortrait
            logger.info(f'{turn} {stage} {stageTurn} {servant}')
            for i,j in((i,j)for i in range(3)if servant[i]<6for j in range(3)if skill[i][j]and skillInfo[servant[i]][j][0]and stage<<4|stageTurn>=min(skillInfo[servant[i]][j][0],stageTotal)<<4|skillInfo[servant[i]][j][1]):
                doit(('ASD','FGH','JKL')[i][j],(300,))
                if skillInfo[servant[i]][j][2]:doit('234'[skillInfo[servant[i]][j][2]-1],(300,))
                sleep(1.7)
                while not Check(0,.2).isTurnBegin():pass
            for i in(i for i in range(3)if stage==min(masterSkill[i][0],stageTotal)and stageTurn==masterSkill[i][1]):
                doit(('Q','WER'[i]),(300,300))
                if masterSkill[i][2]:
                    if i==2and masterSkill[2][3]:doit(('TYUIOP'[masterSkill[2][2]-1],'TYUIOP'[masterSkill[2][3]-1],'Z'),(300,300,300))
                    else:doit('234'[masterSkill[i][2]-1],(300,))
                sleep(2.3)
                while not Check(0,.2).isTurnBegin():pass
            doit(' ',(2350,))
            doit((lambda c,h:['678'[i]for i in sorted((i for i in range(3)if h[i]),key=lambda x:-houguInfo[servant[x]][1])]+['12345'[i]for i in sorted(range(5),key=(lambda x:c[x]<<1&2|c[x]>>1&1)if any(h)else(lambda x:(c[x]!=-1and c.count(c[x])>=3)<<2|c[x]<<1&2|c[x]>>1&1))])(Check().getABQ(),[servant[i]<6and j and houguInfo[servant[i]][0]and stage>=min(houguInfo[servant[i]][0],stageTotal)for i,j in zip(range(3),check.isHouguReady())]),(270,270,270,270,10000))
        elif check.isBattleFinished():
            logger.info('Battle Finished')
            return True
        elif check.isBattleFailed():
            logger.warning('Battle Failed')
            return False
def main(appleCount=0,appleKind=0,battleFunc=battle):
    apple,battleCount=0,0
    def eatApple():
        nonlocal apple,appleCount
        if Check(.7,.3).isApEmpty():
            if apple==appleCount:
                logger.info('Ap Empty')
                base.press('Z')
                return True
            else:
                apple+=1
                logger.info(f'Apple {apple}')
                doit(('W4K8'[appleKind],'L'),(400,1200))
                return False
    while True:
        while True:
            if Check(.2,.3).isBegin():
                battleCount+=1
                base.press('8')
                if eatApple():return
                chooseFriend()
                while not Check(.1).isBattleBegin():pass
                if partyIndex and check.getPartyIndex()!=partyIndex:doit(('\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79'[partyIndex-1],' '),(1000,400))
                doit(' ',(12000,))
                break
            if check.isBattleContinue():
                battleCount+=1
                base.press('K')
                if eatApple():return
                chooseFriend()
                break
            if check.isAddFriend():base.press('X')
            base.press(' ')
        logger.info(f'Battle {battleCount}')
        if battleFunc():doit('        ',(200,200,200,200,200,200,200,200))
        else:doit('BIJ',(500,500,500))
def userScript():
    while not Check(0,.2).isTurnBegin():pass
    doit('AHJ3L3QE2 654',(3000,3000,350,3000,350,3000,300,350,3000,2400,350,350,10000))
    while not Check(0,.2).isTurnBegin():pass
    assert Check().getStage()==2
    doit('S 654',(3000,2400,350,350,10000))
    while not Check(0,.2).isTurnBegin():pass
    assert Check().getStage()==3
    doit(' 754',(2400,350,350,10000))
    while not Check(0,.2).isBattleOver():pass
    return True
