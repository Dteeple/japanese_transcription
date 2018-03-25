#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Input tsv file with [type \t token] (type = word/numeral), Japanese text
# Output phonetic transcription

import re
import csv
import os
import numeral_grammar
import json






dictfolder = './dicts/'

inputfolder = './input/'

# And external data cannot be sent inside the archive. Your solution should include some code to fetch and prepare whatever
#you plan to use, either as a step we should run before executing your solution
#  or dynamically at run time.



def word(token, kanadict):
	trans = ""
	for char in token:
		try:
			trans += kanadict[char]
		except KeyError:
			#print("Not found: {0}".format(char))
			trans += "-"
	trans = re.sub(r'.\-DEL ', r'', trans) #deletes vowel of preceding syllable
	trans = re.sub(r'GEM\-(.)', r'\1\1', trans) # geminates following consonant
	trans = re.sub(r'(.)-LG', r'\1\1', trans) # lengthens preceding vowel
	trans = re.sub(r'NIPPON', r'NIHON', trans) # preferred pron

	return(trans)

def to_json(dictio, jsondict):
	print("Saving dictionary to JSON...")
	with open(jsondict, encoding='utf-8', mode='w') as outfile:
		json.dump(dictio, outfile)
		
def from_json(jsonfile):
	with open(jsonfile, encoding='utf-8', mode='r') as infile:  
		lex_items = json.load(infile)
	return(lex_items)

# to create word translit dictionary, json format
def get_dict_from_txt(dicttxt, dictjson, kanajson):  # http://www.edrdg.org/jmdict/edict.html
	dictdict = {}
	kanadict = from_json(kanajson)
	with open(dicttxt, encoding='utf-8', mode='r') as infile:
		for line in infile:

			linelist = line.strip().split('/')
			try:
				(orth, kana) = linelist[0].split('[')
				orth = orth.strip()
				kana = re.sub(r'\]', r'', kana.strip())
				
			except ValueError:
				orth = linelist[0].strip()
				kana = linelist[0].strip()
			try:
				trans = word(kana, kanadict)
				if trans != "":
					if orth not in dictdict.keys():
						dictdict[orth] = []
					if trans not in dictdict[orth]:
						dictdict[orth].append(trans)
			except KeyError:
				trans = "unk"
			#defin = linelist[1] # who cares
			
	to_json(dictdict, dictjson)
	


#to create kana translation dictionary, json format
def create_kana_dict(kanafile, kanajson): # source:  http://memory.loc.gov/diglib/codetables/9.2.html
	kanadict = {}
	with open(kanafile, encoding='utf-8', mode='r') as infile:
		for row in csv.DictReader(infile, delimiter='\t'):
			char = row['CHAR'].strip()
			#pychar = row['UCS'].strip()
			desc = row['NAME'].strip()
			if re.findall(r'Vowel elongation', desc):
				ph = u'-LG'
			elif re.findall(r'small TSU', desc): # makes following consonant geminate:  GAGEM-KOO -> GAKKOO
				ph = u'GEM-'
			elif re.findall(r'small', desc):
				ph = u'-DEL ' + re.sub(r'.*small ', r'', desc) # DEL indicates deletion of previous vowel TE-DEL I -> TI
			else:
				ph = re.sub(r'.*letter ', r'', desc)
			kanadict[char] = ph
			#kanadict[pychar] = ph
	to_json(kanadict, kanajson)

def create_num_dict(numtxt, numjson): # consulted https://en.wikipedia.org/wiki/Japanese_numerals in creating num dict
	numdict = {}
	with open(numtxt, encoding='utf-8', mode='r') as infile:
		for row in csv.DictReader(infile, delimiter='\t'):
			#rom	sino	on	kun
			rom = row["rom"]
			sino = row["sino"]
			on = row["on"]
			kun = row["kun"]
			if rom not in numdict.keys():
				numdict[rom] = ['rom', on, kun]
			if sino not in numdict.keys():
				numdict[sino] = ['sino', on, kun]
	to_json(numdict, numjson)
	
def create_romaji_dict(romajitxt, romajijson): #  For words like Sony, not in regular dictionary
	romdict = {}
	with open(romajitxt, encoding='utf-8', mode='r') as infile:
		for row in csv.DictReader(infile, delimiter='\t'):
			#rom	sino	on	kun
			orth = row["orth"]
			phon = row["phon"]
			if orth not in romdict.keys():
				romdict[orth] = phon

	to_json(romdict, romajijson)
	


	
def parse_num(num, numdict, kanadict, kanjidict):
	reading = 'on'
	if re.findall(r'[0-9]', num):
		numtype = 'rom'
		num = re.sub(r',', r'', num)
	else:
		numtype = 'sino'
	if re.findall(r'\u3064', num) or re.findall(r'\u4eba', num):
		reading = 'kun'
	parsed_num = ""
	if numtype == 'sino':
		if len(num) == 1:
			parsed_num += numdict[char][1]
		else:
			for char in num:
				try:
					info = numdict[char]
					if reading == 'kun': # in cases where the numeral precedes a counter like TSU or RI (person)
						parsed_num += info[2]
					elif char == u'\u4e03' or char == u'\u56db': # 7 and 4 are weird
						parsed_num += info[2] + " "
					else:
						parsed_num += info[1] + " "
				except KeyError:
					try:
						parsed_num += kanadict[char] + " "
					except KeyError:
						try:
							parsed_num += kanjidict[char] + " "
						except KeyError:
							parsed_num += char + " "
	elif reading == 'kun':
		for char in num:
			try:
				info = numdict[char]		
				parsed_num += info[2]
			except KeyError:
				try:
					parsed_num += kanadict[char]
				except KeyError:
					try:
						parsed_num += kanjidict[char]
					except KeyEror:
						parsed_num += char
	else:
		parsed_num = numeral_grammar.get_numeral(num) # for reading Arabic numerals only
	parsed_num = parsed_num.upper()
	parsed_num = re.sub(r'YONTSU', r'YOTTSU', parsed_num)
	return(parsed_num)



def transliterate(inf, dictjson, kanjijson, kanajson, numjson, romajijson):
	edict = from_json(dictjson)
	kanjidict = from_json(kanjijson)
	numdict = from_json(numjson)
	kanadict = from_json(kanajson)
	romajidict = from_json(romajijson)
	outf = './output/' + re.sub(r'.*\/input\/(.*)\.([tc][xs][tv])', r'\1-output.\2', inf)
	with open(inf, encoding='utf-8', mode='r') as infile, open(outf, encoding='utf-8', mode='w') as outfile:
		outfile.write('type\ttoken\ttranscription\tsource\n')
		for row in csv.DictReader(infile, delimiter='\t'):
			if row['type'] == 'word':
				tokens = row['tokens'].split(' ')
				for token in tokens:
					token = token.strip()
					#print(token)
					try:
						phon = kanjidict[token]
						source = "kanji dict"
					except KeyError:
						try:
							phon = romajidict[token]
							source = "small Romaji dictionary"
						except KeyError:
							try:
								phon = edict[token][0]
								source = "supplemental dictionary"
							except KeyError:
								try:
									phon = word(token, kanadict)
									source = "transliterated"
							
								except KeyError:
									phon = 'unk'
									source = "not found"
						
					newline = "word\t{0}\t{1}\t{2}\n".format(token, phon, source)
					print(newline)
					outfile.write(newline)
			elif row['type'] == 'num':
				tokens = row['tokens'].split(' ')		
				for token in tokens:
					try:
						phon = parse_num(token, numdict, kanadict, kanjidict)
						source = "number parser"
					except KeyError:
						try:
							phon = kanjidict[token]
							source = "kanji dict"
						except KeyError:	
							phon = 'unk'
							source = "not found"
					newline = "num\t{0}\t{1}\t{2}\n".format(token, phon, source)
					print(newline)
					outfile.write(newline)







def get_kanji_dict(kanjixml, kanjijson, kanajson): # https://github.com/Doublevil/JmdictFurigana
	kanadict = from_json(kanajson)
	kanjidict = {}
	import xmltodict

	print("Getting XML dict...")
	with open(kanjixml, encoding='utf-8', mode = 'r') as xmlf:
		fromxmldict = xmltodict.parse(xmlf.read())
		for i in range(len(fromxmldict['JMdict']['entry'])):
			rentry = fromxmldict['JMdict']['entry'][i]['r_ele']
			trans = ""

			try: 
					if len(rentry) > 1:
						for r in rentry:
							
							kana = r['reb']
							try:
								trans = word(kana, kanadict)
								if trans != "":
									if kana not in kanjidict.keys():
										kanjidict[kana] = trans
							except KeyError:
								print("no trans: {0}".format(kana))
					else:
						kana = rentry['reb']
						try:
							trans = word(kana, kanadict)
							if trans != "":
								if kana not in kanjidict.keys():
									kanjidict[kana] = trans
						except KeyError:
							print("no trans: {0}".format(kana))
			except TypeError:
					try:
						kana = rentry['reb']
						try:
							trans = word(kana, kanadict)
							if trans != "":
								if kana not in kanjidict.keys():
									kanjidict[kana] = trans
						except KeyError:
							print("no trans: {0}".format(kana))
					except KeyError:
						print("KeyError:", kana)	

				

				
			if trans != "":
				try:
					kentry = fromxmldict['JMdict']['entry'][i]['k_ele']
					try: 
						if len(kentry) > 1:
							for k in kentry:
								kanji = k['keb'].strip()
								if kanji not in kanjidict.keys():
									kanjidict[kanji] = trans
						else:
							kanji = kentry['keb']
							if kanji not in kanjidict.keys():
								kanjidict[kanji] = trans
					except TypeError:
						kanji = kentry['keb']
						if kanji not in kanjidict.keys():
							kanjidict[kanji] = trans

				except KeyError:
					kanji = ""
				
	to_json(kanjidict, kanjijson)
	
	
dicttxt = dictfolder + 'japanese_dict.txt'	
dictjson = dictfolder + 'japanese_dict.json'
kanajson = dictfolder + 'kanatrans.json'
numjson = dictfolder + 'num.json'
romajijson = dictfolder + 'romajidict.json'
kanjijson = dictfolder + 'kanji.json'
romajijson = dictfolder + 'romaji.json'
kanjixml = dictfolder + 'JmdictFurigana/JmdictFurigana/Resources/JMdict.xml'

if not os.path.exists(kanajson):
	kanafile = dictfolder + 'kana_table.txt'
	create_kana_dict(kanafile, kanajson)
if not os.path.exists(numjson):
	numtxt = dictfolder + 'num.txt'
	create_num_dict(numtxt, numjson)
if not os.path.exists(romajijson):
	romajitxt = dictfolder + 'romaji.txt'
	create_romaji_dict(romajitxt, romajijson)
	
if not os.path.exists(dictjson):
	import urllib.request
	URL = 'http://ftp.monash.edu/pub/nihongo/edict2u.gz'
	if not os.path.exists(dictfolder + '/edict2u.gz'):
		urllib.request.urlretrieve(URL, dictfolder + '/edict2u.gz')
	
	import gzip
	with gzip.open(dictfolder + '/edict2u.gz', 'rb') as f_in, open(dicttxt, 'wb') as f_out:
		f_out.write( f_in.read() )

	get_dict_from_txt(dicttxt, dictjson, kanajson)
	
if not os.path.exists(kanjixml):  # clones git repository containing dictionary JMdict.xml, to be converted to JSON
	URL = 'https://github.com/Doublevil/JmdictFurigana.git'
	
	from git import Repo
	Repo.clone_from(URL, dictfolder + 'JmdictFurigana/')
if not os.path.exists(kanjijson):
	get_kanji_dict(kanjixml, kanjijson, kanajson)

	
transliterate(inputfolder + 'tokens.tsv', dictjson, kanjijson, kanajson, numjson, romajijson)