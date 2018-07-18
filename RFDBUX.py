#usage: python 20180510_rf.py in_dir out_dir pairlist_name predlist_name NTREES MINNODESIZE Maxlevel COL ROW NV MULTI
import os; import glob; import sys
import numpy as np;
from sklearn.ensemble import RandomForestRegressor
from multiprocessing import Pool

FEATURE=1

def RFDBUX(i,t_pair,s_pair,PAIRS,PREDS,t_pred,NTREES,MINNODESIZE,Maxlevel,NV):
    if(i%100==0):
        print(i)
    r_forest = RandomForestRegressor(
        n_estimators=NTREES,
        criterion='mse',
        max_depth=Maxlevel,
        min_samples_leaf=MINNODESIZE,
        n_jobs=1 #if -1, all cores are used (not recommended)
    )
    s_training=s_pair[i][(s_pair[i]!=NV)&(t_pair[i]!=NV)]
    t_training=t_pair[i][(s_pair[i]!=NV)&(t_pair[i]!=NV)]
    s_pred=np.ones(t_pred.shape[1])*NV
    r_forest.fit(t_training.reshape(t_training.shape[0],FEATURE),s_training) #create pixel i regressor
    for t in range(PREDS):
        if(t_pred[i][t]==NV):
            s_pred[t]=NV
        else:
            s_pred[t]=r_forest.predict(t_pred[i][t])
    return s_pred

def wrapper(args):
    return RFDBUX(*args)

def multi_process(List,MULTI):
    p=Pool(MULTI)
    output=p.map(wrapper,List)
    p.close()
    return output

if __name__ == "__main__":
    argvs=sys.argv; argc=len(argvs)
    if(argc != 12):
        print('usage: python '+__file__+' in_dir out_dir pair.txt pred.txt NTREES MINNODESIZE Maxlevel')
        sys.exit()
    in_dir=os.path.abspath(argvs[1]); out_dir=os.path.abspath(argvs[2]); input=argvs[3]; input2=argvs[4];
    NTREES=int(argvs[5]); MINNODESIZE=int(argvs[6]); Maxlevel=int(argvs[7]);
    COL=int(argvs[8]); ROW=int(argvs[9]); NV=int(argvs[10]); MULTI=int(argvs[11])
    #----------------read match-up pairs-------------------
    with open(input,mode='r') as fp1:
        LINES=len(fp1.readlines())
    with open(input,mode='r') as fp1:
        tmp=fp1.readline().replace('\n','').replace('\r','')
        tname=in_dir+'/'+tmp.split(',')[0]; sname=in_dir+'/'+tmp.split(',')[1]
        with open(sname,mode='rb') as fp2:
            tmp=np.fromfile(fp2,np.int16,ROW*COL)
            s_pair=np.c_[tmp]
        with open(tname,mode='rb') as fp2:
            tmp=np.fromfile(fp2,np.int16,ROW*COL)
            t_pair=np.c_[tmp]
        for i in range(2,LINES+1):
            tmp=fp1.readline().replace('\n','').replace('\r','')
            tname=in_dir+'/'+tmp.split(',')[0]; sname=in_dir+'/'+tmp.split(',')[1]
            with open(sname,mode='rb') as fp2:
                tmp=np.fromfile(fp2,np.int16,ROW*COL)
                s_pair=np.concatenate((s_pair,np.c_[tmp]),axis=1)
            with open(tname,mode='rb') as fp2:
                tmp=np.fromfile(fp2,np.int16,ROW*COL)
                t_pair=np.concatenate((t_pair,np.c_[tmp]),axis=1)
    PAIRS=LINES
    #-----------read prediction input----------------
    with open(input2,mode='r') as fp1:
        LINES=len(fp1.readlines())
    with open(input2,mode='r') as fp1:
        tname=in_dir+'/'+fp1.readline().replace('\n','').replace('\r','').split(',')[0]
        with open(tname,mode='rb') as fp2:
            tmp=np.fromfile(fp2,np.int16,ROW*COL)
            t_pred=np.c_[tmp]
        for i in range(2,LINES+1):
            tname=in_dir+'/'+fp1.readline().replace('\n','').replace('\r','').split(',')[0]
            with open(tname,mode='rb') as fp2:
                tmp=np.fromfile(fp2,np.int16,ROW*COL)
                t_pred=np.concatenate((t_pred,np.c_[tmp]),axis=1)
    PREDS=LINES;
    print('input data loaded! execute RFDBUX...')

    #-----------execute RFDBUX with multiprocessing--------
    List=[(i,t_pair,s_pair,PAIRS,PREDS,t_pred,NTREES,MINNODESIZE,Maxlevel,NV) for i in range(COL*ROW)]
    s_pred=np.array(multi_process(List,MULTI))
    print('RFDBUX completed! write predicted maps...')
    #-----------write predicted maps----------------------
    with open(input2,mode='r') as fp1:
        LINES=len(fp1.readlines())
    with open(input2,mode='r') as fp1:
        for i in range(PREDS):
            sname=out_dir+'/'+fp1.readline().replace('\n','').replace('\r','').split(',')[1]
            make_ENVI_header_file(sname.replace('.raw',''),2)
            with open(sname,mode='wb') as fp2:
                s_pred[:,i].astype('int16').tofile(fp2)

