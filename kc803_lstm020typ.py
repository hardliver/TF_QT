# -*- coding: utf-8 -*-
'''
TopQuant-简称TQ极宽智能量化回溯分析系统，培训课件-配套教学python课件程序

Top极宽量化(原zw量化)，Python量化第一品牌 
by Top极宽·量化开源团队 2017.10.1 首发

网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化1群，124134140
      Top极宽量化2群，650924099
      Top极宽量化3群，450853713
  
'''
#1
import os,arrow
import pandas as pd
import numpy as np
#2
import keras
from keras import initializers,models,layers
from keras.models import Sequential
from keras.layers import Flatten,Dense, Input, Dropout, Embedding,SimpleRNN,Bidirectional,LSTM,Conv1D, GlobalMaxPooling1D,Activation,MaxPooling1D,GlobalAveragePooling1D
from keras.optimizers import RMSprop
from keras.utils import plot_model

#3
import tensorlayer as tl
import tensorflow as tf

#4
import zsys
import ztools as zt
import ztools_str as zstr
import ztools_data as zdat
import ztools_draw as zdr
import ztools_tq as ztq
import zpd_talib as zta
#
import zai_keras as zks

#
#------------------------------------

#1
print('\n#1,set.sys')
pd.set_option('display.width', 450)    
pd.set_option('display.float_format', zt.xfloat3)    
rlog='/ailib/log_tmp'
if os.path.exists(rlog):tf.gfile.DeleteRecursively(rlog)

#2.1
print('\n#2.1,读取数据')
rss,fsgn,ksgn='/ailib/TDS/','TDS2_sz50','avg'
xlst=zsys.TDS_xlst9
zt.prx('xlst',xlst)

#
df_train,df_test,x_train,y_train,x_test, y_test=zdat.frd_TDS(rss,fsgn,ksgn,xlst)
#
df_train,df_test,y_train,y_test=zdat.df_xed_xtyp2x(df_train,df_test,'3',k0=99.5,k9=100.5)
y_train,y_test=pd.get_dummies(df_train['y']).values,pd.get_dummies(df_test['y']).values
#
typ_lst=y_train[0]
num_in,num_out=len(xlst),len(typ_lst)
print('\nnum_in,num_out:',num_in,num_out)
#
print('\ndf_test.tail()')
print(df_test.tail())
print('\nx_train.shape,',x_train.shape)
print('\ntype(x_train),',type(x_train))

#
#2.2
print('\n#2.2,转换数据格式shape')
rxn,txn=x_train.shape[0],x_test.shape[0]
x_train,x_test = x_train.reshape(rxn,num_in,-1),x_test.reshape(txn,num_in,-1)
print('\nx_train.shape,',x_train.shape)
print('\ntype(x_train),',type(x_train))



#3
print('\n#3,model建立神经网络模型')
mx=zks.lstm020typ(num_in,num_out)
#
mx.summary()
plot_model(mx, to_file='tmp/lstm020.png')



#4 模型训练
print('\n#4 模型训练 fit')
tbCallBack = keras.callbacks.TensorBoard(log_dir=rlog,write_graph=True, write_images=True)
tn0=arrow.now()
mx.fit(x_train, y_train, epochs=500, batch_size=512,callbacks=[tbCallBack])
tn=zt.timNSec('',tn0,True)
mx.save('tmp/lstm020.dat')

#5 利用模型进行预测 predict
print('\n#5 模型预测 predict')
tn0=arrow.now()
y_pred0 = mx.predict(x_test)
tn=zt.timNSec('',tn0,True)
y_pred=np.argmax(y_pred0, axis=1)+1
df_test['y_pred']=zdat.ds4x(y_pred,df_test.index,True)
df_test.to_csv('tmp/df_lstm020.csv',index=False)


#6
print('\n#6 acc准确度分析')
df=df_test
dacc,dfx,a10=ztq.ai_acc_xed2ext(df.y,df.y_pred,ky0=10,fgDebug=True)

#4
print('\n#4 acc准确度分类分析')
x1,x2=df['y'].value_counts(),df['y_pred'].value_counts()
zt.prx('x1',x1);zt.prx('x2',x2)


