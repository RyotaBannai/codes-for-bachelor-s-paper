#coding:utf-8
'''
Teaching machine
- Decide each weight under hidden layers
- this time only 2 hidden layers 
- write out all weights into two text files
- which two files will be used in myGA.py file to judge what combination of foods would be good(user review in Tukurepo)
'''
import sklearn.datasets
import scipy as sp
import numpy as np
import mysql.connector
import os
import tempfile
import sys
import re
import pylab
import time
from numba import double
from numba.decorators import jit
#####入力データ作成#####

@jit
def machineLeaning(w1,w2,xlist):
    start = time.time() #時間測定#start
    # 隠れ層と出力層の出力配列を確保
    z = np.zeros(NUM_HIDDEN)
    y = np.zeros(NUM_OUTPUT)

    # 誤差（delta）の配列を確保
    d1 = np.zeros(NUM_HIDDEN)
    d2 = np.zeros(NUM_OUTPUT)

    # 訓練データにバイアスの1を先頭に挿入
    x = np.array([xlist[n]]) 
    x = np.insert(x, 0, 1) 
    
    # 順伝播により隠れ層の出力を計算
    for j in range(NUM_HIDDEN):
        # 入力層にはバイアスの1が先頭に入るので注意
        a = np.zeros(NUM_HIDDEN)
        for i in range(NUM_INPUT):
            a[j] += w1[j, i] * x[i]
        z[j] = np.tanh(a[j])

    # 順伝播により出力層の出力を計算
    for k in range(NUM_OUTPUT):
        for j in range(NUM_HIDDEN):
            y[k] += w2[k,j] * z[j]
            
    # 出力層の誤差を評価
    for k in range(NUM_OUTPUT):
        d2[k] = y[k] - tlist[n, k]
        #print 'y[k]', y[k]
    # 出力層の誤差を逆伝播させ、隠れ層の誤差を計算
    for j in range(NUM_HIDDEN):
        temp = 0.0
        for k in range(NUM_OUTPUT):
            temp += w2[k, j] * d2[k]
            ##print 'temp is ',temp
            ##print w2[k, j]
        d1[j] = (1 - z[j] * z[j]) * temp
        
    # 第1層の重みを更新　# ここで重みを更新している
    for j in range(NUM_HIDDEN):
        for i in range(NUM_INPUT):
            w1[j, i] -= ETA * d1[j] * x[i] #ETAは学習率
    
    # 第2層の重みを更新　# ここで重みを更新している
    for k in range(NUM_OUTPUT):
        for j in range(NUM_HIDDEN):
            w2[k, j] -= ETA * d2[k] * z[j]

    print (w1 ,w2,sep=',')
    elapsed_time = time.time() - start #時間測定end
    print (elapsed_time)

    return (w1, w2)

#@jit
def output(x,w1,w2):#評価
    
    """レシピの評価関数"""
    
    start = time.time() # time measuring
    
    # 配列に変換して先頭にバイアスの1を挿入
    x = np.insert(x, 0, 1)
    z = np.zeros(NUM_HIDDEN)
    y = np.zeros(NUM_OUTPUT)
    # 順伝播で出力を計算
    for j in range(NUM_HIDDEN):
        a = np.zeros(NUM_HIDDEN)
        for i in range(NUM_INPUT):
            a[j] += w1[j, i] * x[i]
        z[j] = np.tanh(a[j])
    for k in range(NUM_OUTPUT):
        for j in range(NUM_HIDDEN):
            y[k] += w2[k, j] * z[j]
    #[y[k] + w2[k, j] * z[j] for k in range(NUM_OUTPUT) for j in range(NUM_HIDDEN)]
    
    elapsed_time = time.time() - start #時間測定end
    print (elapsed_time)
    return y

f = open('/Users/ryotabannai/Desktop/key4.txt')
ing = f.read()
f.close()
ingre = ing.split('\n')

connector = mysql.connector.connect(host="localhost", db="cookpad_data", user="root", charset="utf8")
cursor = connector.cursor()
###鍋レシピの食材を全て取得###
##ingre_sql = "select name from soup_Not_override_ingredients;" # limit 100
##cursor.execute(ingre_sql)
##ingre = cursor.fetchall()
###鍋レシピのIDを全て取得###
i_d_sql = "select id from recipes where title like '%鍋' limit 2500;" #limit 100
cursor.execute(i_d_sql)
i_d = cursor.fetchall()
cursor.close()
connector.close()
#####始めの処理######
All_ID=[]
All_ingredients=[]
Count_Of_Id = len(i_d)
Count_Of_Ingre = len(ingre)
print (Count_Of_Ingre)
for count in range (0, Count_Of_Ingre):
    All_ingredients.append(ingre[count]) #encodeしといたほうがのちのち楽 #keywoed.txtを使う分には初めからok
for count in range (0, Count_Of_Id):
    All_ID.append(i_d[count][0].encode('utf-8'))#食材indexをハッシュっぽく使う

input_data = np.zeros(Count_Of_Id*Count_Of_Ingre)#.reshape(Count_Of_Ingre,1)#行列作成

connector = mysql.connector.connect(host="localhost", db="cookpad_data", user="root", charset="utf8")
cursor = connector.cursor()

for outer in range(0, Count_Of_Id):
    print ('inputデータ作成中',outer,'/',Count_Of_Id,sep=',')
    sql = "select name from recipes_new3 where recipe_id ='" + All_ID[outer].decode('utf-8')+ "';"
    cursor.execute(sql)
    ingredients = cursor.fetchall()
    for middle in range(0, len(ingredients)):
        for inner in range(0 , len(All_ingredients)):
            if(ingredients[middle][0] == All_ingredients[inner]):
                np.put(input_data,outer * Count_Of_Ingre + inner,1)
            #if type(ingredients[middle][0]) == unicode:
                #if type(All_ingredients[inner]) == unicode :
                    #if(ingredients[middle][0].encode('utf-8') == All_ingredients[inner].encode('utf-8')):
                        #np.put(input_data,outer * Count_Of_Ingre + inner,1)
                #else:
                    #if(ingredients[middle][0].encode('utf-8') == All_ingredients[inner]):
                        #np.put(input_data,outer * Count_Of_Ingre + inner,1)
            #else:
                #if(ingredients[middle][0] == All_ingredients[inner].encode('utf-8')):
                    #np.put(input_data,outer * Count_Of_Ingre + inner,1)

cursor.close()
connector.close()
#入力データ完成
input_data = input_data.reshape(Count_Of_Id , Count_Of_Ingre) #最後にmultidemensinal

######教師データ作成######

teacher_data = np.zeros(Count_Of_Id).reshape(Count_Of_Id,1)
#teacher_data = np.linspace(0.1, 0.1, 100).reshape(100,1)

connector = mysql.connector.connect(host="localhost", db="cookpad_data", user="root", charset="utf8")
cursor = connector.cursor()
for count in range (0, Count_Of_Id) :
    print ('teacharデータ作成中',count,'/',len(All_ID),sep=',')
    sql = "select * from tsukurepos where recipe_id = '" + All_ID[count].decode('utf-8') + "';"
    cursor.execute(sql)
    result = cursor.fetchall()
    if(len(result)>0):
        np.put(teacher_data, count ,1)
    else :
        pass
cursor.close()
connector.close()

#learning settings

N = Count_Of_Id                      # 訓練データ数 # DBから取り出したレシピID数に応じる
ETA = 0.0001                         # leareing rate
NUM_LOOP = 10                        # loop counts
NUM_INPUT = Count_Of_Ingre + 1       # input layer + bias 
NUM_HIDDEN = NUM_INPUT               # hidden layer, same as input layer
NUM_OUTPUT = 1                       # the number of output

def sum_of_squares_error(xlist, tlist, w1, w2):
    """二乗誤差和を計算する"""
    error = 0.0
    for n in range(N):
        print ('sum_of_squares_error 第一 roop',n,sep=',')
        z = np.zeros(NUM_HIDDEN)
        y = np.zeros(NUM_OUTPUT)
        x = np.insert(xlist[n], 0, 1) #insert bias into the beginning 
        # 順伝播で出力を計算
        for j in range(NUM_HIDDEN):
            a = np.zeros(NUM_HIDDEN)
            for i in range(NUM_INPUT):
                a[j] += w1[j, i] * x[i]
            z[j] = np.tanh(a[j]) # 隠れ層の出力
            
        for k in range(NUM_OUTPUT):
            for j in range(NUM_HIDDEN):
                y[k] += w2[k, j] * z[j]
        # 二乗誤差を計算
        for k in range(NUM_OUTPUT):
            error += 0.5 * (y[k] - tlist[n, k]) * (y[k] - tlist[n, k])
    return error

if __name__ == "__main__":
    xlist = input_data
    tlist = teacher_data
    #print ('Learning starts!')
    
    # Initialize weights at random
    w1 = np.random.random((NUM_HIDDEN, NUM_INPUT))
    w2 = np.random.random((NUM_OUTPUT, NUM_HIDDEN))
    # 二乗誤差和がepsilon以下になったら終了でもOK
    for loop in range(NUM_LOOP): #レシピ数
        print (loop)
        for n in range(len(xlist)): 
            print (n)
            # 訓練データすべてを使って重みを訓練する
            w1, w2 = machineLeaning(w1,w2,xlist)
        np.savetxt('/Users/ryotabannai/Desktop/text_w1.txt', w1, delimiter=',')   # X is an array
        np.savetxt('/Users/ryotabannai/Desktop/text_w2.txt', w2, delimiter=',')

    #print "学習前の二乗誤差:", sum_of_squares_error(xlist, tlist, w1, w2) #ここが時間がかかる @jit    
        # 全データで重み更新後の二乗誤差和を出力
        #print loop, sum_of_squares_error(xlist, tlist, w1, w2)  ここが物凄い時間がかかる!!!!!! @jit

    # 学習後の重みを出力
    #print ("w1:", w1,sep=',')
    #print ("w2:", w2,sep=',')
    #np.savetxt('/Users/ryotabannai/Desktop/text_w1.txt', w1, delimiter=',')   # X is an array
    #np.savetxt('/Users/ryotabannai/Desktop/text_w2.txt', w2, delimiter=',')
    # 訓練データの入力に対する隠れユニットと出力ユニットの出力を計算
    #ylist = np.zeros((N, NUM_OUTPUT))
    #zlist = np.zeros((N, NUM_HIDDEN))
    #for n in range(N):
    #    ylist[n], zlist[n] = output(xlist[n], w1, w2)

