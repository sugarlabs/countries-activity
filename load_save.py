#load_save.py
import g,ctry

loaded=[] # list of strings

def load(f):
    global loaded
    try:
        for line in f.readlines():
            loaded.append(line)
    except:
        pass

def save(f):
    for c in g.answers:
        f.write(c+'\n')

# note need for rstrip() on strings
def retrieve():
    global loaded
    if len(loaded)>0:
        g.answers=[]; v=65
        for line in loaded:
            lne=line.rstrip()
            g.answers.append(lne)
            if lne!='' and lne!='none': ctry.text(chr(v),lne)
            v+=1


    
