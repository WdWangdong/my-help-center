from contextlib import closing
import datetime
import ftplib
import hashlib
import json
import os
import random
import sys
import getpass
import requests
from loguru import logger as log
import public


def send_api_nei(leixing, zhanghao, name):
    """
    发送内网服务器进行直通车api请求
    :param name: 请求名称
    :param leixing: 查询类型
    :param zhanghao: 账号
    :return: 数据字典
    """
    verify_url = 'http://10.16.2.180:6096/task/ztcapi'
    verify_data = {
        'name': name,
        'leixing': leixing,
        'zhanghao': zhanghao
    }
    ret = requests.request('POST', url=verify_url, json=verify_data).json()
    return ret['data']


def send_api_nei_general(zhanghao, task_type, name=''):
    """
    发送内网服务器进行通用任务处理
    :param zhanghao: 账号
    :param task_type: 任务类型
    :param name: 软件名称
    :return: dict {
        code:状态,
        data:返回的数据格式 *未全面适配 可能有返回的为文本,
        display_mode:显示模式,py项目无效}
    """
    verify_url = 'http://10.16.2.180:6096/task/general'
    verify_data = {
        'zhanghao': zhanghao,
        'task_type': task_type,
        'host_name': getpass.getuser(),
        'name': name
    }
    #print(verify_data)
    ret = requests.request('POST', url=verify_url, json=verify_data).json()
    return ret


def send_api_nei_aaa_info(dict1):
    verify_url = 'http://10.16.2.180:6099/aaa_info'
    verify_data = {
        'zhanghao_info': dict1,
    }
    ret = requests.request('POST', url=verify_url, json=verify_data).json()
    return ret['data']


def send_api_wai(leixing, zhanghao, name):
    """
    发送外网服务器进行直通车api请求
    :param name: 请求名称
    :param leixing: 查询类型
    :param zhanghao: 账号
    :return: 返回数据字典
    """
    verify_url = 'http://ofe6z14.nat.ipyingshe.com/task/ztcapi'
    verify_data = {
        'name': name,
        'leixing': leixing,
        'zhanghao': zhanghao
    }
    # print(verify_data)
    ret = requests.request('POST', url=verify_url, json=verify_data).json()
    return ret['data']


def send_api_dai_wx_msg(name, room_id, msg_text):
    """
    发送代理服务器进行微信消息发送
    :param room_id: 群名
    :param msg_info: 消息类型
    :return:
    """
    verify_url = 'http://ofe6z14.nat.ipyingshe.com/wx/send_str'
    verify_data = {
        'name': name,
        'msg_info': {'room_id': room_id, 'msg_text': msg_text},
    }
    # print(verify_data)
    ret = requests.request('POST', url=verify_url, json=verify_data).json()
    return ret['data']


def send_api_nei_aaa_daikuan(dict1):
    verify_url = 'http://10.16.2.180:6099/aaa_daikuan'
    verify_data = {
        'zhanghao_info': dict1,
    }
    ret = requests.request('POST', url=verify_url, json=verify_data).json()
    return ret['data']


def send_api_nei_account_guangshuai(uid):
    """
    发送内网服务器进行查询账号的光衰
    :param uid:
    :return:
    """
    try:
        verify_url = 'http://10.16.2.180:6099/uid_guanggong'
        verify_data = {
            'zhanghao': uid,
        }
        ret = requests.request('POST', url=verify_url, json=verify_data, timeout=5).json()
        return ret['data']
    except:
        return {'data': [{}]}


def send_api_nei_aaa_jiebang(account):
    """
    发送内网服务器进行查询账号的光衰
    :param account: 账号
    :return:
    """
    try:
        verify_url = 'http://10.16.2.180:6096/task/aaa_jiebang'
        verify_data = {
            'zhanghao': account,
        }
        ret = requests.request('POST', url=verify_url, json=verify_data, timeout=5).json()
        return ret['data']
    except:
        return {'data': [{}]}


def send_api_nei_neikai_account_info(account):
    """
    请求能开平台获取账号数据
    :param account: 账号
    :return: 数据字典
    """
    url = "http://10.20.131.91:11081/ServiceOpenFrame/gate"
    app_key = "1278be8a-6d3c-4553-9e78-506cd381cba1"
    app_secret = "ySn3U68FMnh1WfGmGUzH"
    method = "jiake.resource.userResourceInformation"
    post_headers = {
        "app_key": app_key,
        "app_secret": app_secret,
        "method": method,
        "v": "1"
    }

    adata = {
        "account": account,
    }
    # print(adata)
    ret_data = requests.post(url, headers=post_headers, json=adata).json()
    if ret_data['data']['city'] is not None:
        return ret_data
    else:
        return {'msg': '查询失败'}


def send_api_wai_mdy_log_error(name, value):
    """
    将错误发送到明道云本地软件权限管理系统
    :param name: 软件名称
    :param value: 错误原因
    :return: 无
    """
    try:
        mdy_head = {
            'Content-Type': "application/json"
        }
        mdy_re = requests.session()
        new_dict = {"code": 200, "data": {"zdmc": name, 'cwrz': value}}
        mdy_url = 'http://120.221.159.84:8880/api/workflow/hooks/NjNjMGQ0NTEwYTc3MWE3MmUxOTRlNGFk'
        mdy_re.post(mdy_url, json=new_dict, headers=mdy_head).json()
        return True
    except:
        return False


def send_api_nei_get_server_cookies(u='', name=''):
    """
    获取内网服务器cookes
    :param name: 支持cook: ['ksh','ztctb','ztc','ztcapi','pd','cook','zd'],默认获取cook
    :param u:软件名称
    :return: 返回一个字典
    """
    ret_data = requests.post(url='http://10.16.2.180:6096/cookies', json={'zhanghao': u, 'name': name}).json()
    return ret_data['data']


def send_api_dai_get_server_cookies(u='', name=''):
    """
    获取内网服务器cookes
    :param name: 支持cook: ['ksh','ztctb','ztc','ztcapi','pd','cook','zd'],默认获取cook
    :param u:软件名称
    :return: 返回一个字典
    """
    ret_data = requests.post(url='http://ofe6z14.nat.ipyingshe.com/cookies', json={'zhanghao': u, 'name': name}).json()
    return ret_data['data']


def send_api_wai_mdy_add_log(rj_name, banben, qita=""):
    """
    本地权限工具添加明道云启动日志
    :param rj_name: 软件名称
    :param banben: 版本
    :param qita: 备注
    :return:
    """
    try:
        mdy_head = {
            'Content-Type': "application/json"
        }
        mdy = requests.Session()
        mdy_add_url = 'http://120.221.159.84:8880/api/v2/open/worksheet/addRow'
        mdy_add_data = {
            'appKey': '6f365477c211d998',
            'sign': 'YTI2ZGZkNjJmYmI2Y2Y0YWY5MTFmN2QyOTFjZTU1ZDc4YzY2ZjczMWI0NGNiOTFhMmY1ZTRlNmI1ZDIzZTZjMg==',
            'worksheetId': 'rjqdrz',
            'controls': [
                {"controlId": "rjmc", "value": "%s" % rj_name, 'valueType': 2},
                {"controlId": "banben", "value": "%s" % banben},
                {"controlId": "qita", "value": "%s" % qita},
                {"controlId": "ownerid", "value": "3e923e90-fc8a-4949-8372-3cf1d53d1b6f"}
            ],
            "triggerWorkflow": 'true'
        }
        ret_mdy = mdy.post(url=mdy_add_url, data=json.dumps(mdy_add_data), headers=mdy_head).json()
        return 1
    except:
        return 0


def send_api_dai_get_verify(value):
    """
    发送闪库中转外网服务器进行鉴权请求,返回数据字典
    注意返回后数据在['data'] 中
    :param value: 验证名称
    :return: {
    'rjmc':'软件名称',
    'jzrq':'截止日期',
    'sfyzbb':'是否验证版本',
    'banben':'版本',
    'sjdz':'升级地址',
    'ddurl':'钉钉url',
    'sjnr':'升级内容',
    'json':{'配置文件':''},
    }
    """
    verify_url = 'http://ofe6z14.nat.ipyingshe.com/verify/mdy_verify'
    verify_data = {
        'value': value
    }
    ret = requests.request('POST', url=verify_url, json=verify_data).json()
    return ret['data']


def send_api_wai_get_verify(value):
    """
    发送120段外网无代码服务器进行鉴权请求,返回数据字典
    :param value:软件名称
    :return:
    {
    'rjmc':'软件名称',
    'jzrq':'截止日期',
    'sfyzbb':'是否验证版本',
    'banben':'版本',
    'sjdz':'升级地址',
    'ddurl':'钉钉url',
    'sjnr':'升级内容',
    'json':{'配置文件':''},
    }
    """
    try:
        mdy_head = {
            'Content-Type': "application/json"
        }
        mdy = requests.Session()
        mdy_add_url = 'http://120.221.159.84:8880/api/v2/open/worksheet/getFilterRows'
        mdy_add_data = {
            "appKey": '6f365477c211d998',
            "sign": 'YTI2ZGZkNjJmYmI2Y2Y0YWY5MTFmN2QyOTFjZTU1ZDc4YzY2ZjczMWI0NGNiOTFhMmY1ZTRlNmI1ZDIzZTZjMg==',
            "worksheetId": "jkzcjqr",
            "viewId": "",
            "pageSize": 50,
            "pageIndex": 1,
            "filters": [
                {
                    "controlId": "rjmc",
                    "dataType": 11,
                    "spliceType": 1,
                    "filterType": 1,
                    'value': value,
                },
            ],
        }
        res_mdy = mdy.post(url=mdy_add_url, data=json.dumps(mdy_add_data), headers=mdy_head).json()
        # print(res_mdy)
        res_mdy_list = []
        if res_mdy['data']['total'] == 0:
            # print('无记录')
            return res_mdy_list
        else:
            # print(res_mdy['data']['rows'][0]['json'].split('"><span>')[1].replace('<p>', '').replace('</p>', '').replace('</span>', '').replace('</span>', ''))
            res_mdy['data']['rows'][0]['json'] = json.loads(res_mdy['data']['rows'][0]['json'])
            return res_mdy['data']['rows'][0]
    except:
        return public.try_error('无代码', True)


def send_api_nei_get_verify(value):
    """
    发送134段内网无代码服务器进行鉴权请求,返回数据字典
    :param value:软件名称
    :return:
    {
    'rjmc':'软件名称',
    'jzrq':'截止日期',
    'sfyzbb':'是否验证版本',
    'banben':'版本',
    'sjdz':'升级地址',
    'ddurl':'钉钉url',
    'sjnr':'升级内容',
    'json':{'配置文件':''},
    }
    """
    try:
        mdy_head = {
            'Content-Type': "application/json"
        }
        mdy = requests.Session()
        mdy_add_url = 'http://134.80.215.221:8880/nocode/api/v2/open/worksheet/getFilterRows'
        mdy_add_data = {
            "appKey": '6f365477c211d998',
            "sign": 'YTI2ZGZkNjJmYmI2Y2Y0YWY5MTFmN2QyOTFjZTU1ZDc4YzY2ZjczMWI0NGNiOTFhMmY1ZTRlNmI1ZDIzZTZjMg==',
            "worksheetId": "jkzcjqr",
            "viewId": "",
            "pageSize": 50,
            "pageIndex": 1,
            "filters": [
                {
                    "controlId": "rjmc",
                    "dataType": 11,
                    "spliceType": 1,
                    "filterType": 1,
                    'value': value,
                },
            ],
        }
        res_mdy = mdy.post(url=mdy_add_url, data=json.dumps(mdy_add_data), headers=mdy_head).json()
        #print(res_mdy)
        res_mdy_list = []
        if res_mdy['data']['total'] == 0:
            # print('无记录')
            return res_mdy_list
        else:
            # print(res_mdy['data']['rows'][0]['json'].split('"><span>')[1].replace('<p>', '').replace('</p>', '').replace('</span>', '').replace('</span>', ''))
            res_mdy['data']['rows'][0]['json'] = json.loads(res_mdy['data']['rows'][0]['json'])
            return res_mdy['data']['rows'][0]
    except:
        return public.try_error('无代码', True)


def send_dai_phone_msg(send_name, send_phone, send_text):
    """
    发送到闪库中转外网服务器发送短信
    :param send_name: 发送名称   如果不为 传参不为 本地 则效验 发送账号是否在白名单内
    :param send_phone: 发送手机号
    :param send_text: 发送短信文本
    :return:
    """
    send_data = {
        'name': send_name, 'zhanghao': send_phone, 'text': send_text
    }
    try:
        return requests.post(url='http://ofe6z14.nat.ipyingshe.com/task/send_msg', json=send_data).json()
    except:
        return {'code': '发送失败', 'msg1': send_data}


#print(send_api_nei_get_verify('综调中心'))

def send_wx_img(chatroom_name, file_path):
    """
    发送内网服务器wx消息
    :param chatroom_name:群聊天
    :param file_path: 文件目录
    :return:
    """
    print(file_path)
    # 先判断file_path文件是否存在
    if file_path.find('http') == -1:
        if not os.path.exists(file_path):
            return {'code': 404, 'data': '%s文件不存在' % file_path}
    verify_url = 'http://10.16.2.180:6088/wx/send_img'
    verify_data = {
        'chatroom_name': chatroom_name,
        'url': file_path
    }
    ret = requests.request('POST', url=verify_url, json=verify_data).json()
    #print(ret)
    return {'code': ret['code'], 'data': ret['data']}


def send_wx_text(chatroom_name, send_text):
    """
    发送内网服务器wx文本消息
    :param chatroom_name:群聊天
    :param file_path: 文件目录
    :return:
    """
    # 先判断file_path文件是否存在
    verify_url = 'http://10.16.2.180:6088/wx/send_str'
    verify_data = {
        'chatroom_name': chatroom_name,
        'send_str': send_text
    }
    ret = requests.request('POST', url=verify_url, json=verify_data).json()
    #print(ret)
    return {'code': ret['code'], 'data': ret['data']}


def send_wx_file(chatroom_name, file_path, file_name=None):
    """
    发送内网服务器进行发送微信消息
    :param file_name: 如果为url传参可进行改名
    :param chatroom_name: 群名
    :param file_path: 文件目录
    :return:
    """
    if file_path.find('http') == -1:
        if not os.path.exists(file_path):
            return {'code': 404, 'data': '%s文件不存在' % file_path}
    verify_url = 'http://10.16.2.180:6088/wx/send_file'
    verify_data = {
        'chatroom_name': chatroom_name,
        'url': file_path,
        'file_name': file_name
    }
    ret = requests.request('POST', url=verify_url, json=verify_data).json()
    return {'code': ret['code'], 'data': ret['data']}


def send_wx_file_new(send_type, wxId, filePath, robotId='wxid_42vw5k20qoaq22'):
    """
    发送内网服务器进行发送微信消息
        "send_type": "{1}",     # 发送类型   0群聊  1私聊
        "wxId": "{2}",          # 群聊名/微信号
        "message": "{3}"    # 发送消息
    """
    verify_url = 'http://10.16.2.180:6096/send_wx_file_new'
    return requests.request('POST', url=verify_url, json={
        "send_json": {
            "send_pop": '本地公共模块',
            "send_type": str(send_type),
            "robotId": robotId,
            "wxId": wxId,
            "filePath": filePath
        }
    }).json()['data']


def send_wx_text_new(wxId, message, robotId="wxid_42vw5k20qoaq22"):
    """
    发送新版机器人通报
    """

    verify_url = 'http://10.16.2.180:10001/api/processor'
    return requests.request('POST', url=verify_url, json={
        "type": "sendTextMessage",
        "params": {
            "robotId": robotId,
            "instanceId": "",
            "wxId": wxId,
            "message": message
        }
    }).json()


def send_wx_img_new(send_type, wxId, filePath, robotId='wxid_42vw5k20qoaq22'):
    """
    发送内网服务器进行发送微信消息
    注意错误 此接口通报main_内进行消息转发
        "send_type": "{1}",     # 发送类型   0群聊  1私聊
        "wxId": "{2}",          # 群聊名/微信号
        "message": "{3}"    # 发送消息
    """
    verify_url = 'http://10.16.2.180:6096/send_wx_img_new'
    return requests.request('POST', url=verify_url, json={
        "send_json": {
            "send_pop": '本地公共模块',
            "send_type": str(send_type),
            "robotId": robotId,
            "wxId": wxId,
            "imagePath": filePath
        }
    }).json()


def send_wx_friends_file(chatroom_name, file_path):
    """
    发送潍坊Wechat 好友文件消息
    :param chatroom_name: 好友姓名/备注
    :param file_path: 如果是本机可以传绝对路径,跨机传url
    :return: 
    """""
    if not os.path.exists(file_path):
        return {'code': 404, 'data': '%s文件不存在' % file_path}
    verify_url = 'http://10.16.2.180:6088/wx/send_file_friends'
    verify_data = {
        'chatroom_name': chatroom_name,
        'url': file_path
    }
    ret = requests.request('POST', url=verify_url, json=verify_data).json()
    return {'code': ret['code'], 'data': ret['data']}


def send_wx_friends_text(chatroom_name, send_text):
    """
    发送潍坊Wechat 好友私聊消息
    :param chatroom_name: 好友姓名/备注
    :param send_text: 发送的文本消息
    :return: 
    """""
    verify_url = 'http://10.16.2.180:6088/wx/send_str_friends'
    verify_data = {
        'chatroom_name': chatroom_name,
        'send_str': send_text
    }
    ret = requests.request('POST', url=verify_url, json=verify_data).json()
    #print(ret)
    return {'code': ret['code'], 'data': ret['data']}


def send_wx_friends_img(chatroom_name, file_path):
    """
    发送潍坊Wechat 好友图片消息
    :param chatroom_name: 好友姓名/备注
    :param file_path: 如果是本机可以传绝对路径,跨机传url
    :return: 
    """""
    print(file_path)
    # 先判断file_path文件是否存在
    if file_path.find('http') == -1:
        if not os.path.exists(file_path):
            return {'code': 404, 'data': '%s文件不存在' % file_path}
    verify_url = 'http://10.16.2.180:6088/wx/send_img_friends'
    verify_data = {
        'chatroom_name': chatroom_name,
        'url': file_path
    }
    ret = requests.request('POST', url=verify_url, json=verify_data).json()
    #print(ret)
    return {'code': ret['code'], 'data': ret['data']}


def upload_file_ioral(file_path):
    """通过ftp上传的省公司130服务器

    Args:
        file_path (_type_): 文件路径
    """

    def get_md5(string):
        """计算字符串的MD5值"""
        return hashlib.md5(string.encode()).hexdigest()

    def get_random_string(length):
        """生成长度为length的随机字符串"""
        return ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for _ in range(length))

    def upload_file_to_ftp(host, username, password, remote_dir, local_file_path, remote_file_name=None):
        """
        上传文件到FTP服务器

        :param host: FTP服务器的地址
        :param username: FTP服务器的用户名
        :param password: FTP服务器的密码
        :param remote_dir: FTP服务器上的目标目录
        :param local_file_path: 本地文件的路径
        :param remote_file_name: 上传到FTP服务器的文件,默认为本地文件名
        :return: 上传结果(True/False)
        """
        if not remote_file_name:
            remote_file_name = os.path.basename(local_file_path)

        try:
            with closing(ftplib.FTP()) as ftp:
                log.info("尝试连接到FTP服务器...")
                ftp.connect(host)
                log.info("连接成功，尝试登录...")
                ftp.login(username, password)
                log.info("登录成功，尝试切换目录...")
                ftp.cwd(remote_dir)
                log.info("目录切换成功，开始上传文件...")
                with open(local_file_path, 'rb') as file:
                    ftp.storbinary(f'STOR {remote_file_name}', file)
                log.info("文件上传完成。")
                return True
        except ftplib.all_errors as e:
            public.try_error('1', True)
            log.info(f"FTP错误:{e}")
        except Exception as e:
            public.try_error('1', True)
            log.info(f"发生错误：{e}")
        return False

    size = 1000000000
    #file_bytes = get_bytes(file_path, size)
    ftp_server = "10.214.70.130"
    remote_dir = '/UserRecord/UploadFiles'
    ftp_username = "ioraiLog"
    ftp_password = "iL@123@#"
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    origin_filename = os.path.basename(file_path)
    filename = f"{timestamp}{get_md5(origin_filename)}{get_random_string(5)}{os.path.splitext(origin_filename)[1]}"

    if upload_file_to_ftp(ftp_server, ftp_username, ftp_password, remote_dir, file_path, filename):
        url2 = f"https://pic.iorai.com/xcx/{filename}"
        log.info(f"文件上传成功,URL2为:{url2}")
        return True, url2
    else:
        log.info("文件上传失败。")
        return False, "文件上传失败。"


#print(send_api_dai_get_server_cookies('ksh'))
if __name__ == '__main__':
    try:
        #print(send_dai_phone_msg('本地', '18766160226', '密码SDyd2024..'))
        #print(send_wx_text_new('w609669521', '测试消息'))
        #print(send_wx_img_new('0', '21135849945@chatroom','D:\\王东\\支撑程序\\综调中心通报\\质检组\\一级督办单通报\\一级督办单通报.png'))
        print(send_wx_file_new('0', '21135849945@chatroom', 'D:\王东\支撑程序\综调中心通报\质检组\一级督办单通报\log\一级督办单2025-01-19 08-15-13.log'))
    except:
        s = sys.exc_info()
        print(("错误为: %s 在第%d行" % (s[1], s[2].tb_lineno)))
        pass
[]
{}
