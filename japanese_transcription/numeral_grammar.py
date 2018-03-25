#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import re

ones = {'0': r'rei', '1': 'ichi', '2': 'ni', '3': "san'", '4': 'shi', '5': 'go', '6': 'roku', '7': 'shichi', '8': 'hachi', '9': 'kyuu'}
counters = { '0': r'', '1': 'ichi', '2': 'ni', '3': 'san', '4': 'yon', '5': 'go', '6': 'roku', '7': 'nana', '8': 'hachi', '9': 'kyuu'}
hundreds = { '1': 'hyaku', '2': 'nihyaku', '3': 'sambyaku', '4': 'yonhyaku', '5': 'gohyaku', '6': 'roppyaku', '7': 'nanahyaku', '8': 'happyaku', '9': 'kyuuhyaku'}

def tensgram(j, k):
    if j == '1':
        tensword = ' juu ' + counters[k]

    elif j != '0':
        tensword = counters[j] + ' juu ' + counters[k]
    elif k != '0':
        tensword = counters[k]
    else:
        tensword = ''
    return tensword

def hungram(j, tensword):
    hunlist = []
    if j != '0':
        hunlist = [hundreds[j]]
    if tensword != '':
        hunlist.append(tensword)
    hunsword = ' '.join(hunlist)
    return hunsword

def thougram(j, hunsword):
    thoulist = []
    if j != '0':
        thoulist = [thousands[j]]
        print(thoulist)
    if hunsword != '':
        thoulist.append(hunsword)
    thouword = ' '.join(thoulist)
    return thouword


def numgram(num):
    length = len(num)
    digits = {}
    i = 0
    while (length + i) > 0:
        i -= 1
        if -3 <= i:
            ct = i
            dig = 'hyaku'
        elif -4 <= i < -3:
            ct = i + 3
            dig = 'sen'
            #print(digits, str(ct))
        elif -7 <= i < -4:
            ct = i + 4
            dig = 'man'
            #print(digits)
        elif -9 <= i < -7:
            ct = i + 7
            dig = 'sen man'
        elif -11 <= i < -9:
            ct = i + 9
            dig = 'oku'
        elif -12 <= i < -11:
            ct = i + 11
            dig = 'sen oku'
        elif -15 <= i < -12:
            ct = i + 12
            dig = 'choo'
        #print(str(ct))
        if ct == -1:
            onesdig = num[i]
            if (length == 1): # ones
                if onesdig == '0':
                    onesword = 'rei'
                else:
                    onesword = ones[onesdig]
            elif onesdig == '0':
                onesword = ''
            else:
                onesword = counters[onesdig]
            tensword = onesword
            hunsword = tensword
        elif ct == -2:
            tensdig = num[i]
            tensword = tensgram(tensdig, onesdig)
            hunsword = tensword
        elif ct == -3:
            hunsdig = num[i]
            hunsword = hungram(hunsdig, tensword)

        digits[dig] = hunsword
        #print(digits)
    return digits
            
def decgram(decimal):
    declist = []
    for dec in decimal:
        if dec == '0':
            declist.append('rei')
        else:
            declist.append(ones[dec])
    return(declist)



def get_numeral(num): 
    numwords = num.split(' ')
    #print numwords
    num = str(numwords[0])


    num = re.sub(',', '', num)
    splitondot = num.split('.')
    #print splitondot
    normal = splitondot[0]
    #print normal
    numlist = []
    if re.findall(r'[0-9]', normal):
        digits = numgram(normal)
        for chunk in ['choo', 'billion', 'sen man', 'man', 'sen', 'hyaku']:
            if (chunk in digits.keys()) and (digits[chunk] != ''):
                numlist.append(digits[chunk])
                if chunk != 'hyaku':
                    numlist.append(chunk)

        if (len(splitondot) > 1):
            for item in splitondot[1:]:
                decimal = item
                declist = decgram(decimal)
                numlist.append('ten')
                for decword in declist:
                    numlist.append(decword)


    numeral = [word for word in numlist if (word != '')]
    
    numeral = phon_adjust(' '.join(numeral))
    return numeral  


def phon_adjust(num):
    num = re.sub(r'  ', r' ', num.strip())
    num = re.sub(r'ichi sen', r'issen', num)
    num = re.sub(r'ichi man', r'imman', num)

    return(num)
    

def ordinals(num):
    numeral = get_numeral(num).split(' ')
    #print numeral
    last = numeral.pop(-1)
    if '-' in last:
        hyphened = last.split('-')
        pre = hyphened[0] + '-'
        last = hyphened[1]
    else:
        pre = ''
    if last in trans.keys():
        newlast = trans[last]
    elif last.endswith('y'):
        newlast = re.sub('y', 'ieth', last)
    else:
        newlast = last + 'th'    
    numeral.append(pre + newlast)
    ordnum = ' '.join(numeral)
    return ordnum
    

    
def test_loop():      
    nums = ['10', '343', '3234', '50001', '652001', '54.32', '6,500,504', '75,200,122', '1,000,000', '10,000,000']
    for num in nums: 
        num = str(num)
        if num.endswith('th'):
            num = num.strip('th')
            print(num, ordinals(num))
        else:
            print(num, get_numeral(num))
       
#test_loop()
    

    

#test2()

#ords = ['12', '31', '30', '20', '100', '101', '100000']
#for num in ords: 
    #print get_numeral(num)
 #   ordnum = ordinals(num)
    #print ordnum