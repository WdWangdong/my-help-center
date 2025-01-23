# -*- coding: utf-8 -*-
import datetime
import json
import os
import sys
import socket
import getpass
import time
from typing import Optional
import public_time
import requests
from loguru import logger as log

#from win10toast_click import ToastNotifier

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'Keep-Alive',
}
mdy_head = {
    'Content-Type': "application/json"
}

TIME_STYLE_YYYYMMDD_000000 = '%Y-%m-%d 00:00:00'
TIME_STYLE_YYYYMMDD_235900 = '%Y-%m-%d 23:59:00'
TIME_STYLE_YYYYMMDDHHMMDD = '%Y-%m-%d %H-%M-%S'
TIME_STYLE_YYYYMMDDHH = '%Y%m%d%H'
TIME_STYLE_YYYYMMDDHHMM = '%Y%m%d%H%M'
TIME_STYLE_YYYYMMDD = '%Y%m%d'
TIME_STYLE_YYYY_MM_DD = '%Y-%m-%d'
TIME_STYLE_YYYYMM = '%Y%m'
TIME_STYLE_HH = '%H'
#toaster = ToastNotifier()

PJ_COLOR = (249, 251, 238)


def add_file(path):
    """
    创建文件夹
    :param path:  绝对路径
    :return: 布尔值
    """
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True

    else:
        return False


def delete_old_log():
    """
    删除3天之前的历史log
    :return:
    """
    log.info('开始删除历时log...')
    directory = os.getcwd() + '\log'
    # 检查目录是否存在
    if not os.path.exists(directory):
        log.error(f"指定目录 {directory} 不存在。")
        return
    #log.info('删除历时log...')
    # 获取当前时间
    current_time = time.time()
    # 3 天前的时间
    seven_days_ago = current_time - (3 * 24 * 60 * 60)
    # 遍历目录中的文件
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # 检查文件是否是普通文件（不是目录）
        if os.path.isfile(file_path):
            # 获取文件的创建时间
            file_creation_time = os.path.getctime(file_path)
            # 如果文件的创建时间早于 3 天前，则删除文件
            if file_creation_time < seven_days_ago:
                try:
                    os.remove(file_path)
                    print(f"删除文件: {file_path}")
                except Exception as e:
                    print(f"无法删除文件 {file_path}，错误: {e}")
    log.info('删除历时log完成...')


# def send_win_notice(title, message, duration=5):
#     """
#     发送win10 -11 系统通知
#     :param title: 主题
#     :param message: 消息
#     :param duration: 显示秒数  默认5秒
#     :return:
#     """
#     toaster.show_toast(
#         title,  # title
#         message,  # message
#         icon_path=None,  # 'icon_path'
#         duration=duration,  # 吐司应该可见多少秒;无 = 通知中心中的离开通知
#         threaded=True,  # True = 并行运行其他代码;False = 代码执行将等到通知消失
#         # callback_on_click=open_url  # 点击通知运行功能
#     )


def got_json(res):  # 从回复信息里提取json
    try:
        # print(res)
        res = res[res.find('{'):]
        # print(res)
        while True:
            # print(1, res[-1])
            if res[-1] != '}':
                res = res[:-1]
                # print(2, res)
            else:
                return json.loads(res)
    except:
        try_error('pub的got_json')


def get_cookies(u=''):  # 获取本地cookies字典
    """
    获取本地cookies字典
    :param u: 空:cook.txt pd:pd.txt  57:57.txt
    :return: cookies字典数据
    """

    if u == '':
        f_path = 'd:/cook.txt'
    elif u == 'pd':
        f_path = 'd:/pd.txt'
    elif u == 'ts':
        f_path = 'd:/tousu.txt'
    else:
        f_path = 'd:/cook.txt'

    with open(f_path) as f:
        # with open('d:/wxjqr.txt') as f:
        c_v = f.read()
        c_v = c_v.replace('\n', '')
        c_v = c_v.replace('\r', '')
        c_v = c_v.replace(' ', '')

        cok_jkzc = {}  # 初始化一个空字典

    try:
        for one in c_v.split(';'):  # 遍历cookies字符串，以分号分隔
            key, value = one.split('=', 1)  # 将遍历到的每一个分项按等号分隔为键值对
            cok_jkzc[key] = value  # 将键值对添加到字典中
        return cok_jkzc  # 返回cookies字典
    except:
        return cok_jkzc  # 如果发生异常，返回空字典


def cook_to_txt(cook: dict, path):
    """将获取的远端字典写入到本地txt中

    Args:
        cook (dict): 远端字典
        path (_type_): 保存的文件地址
    """
    zc_str = ''
    for i in cook.keys():
        zc_str += i + '=' + cook[i] + ';'
    #print(zc_str)
    with open(path, 'w') as f:
        f.write(zc_str)


def get_time_13_timestamp():
    """
    生成13位时间戳返回 文本格式
    :return: 时间戳 注意文本格式
    """
    return str(int(round(time.time() * 1000)))


def try_error(name, show_log: Optional[bool] = None, send_msg: Optional[bool] = None, send_log: Optional[bool] = None, send_wx: Optional[bool] = None,send_wx_data: Optional[dict] = None):  # try异常提示
    """
    tiy模块提示异常
    :param name: 展示的名称
    :param send_log: 是否上传明道云log 默认上传云log
    :param show_log: 是否log显示
                            True: 表示需要log显示。
                            False: 明确表示不需要log显示。
                            None: 不传递此参数或显式传递None，则默认不显示log错误。
    :param send_msg: 发送短信提醒
                            True: 表示需要发送短信。
                            False: 明确表示不需要发送短信。
                            None: 不传递此参数或显式传递None，则默认不发送短信。
    :param send_wx: 是否发送微信信息提示 逻辑值
    :param send_wx_data:发送自定义微信内容数组 {'name':'微信号','text':'自定义发送内容'}
    :return: 返回文本格式的错误提示
    """
    s = sys.exc_info()
    str_error = "%s 在%s第%d行" % (s[1], name, s[2].tb_lineno)
    if show_log is True or show_log is None:
        log.error("错误为: %s 在%s第%d行" % (s[1], name, s[2].tb_lineno))
    if send_msg is True:
        if not s[1]:
            requests.post(url='http://ofe6z14.nat.ipyingshe.com/task/send_msg', json={'name': name, 'zhanghao': '15706307433', 'text': '%s发生程序错误,请及时查看!' % name}).json()
    if send_log is not None or send_log is True:
        requests.post(url='http://ofe6z14.nat.ipyingshe.com/mdy/add_log', json={'name': name, 'text': str_error}).json()
    if send_wx is not None:
        if not send_wx_data:
            requests.post(url='http://10.16.2.180:6096/send_wx_msg_new', json={
                'send_json':{
                    "send_pop": "本地公共模块",   # 发送标识
                    "send_type": "1",     # 发送类型   0群聊  1私聊
                    "wxId": "dongdong609669",          # 群聊名/微信号
                    "message": f"软件错误提示!\n\n软件名称:{name}\n\n{str_error}\n\n错误时间:{public_time.get_now_time()}"    # 发送消息
                }}).json()
        else:
            """发送微信自定义错误"""
            #print(send_wx_data)
            requests.post(url='http://10.16.2.180:6096/send_wx_msg_new', json={
                'send_json':{
                    "send_pop": "本地公共模块",   # 发送标识
                    "send_type": "1",     # 发送类型   0群聊  1私聊
                    "wxId": send_wx_data['name'],          # 群聊名/微信号
                    "message": f"软件错误提示!\n\n软件名称:{name}\n\n{send_wx_data['text']}\n\n错误时间:{public_time.get_now_time()}"    # 发送消息
                }}).json()
    return str_error


def get_cook_local(u=''):  # 获取cookies字典
    """
    获取cookies字典
    """
    if u == '':
        f_path = 'd:/cook.txt'
    elif u == 'pd':
        f_path = 'd:/pd.txt'
    elif u == '57':
        f_path = 'd:/57.txt'
    else:
        f_path = 'd:/cook.txt'
    with open(f_path) as f:
        # with open('d:/wxjqr.txt') as f:
        c_v = f.read()
        c_v = c_v.replace('\n', '')
        c_v = c_v.replace('\r', '')
        c_v = c_v.replace(' ', '')
        cok_jkzc = {}
    try:
        for one in c_v.split(';'):
            cok_jkzc[one.split('=', 1)[0]] = one.split('=', 1)[1]
        return cok_jkzc
    except:
        return cok_jkzc


class pub:
    # 全局变量 时间格式
    TIME_STYLE_YYYYMMDD_000000 = '%Y-%m-%d 00:00:00'
    TIME_STYLE_YYYYMMDD_235900 = '%Y-%m-%d 23:59:00'
    TIME_STYLE_YYYYMMDDHHMMDD = '%Y-%m-%d %H-%M-%S'
    TIME_STYLE_YYYYMMDDHH = '%Y%m%d%H'
    TIME_STYLE_YYYYMMDDHHMM = '%Y%m%d%H%M'
    TIME_STYLE_YYYYMMDD = '%Y%m%d'
    TIME_STYLE_YYYY_MM_DD = '%Y-%m-%d'
    TIME_STYLE_YYYYMM = '%Y%m'
    TIME_STYLE_HH = '%H'

    head = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; SLCC2; Media Center PC 6.0)',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
    }

    # 通用head

    head_ph = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; SM-G973N Build/PPR1.190810.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        "Host": "211.137.182.249:52713",
        'X-Requested-With': 'com.inspur.resquery.ResQueryShandong'
    }

    head_ph_gejie = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; SM-G973N Build/PPR1.190810.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        "Host": "211.137.182.249:52713",
        'X-Requested-With': 'com.inspur.resquery.ResQueryShandong'

    }
    mdy_head = {
        'Content-Type': "application/json"
    }
    bulu_head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'Referer': 'http://10.214.52.71:8999/usi-ntelligent-terminal/unify/unifymanagement',
    }

    def division(self, str_info=''):
        """分隔符
        Args:
            str (str, optional):如果输入内容分隔符中间带文字 ''.
        """
        if str_info == '':
            print('------------------')
        else:
            print('----%s----' % str_info)

    def now_time(self):  # 获取当前时间
        """
        #获取当前时间
        """
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def time_now_riqi(self):  # 获取当前时间
        """
        #获取当前时间(只日期)
        """
        return datetime.datetime.now().strftime('%Y-%m-%d')

    def now_time_time(self):  # 获取当前时间
        """
        #获取当前时间(%H:%M:%S)
        """
        return datetime.datetime.now().strftime('%H:%M:%S')

    def now_time_hh_ss(self):  # 获取当前时间
        """
        #获取当前时间(%H:%M:%S)
        """
        return datetime.datetime.now().strftime('%H:%M')

    def time_set_now(self, set):  # 获取当前时间
        """
            设置自定义格式时间

        :param set:'小时': '%H','秒': '%S','日期无横杠': '%Y%m%d%H',
        :return:
        """

        set_dict = {
            '小时': '%H',
            '秒': '%S',
            '日期小时无横杠': '%Y%m%d%H',
            '日期加时间0点': '%Y%m%d%H 00:00:00',
            '日期加时间23点': '%Y%m%d%H 23:59:00',
        }
        return datetime.datetime.now().strftime(set)

    def mkdir(self, path):
        path = path.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True

        else:
            return False

    def got_json(self, res):  # 从回复信息里提取json
        try:
            # print(res)
            res = res[res.find('{'):]
            # print(res)
            while True:
                # print(1, res[-1])
                if res[-1] != '}':
                    res = res[:-1]
                    # print(2, res)
                else:
                    return json.loads(res)
        except:
            self.try_tishi('pub的got_json')

    def get_cok(self, u=''):  # 获取cookies字典
        """
        获取cookies字典
        """
        if u == '':
            f_path = 'd:/cook.txt'
        elif u == 'pd':
            f_path = 'd:/pd.txt'
        elif u == '57':
            f_path = 'd:/57.txt'
        else:
            f_path = 'd:/cook.txt'
        with open(f_path) as f:
            # with open('d:/wxjqr.txt') as f:
            c_v = f.read()
            c_v = c_v.replace('\n', '')
            c_v = c_v.replace('\r', '')
            c_v = c_v.replace(' ', '')
            cok_jkzc = {}
        try:
            for one in c_v.split(';'):
                cok_jkzc[one.split('=', 1)[0]] = one.split('=', 1)[1]
            return cok_jkzc
        except:
            return cok_jkzc

    def get_cook_zd(self):  # 获取cookies字典 终端
        f_path = 'd:/zd.txt'
        with open(f_path) as f:
            c_v = f.read()
            c_v = c_v.replace('\n', '')
            c_v = c_v.replace('\r', '')
            c_v = c_v.replace(' ', '')
            cok_jkzc = {}
        try:
            for one in c_v.split(';'):
                cok_jkzc[one.split('=', 1)[0]] = one.split('=', 1)[1]
                return cok_jkzc
        except:
            return cok_jkzc

    def try_tishi(self, name, show=''):  # try异常提示
        """
        try异常提示
        """
        s = sys.exc_info()
        if show == '':
            # print("错误为: %s \n在%s第%d行" % (s[1], name, s[2].tb_lineno))
            log.error("错误为: %s 在%s第%d行" % (s[1], name, s[2].tb_lineno))
        return "%s 在%s第%d行" % (s[1], name, s[2].tb_lineno)

    def date_time_day_hors_seconds(self, s):  # date 转 返回 天 小时 秒
        """
        date 转 返回 天 小时 秒
            1/天
            2/小时
            3/分钟
        """
        shicha_days = s.days
        shicha_hours = (s.seconds // 3600) % 60
        shicha_seconds = (s.seconds // 60) % 60
        return shicha_days, shicha_hours, shicha_seconds

    def time_datetime(self, s):  # 转换日期格式
        """
        转换日期格式(日期加时间)
        """
        # print(s)
        # print(len(s))
        if len(s) > 1:
            s = s.replace('.0', '')
            time = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
            return time
        else:
            return ""

    def time_datetime_riqi(self, s):  # 转换日期格式
        """
        转换日期格式(日期)
        """
        # print(s)
        # print(len(s))
        if len(s) > 1:
            time = datetime.datetime.strptime(s, "%Y-%m-%d")
            return time
        else:
            return ""

    def time_getyesterday(self):
        """
        获取昨天日期
        :return:
        """
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return yesterday

    def add_file(self, path):
        """
        创建文件夹
        :param path:  绝对路径
        :return: 布尔值
        """
        path = path.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True

        else:
            return False

    def message_info_url(self, url, type, link):
        """
        钉钉发送消息
        :param url:发送的url
        :param type:任务类型的名称
        :param link: 任务描述
        :return:
        """
        pagrem = {
            "msgtype": "text",
            "text": {
                "content": "%s:\n%s\n%s\n%s" % (type, link, self.get_ComputerInfo(), self.now_time())
            },
            "at": {
                "atMobiles": [
                    "14755721700"  # 需要填写自己的手机号，钉钉通过手机号@对应人
                ],
                "isAtAll": False  # 是否@所有人，默认否
            }
        }
        headers = {
            'Content-Type': 'application/json'
        }
        # print(pagrem)
        requests.post(url, data=json.dumps(pagrem), headers=headers)

    def getBeijinTime(self):  # 获取北京时间
        try:
            # HTTP客户端运行的浏览器类型的详细信息。通过该头部信息，web服务器可以判断到当前HTTP请求的客户端浏览器类别。
            hea = {'User-Agent': 'Mozilla/5.0'}  # 站点服务器认为自己（浏览器）兼容Moailla的一些标准
            # 设置访问地址，我们分析到的；
            url = r'http://vv.video.qq.com/checktime?otype=json'
            # 用requests get这个地址，带头信息的；
            r = requests.get(url=url, headers=hea, timeout=3)
            # 检查返回的通讯代码，200是正确返回；
            if r.status_code == 200:
                # 定义result变量存放返回的信息源码；
                result = r.text
                result = json.loads(result.replace('QZOutputJson=', '').replace(';', ''))
                beijing_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result['t']))
                # 通过;分割文本；
                # data = result.split(";")
                # # 以下是数据文本处理：切割、取长度
                # year = data[1][len("nyear") + 3: len(data[1])]
                # month = data[2][len("nmonth") + 3: len(data[2])]
                # day = data[3][len("nday") + 3: len(data[3])]
                # # wday = data[4][len("nwday")+1 : len(data[4])-1]
                # hrs = data[5][len("nhrs") + 3: len(data[5])]
                # # hrs = data[5][len("nhrs") + 3: len(data[5]) - 1] #不需要减1
                # minute = data[6][len("nmin") + 3: len(data[6])]
                # sec = data[7][len("nsec") + 3: len(data[7])]
                # # 这个也简单把切割好的变量拼到beijinTimeStr变量里；
                # beijinTimeStr = "%s-%s-%s %s:%s:%s" % (year, month, day, hrs, minute, sec)
                # print(beijinTimeStr)
                # ltime = time.strptime(beijinTimeStr, "%Y-%m-%d %H:%M:%S") # 返回结果是一个结构体
                # ltime：time.struct_time(tm_year=2020, tm_mon=10, tm_mday=9, tm_hour=9, tm_min=32, tm_sec=39, tm_wday=4, tm_yday=283, tm_isdst=-1)
                return beijing_time
        except:
            return self.now_time()

# print(add_log('一址多户审批', '3.0', ()
# print(pub.time_getyesterday(''))
# print(get_nei_server_cookies('ztc'))
# print(res['json'])
# print(res['json']['option']['Min time'])
