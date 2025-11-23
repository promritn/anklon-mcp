#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os
from flask import Flask
import json
import mimerender
import requests
import ast
import pythainlp
mimerender = mimerender.FlaskMimeRender()

render_json = lambda **args: json.dumps(args)


app = Flask(__name__)
#@app.route('/')
@app.route('/<word>')


@mimerender(
    default = 'json',
    json = render_json
)

def getData(word):
	print (word)
	import json
	import requests
	import re
	#=====[ก-ฮ]=====#
	consonant = ['ก','ข','ฃ','ค','ฅ','ฆ','ง','จ','ฉ','ช','ซ','ฌ','ญ','ฎ','ฏ','ฐ','ฑ','ฒ','ณ','ด','ต','ถ','ท','ธ','น','บ','ป','ผ','ฝ','พ','ฟ','ภ','ม','ย','ร','ล','ว','ศ','ษ','ส','ห','ฬ','อ','ฮ']
	#=====สระตาม=====#
	sara_after = ['ั','ะ','า','ิ','ี','ึ','ื','ุ','ู','่','้','๊','๋','ำ']
	#=====วรรณยุกต์=====#
	mai_eek = "่"
	mai_thoo = "้"
	mai_trii = "๊"
	mai_chattawaa = "๋"
	tone = mai_eek+"|"+mai_thoo+"|"+mai_trii+"|"+mai_chattawaa
	#=================#
	#ขึ้นต้นด้วยพยัญชนะ
	rule_consonant = []
	cc = "กร|กล|กว|ขร|ขล|ขว|คร|คล|คว|ตร|ปร|ปล|พร|พล|ผล|หง|หญ|หน|หม|หย|หร|หล|หว"
	c = "[ก-ฮ]"
	cf = "(ก|ข|ค|ฆ|ง|จ|ช|ซ|ญ|ฎ|ฏ|ฐ|ฑ|ฒ|ณ|ด|ต|ถ|ท|ธ|น|บ|ป|พ|ฟ|ภ|ม|ย|ร|ล|ว|ศ|ษ|ส|ฬ)"
	final = "(ง|ม|ย|ว|น|ก|ด|บ)"
	#สระอะ
	sara_a = "^"+"("+"ขร|หณ|สร|กร|คร|คล|ชร|ตร|ทร|ปร|ปล|ผล|พร|หน|หย|หร|หล|หว|ปร"+"|"+c+")"+"("+tone+")?ะ"
	rule_consonant.append(sara_a)
	#สระอือ
	sara_uee = "^"+"("+cc+"|"+c+")"+"ื"+"("+tone+")?อ"
	rule_consonant.append(sara_uee)
	#สระอือ+ตัวสะกด
	sara_uee_cf = "^"+"("+cc+"|"+c+")"+"ื"+"("+tone+")?"+"("+cf+")"
	rule_consonant.append(sara_uee_cf)
	#สระอัวะ
	sara_ua = "^(ผล|จ|ผ|พ|ย|ฮ)ั"+"("+tone+")?วะ"
	rule_consonant.append(sara_ua)
	#สระอัว
	sara_oua = "^"+"("+"ชร"+"|"+cc+"|"+c+")"+"ั"+"("+tone+")?ว"
	rule_consonant.append(sara_oua)
	#สระอำ
	sara_am = "^"+"("+cc+"|"+c+")"+"("+tone+")?ำ"
	rule_consonant.append(sara_am)
	#อัปรา+ตัวสะกด
	sara_r_k = "^(หว|หน|ตร|ขว|คร|หม|อย|หล|พร|ก|ข|ค|จ|ฉ|ช|ซ|ด|ต|ถ|ท|บ|ป|ผ|ฝ|พ|ฟ|ม|ย|ร|ล|ว|ศ|ส|ห|ฮ)"+"("+tone+")?า(ก)"+"|"+"^(จ|น|ภ|ร)"+"("+tone+")?า(ค)"
	rule_consonant.append(sara_r_k)
	sara_r_d = "^(ญ|ช)"+"("+tone+")?า(ติ)"+"|"+"^(บ|ม)"+"("+tone+")?า(ตร)"+"|"+"^(ธ)"+"("+tone+")?า(ตุ)"+"|"+"^(ส)"+"("+tone+")?า(รท)"+"|"+"^(ก|น|อ)"+"("+tone+")?า(จ)"+"|"+"^(หร|หล|หม|หน|หง|กล|ขล|คล|ปร|ปล|หว|พล|หย|ก|ข|ค|จ|ฉ|ช|ซ|ด|น|บ|ถ|พ|ฟ|ม|ย|ร|ล|ว|ส|ห|อ)"+"("+tone+")?า(ด)"+"|"+"^(ว|บ|ฆ|ช|ญ|ด|พ|ล|ว|ศ|ห|อ)"+"("+tone+")?า(ต)"+"|"+"^(หน|น)"+"("+tone+")?า(ถ)"+"|"+"^(หว|น|บ|พ|ม|ย|ว|ษ|ส)"+"("+tone+")?า(ท)"+"|"+"^(บ|พ|ร)"+"("+tone+")?า(ธ)"+"|"+"^(น)"+"("+tone+")?า(ฎ)"+"|"+"^(น|ล)"+"("+tone+")?า(ฏ)"+"|"+"^​(ษ)"+"("+tone+")?า(ฒ)"+"|"+"^(ปร|ก|ภ|ร|ล)"+"("+tone+")?า(ช)"+"|"+"^(ก|ค|ต|ร)"+"("+tone+")?า(ซ)"+"|"+"^(ปร|คล|ก|น|บ|ม|ร|ล|อ)"+"("+tone+")?า(ศ)"+"|"+"^(ก|ด|ธ|ภ|ม|ร)"+"("+tone+")?า(ษ)"+"|"+"^(คร|ก|ค|ณ|ด|ท|บ|ป|พ|ฟ|ล|ภ|ม|ย|ว|ศ|ส|ห|อ)"+"("+tone+")?า(ส)"
	rule_consonant.append(sara_r_d)
	sara_r_b = "^(หย|หว|หน|กร|คร|ชร|ตร|ปร|ปล|ทร|หล|ก|ข|ค|ง|จ|ฉ|ซ|ด|ต|ถ|ท|ป|พ|ม|ร|ล|ว|ส|อ|ฮ)"+"("+tone+")?า(บ)"+"|"+"^(ก|ภ)"+"("+tone+")?า(พ)"+"|"+"^(ล)"+"("+tone+")?า(ภ)"+"|"+"^(กร|คร|ดร|ร|ต|อ)"+"("+tone+")?า(ฟ)"+"|"+"^(ปร|บ|ส)"+"("+tone+")?า(ป)"
	rule_consonant.append(sara_r_b)
	sara_r_n = "^(ขว|หม|หน|หง|กร|กว|คล|คว|คร|ปร|หว|หล|ก|ฉ|ข|ค|ง|จ|ช|ซ|ฐ|ศ|ด|ต|ถ|ท|น|บ|ป|ผ|ฝ|พ|ม|ย|ร|ล|ว|ส|ห|อ|ธ|ฏ)"+"("+tone+")?า(น)"+"|"+"^(ปร|ก|ญ|น|พ|ภ|ม|ร|ศ|ษ|ส|ห)"+"("+tone+")?า(ณ)"+"|"+"^(คร|คว|ผล|ก|ค|ช|น|บ|ร|ล|ห)"+"("+tone+")?า(ญ)"+"|"+"^(ก|ข|ค|จ|ด|ต|ถ|ท|ธ|พ|ภ|ม|ว|ส|ห)"+"("+tone+")?า(ร)"+"|"+"^(ก|ข|ค|จ|ช|ฑ|ด|ต|บ|ป|ฝ|พ|ม|ย|ร|ว|ศ|ส|ฮ)"+"("+tone+")?า(ล)"+"|"+"^(ก|ว|ต)"+"("+tone+")?า(ฬ)"
	rule_consonant.append(sara_r_n)
	sara_r_g = "^(พล|คว|หง|หล|หน|คล|พร|กร|กว|คร|อย|กล|หว|หม|ขว|ปร|สร|ก|ข|ค|ง|จ|ฉ|ช|ซ|ฎ|ด|ต|ถ|ท|ธ|น|บ|ป|ผ|ฝ|พ|ฟ|ภ|ม|ย|ร|ล|ว|ศ|ส|ห|อ|ฮ)"+"("+tone+")?า(ง)"
	rule_consonant.append(sara_r_g)
	sara_r_m = "^(หร|หล|หน|หว|หย|กร|คร|คว|ปร|ทร|พล|พร|ก|ข|ค|ง|จ|ช|ซ|ณ|ด|ต|ถ|ท|น|บ|ป|ผ|พ|ฟ|ภ|ย|ร|ล|ว|ส|ห|อ|ฮ|ม)"+"("+tone+")?า(ม)"
	rule_consonant.append(sara_r_m)
	sara_r_y = "^(หว|หง|หย|ขน|ปร|พร|กล|กร|ขล|คล|ปล|ทร|หล|หม|หน|ก|ข|ค|ง|จ|ฉ|ช|ซ|ด|ต|ภ|ถ|ท|น|บ|ป|ผ|ฝ|พ|ฟ|ม|ร|ล|ว|ส|ห|ย|อ)"+"("+tone+")?า(ย)"
	rule_consonant.append(sara_r_y)
	sara_r_v = "^(หล|หย|หง|กร|กล|กว|คร|คว|พร|หน|ก|ข|ค|ง|จ|ฉ|ช|ซ|ด|ต|ท|น|บ|ป|ผ|พ|ฟ|ย|ร|ล|ว|ส|ห|อ)"+"("+tone+")?า(ว)"
	rule_consonant.append(sara_r_v)
	sara_r = "^(หง|หย|ปล|ขว|หม|กว|หญ|กล|กร|ขล|คร|คล|คว|ตร|ปร|ผล|พร|หน|หว|หร|หล|อย|ทร|[ก-ฮ])"+"("+tone+")?า"
	rule_consonant.append(sara_r)
	#สระอิ+ตัวสะกด
	sara_i_k = "^(หร|หล|หง|หย|พร|ก|ข|ค|จ|ช|ซ|ญ|ฐ|ด|ต|ถ|ท|น|บ|ป|ฟ|ภ|ม|ย|ล|ว|ศ|ส|อ)ิ"+"("+tone+")?(ก)"+"|"+"^(ล)ิ"+"("+tone+")?(ข)"+"|"+"(ช|ต|น|บ|ป|ฟ|ม|ร|ล|ว|ส|อ)ิ"+"("+tone+")?(ค)"
	rule_consonant.append(sara_i_k)
	sara_i_d = "^(จ|ม|พ|ว|ล)ิ"+"("+tone+")?(ตร)"+"|"+"^(ม|ก|น)ิ"+"("+tone+")?(จ)"+"|"+"^(หว|หง|หน|คล|ปล|ก|ข|ค|จ|ช|ซ|น|ด|ต|บ|ป|ผ|ว|ม|ร|อ)ิ"+"("+tone+")?(ด)"+"|"+"^(กร|หร|หล|ก|ค|จ|ช|ฑ|ณ|ต|ม|ว|ศ|ษ|ส|ห|ถ|พ|ข|ท)ิ"+"("+tone+")?(ต)"+"|"+"^(หน|ซ|ด|บ|พ|ฟ|ม|ร|ว|ส|ห|อ)ิ"+"("+tone+")?(ท)"+"|"+"^(กร|ค|ณ)ิ"+"("+tone+")?(ช)"+"|"+"^(ว)ิ"+"("+tone+")?(ซ)"+"|"+"^(ปร|ก|ว|ท|พ)ิ"+"("+tone+")?(ศ)"+"|"+"^(กร|พ|ว|ศ|ห|ด|ธ)ิ"+"("+tone+")?(ษ)"+"|"+"^(คร|ส|ก|จ|ซ|ว|ห)ิ"+"("+tone+")?(ส)"+"|"+"^(พ)ิ"+"("+tone+")?(ธ)"
	rule_consonant.append(sara_i_d)
	sara_i_b = "^(หม|หย|พร|กร|ขร|ขล|ก|จ|ง|ฉ|ช|ซ|ด|ธ|บ|ย|ร|ล|ว|ส|อ)ิ"+"("+tone+")?(บ)"+"|"+"^(ข|ช|ซ|ท|ธ|น|ย|ล|ส|ฮ)ิ"+"("+tone+")?(ป)"+"|"+"^(ก|ซ|ด|ท|ล)ิ"+"("+tone+")?(ฟ)"+"|"+"^(น|ท)ิ"+"("+tone+")?(พ)"
	rule_consonant.append(sara_i_b)
	sara_i_n = "^(หว|หม|ปล|กล|ก|ข|ค|ฆ|จ|ฉ|ช|ซ|ด|ต|ถ|ฐ|ท|บ|ป|ผ|ฝ|พ|ฟ|ภ|ม|ย|ร|ล|ว|ศ|ษ|ส|ห|อ|ฮ|น)ิ"+"("+tone+")?(น)"+"|"+"^(ก|ข|จ|บ|พ|ษ|ส)ิ"+"("+tone+")?(ณ)"+"|"+"^(ข|ภ|ว|ส)ิ"+"("+tone+")?(ญ)"+"|"+"^(หว|จ|บ|พ|ม|ร|ว|ศ|อ|ฮ|น)ิ"+"("+tone+")?(ล)"+"|"+"^(พ|ม)ิ"+"("+tone+")?(ฬ)"
	rule_consonant.append(sara_i_n)
	sara_i_g = "^(หล|หย|หน|หง|หว|หม|หญ|หร|กร|คล|จร|พร|ก|ข|ค|จ|ฉ|ช|ซ|ด|ต|ท|ธ|น|บ|ป|ผ|พ|ภ|ม|ย|ล|ว|ศ|ส|ห|อ|ฮ)ิ"+"("+tone+")?(ง)"
	rule_consonant.append(sara_i_g)
	sara_i_m = "^(หง|หน|หย|ปร|กร|กล|พร|ก|ข|ค|จ|ฉ|ช|ซ|ฌ|ต|ท|น|ป|พ|ม|ห|ย|ร|ล|ว|อ)ิ"+"("+tone+")?(ม)"
	rule_consonant.append(sara_i_m)
	sara_i_v = "^(หว|หย|หล|พร|พล|ปล|ก|ค|ง|จ|ฉ|ช|ซ|ด|ต|ท|น|บ|ป|ผ|พ|ฟ|ม|ย|ร|ว|ศ|ส|ห|อ|ฮ|ล)ิ"+"("+tone+")?(ว)"
	rule_consonant.append(sara_i_v)
	sara_i = "^(กล|หน|หร|ตร|ผล|[ก-ฮ])ิ"+"("+tone+")?"
	rule_consonant.append(sara_i)
	#สระอี+ ตัวสะกด
	sara_ee_k = "^(หล|ปล|ฉ|ซ|ป|ล|ว|อ|ผ)ี"+"("+tone+")?(ก)"+"|"+"^(พ|ล|ว)ี"+"("+tone+")?(ค)"
	rule_consonant.append(sara_ee_k)
	sara_ee_d = "^(หว|หร|กร|ปร|ก|ข|จ|ฉ|ซ|ด|ป|ม)ี"+"("+tone+")?(ด)"+"|"+"^(ข|ค|ด)ี"+"("+tone+")?(ต)"
	rule_consonant.append(sara_ee_d)
	sara_ee_b ="^(หล|หน|กล|คร|ก|ค|จ|ต|ล|ถ|ธ|บ|ป|ร|ห)ี"+"("+tone+")?(บ)"+"|"+"^(ว|ท)ี"+"("+tone+")?(ป)"+"|"+"^(ช)ี"+"("+tone+")?(พ)"
	rule_consonant.append(sara_ee_b)
	sara_ee_n = "^(จ|ซ|ด|ต|บ|ป|ร|ล|ว|ม)ี"+"("+tone+")?(น)"+"|"+"^(ศ)ี"+"("+tone+")?(ล)"
	rule_consonant.append(sara_ee_n)
	sara_ee_m = "^(คร|คล|ค|ต|บ)ี"+"("+tone+")?(ม)"
	rule_consonant.append(sara_ee_m)
	sara_ee = "^(หว|หม|หล|หย|พล|กร|กล|ขร|คล|ปร|ปล|ศร|ตร|หน|[ก-ฮ])ี"+"("+tone+")?"
	rule_consonant.append(sara_ee)
	#สระอึ+ตัวสะกด
	#สระอึ+ตัวสะกด
	sara_ue = "^"+"("+"กร|กล|กว|ขร|ขล|ขว|คร|คล|คว|ตร|ปร|ปล|พล|ผล|หง|หญ|หน|หม|หย|หล|หว"+"|"+c+")"+"ึ"+"("+tone+")?(ก|ด|บ|น|ง|ม|ย)?|พร(ึ)(่|้|๊|๋)?(ติ|ง|ก|น|บ)"
	rule_consonant.append(sara_ue)
	#สระอุ+ตัวสะกด
	sara_u_k = "^(บ)ุ"+"("+tone+")?(ตร)"+"|"+"^(หล|หน|หย|หม|คล|ขล|ปล|ค|ฉ|ช|ซ|ต|ท|อ|ร|ล|อ|ส|จ|บ)ุ"+"("+tone+")?(ก)"+"|"+"^(ม|ส)ุ"+"("+tone+")?(ขล|ข)"+"|"+"^(ม|ย|บ)ุ"+"("+tone+")?(ค)"
	rule_consonant.append(sara_u_k)
	sara_u_d = "^(หม)ุ"+"("+tone+")?(ทร)"+"|"+"^(ว|ม)ุ"+"("+tone+")?(ฒิ|ติ)"+"|"+"^(พ)ุ"+"("+tone+")?(ทธ)"+"|"+"^(ม|ด)ุ"+"("+tone+")?(จ)"+"|"+"^(คร|หว|หง|หม|หล|ผล|ทร|หย|ก|ข|ค|จ|ฉ|ช|ด|ต|ผ|พ|ย|ว|ส|อ|ร)ุ"+"("+tone+")?(ด)"+"|"+"^(หล|ม)ุ"+"("+tone+")?(ต)"+"|"+"^(ม)ุ"+"("+tone+")?(ถ)"+"|"+"^(ศ|ส|อ)ุ"+"("+tone+")?(ท)"+"|"+"^(ม|ว|ย)ุ"+"("+tone+")?(ธ)"+"|"+"^(ธ|น)ุ"+"("+tone+")?(ช)"+"|"+"^(ตร|น|ด|ร)ุ"+"("+tone+")?(ษ)"
	rule_consonant.append(sara_u_d)
	sara_u_b = "^(หร|หง|หล|หย|หม|กร|ง|จ|ช|ด|ต|ท|บ|ป|ฟ|ม|ว|ห)ุ"+"("+tone+")?(บ)"+"|"+"^(หร|ฉ|ซ|บ)ุ"+"("+tone+")?(ป)"+"|"+"^(ท|บ)ุ"+"("+tone+")?(พ)"
	rule_consonant.append(sara_u_b)
	sara_u_n = "^(หง|หย|หม|หน|กร|คร|ก|ข|ง|ฉ|น|ต|ฝ|ม|ล|ว|ส|ห|อ|ท|ค|จ|ด|ร)ุ"+"("+tone+")?(น)"+"|"+"^(ก|ค|ร)ุ"+"("+tone+")?(ณ)"+"|"+"^(ก|บ|ร)ุ"+"("+tone+")?(ญ)"+"|"+"^(ก|ช|ว|ด)ุ"+"("+tone+")?(ล)"
	rule_consonant.append(sara_u_n)
	sara_u_m = "^(หร|หย|หน|กล|ขล|คล|ก|ข|ค|จ|ช|ซ|ฎ|ด|ต|ท|ม|ร|ล|อ|พ|ส)ุ"+"("+tone+")?(ม)"
	rule_consonant.append(sara_u_m)
	sara_u_g = "^(หน|หล|พร|กร|ผล|ปร|ง|บ|พ|ฟ|ม|ย|ร|ล|ห|ท|ต|ถ)ุ"+"("+tone+")?(ง)"
	rule_consonant.append(sara_u_g)
	sara_u_y = "^(หม|หน|หง|หย|ขล|คร|ก|ข|ค|จ|ถ|บ|ป|อ|ต)ุ"+"("+tone+")?(ย)"
	rule_consonant.append(sara_u_y)
	sara_u = "^(คร|ตร|หน|ขร|หม|หล|ผล|[ก-ฮ])ุ"+"("+tone+")?"
	rule_consonant.append(sara_u)
	#ไม้หันอากาศ
	mai_hunargard = "^(ผร|หง|ศร|พร|ผล|ปล|ชร|ขล|กร|ปร|คล|คว|หย|ตร|ทร|หม|คร|คล|กล|พล|หว|ขว|หล|หน|หร|[ก-ฮ])ั"+"("+tone+")?(ตร|กร|ติ|ตุ|[ก-ฮ])"
	rule_consonant.append(mai_hunargard)
	#สระอู+ ตัวสะกด
	sara_uu_k = "^(หม|หย|ปล|ก|ด|ต|ถ|ผ|ฟ|ม|ล|ห|ฮ)ู"+"("+tone+")?(ก)"
	rule_consonant.append(sara_uu_k)
	sara_uu_d = "^(ส)ู"+"("+tone+")?(ติ|ตร)"+"|"+"^(ส)ู"+"("+tone+")?(จ)"+"|"+"^(หว|ก|ข|จ|ฉ|ซ|ต|ท|บ|ป|พ|ฟ|ร|ว|ส|ห|อ)ู"+"("+tone+")?(ด)"+"|"+"^(ก|ฑ|ท|ภ)ู"+"("+tone+")?(ต)"+"|"+"^(บ|ส)ู"+"("+tone+")?(ท)"+"|"+"^(ฎ)ู"+"("+tone+")?(ก)"+"|"+"^(ฏ)ู"+"("+tone+")?(ก)"+"|"+"^(ม)ู"+"("+tone+")?(ส)"
	rule_consonant.append(sara_uu_d)
	sara_uu_b = "^(ชร|ก|ง|จ|ซ|ต|ท|ล|ว|ส|อ)ู"+"("+tone+")?(บ)"+"|"+"^(ก|ถ|ธ|ร|ล)ู"+"("+tone+")?(ป)"
	rule_consonant.append(sara_uu_b)
	sara_uu_n = "^(ก|จ|ต|ท|บ|ป|พ|ล|ศ)ู"+"("+tone+")?(น)"+"|"+"^(ก|ค)ู"+"("+tone+")?(ณ)"+"|"+"^(ย|ส)ู"+"("+tone+")?(ญ)"+"|"+"^(ก|ฐ|ณ|ธ|ด|บ)ู"+"("+tone+")?(ร)"+"|"+"^(ก|จ|ท|บ|ฝ|ภ|ศ|ม)ู"+"("+tone+")?(ล)"
	rule_consonant.append(sara_uu_n)
	sara_uu_m = "^(ต|ท|บ|ฟ|ม|อ|ฮ)ู"+"("+tone+")?(ม)"
	rule_consonant.append(sara_uu_m)
	sara_uu_g = "^(ปร|ง|จ|ฝ|ย|ส)ู"+"("+tone+")?(ง)"
	rule_consonant.append(sara_uu_g)
	sara_uu_y = "^(อ)ู"+"("+tone+")?(ย)"
	rule_consonant.append(sara_uu_y)
	sara_uu = "^(หม|หน|กล|กร|ขล|คร|ตร|ปร|หร|ทร|หล|อย|[ก-ฮ])ู"+"("+tone+")?"
	rule_consonant.append(sara_uu)
	#สระออ + ตัวสะกด
	sara_or_k = "^(พร|ปล|ตร|กล|หร|กร|หย|หม|หล|ก|ข|ค|ง|จ|ฉ|ช|ซ|น|ด|ต|ถ|ท|บ|ป|ผ|พ|ฟ|ย|ร|ล|ว|ศ|ห|อ|ฮ)"+"("+tone+")?อ(ก)"+"|"+"^(ช|ซ|ล)"+"("+tone+")?อ(ค)"
	rule_consonant.append(sara_or_k)
	sara_or_d = "^(กร|หร|หว|หย|หล|พร|ปล|คล|ก|ต|ถ|ท|บ|ป|ม|ย|ร|ล|ว|ส|อ|ฮ|ง)"+"("+tone+")?อ(ด)"+"|"+"^(บ|พ|ร|ล|ฮ)"+"("+tone+")?อ(ต)"+"|"+"^(ร)"+"("+tone+")?อ(ธ)"+"|"+"^(ท)"+"("+tone+")?อ(ช)"+"|"+"^(ฮ)"+"("+tone+")?อ(ส)"+"|"+"^(หร)"+"("+tone+")?อ(ท)"
	rule_consonant.append(sara_or_d)
	sara_or_b = "^(ข)อ(บ)|^(หม|หน|คร|ปล|ก|ต|ถ|บ|ป|ผ|ม|ร|ล|ส|ห|ช|ง)"+"("+tone+")?อ(บ)" #ข้อบกพ่อง ขอบ
	rule_consonant.append(sara_or_b)
	sara_or_n = "^(หง|กร|คล|หล|หย|หม|หน|กล|ก|ค|ฌ|ฎ|ฏ|ต|ง|ถ|บ|ซ|ผ|ป|พ|ฟ|น|ร|ย|ล|ว|ส|ห|ท|อ|ย|ฮ|ด|ข|ช|ฉ)"+"("+tone+")?อ(น)"+"|"+"^(ม)"+"("+tone+")?อ(ญ)"+"|"+"^(ต|บ|ร|ฮ|ว)"+"("+tone+")?อ(ล)"
	rule_consonant.append(sara_or_n)
	sara_or_m = "^(หย|หง|หม|คร|หน|ปล|หล|ตร|กล|พร|ซ|ค|ต|บ|ป|ผ|ม|ย|ร|ห|จ|น|ล|อ|ด|ว|ท|พ|ถ)"+"("+tone+")?อ(ม)"
	rule_consonant.append(sara_or_m)
	sara_or_g = "^(กล|หง|หย|ปล|หล|พร|หน|คร|หม|คล|กร|ตร|ก|ค|จ|ข|ต|ถ|ท|บ|ป|ผ|พ|น|ฟ|ม|ร|ล|ส|ห|ย|ซ|ช|อ|ฉ|ด|ฆ|ว)"+"("+tone+")?อ(ง)"
	rule_consonant.append(sara_or_g)
	sara_or_y = "^(กล|หร|หย|หม|หล|หง|พร|คล|สร|หน|ปล|พล|ก|ค|ถ|บ|ป|ฝ|พ|ฟ|ร|ล|ส|ห|น|ง|ด|ย|อ|ซ|ต|ช|ม|จ)"+"("+tone+")?อ(ย)"
	rule_consonant.append(sara_or_y)
	sara_or = "^(หว|หล|หง|หม|คล|หร|หน|[ก-ฮ])"+"("+tone+")?อ"
	rule_consonant.append(sara_or)
	#สระว+ตัวสะกด
	sara_v_k = "^(หน|หม|ก|จ|ซ|ด|บ|ป|พ|ม|ร|ล|อ)"+"("+tone+")?วก"
	rule_consonant.append(sara_v_k)
	sara_v_d = "^(ตร|ร)"+"("+tone+")?วจ"+"|"+"^(หน|หม|หร|กร|ก|ข|ง|จ|ช|ซ|ด|ท|บ|ป|พ|ร|ล|ส|ห|อ|ฮ)"+"("+tone+")?วด"+"|"+"^(จ)"+"("+tone+")?วต"+"|"+"^(หน|บ)"+"("+tone+")?วช"
	rule_consonant.append(sara_v_d)
	sara_v_b = "^(หย|ข|ค|จ|บ|ร|อ|ฮ)"+"("+tone+")?วบ"
	rule_consonant.append(sara_v_b)
	sara_v_n = "^(หย|หง|หน|หม|ตร|ปร|ก|ข|ค|ง|จ|ฉ|ช|ซ|ญ|ณ|ด|ต|ถ|ท|บ|ป|ผ|พ|ม|น|ร|ล|ส|ห|อ|ย|ฮ)"+"("+tone+")?วน"+"|"+"^(ค|ญ|น)"+"("+tone+")?วณ"+"|"+"^(ค|ช|ศ)"+"("+tone+")?วร"+"|"+"^(สร|ช|ด|ม|อ|น|ม|ห)"+"("+tone+")?วล"+"|"+"^(คร)"+"("+tone+")?วญ"
	rule_consonant.append(sara_v_n)
	sara_v_m = "^(หล|สร|ก|ช|ด|ต|ท|บ|ร|ส|อ|น)"+"("+tone+")?วม"
	rule_consonant.append(sara_v_m)
	sara_v_g = "^(คล|กล|ทร|หล|สร|หน|ก|ข|ค|ง|จ|ช|ด|ต|ถ|ท|บ|ป|พ|ม|ร|ล|ห|ฮ|ย)"+"("+tone+")?วง"
	rule_consonant.append(sara_v_g)
	sara_v_y = "^(หน|หล|หม|กร|กล|ก|ข|ค|น|ง|ฉ|ช|ซ|ด|ถ|ท|บ|ป|ผ|พ|ม|ร|ส|ห|อ|ฮ)"+"("+tone+")?วย"
	rule_consonant.append(sara_v_y)
	#ตัว รร
	tua_rr = "^(บ)(รร)|^.(รร)(ม|ช|ก|ศ|ค|ณ|พ|ถ|ษ)|^.(รร)"
	rule_consonant.append(tua_rr)
	#พยัญชนะ + ตัวสะกด
	c_cf_k = "^(หม|หน|หง|หล|คร|ปร|หย|หน|บ|ป|อ|ต|ย|ด|น|ผ|ร|พ|ห|ศ|จ|ว|ช|ส)"+"("+tone+")?ก|(ห)(ค)"
	rule_consonant.append(c_cf_k)
	c_cf_g = "^หง(บ|น)|^(หง|หย|หน|ปล|ทร|กร|หล|ตร|สร|ย|อ|ง|ร|ล|ส|น|ม|ค|จ|ล|ด|พ|บ|ท|ว|ช|ผ|ห|อ)"+"("+tone+")?(ง)" #หงบ
	rule_consonant.append(c_cf_g)
	c_cf_d = "^(หร|หล|ปร|หน|หม|หย|ก|ง|ป|ล|อ|ส|ห|จ|ค|ฎ|บ|ท|ร|ช|ถ)"+"("+tone+")?ด"+"|"+"^(ร)"+"("+tone+")?ถ"+"|"+"^(ก)"+"("+tone+")?(ฎ|ฏ)"+"|"+"^(ร|บ)"+"("+tone+")?ส"+"|"+"^(ท|ย)"+"("+tone+")?ศ"+"|"+"^(บ)"+"("+tone+")?ท"+"|"+"^(พร|ค|ณ)"+"("+tone+")?ต"+"|"+"^(ร|พ)"+"("+tone+")?จ"+"|"+"^(หร)"+"("+tone+")?ส"
	rule_consonant.append(c_cf_d)
	c_cf_b = "^(หย|หน|ปร|ขล|หง|กล|หล|คร|ซ|พ|ส|จ|ต|อ|ร|ท|ค|ล|น|ง|ก|ข)"+"("+tone+")?บ"+"|"+"^(ศ|อ|ย|ส|ภ|ร|น|ล)"+"("+tone+")?พ"
	rule_consonant.append(c_cf_b)
	c_cf_n = "^(กล|หน|หง|ปร|กร|หล|หม|พร|ย|ช|จ|ข|ด|ค|ต|ห|ฝ|บ|ว|พ|ร|ล|ช|ส|ท|ห|ป|ม|ก|ซ|อ)"+"("+tone+")?(น|ม)"+"|"+"^(ก|ข|ด|ค|ศ|ษ|พ|จ|ท|ว|ส|ม|ห|อ|น|ธ|ฎ|ภ)"+"("+tone+")?ร"+"|"+"^(ก|ด|ค|ผ|ม|ศ|พ|ย|ว|ช|อ)"+"("+tone+")?ล"+"|"+"^(จ)"+"("+tone+")?ญ"+"|"+"^(ส)"+"("+tone+")?ณ"
	rule_consonant.append(c_cf_n)
	c_cf_m = "^(หง|หล|หร|หย|หน|ขล|กล|พร|ตร|ก|ค|ช|ซ|ร|ส|ท|ล|ย|ด|ต|ง|จ|ฐ|ถ|ข|ป|บ|น|ห|อ|ผ)"+"("+tone+")?ม"
	rule_consonant.append(c_cf_m)
	#ไม้ไต่คู้
	tai_khoo = "^"+"("+cc+"|"+c+")"+"็"+"อ"+"("+cf+")"+"|"+"^(ก็)"
	rule_consonant.append(tai_khoo)
	c = "^."
	rule_consonant.append(c)
	#=====================ขึ้นต้นด้วยสระเอ=====================#
	c = "[ก-ฮ]"
	rule_sara_aa = []
	#สระเอะ
	sara_eh = "^เ"+"("+cc+"|"+c+")"+"("+tone+")?ะ"
	rule_sara_aa.append(sara_eh)
	#สระเอาะ
	sara_orh = "^เ"+"("+"ซร"+"|"+cc+"|"+c+")"+"("+tone+")?าะ"
	rule_sara_aa.append(sara_orh)
	#สระเออะ
	sara_oeh = "^เ"+"("+cc+"|"+c+")"+"("+tone+")?อะ"
	rule_sara_aa.append(sara_oeh)
	#สะเอียะ
	sara_iah = "^เ"+"("+cc+"|"+c+")"+"ี"+"("+tone+")?ยะ"
	rule_sara_aa.append(sara_iah)
	#สระเอา
	sara_ao = "^เ"+"("+"ชร|ศร"+"|"+cc+"|"+c+")"+"("+tone+")?า"
	rule_sara_aa.append(sara_ao)
	#ไม้ไต่คู้
	mai_tai_khoo = "^"+"เ"+"("+"สร"+"|"+cc+"|"+c+")"+"็"+"("+cf+")"
	rule_sara_aa.append(mai_tai_khoo)
	#สระเอีย + ตัวสะกด
	sara_ia_k = "^เ(ก|จ|ป|ร)ี"+"("+tone+")?ย(ก)"
	rule_sara_aa.append(sara_ia_k)
	sara_ia_d = "^เ(ก)ี"+"("+tone+")?ย(รติ)"+"|"+"^เ(ก)ี"+"("+tone+")?ย(จ)"+"|"+"^เ(กร|หย|หน|กล|คร|ตร|ก|ข|ค|จ|ฉ|ด|ท|บ|ป|พ|ฟ|ม|ย|ล|ว|อ|ส)ี"+"("+tone+")?ย(ด)"+"|"+"^เ(ล|ว)ี"+"("+tone+")?ย(ต)"
	rule_sara_aa.append(sara_ia_d)
	sara_ia_b = "^เ(หย|ปร|กร|ตร|พร|ก|ง|ฉ|ช|ซ|ต|ท|บ|พ|ย|ร|ล|ส|น)ี"+"("+tone+")?ย(บ)"+"|"+"^(เจี๊ยบ)"
	rule_sara_aa.append(sara_ia_b)
	sara_ia_n = "^เ(หล|หม|หน|หว|กว|ปล|ก|ข|ค|จ|ซ|ต|ถ|ท|บ|ป|ฆ|ผ|พ|ย|ร|ล|ว|ส|ห|อ|น|ษ|ม|ช|ง)ี"+"("+tone+")?ย(น)"+"|"+"^เ(จ|ค|ช|ฑ|ถ|ท|พ|ม|ศ|ส|ห)ี"+"("+tone+")?ย(ร)"+"|"+"^เ(ช)ี"+"("+tone+")?ย(ล)"+"|"+"^เ(หร)ี"+"("+tone+")?ย(ญ)"+"|"+"^เ(ษ)ี"+"("+tone+")?ย(ณ)"
	rule_sara_aa.append(sara_ia_n)
	sara_ia_m = "^เ(หง|หน|หล|ตร|ปร|พร|ข|ค|จ|ช|ซ|ด|ท|ป|ม|ร|ล|ส|ห|อ|ย|น|ฟ)ี"+"("+tone+")?ย(ม)"
	rule_sara_aa.append(sara_ia_m)
	sara_ia_g = "^เ(หน|หว|หล|พล|กร|กล|จร|จล|พร|ก|ข|ค|จ|ฉ|ช|ซ|ด|ต|ถ|บ|ป|พ|ม|ย|ร|ล|ว|ส|ห|ท|น|อ)ี"+"("+tone+")?ย(ง)"
	rule_sara_aa.append(sara_ia_g)
	sara_ia_v = "^เ(พร|ปล|หย|หม|หล|หน|กล|กร|คร|ปร|ก|ข|ค|จ|ฉ|ส|ช|ซ|ด|ต|พ|ย|ล|ท|ห|ร|อ|บ)ี"+"("+tone+")?ย(ว)"
	rule_sara_aa.append(sara_ia_v)
	sara_ia_y = "^เ(ปล|หล|คล|พล|กล|[ก-ฮ])ี"+"("+tone+")?ย"+"|"+"^(เจี๊ยบ)"
	rule_sara_aa.append(sara_ia_y)
	#สระเอือ + ตัวสะกด
	sara_euah_k = "^เ(หย|หล|กล|ก|ง|จ|ช|ด|ถ|ท|ป|ผ|ฝ|ม|ย|ร|ล|ส)ื"+"("+tone+")?อ(ก)"
	rule_sara_aa.append(sara_euah_k)
	sara_euah_d = "^เ(ง|ช|ด|ล|ห|อ|ผ)ื"+"("+tone+")?อ(ด)"
	rule_sara_aa.append(sara_euah_d)
	sara_euah_b = "^เ(หล|คล|ก|บ|ง|ม)ื"+"("+tone+")?อ(บ)"
	rule_sara_aa.append(sara_euah_b)
	sara_euah_n = "^เ(หย|กล|หม|คล|ข|ฉ|ช|ด|ต|ท|บ|ผ|ถ|ฟ|ย|ร|ล|อ|ฮ|พ|ง|ป|ฝ)ื"+"("+tone+")?อ(น)"
	rule_sara_aa.append(sara_euah_n)
	sara_euah_m = "^เ(หล|ข|อ|ช|ส|ล|ง|พ|ท)ื"+"("+tone+")?อ(ม)"
	rule_sara_aa.append(sara_euah_m)
	sara_euah_g = "^เ(หม|หล|ปร|คร|ปล|ข|ค|บ|ฝ|ฟ|ม|ย|ร|ล|น|ท|ต|ด)ื"+"("+tone+")?อ(ง)"
	rule_sara_aa.append(sara_euah_g)
	sara_euah_y = "^เ(หม|หน|ปล|ด|ฟ|ร|อ|ม|ล|ฉ|ป|จ)ื"+"("+tone+")?อ(ย)"
	rule_sara_aa.append(sara_euah_y)
	sara_euah = "^เ(หย|คร|หน|กล|พร|หล|หง|[ก-ฮ])ื"+"("+tone+")?อ"
	rule_sara_aa.append(sara_euah)
	#สระเออ
	sara_oe = "^(เทอญ|เทอม|เยอว)"+"|"+"^เ"+"("+"สร|บล|"+cc+"|"+c+")"+"("+tone+")?อ"
	rule_sara_aa.append(sara_oe)
	#สระลดรูป เ-ิ-
	lodrub_sara_oe = "^เ"+"("+"สร|"+cc+"|"+c+")"+"ิ"+"("+tone+")?"+cf
	rule_sara_aa.append(lodrub_sara_oe)
	#สระเอ + ตัวสะกด
	sara_aa_k = "^เ(หน|หว|หย|ก|ข|ค|ง|จ|ฉ|ด|ต|บ|ม|ย|ล|ว|ษ|ส|อ)"+"("+tone+")?ก"+"|"+"^เ(ล|ม)"+"("+tone+")?(ข|ฆ)"+"|"+"^เ(ช|ถ|อ|ท)"+"("+tone+")?ค"
	rule_sara_aa.append(sara_aa_k)
	sara_aa_d =  "^เ(น|ม)ตร"+"|"+"^เ(ห)"+"("+tone+")?ตุ"+"|"+"^เ(ก|ท|ร)"+"("+tone+")?จ"+"|"+"^เ(ก|จ|ฉ|ช|ซ|ด|ป|ม|ห|อ|ส)"+"("+tone+")?ด"+"|"+"^เ(หว|ข|ม|จ|ก)"+"("+tone+")?ต"+"|"+"^เ(ก|ภ|ว)"+"("+tone+")?ท"+"|"+"^เ(ก|ร|ท|พ|บ)"+"("+tone+")?ศ"+"|"+"^เ(ค|ล)"+"("+tone+")?ส"+"|"+"^เ(หล|ศร|ศ|ม|ช)"+"("+tone+")?ษ"+"|"+"^เ(ด|ว)"+"("+tone+")?ช"+"|"+"^เ(ม|ว|ส)"+"("+tone+")?ธ"+"|"+"^เ(ส|ช|ว)"+"("+tone+")?ฐ"
	rule_sara_aa.append(sara_aa_d)
	sara_aa_b = "^เ(ก|ข|จ|ว|ห)"+"("+tone+")?บ"+"|"+"^เ(ท)"+"("+tone+")?ป"+"|"+"^เ(ท|ส)"+"("+tone+")?พ"
	rule_sara_aa.append(sara_aa_b)
	sara_aa_n = "^เ(คล|กร|หล|ก|ข|ค|ฆ|จ|ช|ซ|ด|ต|บ|น|ป|ผ|ฟ|ย|ร|ล|ว|ส|อ)"+"("+tone+")?น"+"|"+"^เ(ก|ว)"+"("+tone+")?ณ"+"|"+"^เ(ข|บ|พ)"+"("+tone+")?ญ"+"|"+"^เ(ณ|ว)"+"("+tone+")?ร"+"|"+"^เ(จ|ว)"+"("+tone+")?ล"
	rule_sara_aa.append(sara_aa_n)
	sara_aa_m = "^เ(ปร|ก|ข|ค|จ|ษ|อ|ล)"+"("+tone+")?ม"
	rule_sara_aa.append(sara_aa_m)
	sara_aa_g = "^เ(หว|หน|หย|หม|คล|ขล|ปล|คร|คว|พล|กร|ก|ข|ค|ง|ฉ|ด|ต|ผ|ม|ร|บ|ล|ห|อ|ฮ|ว|พ|จ|ป)"+"("+tone+")?ง"
	rule_sara_aa.append(sara_aa_g)
	sara_aa_y = "^เ(หน|ปร|หม|หล|หว|ข|ค|ง|จ|ฉ|ช|ด|ป|ร|ย|ล|ส|ห|อ|ว|ผ|พ|บ)"+"("+tone+")?ย"
	rule_sara_aa.append(sara_aa_y)
	sara_aa_v = "^เ(หล|ปล|ล|ห)"+"("+tone+")?ว"
	rule_sara_aa.append(sara_aa_v)
	sara_aa = "^เ(หว|หน|หล|หม|ขว|พล|[ก-ฮ])"+"("+tone+")?"+"|"+"^(เจี๊ยบ)"
	rule_sara_aa.append(sara_aa)
	#สระแอ
	rule_sara_ae = []
	sara_ae_maitaikhoo = "^แ(กร|[ก-ฮ])็[ก-ฮ]"
	rule_sara_ae.append(sara_ae_maitaikhoo)
	sara_aeh = "^แ(หว|กร|กล|ขว|คร|ผล|พล|หน|หม|หย|หล|ก|ข|ค|ง|จ|ฉ|ช|ซ|ด|ต|ท|น|บ|ป|พ|ฟ|ม|ย|ร|ล|ว|ส|ห|อ|ฮ)(่|้|๊|๋)?ะ"
	rule_sara_ae.append(sara_aeh)
	sara_ae_g = "^แ(กว|หง|หว|หย|พล|ปร|คร|ขว|คล|หล|สร|ปล|กล|กว|ผล|หน|จร|กร|ก|ข|ค|ง|จ|ฉ|ช|ซ|ด|ต|ท|บ|ป|ผ|ฝ|พ|ฟ|ม|ย|ร|ล|ว|ส|ห|อ|ฮ)"+"("+tone+")?(ง|น)"
	rule_sara_ae.append(sara_ae_g)
	sara_ae_k = "^แ(หร|หย|คร|ปล|หว|หล|กร|ทร|ข|ง|จ|ฉ|ซ|ด|ต|ท|บ|ผ|ฝ|ฟ|ม|ย|ร|ล|ว|ส|ห|อ|น)"+"("+tone+")?ก"+"|"+"^แ(จ|ซ|ท|บ|พ|ฟ|ร|ล)"+"("+tone+")?ค"
	rule_sara_ae.append(sara_ae_k)
	sara_ae_n = "^แ(หง|กล|หว|ปล|คว|คล|ก|ข|ค|ง|จ|ซ|ด|ต|ท|บ|ป|ผ|พ|ฟ|ม|ร|ล|ว|ส|อ|น|ถ)"+"("+tone+")?น"+"|"+"^แ(กล|คล|ค|ซ|อ|น)"+"("+tone+")?(ล|ว)"
	rule_sara_ae.append(sara_ae_n)
	sara_ae_v = "^แ(หว|กร|พร|คล|ก|จ|ซ|ด|ถ|บ|ผ|พ|ม|ร|ล|ว|ห|อ|น)"+"("+tone+")?ว"
	rule_sara_ae.append(sara_ae_v)
	sara_ae_d = "^แ(หว|ปร|ง|จ|ซ|ด|ต|บ|ป|ผ|ฝ|ร|ล|ว|ส|อ)"+"("+tone+")?ด"+"|"+"^แ(ช|บ|ม|ว)"+"("+tone+")?ต"+"|"+"^แ(ช|ซ|พ|ม|ล|อ|น)"+"("+tone+")?ท"+"|"+"^แ(ม)"+"("+tone+")?ช"+"|"+"^แ(ก|จ|ม)"+"("+tone+")?ซ"+"|"+"^แ(พ)"+"("+tone+")?ศ"+"|"+"^แ(ก|จ)"+"("+tone+")?ส"
	rule_sara_ae.append(sara_ae_d)
	sara_ae_b = "^แ(หล|ปล|ก|ค|จ|ถ|บ|ป|ฟ|ย|ล|ว|ส|อ|น|ห|ท)"+"("+tone+")?บ"+"|"+"^แ(ก|ค|ซ|อ)"+"("+tone+")?ป"
	rule_sara_ae.append(sara_ae_b)
	sara_ae_m = "^แ(หน|หม|หย|หล|พล|ก|ค|ง|จ|ช|ซ|ต|ถ|ท|บ|ป|ฟ|ม|ย|ร|ล|ว|อ|ฮ|น|ข)"+"("+tone+")?ม"
	rule_sara_ae.append(sara_ae_m)
	sara_ae = "^แ(หล|หม|ปล|พร|ปร|หย|ผล|ปร|[ก-ฮ])"+"("+tone+")?"
	rule_sara_ae.append(sara_ae)
	#สระโอ + ตัวสะกด
	rule_sara_o = []
	sara_oh = "^โ(หว|หย|หน|คร|กร|หล|ก|ข|ค|ง|จ|ฉ|ช|ซ|ต|ท|บ|ป|พ|ม|ย|ร|ล|ศ|ส|ฮ)"+"("+tone+")?ก"+"|"+"^โ(ช|ภ|ร|ย)"+"("+tone+")?ค"
	rule_sara_o.append(sara_oh)
	sara_o_k = "^โ(ช)"+"("+tone+")?ติ"+"|"+"^โ(ร|ล)"+"("+tone+")?จ"+"|"+"^โ(หว|หม|หน|ปร|ข|ค|ฉ|ด|ท|พ|ร|ล|ส|ห)"+"("+tone+")?ด"+"|"+"^โ(หว|ม|ร|ส)"+"("+tone+")?ต"+"|"+"^โ(จ|ม|ร)"+"("+tone+")?ท"+"|"+"^โ(กร|ร)"+"("+tone+")?ธ"+"|"+"^โ(ก)"+"("+tone+")?ฏ"+"|"+"^โ(ค|พ|ภ|ย|ร)"+"("+tone+")?ช"+"|"+"^โ(กร|ก)"+"("+tone+")?ศ"+"|"+"^โ(จ|ด|ท|ม|อ)"+"("+tone+")?ษ"+"|"+"^โ(ค|ต|ท|บ|พ|ม|ร|ล|ฮ)"+"("+tone+")?ส"
	rule_sara_o.append(sara_o_k)
	sara_o_b = "^โ(ฉ|ถ|ม|อ|ฮ)"+"("+tone+")?บ"+"|"+"^โ(ค|ป|ร|ล)"+"("+tone+")?ป"+"|"+"^โ(ข|ม|ล)"+"("+tone+")?ภ"
	rule_sara_o.append(sara_o_b)
	sara_o_g = "^โ(หว|หล|หย|หม|หน|หร|พล|ปล|ปร|กร|คร|คล|ก|ข|ค|จ|ฉ|ช|ซ|ต|ถ|ท|ป|ผ|พ|ม|ย|ร|ล|ว|ห|อ|ฮ)"+"("+tone+")?ง"
	rule_sara_o.append(sara_o_g)
	sara_o_n = "^โ(พล|ขล|กร|หล|คล|ก|ข|ค|ง|จ|ช|ซ|ด|ต|น|ถ|ท|ป|ผ|พ|ฟ|ม|ย|ร|ล|ห|อ)"+"("+tone+")?น"+"|"+"^โ(ก)"+"("+tone+")?ณ"+"|"+"^โ(ก)"+"("+tone+")?ญ"+"|"+"^โ(จ|ด)"+"("+tone+")?ร"+"|"+"^โ(จ|ร|ว)"+"("+tone+")?ล"
	rule_sara_o.append(sara_o_n)
	sara_o_m = "^โ(ซร|คร|กร|ทร|ข|ค|จ|ฉ|ช|ด|ถ|บ|ฟ|ร|ล|ส|ห|อ|ฮ|น|ย)"+"("+tone+")?ม"
	rule_sara_o.append(sara_o_m)
	sara_o_y = "^โ(กร|ปร|ก|ช|ด|ต|ถ|บ|ผ|พ|ม|ร|ว|ห|อ)"+"("+tone+")?ย"
	rule_sara_o.append(sara_o_y)
	sara_o_v = "^โ(อ|จ|ล)"+"("+tone+")?ว"
	rule_sara_o.append(sara_o_v)
	sara_o = "^โ(พล|หน|หล|หว|ทร|[ก-ฮ])"+"("+tone+")?"
	rule_sara_o.append(sara_o)
	#สระใอ
	sara_ai_maimuan = "^ใ(กล|คร|หญ|หม|หล|จ|ช|ด|ต|น|บ|ฝ|ภ|ย|ส|ห)"+"("+tone+")?"
	#สระไอ
	sara_ai_maimalai = "^ไ(ตรย|ชย|ทย|กร|กล|กว|ขว|คร|คล|คว|ซร|ดร|ตย|ตร|ทร|บร|ปร|ปล|ผล|พร|พล|หน|หม|หร|หล|หว|[ก-ฮ])"+"("+tone+")?"
	#อักษรนำ
	aksonnam = ['ตง','ผว','อล','อน','อง','ปล','ปร','ตน','ตว','ตล','ตม','จม','กน','ศว','ผล','ถม', 'ถน', 'ขร', 'ขณ', 'ขน', 'ขม', 'ขย', 'จว', 'จร', 'ฉง', 'ฉน', 'ฉม', 'ฉล', 'ฉว', 'ฉง', 'ถง', 'ถน', 'ถล', 'ถว', 'ผง','ผน','ผย', 'ศย', 'ศล', 'สง', 'สน', 'สม', 'สย', 'สล','สร','สว', 'อร', 'ตล']
	a_sound = []
	a_sound_sara_a = "^(ขณ|ขย|สน|สว|สล|สว)"+"("+tone+")?ะ"
	a_sound.append(a_sound_sara_a)
	a_sound_sara_aeh = "^แ(ฉล|สย)"+"("+tone+")?ะ" 
	a_sound.append(a_sound_sara_aeh)
	a_sound_sara_orh = "^เ(สน|ฉพ)"+"("+tone+")?าะ"
	a_sound.append(a_sound_sara_orh)
	a_sound_sara_am = "^(ขน|ขม|ขย|ฉน|ฉม|ถน|ผย|สม|ถล)"+"("+tone+")?ำ" 
	a_sound.append(a_sound_sara_am)
	a_sound_sara_ao = "^เ(ขย|ฉล|สน)"+"("+tone+")?า"
	a_sound.append(a_sound_sara_ao)
	a_sound_sara_ai_maimalai = "^ไ(ฉน|ถล|ศล|สว|ผท)"+"("+tone+")?"
	a_sound.append(a_sound_sara_ai_maimalai)
	a_sound_sara_lodrub = "^เ(ผช|ตล|ผอ|ผน|ฉล)ิ([ก-ฮ])"
	a_sound.append(a_sound_sara_lodrub)
	a_sound_mai_hunargard = "^(อล|ปล|ตว|ตล|ผน|ถว|ถล|ถน|ถง|ฉว|ฉล|ฉม|ฉน|ขย|ขน|สม|จร|ขม|สล|สว|สน)ั"+"("+tone+")?[ก-ฮ]"
	a_sound.append(a_sound_mai_hunargard)
	a_sound_sara_oe = "^เ(ผย|สน|สม)"+"("+tone+")?อ"
	a_sound.append(a_sound_sara_oe)
	a_sound_mai_taikhu = "^(เ)(สด|ขบ|สม|จว|อร)็"+"([ก-ฮ])"
	a_sound.append(a_sound_mai_taikhu)
	a_sound_sara_ia = "^เ(สง|กษ)ี(่|้|๋|๊)?ย(ม|ณ)|^เ(ฉล)ี(่|้|๋|๊)?ย"
	a_sound.append(a_sound_sara_ia)
	a_sound_sara_or = "^(อล|อร|ปร|ถน|ขน|ขม|ขย|ฉม|ฉล|ถล|ผง|ผย|สน|สย|สล|ตล|ขม)"+"("+tone+")?อ([ก-ฮ])|^(สมอง|สมอ)"
	a_sound.append(a_sound_sara_or)
	a_sound_sara_o = "^โ(ตน|สร|ฉน|สด|ฉล|พย)(่|้|๋|๊)?(ก|ง|ม|ด)|โ(สน)"
	a_sound.append(a_sound_sara_o)
	a_sound_sara_i = "^(สน)ิ(่|้|๋|๊)?(ท)|^(ขม|ขย)ิ(่|้|๋|๊)?(บ)|^(จร|ขย)ิ(่|้|๋|๊)?(ก)|^(สน|ขย|ถน)ิ(่|้|๋|๊)?(ม)|^(สย|ฉล)ิ(่|้|๋|๊)?(ว)|^(ถว)ิ(่|้|๋|๊)?(น)|^(ถว)ิ(่|้|๋|๊)?(ล)|^(ผน|ตง)ิ(่|้|๋|๊)?(ด)|^(จร|ผล)ิ(่|้|๋|๊)?(ต)|^(ตล|สว|สม)ิ(่|้|๋|๊)?(ง)|(อร)ิ"
	a_sound.append(a_sound_sara_i)
	a_sound_sara_ee = "^(ฉล)ี(ก)|^(สม|ขม|ถล|ฉว)ี"
	a_sound.append(a_sound_sara_ee)
	a_sound_sara_ue = "^(อล|อน|สล|ผล|ถม|ถล)ึ(่|้|๋|๊)?(ก|ง)"
	a_sound.append(a_sound_sara_ue)
	a_sound_sara_aa = "^เ(ศว|ศล|ฉล|กษ|สบ|สว|ลบ)(ต|ษ|ม|ย|ว|ง)|^เ(ถล|สน่)"
	a_sound.append(a_sound_sara_aa)
	a_sound_sara_euah = "^เ(สม|ขย)ื(่|้|๋|๊)?อ(น)|^เ(อล)ื(่|้|๋|๊)?อ"
	a_sound.append(a_sound_sara_euah)
	a_sound_sara_v = "^(ผน|ฉม)ว(ก)|^(ปร|ขม|จร)ว(ด)|^(สน|สง|ขม|ฉน)ว(น)|^(สล|ฉม|ฉล)ว(ย)|^(ผน)ว(ช)"
	a_sound.append(a_sound_sara_v)
	a_sound_sara_ia = "^เ(กษ|สล|สม|สน|ฉน|ฉว|สถ|สบ|สว)ี(่|้|๋|๊)?ย(ด|ร|ง|น)"
	a_sound.append(a_sound_sara_ia)
	a_sound_sara_ae = "^แ(สว|สล|สย|ถล|ฉล|สบ|สด|สต|ขย|มล)(่|้|๋|๊)?(ก|ง|ม|บ)|แ(สร)ก|แ(ถง)"
	a_sound.append(a_sound_sara_ae)
	a_sound_r = "^(จร|ขน|ฉน|ฉล)(่|้|๋|๊)?า(ก)|^(อล|ขน|ฉล|ฉว)(่|้|๋|๊)?า(ง)|^(สม|สน|ผง|ขน)(่|้|๋|๊)?า(น)|^(ขน)(่|้|๋|๊)?า(บ)|^(สย|ถว|ขน|ขย|ฉง|ฉล)(่|้|๋|๊)?า(ย)|^(ตว|ตล|ผง|ขย|ถง)(่|้|๋|๊)?า(ด)|^(อน)(่|้|๋|๊)?า(ถ)|^(อร|สย|สน|ศย|ฉล)(่|้|๋|๊)?า(ม)|^(สว|สล|ถล|สง|ผว)(่|้|๋|๊)?า"
	a_sound.append(a_sound_r)
	a_sound_sara_u = "^(สม)ุ(่|้|๋|๊)?(ทร)|^(สม)ุ(่|้|๋|๊)?(ด)|^(ถล)ุ(่|้|๋|๊)?(ง)|^(อง|ขน)ุ(่|้|๋|๊)?(น)|^(สน|ฉล|ขม|ขย)ุ(่|้|๋|๊)?(ก)|^(สล|ขม|ขย)ุ(่|้|๋|๊)?(บ)|^(ขย)ุ(่|้|๋|๊)?(ย)|^(อร|สย|ขย)ุ(่|้|๋|๊)?(ม)|^(สร)ุ(่|้|๋|๊)?(ป)|^(สล)ุ(่|้|๋|๊)?(ต)|^(ฉล|สม)ุ(่|้|๋|๊)?"
	a_sound.append(a_sound_sara_u)
	a_sound_sara_uu = "^(ตม|จม)ู(ก)|^(ฉล)ู"
	a_sound.append(a_sound_sara_uu)
	a_sound_sara_rr = "^(สว)รร"
	a_sound.append(a_sound_sara_rr)
	a_sound_c = "^(ปล|ตล|กน|ผง|ถล)(่|้|๊|๊)?(ก)|^(ขน)(่|้|๊|๊)?(ง)|^(จร|สล|ขน|ขย)(่|้|๊|๊)?(ด)|^(จร)(่|้|๊|๊)?(ส)|^(สน|ขน|ฉง|ถน|ถล)(่|้|๊|๊)?(น)|^(ตล|สล|สย|ขน|สง)(่|้|๊|๊)?(บ)|^(สย|สน|ผง|ถล|ขน|ขย|ขร)(่|้|๊|๊)?(ม)"
	a_sound.append(a_sound_c)

	#a_sound_sara_r = "^(ขน|ขย|ฉง|ฉน|ฉล|ฉว|ถง|ถว|ผง|สน|สย|สล)"+"("+tone+")?า([ก-ฮ])|^(ศย)า(ม)?|^(ถล)า(ก|ย)?|^(สว)"+"("+tone+")?"+"า(ง|ท)?"

	def callPhlongTaIam(sent):
		#===ลบอักขระพิเศษ===#
		find = re.search("[\d]+|ฯ|\s",sent)
		if find:
			sent = sent.replace(find.group(0),"")
		if sent != "":
			url = "http://27.254.94.12/owcut/wcut.php?string="
			response = requests.get(url+sent)
			response = response.json()
			data = response.get("words")
		else:
			data = ""
		#print (data)
		return data

	def callThphonemes(Klon):
		print (Klon)
		# url = "https://th-phonetic.herokuapp.com/?poemsy="
		url = "http://170.64.173.219:8888/th-phonetic.php?poemsy="
		response = requests.get(url+Klon)
		response = response.json()
		data = response.get("phonetic")
		print ("phonemes",data)
		return data

	def replaceKaran(word):
		find = re.search("([ก-ฮ](ิ|ุ)์|ษมณ์|ดร์|ทร์|ตร์|ทน์|ษณ์|ริย์|ฎร์|[ก-ฮ]์)",word) #ศิษย์ ลักษมณ์ จันทร์ เวทมนตร์ ลักษณ์ กาญจน์ กษัตริย์
		if find:
			word = word.replace(find.group(0),"")
		print ("===>",word)
		return word

	def backPayang(word,payang):
		length = len(word) - len(payang)
		if len(word) == 2:
			payang = word[0]
		elif word[len(payang)] in sara_after:
			payang = payang[:-1]
		elif word[len(payang)] in consonant and length == 1 and word[len(payang)-1] not in sara_after:
			payang = payang[:-1]
		return payang

	def findRue(word):
		newword = word
		if len(word) > 2:
			find = re.search("ฤกษ์",word)
			find1 = re.search("(ฤทธิ์|ฤท)",word)
			find2 = re.search("(ค|น|พ|ม|ห)ฤ",word) #รึ
			find3 = re.search("(ก|ต|ท|บ|ป|ศ|ส|ห)ฤ",word)#ริ
			find4 = re.search("ฤ",word) 
			if find:
				newword = word.replace("ฤกษ์","เริก")
			elif find1:
				newword = word.replace(find1.group(0),"ริด")
			elif find2:
				newword = word.replace("ฤ","รึ")
			elif find3:
				newword = word.replace("ฤ","ริ")
			elif find4:
				newword = word.replace("ฤ","รึ")
		return newword

	def finda_sound(word):
		#print (word,"finda_sound")
		newWord = word
		#print (len(a_sound))
		for rule in a_sound:
			#print (rule)
			find = re.search(rule,word)
			#print (find)
			if find:
				print ("พบ")
				match = find.group(0)
				#print ("ที่พบ",match)
				if match[0] in ['เ','ไ','แ','โ'] and match[1]+match[2] in aksonnam:
					newWord = word[1]+"ะ"+word[0]+"ห"+word[2:]

				elif match == "สวรร":
					newWord = word[0]+"ะ"+"หวัน"+word[4:]

				elif match[0]+match[1] in aksonnam:
					newWord = word[0]+"ะ"+"ห"+word[1:]

				else:
					#print ("ไม่ใช่อักษรนำ")
					newWord = word[1]+"ะ"+word[0]+word[2:]
				break
		print ("w",newWord)
		return newWord

	def findPayang(word,list_payang):
		print ("คำที่มาตัดพยางค์",word)
		payang = "N"
		if word[0] in consonant:
			for r in rule_consonant:
				find = re.search(r,word)
				if find:
					payang = find.group(0)
					#print (r,payang)
					break
		elif word[0] == 'เ':
			for r in rule_sara_aa:
				#print ("rule",r)
				find = re.search(r,word)
				if find:
					payang = find.group(0)
					break
		elif word[0] == 'ใ':
			find = re.search(sara_ai_maimuan,word)
			if find:
				payang = find.group(0)
		elif word[0] == 'ไ':
			find = re.search(sara_ai_maimalai,word)
			if find:
				payang = find.group(0)
		elif word[0] == 'แ':
			for r in rule_sara_ae:
				find = re.search(r,word)
				if find:
					payang = find.group(0)
					break
		elif word[0] == 'โ':
			for r in rule_sara_o:
				find = re.search(r,word)
				if find:
					payang = find.group(0)
					break
		
		print("พยางค์ที่ตัดได้",payang)


		#คำหลายพยางค์
		if payang != "N":
			if len(word) > len(payang):
				print ("คำหลายพยางค์")
				payang = backPayang(word,payang)
				print ("ย้อนอักษร")
				list_payang.append(payang)
				print("ลิส",list_payang)
				word = word[len(payang):]
				word = replaceKaran(word)
				print ("การันนน")
				word = finda_sound(word)
				print ("อักษรนำ")
				findPayang(word,list_payang)
			else:
				list_payang.append(payang)
		print ("ลิสพยางค์")
		return list_payang

	def checkFinal(listpayang):
		cf = ['ฐ','ต','ฒ']
		aList = listpayang
		sara = ['ิ','ี','ึ','ื','ุ','ู','่','้','๊','๋','ะ','า','ำ']
		sara_na = ['ใ','ไ','โ','แ','เ']
		if len(listpayang) > 1:
			for x in range(0,len(listpayang)-1):
				if listpayang[x][-1] not in sara and listpayang[x][-1] in ['จ','ป','ต','ช','พ','ศ','ษ','ล','ณ','ธ'] and len(listpayang[x])>1 and listpayang[x][0] not in sara_na and listpayang[x+1][0] != listpayang[x][-1]:
					#if listpayang[x+1][0] in ['เ']:
					#	if listpayang[x][-1]+listpayang[x+1][1] not in ['ชฌ']:
					#		addpayang = listpayang[x][-1]+"ะ"
					#		aList.insert(x+1, addpayang)

					if listpayang[x][-1]+listpayang[x+1][0] not in ["จฉ",'ปผ','ตถ','ชฌ','พภ','จส','ศห','ษฐ','ลห','ณค','ศพ','ชผ','พส','ชฌ','ตบ','ณง','ธร','จด','ศท','ชไ','ษด','ชฌ','ณห'] and listpayang[x] not in ['ผล','มวล','ดล','ตรวจ']:
						addpayang = listpayang[x][-1]+"ะ"
						aList.insert(x+1, addpayang)

				elif listpayang[x][-1] not in sara and listpayang[x][-1] == "ท" and len(listpayang[x])>1 and listpayang[x][0] not in sara_na and listpayang[x+1][0] != listpayang[x][-1]:
					if listpayang[x][-1]+listpayang[x+1][0] in ["ทย"]:
						addpayang = listpayang[x][-1]+"ะ"
						aList.insert(x+1, addpayang)


				elif listpayang[x][-1] not in sara and listpayang[x][-1] == "ส" and len(listpayang[x])>1 and listpayang[x][0] not in sara_na and listpayang[x+1][0] != listpayang[x][-1] and listpayang[x] not in ['รส']:
					if listpayang[x][-1]+listpayang[x+1] in ["สนา"]:
						listpayang[x+1] = "หนา"
						addpayang = listpayang[x][-1]+"ะ"
						aList.insert(x+1, addpayang)
					
					elif listpayang[x][-1]+listpayang[x+1][0] not in ["สต"]:
						addpayang = listpayang[x][-1]+"ะ"
						aList.insert(x+1, addpayang)
				 	
				elif listpayang[x][-1] not in sara and listpayang[x][-1] in cf and len(listpayang[x])>1 and listpayang[x][0] not in sara_na and listpayang[x+1][0] != listpayang[x][-1] and listpayang[x] not in ["ผล",'ศล','ธิษ']:
					addpayang = listpayang[x][-1]+"ะ"
					aList.insert(x+1, addpayang)

		return aList

	#เพิ่มเครื่องหมายขีดขั้นกลางเพื่อส่งให้ Thphonemes
	def addHyphen(payang):
		newpayang = ""
		for i in range(len(payang)):
			if i == (len(payang)-1):
				newpayang = newpayang + payang[i]
			else:
				newpayang = newpayang + payang[i] + "-"
		return newpayang

	def jsonOutput(payang,wak):
		phonemes = callThphonemes(payang)
		i = 0
		j = 0
		dict_output = {}

		for word in wak:
			for w in word:
				json = {}
				length = len(wak[i][w])
				syll = []
				for l in range(length):
					syll.append(phonemes[j])
					j = j+1
				pn = addHyphen(syll)
				json["phonemes"] = pn
				py = addHyphen(wak[i][w])
				json["payang"] = py
				json["word"] = w
				
			dict_output[i+1] = json
			i = i + 1
		return dict_output

	def changefinalconsonant(listpayang):
		print(listpayang)
		newlistpayang = []
		newpayang = ""
		length = len(listpayang)-1
		print (length)

		for i in range(len(listpayang)):

			find = re.search("(รติ|ตร|ตุ|ติ|ทธ|ฒิ|รท)$",listpayang[i])
			find1 = re.search("จักร",listpayang[i])
			find3 = re.search(".รร$",listpayang[i])
			find4 = re.search(".รร.$",listpayang[i])
			if i == length:
				if find and len(listpayang[i])>2 and listpayang[i] not in ['ไตร']:
					newpayang = listpayang[i].replace(find.group(0),"ด")
					newlistpayang.append(newpayang)
				elif find1:
					newpayang = listpayang[i].replace(find1.group(0),"จัก")
					newlistpayang.append(newpayang)
				elif find3:
					newpayang = listpayang[i][0]+"ัน"
					newlistpayang.append(newpayang)
				elif find4:
					newpayang = listpayang[i][0]+"ั"+listpayang[i][-1]
					newlistpayang.append(newpayang)				
				else:
					newlistpayang.append(listpayang[i])
			else:
				if find and listpayang[i] in ['เกียรติ','พรึติ']:
					newpayang = listpayang[i].replace(find.group(0),"ด")
					newlistpayang.append(newpayang)
					newlistpayang.append("ติ")

				elif find and listpayang[i] in ['มาตร','จิตร']:
					newpayang = listpayang[i].replace(find.group(0),"ด")
					newlistpayang.append(newpayang)
					newlistpayang.append("ตระ")
				
				elif find and listpayang[i] in ['พุทธ']:
					newpayang = listpayang[i].replace(find.group(0),"ด")
					newlistpayang.append(newpayang)
					newlistpayang.append("ทะ")

				elif find1:
					newpayang = listpayang[i].replace(find1.group(0),"จัก")
					newlistpayang.append(newpayang)
					newlistpayang.append("กระ")

				elif find and len(listpayang[i])>2 and listpayang[i] not in ['ไตร']:
					newpayang = listpayang[i].replace(find.group(0),"ด")
					newlistpayang.append(newpayang)

				elif find3:
					newpayang = listpayang[i][0]+"ัน"
					newlistpayang.append(newpayang)
				
				elif find4:
					newpayang = listpayang[i][0]+"ั"+listpayang[i][-1]
					newlistpayang.append(newpayang)	

				else:
					newlistpayang.append(listpayang[i])
		return newlistpayang

	def checkAksonkuapmaitae(listpayang):
		maitae = {'ซร':'ซ','ศร':'ส','ทร':'ซ','สร':'ส','หณ':'หน'}
		match = ""
		newlistpayang = []
		for payang in listpayang:
			newpayang = payang
			if len(payang) > 2 and payang not in ['โทร','ทรา']: #จันทรา #พุทรา 
				find = re.search("(ซร|ศร|ทร|สร|หณ)",payang)
				if find:
					match = find.group(0)
					akson = maitae[match]
					newpayang = payang.replace(match,akson)
			newlistpayang.append(newpayang)
		return newlistpayang

	def checkconsonantLengthOne(listpayang):
		aList = listpayang
		if len(listpayang) > 1:
			for i in range(0,len(listpayang)-1):
				if listpayang[i] == "บ":
					addpayang = "บอ"
					aList[i] = addpayang
				elif len(listpayang[i]) == 1 and listpayang[i] in consonant:
					addpayang = listpayang[i]+"ะ"
					aList[i] = addpayang
		return aList

	def checkTuaRor(listpayang):
		aList = listpayang
		if len(listpayang) > 1:
			if listpayang[0] in ['จร','ทร','ธร','นร','วร','มร','อร']:
				addpayang = listpayang[0][0]+"อ"
				aList[0] = addpayang
				aList.insert(1,'ระ')

		return aList

	def checkWord(words):
		#ขรุขระ
		listklon = []
		length = len(words)
		i = 0
		while(i<length):
				#print (i)
			if len(words[i]) == 1 and len(words) > 1 and i != length-1:
				newWord = words[i]+words[i+1]
				listklon.append(newWord)
				i = i+2
			else:
				listklon.append(words[i])
				i = i+1
		return listklon

	def KamKom(sent):
		print (sent)
		data = {}
		with open('KK.json') as json_data:
			data = json.load(json_data)

		#print (data)
		prob = {}

		with open("prob.txt") as f:
			for line in f:
				prob = ast.literal_eval(line)
		#print ("prob",len(prob))

		def findindex(sent):
			index = ""
			words = []
			for d in data:
				words.append(d)
			#print (words)
			for i in range(0,len(sent)):
				for j in range(len(words)):
					if sent[i] == words[j]:
						index = i
						break
			return index

		def find_bigrams(input_list):
		  bigram_list = []
		  for i in range(len(input_list)-1):
		      bigram_list.append((input_list[i], input_list[i+1]))
		  return bigram_list

		def findvalue(pair):
			value = 0
			for p in prob:
				if pair == p:
					value = prob[pair]
			return value

		index = findindex(sent)
		
		if index != "":
			sentAll = []
			kamkom = data[sent[index]]

			for i in range(0,len(kamkom)):
				sent[index] = kamkom[i]
				sentAll.append(list(sent))

			#print ("sentAll",sentAll)
			#print (index)
			#สองประโยคที่จะเอาไปคำนวณหาค่าความน่าจะเป็น
			print ("\n")
			bigrams_list = []
			valueAll = []
			if index == 0:
				for s in sentAll:
					se = []
					se.append((s[0],s[1]))
					bigrams_list.append(se)
			elif index == len(sent)-1:
				for s in sentAll:
					se = []
					se.append((s[0],s[1]))
					bigrams_list.append(se)
			else:
				for s in sentAll:
					se = []
					se.append((s[index-1],s[index]))
					se.append((s[index],s[index+1]))
					print (se)
					bigrams_list.append(se)
			print ("bigrams",bigrams_list)


			#bigrams_list = [find_bigrams(d) for d in sentAll]

			for bigram in bigrams_list:
				#print(bigram)
				value = []
				for bi in bigram:
					#print (bi)
					v = findvalue(bi)
					value.append(v)
					#if v != 0:
					#	value = value*v

				valueAll.append(value)

			cal = []
			valuelast = []
			valuestart = 1
			print ("valueAll",valueAll)

			for i in range(len(valueAll)):
				j = 0
				for k in valueAll[i]:
					if k == 0:
						j = j+1
				#print (j)
				if j == len(valueAll[i]):
					cal.append((i,0))
					valuelast.append(0)
				else:
					for l in valueAll[i]:
						if l != 0:
							valuestart = valuestart*l
					cal.append((i,valuestart))
					valuelast.append(valuestart)

			print (cal)
			print ("valuelast",valuelast)
			print (sentAll)
			#print (valueAll)
			sentProbMax = []
			valueMax = max(valuelast)
			print (valueMax)
			for k,v in cal:
				if v == valueMax:
					sentProbMax = sentAll[k]
					break;

			#print (indexMax)
			#sentProbMax = sentAll[indexMax]
			print (sentProbMax)
			newsentProbMax = []
			for sent in sentProbMax:
				words = sent.split("-")
				for w in words:
					newsentProbMax.append(w)
			print("ประโยคที่สมบูรณ์",newsentProbMax)
			sent = list(newsentProbMax)

		return sent


	def readData(word):
		# words = callPhlongTaIam(word)
		words = pythainlp.tokenize.word_tokenize(word)
		print ("\nตัดคำ : ",words,"\n")
		if len(words) > 1:
			words = KamKom(words)

		words = checkWord(words)
		print("words",words)
		payang = []
		wak = []
		with open('words.json') as json_data:
		    data = json.load(json_data)

		#print ("คำในDict",len(data))
		for word in words:
			print ("word2",word)
			list_payang = []
			
			find = re.search("[a-zA-Z]+",word)
			if find:
				print ("พบ")
				list_payang.append(word)
				dict_payang = {}
				dict_payang[word] = list_payang
				wak.append(dict_payang)
				payang = payang + [p for p in list_payang]
			
			else:
				w = findRue(word)
				
				for d in data:
					find = re.search(d,w)
					if find:
						w = w.replace(d,data[d])
				
				w = finda_sound(w)
				w = replaceKaran(w)
				print ("การันต์",w)
				listp = findPayang(w,list_payang)
				print ("****พยางค์",listp)
				list_payang = changefinalconsonant(listp)#เช็คคำที่มีตัวสะกด 2 ตัวเช่น เมตร *
				print ("****เช็คคำที่มีตัวสะกด 2 ตัว",list_payang)
				listpII = checkAksonkuapmaitae(list_payang)#ตรวจอักษรควบไม่แท้ และแปลงอักษรควบไม่แท้
				print ("****ตรวจอักษรควบไม่แท้",listpII)
				list_payang = checkFinal(listpII)
				print ("****ตรวจสอบพยางที่ลงท้ายไม่ตรงตามมาตราตัวสะกด",list_payang)
				list_payang = checkconsonantLengthOne(list_payang)
				print ("****ตรวจสอบพยางค์ที่มีความยาว == 1",list_payang)
				print ("--",list_payang)
				list_payang = checkTuaRor(list_payang)
				print ("list_payang",list_payang)
				dict_payang = {}
				dict_payang[word] = list_payang
				wak.append(dict_payang)
				payang = payang + [p for p in list_payang]

		payang = addHyphen(payang)
		#w = open("orathai11.txt","a+")
		#w.write(str(words)+str(payang)+"\n")
		print (payang)
		june = jsonOutput(payang,wak)
		print (june)
		return june

	def readFile(namefile):
		f = open(namefile)
		words = f.readlines()
		words = [word[:-1] for word in words] #clean \n
		for word in words:
			readData(word)
			#print (findPayang(word))
	#word = "ศิษย์"
	#word = "กรรณ"
	#word = "ฃะ"
	#print (replaceKaran(word))
	#print (rrHun(word))
	#print (findPayang(word))
	#readFile("cutwordtest1.txt")
	#readData("ลำไส้ไข่มากนักพิษปักเป้า")
	#words = "มนุษยศาสตร์"
	#words = "เสน่ห์"
	#words =  ""
	#words = "เขย่าขยะขนำ"
	#print("***")
	#a = ['นิจ','สิน']
	#print (checkFinal(a))
	try:
		jsonjune = readData(word)
		print (jsonjune)
		return {'message': jsonjune}
	except:
		return {'message' : "ไม่พบคำที่ค้นหา"}
	#return {'message' : reader2(word)}
	#return json.dumps(june)



if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

