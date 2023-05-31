# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 15:03:15 2019

@author: Kamada Kouitirou
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:50:10 2019

@author: Kamada Kouitirou
"""

import sys
import copy
import time
import tkinter as tk

## 確定したマスを候補に移す
def input_can(arg_Candidate, arg_board):
    for i in range(9):
        for j in range(9):
            if arg_board[i][j]!='0':
                arg_Candidate[i][j].clear()
                arg_Candidate[i][j].append(arg_board[i][j])

## 横と縦の被りを確認し、候補を減らす
def dec_can_Ver_Hor(arg_Candidate):
    for i in range(9):
        for j in range(9):
            if len(arg_Candidate[i][j])==1:
                for k in range(9):
                    if k!=j:
                        try:
                            arg_Candidate[i][k].remove(arg_Candidate[i][j][0])
                        except ValueError:
                            pass
                for l in range(9):
                    if l!=i:
                        try:
                            arg_Candidate[l][j].remove(arg_Candidate[i][j][0])
                        except ValueError:
                            pass

## 3×3の被りを確認し、候補を減らす
def dec_can_square(arg_Candidate):
    a = [0,1,2]
    b = [3,4,5]
    c = [6,7,8]
    for i in a,b,c:
        for j in a,b,c:
            for k in i:
                for l in j:
                    if len(arg_Candidate[k][l])==1:
                        for m in i:
                            for n in j:
                                if m==k and n==l:
                                    pass
                                else:
                                    try:
                                        arg_Candidate[m][n].remove(arg_Candidate[k][l][0])
                                    except ValueError:
                                        pass

##　2以上で要素が少ないCandidate
def min_Candidate(arg_Candidate):
    min_len = 10
    for i in range(9):
        for j in range(9):
            if min_len > len(arg_Candidate[i][j]) and len(arg_Candidate[i][j])!=1:
                min_len = len(arg_Candidate[i][j])
    min_Candidate_list = []
    for i in range(9):
        for j in range(9):
            if min_len == len(arg_Candidate[i][j]):
                min_Candidate_list.append([i,j])
    return min_Candidate_list[0]

## チェックする
def check(arg_Candidate):
    for i in range(9):
        for j in range(9):
            if len(arg_Candidate[i][j])==0:
                return True
    return False

## 完成しているかをチェックする
def complete_check(arg_Candidate):
    flag = 0
    for i in range(9):
        for j in range(9):
            if len(arg_Candidate[i][j])!=1:
                flag = 1
    if flag == 0:
        return True

## 横と縦の被りと3×3の被りを確認し、候補を減らす
## この作業を候補が変わらなくなるまで繰り返す
def dec_can_repeat(arg_Candidate):
    tmp_Candidate = copy.deepcopy(arg_Candidate)
    dec_can_Ver_Hor(arg_Candidate)
    dec_can_square(arg_Candidate)
    if tmp_Candidate != arg_Candidate:
        dec_can_repeat(arg_Candidate)


## 仮置きして答えを出し、出力する
def Temporary_placement(arg_Candidate, arg_start):
    dec_can_repeat(arg_Candidate)
    if check(arg_Candidate):
        return
    elif complete_check(arg_Candidate):
        for i in range(9):
            for j in range(9):
                txt[i][j].delete(0, tk.END)
                txt[i][j].insert(tk.END, arg_Candidate[i][j][0])
        elapsed_time = time.time() - arg_start
        labelTime = tk.Label(win, text=u"解答時間:{:.2f}".format(elapsed_time) + "[秒]")
        labelTime.place(x='220', y='20')
    tmp_Candidate_01 = copy.deepcopy(arg_Candidate)
    tmp_Candidate_02 = copy.deepcopy(arg_Candidate)
    place = min_Candidate(tmp_Candidate_01)
    for i in tmp_Candidate_02[place[0]][place[1]]:
        tmp_Candidate_01 = copy.deepcopy(tmp_Candidate_02)
        tmp_Candidate_01[place[0]][place[1]] = [i]
        Temporary_placement(tmp_Candidate_01, arg_start)
        

# ボタンを押したときの処理 --- (*1)
def calc_suudoku():
    start = time.time()
    board=[[] for i in range(9)]
    Candidate = [[["1","2","3","4","5","6","7","8","9"] for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            board[i].append(txt[i][j].get())
    input_can(Candidate, board)
    Temporary_placement(Candidate, start)


# ウィンドウを作成 --- (*2)
win = tk.Tk()
win.title("数独solver")
win.geometry("330x200")

# 部品を作成 --- (*3)

txt = [[tk.Entry(width=3) for i in range(9)] for j in range(9)]
for i in range(9):
    for j in range(9):
        txt[i][j].grid(column=j, row=i)
        txt[i][j].insert(tk.END, '0')

calcButton = tk.Button(text=u'解く')
calcButton["command"] = calc_suudoku
calcButton.place(x='220', y='0')


# ウィンドウを動かす
win.mainloop()