import requests,json

data={
    "name":"AUTO",
    "lastName":"SHUANG",
    "secondLastName":"TEST"
}
head={"ApiKey":"ngkgi7CQ","Content-Type": "application/json;charset=UTF-8"}
r=requests.post('https://web-prod01.tuidentidad.com/api/BackgroundCheck/physicalPerson',data=json.dumps(data),headers=head)
print(r.json())