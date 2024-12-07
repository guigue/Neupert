import poemas
import numpy as np
from CraamTools.filters import RunningMean as rm

def d29(savefits=False):

    p1 = poemas.Poemas()
    p1.read('SunTrack_131028_210001.TRK',subintegration=False)
    p2 = poemas.Poemas()
    p2.read('SunTrack_131028_220001.TRK',subintegration=False)
    p28=p1+p2

    p1.read('SunTrack_131029_210001.TRK',subintegration=False)
    p2.read('SunTrack_131029_220001.TRK',subintegration=False)
    p29=p1+p2

    bkg = np.interp(p29.data['ms'],p28.data['ms'],p28.data['flux45'])

    p29.data['flux45']-=bkg+20

    f=np.concatenate([p29.data['flux90'][:2735],p29.data['flux90'][3290:]])
    x=np.concatenate([p29.data['ms'][:2735],p29.data['ms'][3290:]])
    par=np.polyfit(x,f,2)
    fit=x**2*par[0]+x*par[1]+par[2]
    ifit=np.interp(p29.data['ms'],x,fit)
    p29.data['flux90']-=(ifit+30)

    p29.add_history('Flux Background subtracted')
    p29.add_history('Background data 2013-10-28T21:00:01')
    p29.change_level('L1')

    if savefits:
        p29.to_fits()
        
    return p29

def d28(savefits=False):

    p1 = poemas.Poemas()
    p1.read('SunTrack_131028_200001.TRK',subintegration=False)

    p2=poemas.Poemas()
    p2.read('SunTrack_131027_200001.TRK',subintegration=False)

    bkg = rm.rm1d(np.interp(p1.data['ms'],p2.data['ms'],p2.data['flux45']),100,mirror=True)+25

    p1.data['flux45']-=bkg
    p1.data['flux45']=rm.rm1d(p1.data['flux45'],30,mirror=True)
    
    p1.level='L1'
    p1.add_history('Flux Background subtracted')
    p1.add_history('Background data 2013-10-27T20:00:01, smooth out 100 bins')
    p1.add_history('Flux smooth out 30 bins')

    # Unfortunately no flare at 90 GHz. Better to clean the channel
    p1.data['flux90']=np.zeros(p1.data['flux90'].shape[0])

    p1.add_history('Flux 90 GHz erased')

    if savefits:
        p1.to_fits()

    return p1

    






    

    
