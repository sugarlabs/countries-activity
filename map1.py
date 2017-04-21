#map1.py
import utils,g,os

class Map1:
    def __init__(self):
        self.img=None; self.capital=''; self.xy=None
        self.side=None # calculated after image loaded
        self.origin=(g.sx(16),g.sy(8))
        self.textxy=(g.sx(16),g.sy(17))

    def setup(self,country):
        self.country=country
        if self.img==None:
            self.img=utils.load_image('map.png')
            self.side=float(self.img.get_width())/360.0
            self.circle=utils.load_image('circle.png',True)
        ln=len(country); capital=''; lat=''; lon=''; self.xy=None
        self.latlon=None
        fname=os.path.join('data','latlon.txt')
        f=open(fname, 'r')
        for line in f.readlines():
            if line[:ln]==country:
                c,self.capital,lat,lon=line.rstrip().split(','); break
        if lat!='':
            self.latlon='Latitude: '+lat_deg(lat)
            self.latlon+='  Longitude: '+lon_deg(lon)
            lat=float(lat); lon=float(lon); x0,y0=self.origin
            x=lon*self.side+x0; x=int(x)
            y=y0-lat*self.side; y=int(y)
            self.xy=(x,y)

    def draw(self):
        g.screen.fill(utils.BLACK)
        g.screen.blit(self.img,(g.sx(0),0))
        if self.xy!=None: utils.centre_blit(g.screen,self.circle,self.xy)
        s=self.country
        utils.text_blit(g.screen,s,g.font2,self.textxy,utils.CREAM,False)
        x,y=self.textxy
        if self.capital!='':
            s='Capital: '+self.capital
            utils.text_blit(g.screen,s,g.font1,(x,y+g.sy(1.1)),utils.CREAM,False)
        if self.latlon!=None:
            s=self.latlon
            utils.text_blit(g.screen,s,g.font1,(x,y+g.sy(2)),utils.CREAM,False)
        
def lat_deg(lat0):
    lat=abs(float(lat0))
    d=int(lat); m=int((lat-d)*60+.5)
    l='N'; z=''
    if m<10: z='0'
    if float(lat0)<0: l='S'
    s=str(d)+chr(176)+z+str(m)+"'"+l
    return s

def lon_deg(lon0):
    lon=abs(float(lon0))
    d=int(lon); m=int((lon-d)*60+.5)
    l='E'; z=''
    if float(lon0)<0: l='W'
    if m<10: z='0'
    s=str(d)+chr(176)+z+str(m)+"'"+l
    return s



    
