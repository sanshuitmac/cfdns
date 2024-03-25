import json
import os

import requests


# 读取txt的ip文件
def read_txt(file_path):
    global ip_list
    # 读取文本文件
    with open(file_path, 'r') as file:
        # 逐行读取文件内容
        for line in file:
            # 去除每行末尾的换行符并添加到列表中
            ip_list.append(line.strip())


"""
request得到的请求响应对象数据处理，json处理：
①response.json(): 这个方法会尝试将响应内容解析为 JSON 格式（对象），并返回对应的 Python 字典。如果响应内容不是有效的 JSON 格式，那么会引发 json.decoder.JSONDecodeError 异常。
②response.text: 这个方法返回响应内容的原始文本，以字符串的形式返回。仍需要 json.load(s) 获得json格式数据， 参数s只能是字符串或者字符串字节数组，不能是字典
③json格式数据获取key两种方法 如json_re =response.json()  a：字典方法： json_re.get('key') 或者b:索引方法 json_re['key']获取value。具体见下方应用
"""


# 更新cf的dns记录
def update_dns_records(email, global_key, zone_id, domain, ip_list):
    # 获取当前域名的记录列表
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=A&name={domain}'
    headers = {
        'X-Auth-Email': email,
        'X-Auth-Key': global_key,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    records = response.json()['result']
    print('删除原有dns记录。')
    # 删除已存在的记录
    for record in records:
        delete_url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record["id"]}'
        requests.delete(delete_url, headers=headers)

    # 添加优选ip进域名新记录
    print('正在新增新的dns记录...')
    for ip_address in ip_list:
        # 添加新的记录
        data = {
            'type': 'A',
            'name': domain,
            'content': ip_address,
            'ttl': 1,
            'proxied': False
        }
        add_url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
        response = requests.post(add_url, json=data, headers=headers)
        response_json = response.json()  # Response对象转json对象，无需再json.load(X) 也会提示类型错误。
        # print(response_json)
        result = response_json["success"]  # json对象直接获取key，方法可以json['key'] 或者json.get('key')

        if result:
            print(f'{ip_address}\t新增dns记录成功')


# 发送 GET 请求
def send_get_request(url):
    response = requests.get(url)
    return response.text  # response是Response类型对象，这个response.text是字符串类型，


# 发送 POST 请求
def send_post_request(url, data):
    response = requests.post(url, data=data)
    return response.text


# 解析接口响应，获取所有优选ip列表
def get_best_ip(response_str):
    response_json = json.loads(response_str)  # 解析json串为json对象的工具：json.loads(response)。形参是字符串
    goods_list = response_json["data"]["good"]
    # print(goods_list)
    ip_lists = [item["ip"] for item in goods_list]
    print(ip_lists)
    return ip_lists


if __name__ == "__main__":
    # 读取本地已经优选好的txt的ip列表：
    # ip_list = []
    # file_path = 'D:/VPN/updateDns/ip.txt'
    # read_txt(file_path)
    # print(ip_list)

    # 发送请求到指定接口获取优选ip列表
    url = 'https://vps789.com/vps/sum/cfIpTop20'
    # 发送get请求到接口获取json串
    response = send_get_request(url)
    # 解析json串获取所有优选ip列表
    ip_list = get_best_ip(response)
    # 获取ip_lists前5个
    best5_ip_list = ip_list[:5]

    # 更新至cf域名： CloudFlare API相关必要参数信息，通过github环境变量设置
    EMAIL_NAME = os.environ.get("EMAIL")
    GLOBAL_KEY_TOKEN = os.environ.get("GLOBAL_KEY")
    ZONE_ID_TOKEN = os.environ.get("ZONE_ID")
    DOMAIN_NAME = os.environ.get("DOMAIN")

    # 更新cf域名记录为最新5个优选ip
    update_dns_records(EMAIL_NAME, GLOBAL_KEY_TOKEN, ZONE_ID_TOKEN, DOMAIN_NAME, best5_ip_list)
