# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:50:10 2019

@author: Kamada Kouitirou
"""

import sys
import copy
import time

## 入力を二次元配列のリストにする
lst = input()
board = [[] for i in range(9)]
cnt = 0
for c in lst:
    if c in ".0123456789":
        if c == ".":
            c = "0"
        if len(board[cnt])==9:
            cnt+=1
            board[cnt].append(c)
        else:
            board[cnt].append(c)

## 候補のリスト
Candidate = [[["1","2","3","4","5","6","7","8","9"] for i in range(9)] for j in range(9)]

## 確定したマスを候補に移す
def input_can(arg_Candidate, arg_board):
    for i in range(9):
        for j in range(9):
            if board[i][j]!='0':
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

## Candidateから答えを出力する
def print_ans(arg_Candidate):
    for i in range(9):
        for j in range(9):
            tmp = arg_Candidate[i][j][0]
            print(f" {tmp}",end="")
        print()

## 仮置きして答えを出し、出力する
def Temporary_placement(arg_Candidate):
    dec_can_repeat(arg_Candidate)
    if check(arg_Candidate):
        return
    elif complete_check(arg_Candidate):
        print_ans(arg_Candidate)
        elapsed_time = time.time() - start
        print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
        sys.exit()
    tmp_Candidate_01 = copy.deepcopy(arg_Candidate)
    tmp_Candidate_02 = copy.deepcopy(arg_Candidate)
    place = min_Candidate(tmp_Candidate_01)
    for i in tmp_Candidate_02[place[0]][place[1]]:
        tmp_Candidate_01 = copy.deepcopy(tmp_Candidate_02)
        tmp_Candidate_01[place[0]][place[1]] = [i]
        Temporary_placement(tmp_Candidate_01)

start = time.time()
input_can(Candidate, board)
Temporary_placement(Candidate)
elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")