import json,requests
import uuid
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from flask import current_app
'''   url: http://192.168.12.45:5000/model
    urlv2: http://192.168.12.45:5002/model
    urlv3: http://192.168.12.45:5003/model
    urlv4: http://192.168.12.45:5014/model
'''
bucket_name = 'mex-pdl'
s3_client = boto3.client('s3')
# 所有桶
def list_bucket():
    response = s3_client.list_buckets()
    names = []
    for bucket in response['Buckets']:
        names.append(bucket["Name"])
    return names
def create_presigned_url(bucket_name, object_name, expiration=3600):
    try:
        response = s3_client.generate_presigned_url('get_object',Params={'Bucket': bucket_name,'Key': object_name},
                                                                 ExpiresIn=expiration)
    except ClientError as e:
        print(e)
        return None
    return response
def buildQueryParams(obj_key):
    return json.dumps({
        "apply_id": str(uuid.uuid4()),
        "brand_list": [
            "OkPrestamos",
            "DiCredito",
            "Flash Peso",
            "iCrédito",
            "Quikrédito",
            "ConFiar",
            "Mipeso",
            "Baubap",
            "Captarcash",
            "CASHCASH",
            "Credilikeme",
            "Creditea",
            "iFectivo",
            "Inscash",
            "iPeso",
            "Kueski",
            "lendOn",
            "lime",
            "Moneyman",
            "OKredito",
            "ListoCash",
            "SmartLoan",
            "<Lcash>",
            "CrediYa",
            "FusMoney",
            "prestamospersonales",
            "Cashbox",
            "Crediti",
            "Aprestamo",
            "Credifranco",
            "Kabil",
            "vencash",
            "Creavi",
            "Maxcredito",
            "FastPrestamos",
            "okredit",
            "Super Prestamo",
            "GoCredito",
            "Superapoyo",
            "OKPeso",
            "Mascash",
            "HolaPeso",
            "RapiCredito",
            "VaCash",
            "pagatala",
            " Tala",
            "Tala ",
            "Tala.",
            "Tala!",
            "Incash",
            "Marmaja",
            "CashYa",
            "Órale Crédito",
            "Máximo",
            "OkCrédito",
            "IsiCredit",
            "YumiCash",
            "Paay",
            "Prestamos Personales Urgentes",
            "Moneyme",
            "Rayito Money",
            "SiCredito",
            "EasyCash",
            "Creditlends",
            "Dinero Mágico",
            "CreditoMax",
            "EnviarDinero",
            "FlamingoCash",
            "mioprestamo",
            "SúperPeso",
            "Credit Cash",
            "Credmex",
            "ApPesito",
            "Galaxia",
            "PesoLends",
            "CrediFacil",
            "PesoHub",
            "Mangocredy",
            "PesoX",
            "PPcredito",
            "CentaBoss",
            "XFectivo",
            "MasLana",
            "PesoPrestamos"
        ],
        "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "msg_data": create_presigned_url('mex-pdl', obj_key)})

head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "es","accept-encoding": "gzip","content-length": "63",
          "host": "192.168.12.45","content-type": "application/json"}
def make_data():
    obj_key ='201/20210504/2211020217/11090005_1620162742066.json'
    req = buildQueryParams(obj_key)
    print(req)
    r=requests.post('http://192.168.12.45:5500/app_model_v1',data=req,headers=head)
    print(r.json())
#生成签名等，解决接口响应报错："err_msg":"Download sms file fail: Request has expired"
def pre_signed_url(object_name, expiration=3600):
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
        return response
    except ClientError as e:
        current_app.logger.error(e)
        return None
    return response

if __name__ == '__main__':
    data=pre_signed_url('201/20210504/2211004373/11090001_1620172496471.json',expiration=3600)
    print(data)