import pandas as pd
import numpy as np
import joblib
import json
import pymysql
import re
import scorecardpy as sc
import traceback
from flask import request

#prepare lists
pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'

keyword_list = ['vence pronto','recibido tu pago','prestamo','vencido','no ','u pago','atraso','vence hoy','solucion','gracias por tu solicitud','evitar','recibio su reembolso','dia de pago']

#keyword_length
keyword_len = {}
for i in keyword_list:
    keyword_len[i] = len(list(filter(None,re.split(pattern,i))))

#bins
bins = {'vence pronto':pd.DataFrame([['vence pronto', '0.0', 0.09413192711028394], ['vence pronto', '[-inf,0.0006000000000000001)', 0.10527627860561589], ['vence pronto', '[0.0006000000000000001,0.0014)', -0.13438280250669005], ['vence pronto', '[0.0014,0.0036000000000000003)', -0.4841406966461238], ['vence pronto', '[0.0036000000000000003,inf)', -1.1161786078002012]],columns = ['variable', 'bin', 'woe']),
        'recibido tu pago':pd.DataFrame([['recibido tu pago', '0.0', 0.14748573300090637], ['recibido tu pago', '[-inf,0.001)', 0.13858232845342097], ['recibido tu pago', '[0.001,0.002)', -0.18547720241160578], ['recibido tu pago', '[0.002,0.006)', -0.43490361313952186], ['recibido tu pago', '[0.006,inf)', -1.1687759312289931]],columns = ['variable', 'bin', 'woe']),
        'prestamo':pd.DataFrame([['prestamo', '0.0', 1.2526584916630104], ['prestamo', '[-inf,0.011)', 0.7496130552159821], ['prestamo', '[0.011,0.016)', 0.25044461657720163], ['prestamo', '[0.016,0.019)', -0.1747631608807431], ['prestamo', '[0.019,inf)', -0.4732337083814186]],columns = ['variable', 'bin', 'woe']),
        'vencido':pd.DataFrame([['vencido', '0.0', -0.08378372370414063], ['vencido', '[-inf,0.0006000000000000001)', -0.08051402639793054], ['vencido', '[0.0006000000000000001,0.0009000000000000001)', 0.4640310351475623], ['vencido', '[0.0009000000000000001,inf)', 0.675364163232056]],columns = ['variable', 'bin', 'woe']),
        'no ':pd.DataFrame([['no ', '0.0', 0.1842468880433177], ['no ', '[-inf,0.011)', -0.23180911959958012], ['no ', '[0.011,0.012)', 0.06309400926538399], ['no ', '[0.012,0.013000000000000001)', -0.0847579079194389], ['no ', '[0.013000000000000001,inf)', 0.34923698848563245]],columns = ['variable', 'bin', 'woe']),
        'u pago':pd.DataFrame([['u pago', '0.0', 0.7248212198575216], ['u pago', '[-inf,0.003)', 0.5825558544419484], ['u pago', '[0.003,0.007)', 0.03925671340676643], ['u pago', '[0.007,0.01)', -0.11556054883130891], ['u pago', '[0.01,inf)', -0.3378291928108616]],columns = ['variable', 'bin', 'woe']),
        'atraso':pd.DataFrame([['atraso', '0.0', -0.07107913501144787], ['atraso', '[-inf,0.0005)', -0.07968541197577356], ['atraso', '[0.0005,0.0013000000000000002)', 0.5670319707207743], ['atraso', '[0.0013000000000000002,inf)', 1.0134831288003041]],columns = ['variable', 'bin', 'woe']),
        'vence hoy':pd.DataFrame([['vence hoy', '0.0', 0.018044802888123886], ['vence hoy', '[-inf,0.001)', 0.021941437260911505], ['vence hoy', '[0.001,0.002)', -0.04224505977391905], ['vence hoy', '[0.002,0.003)', -0.09456532457575885], ['vence hoy', '[0.003,inf)', -0.13370056587144338]],columns = ['variable', 'bin', 'woe']),
        'solucion':pd.DataFrame([['solucion', '0.0', -0.060519286739180465], ['solucion', '[-inf,0.00030000000000000003)', -0.05455343617001115], ['solucion', '[0.00030000000000000003,inf)', 0.8771891702076821]],columns = ['variable', 'bin', 'woe']),
        'gracias por tu solicitud':pd.DataFrame([['gracias por tu solicitud', '0.0', -0.06760201697139646], ['gracias por tu solicitud', '[-inf,0.001)', -0.06303367655542998], ['gracias por tu solicitud', '[0.001,0.002)', 0.05403139022253776], ['gracias por tu solicitud', '[0.002,0.005)', 0.26903888320518915], ['gracias por tu solicitud', '[0.005,inf)', 0.5124294733479652]],columns = ['variable', 'bin', 'woe']),
        'evitar':pd.DataFrame([['evitar', '0.0', -0.0208887568880818], ['evitar', '[-inf,0.0016)', -0.0703363441235417], ['evitar', '[0.0016,0.0033)', 0.09584161202663746], ['evitar', '[0.0033,inf)', 0.7863444543334926]],columns = ['variable', 'bin', 'woe']),
        'recibio su reembolso':pd.DataFrame([['recibio su reembolso', '0.0', 0.0083265649178605], ['recibio su reembolso', '[-inf,0.0002)', 0.00897723901129172], ['recibio su reembolso', '[0.0002,inf)', -0.36069842673453195]],columns = ['variable', 'bin', 'woe']),
        'dia de pago':pd.DataFrame([['dia de pago', '0.0', -0.0018313532581890157], ['dia de pago', '[-inf,0.002)', 0.004932066739237802], ['dia de pago', '[0.002,0.003)', -0.06456617430995404], ['dia de pago', '[0.003,0.004)', -0.03494532519260794], ['dia de pago', '[0.004,inf)', 0.04748945070544145]],columns = ['variable', 'bin', 'woe'])}

def getscore_msgmodelv4(json_path,brand_list):
    try:
        #read json into dataframe
        features = []
        data = open(json_path,'rb')
        data = json.load(data)
        df = pd.DataFrame(data)
        print('df1111111=',df)
        #data cleaning
        df['body'] = [str(body).lower() for body in df.pop('body')] #lower body
        df = df[[str(body)[:10] != '[lanaplus]' for body in df['body']]].reset_index()  #drop our msg
        #brand
        hit_brand_list = []
        for i in df['body']:
            hit_brand = 0
            print('i=',i)
            for brand in brand_list:
                if i.find(brand) != -1:
                    hit_brand = 1
                    continue
            hit_brand_list.append(hit_brand)
        df['hit_brand'] = hit_brand_list
        df = df[df['hit_brand'] == 1]
        print('df222222=',df)
        #keyword
        words_num = 0
        dic_key_hit = {}
        for key in keyword_list:
            dic_key_hit[key] = 0
        for i in range(0,len(df)):
            data = df.iloc[i,:]
            words_list = list(filter(None, re.split(pattern, str(data['body'])))) #不包含空格了
            words_num += len(words_list)
            for key in keyword_list:
                if str(data['body']).find(key)!= -1:
                    dic_key_hit[key] += 1
        #TF-term frequency
        keyword_tf = {}
        for i in keyword_list:
            if len(df) != 0:
                tf = keyword_len[i]*dic_key_hit[i]/words_num
                keyword_tf[i] = [tf]
            else:
                keyword_tf[i] = [np.NaN]
        #Woe
        keyword_tf = pd.DataFrame.from_dict(keyword_tf)
        tf_woe = sc.woebin_ply(keyword_tf,bins)
        tf_woe = tf_woe[['vence pronto_woe','recibido tu pago_woe','prestamo_woe','vencido_woe','no _woe','u pago_woe','atraso_woe','vence hoy_woe','solucion_woe','gracias por tu solicitud_woe','evitar_woe','recibio su reembolso_woe','dia de pago_woe']]
        features = tf_woe
        model = joblib.load('C:\\Users\\wangshuang\\Desktop\\model.pkl')
        print('model=',model)
        validation_resu = model.predict_proba(features)[0]
        score = validation_resu[1]
        return {"success": 1, "msg_model_score_v4": score, 'hit_brand_msgnum': len(df)
            , "msgv4_features": features.to_json()
            , "err_msg": None
            , "version": 'Msg_Model_V4_20210528'}
    except Exception as e:
        if str(e) == "'body'" or str(e) == "Expecting value: line 1 column 1 (char 0)" :
            return {"success": 1, "msg_model_score_v4": -99, 'hit_brand_msgnum': -99
                  , "msgv4_features": '[]' if features == [] else features.to_json()
                  , "err_msg": None
                  , "version": 'Msg_Model_V4_20210528'}
        elif str(e) == "Input contains NaN, infinity or a value too large for dtype('float64').":
            return {"success": 1, "msg_model_score_v4": -99, 'hit_brand_msgnum': 0
                  , "msgv4_features": '[]' if features == [] else features.to_json()
                  , "err_msg": None
                  , "version": 'Msg_Model_V4_20210528'}
        else:
            #input('Something goes wrong here')
            print(e)
            if features == []:
                f = []
            return {"success": 0, 'err_msg': traceback.format_exc()
                , "msgv4_features": '[]' if features == [] else features.to_json()
                , "t": str(request.data)}

json_path ='C:\\Users\\wangshuang\\Desktop\\11090005_1622698009644.json'
brand_list=['Baubap', 'Captarcash', 'CASHCASH', 'Credilikeme', 'Creditea', 'iFectivo', 'Inscash', 'iPeso']
getscore_msgmodelv4(json_path,brand_list)
