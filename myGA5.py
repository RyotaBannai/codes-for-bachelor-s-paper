# -*- coding: utf-8 -*-
'''
Genetic Algorithm 
- makes new cuisine recipe
- text_w1.txt and text_w2.txt are in roles of data of weights in hidden layers
- text_w1.txt and text_w2.txt are made beforehand in MyMlp.py file
- keyword.txt is list of ingredients
 '''
##############################
import sklearn.datasets
import numpy as np
import mysql.connector
import os
import tempfile
import sys
import re
import random
import numpy
from numba import double
from numba.decorators import jit
import time

###define
Gene = 1 #世代数
Mutations = 0
Count_Of_Id = 0
Count_Of_Ingre = 0
Count_Of_Mutation = 0
Ingre_Replace_List = []
New_Recipe = []

###重みw1ファイル読み込み
f = open('text_w1.txt')
wei = f.read()
f.close()
weight1 = wei.replace('\n',',')
weight1 = weight1.split(',')
del weight1[-1]

###重みw2ファイル読み込み
f = open('text_w2.txt')
wei = f.read()
f.close()
weight2 = wei.split(',')

###食材リストを読み込み
f = open('keyword.txt')
ing = f.read()
f.close()
ingre = ing.split('\n')
Count_Of_Ingre = len(ingre) + 1 

NUM_INPUT = Count_Of_Ingre
NUM_HIDDEN = NUM_INPUT
NUM_OUTPUT = 1

###w1を形成
w1 = np.zeros(NUM_INPUT * NUM_HIDDEN)
for num ,wgt in enumerate(weight1):
    #print num,wgt
    np.put(w1, num,wgt)
    w1 = w1.reshape(NUM_INPUT , NUM_HIDDEN)
###w2を形成
w2 = np.zeros(1 * NUM_HIDDEN)
for num ,wgt in enumerate(weight2):
    np.put(w2, num ,wgt)
    w2 = w2.reshape(1 , NUM_HIDDEN)

#@jit
def output(x):#評価
    
    """レシピの評価関数"""
    
    start = time.time() #時間測定#start
    
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
    elapsed_time = time.time() - start #時間測定end
    print (elapsed_time)
    return y

def crossover(recipe_dic):

    '''新しいレシピ群を二次元配列にしてreturn'''

    Child_Recipe_Dic = []
    count = 0
    while count < int(Count_Of_Id/2) :
        #crossoverする2つのレシピをランダムで選択する
        Parent_Of_Crossover_1 = random.randint(0, int((Count_Of_Id-1)/2))
        Parent_Of_Crossover_2 = random.randint(0, int((Count_Of_Id-1)/2))
        ###print (Parent_Of_Crossover_1,Parent_Of_Crossover_2)
        #Ingre_Index_Parent1 = np.where(recipe_dic[Parent_Of_Crossover_1] == 1)[0]
        #Ingre_Index_Parent2 = np.where(recipe_dic[Parent_Of_Crossover_2] == 1)[0]
        Child_Recipe = np.zeros(Count_Of_Ingre)
        #親のレシピのどっちを先に読み込むかを決める
        ran = random.randint(0, 2) #1.0 <= x < 2.0
#作成中sakuseichuu
        for count in range(0, int(Count_Of_Ingre/2)):
            if recipe_dic[Parent_Of_Crossover_1][]
        np.put(Child_Recipe, Ingre_Index_Parent1[index] ,1)      
        Child_Recipe_Dic.append(Child_Recipe)
        count += 1
        ###print ('Child_Recipe_Dic ',Child_Recipe_Dic)
    return Child_Recipe_Dic

def mutation_preReserch(recipe_dic):
    
    '''
    ---先行研究のmutation--- 
    ・ランダムに選択した食材1つをレシピに追加
    ・レシピから食材1つを消去
    ・レシピから食材１をランダムに選択した食材1つと入れ替える
    '''
    
    Mutations = random.randint(0, Count_Of_Id)#mutationを行う回数を決める 
    for num in range(0 , Mutations):
        ran = random.randint(0, Count_Of_Id -1)#mutationを行うレシピをランダムで決める
        change_operation = random.randint(1, 3)
        if change_operation == 2 : 
            recipe_dic[ran] = add_ingredient(recipe_dic[ran])
        elif change_operation ==1 : 
            recipe_dic[ran] = remove_ingredient(recipe_dic[ran])
        elif change_operation ==3 : 
            recipe_dic[ran] = replace_ingredient(recipe_dic[ran])
    return recipe_dic

def add_ingredient(recipe):
    
    '''ランダムに選択した食材1つをレシピに追加'''
    
    print ('Hey add_ingredient')
    ran = random.randint(0, Count_Of_Ingre -1)
    np.put(recipe, ran ,1)
    return recipe

def remove_ingredient(recipe):
    
    '''レシピから食材1つを消去'''
    
    print ('Hey remove_ingredient')
    indexIsOne = np.where(recipe == 1)[0]
    if 0 < len(indexIsOne) :
        ran = random.randint(0, len(np.where(recipe == 1)[0])-1)
        np.put(recipe, np.where(recipe == 1)[0][ran] ,0)
    return recipe

def replace_ingredient(recipe):
    
    '''レシピから食材１をランダムに選択した食材1つと入れ替える'''
    
    print ('Hey replace_ingredient')
    ran = random.randint(0, Count_Of_Ingre -1)#追加
    np.put(recipe, ran ,1)
    
    indexIsOne = np.where(recipe == 1)[0]#消去
    if 0 < len(indexIsOne) :
        ran = random.randint(0, len(np.where(recipe == 1)[0])-1)
        np.put(recipe, np.where(recipe == 1)[0][ran] ,0)
    return recipe

def mutation_overwrite(recipe_dic):

    '''新しいレシピ群を二次元配列にしてreturn'''
    
    Mutations = random.randint(0, Count_Of_Id)#mutationを行う回数を決める #1.0 <= x <= Count_Of_Id 
    for num in range(0 , Mutations):
        ran = random.randint(0, Count_Of_Id -1)#mutationを行うレシピをランダムで決める #インデスク0からはじまるため-1
        recipe_dic[ran] = replace_ingredients(recipe_dic[ran])
    return recipe_dic

def mutation(recipe_dic):
    
    '''新しいレシピ群を二次元配列にしてreturn'''
    
    global Mutations
    global New_Recipe
    New_Recipe = []
    Mutations = random.randint(0, int(Count_Of_Id/2))#mutationを行う回数を決める
    for num in range(0 , Mutations):
        ran = random.randint(0, int(Count_Of_Id/2) -1)#mutationを行うレシピをランダムで決める
        New_Recipe.append(replace_ingredients(recipe_dic[ran]))
    return New_Recipe

def ingre_to_index(ingredients): 
    
    '''食材をindex番号にして返す なければNone'''
    
    for i,word in enumerate(All_ingredients):
        if ingredients == word:
            return i
    return 'None'


def make_Ingre_Replace_List():
    
    '''食材代用リストを辞書として作成'''
    
    global Ingre_Replace_List
    f = open('/Users/ryotabannai/Desktop/replaceList.txt')#仮のファイル
    data1 = f.read()
    f.close()
    lines1 = data1.split('\n')
    #del lines1[-1]
    for num in range(0, len(lines1)):
        Ingre_Replace_List.append(lines1[num].split(','))
        Ingre_Replace_List[num][0] = ingre_to_index(Ingre_Replace_List[num][0])
        Ingre_Replace_List[num][1] = ingre_to_index(Ingre_Replace_List[num][1])
    print (Ingre_Replace_List)

def replace_ingredients(recipe):

    '''1つのレシピの食材をランダムに入れ替える'''

    ran = 0;
    Count_Of_Ingredient = len(np.where(recipe == 1)[0])#食材の数を把握
    #print ('Count_Of_Ingredient',Count_Of_Ingredient)
    Count_Of_Replace = random.randint(0, Count_Of_Ingredient)#1つのレシピの食材のうち何個(回)入れ替えるかランダムで決める
    for num in range(0, Count_Of_Replace):
        ran = random.randint(0, Count_Of_Ingredient)
        
        list1 = list(filter(lambda x:x[0] == recipe_Ingredients[ran],Ingre_Replace_List))
        if len(list1) > 1:
            ran_lis1 = random.randint(1, len(list1))
        else :
            ran_lis1 = 1
        if len(list1) > 0 and list1[ran_lis1 - 1][1] != 'None':
            np.put(recipe,list1[ran_list1 - 1][0],0)
            np.put(recipe,list1[ran_list1 - 1][1],1)
            
        list2 = list(filter(lambda x:x[1] == recipe_Ingredients[ran],Ingre_Replace_List))
        if len(list2) > 1:
            ran_lis2 = random.randint(1, len(list2))
        else :
            ran_lis2 = 1
        if len(list2) >0 and list2[ran_lis2-1][1] != 'None':
            np.put(recipe,list2[ran_list2 - 1][1],0)
            np.put(recipe,list2[ran_list2 - 1][0],1)       
    return recipe

def deisplay_contentOf_recipe(recipe):
    
    '''生成後のレシピの食材を表示するた'''
    
    content = []
    indexIsOne = np.where(recipe == 1)[0]
    for index in indexIsOne:
        try:
            content.append(All_ingredients[index])
        except:
            pass
    print (content)
@jit
def evaluation(generatedRecipe):
    
    '''
    最終評価
    どれくらい既存レシピを生成することができたかを評価
    '''
    match_count = 0
    GeneratdRecipe_Indexes = []
    Recipe_Indexes = []
    Temp_Indexes = []
    ID_evaluation = []
    connector = mysql.connector.connect(host="localhost",db="cookpad_data", user="root", charset="utf8")
    cursor = connector.cursor()
    sql = "SELECT id FROM recipes WHERE title LIKE '%鍋';"
    cursor.execute(sql)
    i_d = cursor.fetchall()
    Count_Of_Id_evaluation = int(len(i_d)/2)
    for count in range (Count_Of_Id_evaluation, len(i_d)):
        print ('evaluation count is :',count)
        ID_evaluation.append(i_d[count][0].encode('utf-8'))
    for outer in range(0, Count_Of_Id_evaluation):
        sql = "select name from recipes_new where recipe_id ='" + ID_evaluation[outer].decode('utf-8')+ "';"
        cursor.execute(sql)
        ingredients = cursor.fetchall()
        for middle in range(0, len(ingredients)):
            for inner in range(0 , len(All_ingredients)):
                if(ingredients[middle][0] == All_ingredients[inner]):
                    Temp_Indexes.append(inner)
        Recipe_Indexes.append(Temp_Indexes)
        Temp_Indexes = []
    cursor.close()
    connector.close()    
    #生成したレシピの食材をインデクスにして二次元配列にしておく
    for recipe in generatedRecipe:
        GeneratdRecipe_Indexes.append(np.where(recipe == 1)[0])
    #実際の評価
    for Grecipe in GeneratdRecipe_Indexes:
        for Arecipe in Recipe_Indexes:
            print (set(Grecipe), set(Arecipe))
            if set(Grecipe) == set(Arecipe):#この機能且つもしも1つのレシピに同じ食材が含まれていても重複を削る
                match_count += 1
    return match_count


if __name__ == "__main__":
    
    ###入力データ作成
    global Count_Of_Id
    global Count_Of_Ingre
    connector = mysql.connector.connect(host="localhost",db="cookpad_data", user="root", charset="utf8")
    cursor = connector.cursor()
	###鍋レシピのIDを全て取得
    sql = "SELECT id FROM recipes WHERE title LIKE '%鍋' LIMIT 6;"
    cursor.execute(sql)
    i_d = cursor.fetchall()
    cursor.close()
    connector.close()
    
    All_ID=[]
    All_ingredients=[]
    Count_Of_Id = len(i_d)
    for ing in ingre:
        All_ingredients.append(ing) #encodeしといたほうがのちのち楽
    for count in range (0, Count_Of_Id):
        All_ID.append(i_d[count][0].encode('utf-8'))
        
    make_Ingre_Replace_List()#食材台用リストを作成
    
    input_data = np.zeros(Count_Of_Id*Count_Of_Ingre)#.reshape(Count_Of_Ingre,1)#行列作成
    connector = mysql.connector.connect(host="localhost", db="cookpad_data", user="root", charset="utf8")
    cursor = connector.cursor()
    for outer in range(0, Count_Of_Id):
        sql = "select name from recipes_new where recipe_id ='" + All_ID[outer].decode('utf-8')+ "';"
        cursor.execute(sql)
        ingredients = cursor.fetchall()
        for middle in range(0, len(ingredients)):
            for inner in range(0 , len(All_ingredients)):
                if(ingredients[middle][0] == All_ingredients[inner]):
                    np.put(input_data,outer * Count_Of_Ingre + inner,1)
    cursor.close()
    connector.close()
    ###入力データ
    input_data = input_data.reshape(Count_Of_Id , Count_Of_Ingre) #最後にmultidemensinal

    ###GA-main-
    count = 0
    while count <= Gene:
        result = {}
        try : #初めはoutput_dataが宣言されていないかつ初めだけinputをからで初期化しないように。
            input_data = output_data
        except :
            pass
        output_data = []
        for n in range(0, Count_Of_Id):
            print(n, '個目のレシピを評価中', sep=",")
            result.update({n : output(input_data[n])[0]})    #連想配列で挿入
        result = sorted(result.items(), key=lambda x:x[1])   #評価が低い順に並び替え
        for num, data in result:
            output_data.append(input_data[num])           #評価が低いレシピ順に格納
        temp_result = output_data                         #一時的に保管
        output_data = output_data[int(Count_Of_Id/2) : Count_Of_Id : 1]      #評価の高い上位半分を取り出す(スライス)

        #crossover
        '''
        after_crossover = crossover(output_data)
        output_data.extend(after_crossover)
        #output_data = mutation_overwrite(output_data) #1.自分の研究にcrossoverを適用する時のmutation
        output_data = mutation_preReserch(output_data) #2.先行研究のmutation
        for recipe in output_data:
            deisplay_contentOf_recipe(recipe)
        '''
        
        #mutation 3.置き換え可能食材のみの手法で行った研究
        after_mutation = mutation(output_data)        #自分の研究のmutation
        count_of_reuse_under = int(Count_Of_Id/2) - Mutations  #同じ数に戻すために必要なレシピを確保
        temp_result[int(Count_Of_Id/2) - count_of_reuse_under : int(Count_Of_Id/2) : 1]
        output_data.extend(temp_result)                        #評価の高いレシピのみを残したレシピ群
        for i,word in enumerate(after_mutation):
            output_data.append(word)
        for recipe in output_data:
            deisplay_contentOf_recipe(recipe)
        count += 1
    print (evaluation(output_data))#最終的な評価