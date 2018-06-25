# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 14:45:17 2018

@author: jhs
"""
import pickle




def toPkl(pklData,savePath):
    '''序列化变量后保存为pkl'''
    tmpFile = open(savePath,'wb')
    pickle.dump(pklData, tmpFile)
    tmpFile.close()
    

def readPkl(PklPath):
    '''读取pkl文件'''
    tmpFile = open(PklPath,'rb')
    loadData = pickle.load(tmpFile)
    tmpFile.close()
    return loadData