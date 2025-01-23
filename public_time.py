import datetime
import json
import time

import requests

TIME_STYLE_YYYYMMDD_000000 = '%Y-%m-%d 00:00:00'
TIME_STYLE_YYYYMMDD_Z = '%Y年%m月%d日'
TIME_STYLE_YYYYMMDD_235900 = '%Y-%m-%d 23:59:00'
TIME_STYLE_YYYYMMDDHH_MM_DD = '%Y-%m-%d %H-%M-%S'
TIME_STYLE_YYYYMMDDHH1MM1DD = '%Y-%m-%d %H:%M:%S'
TIME_STYLE_YYYYMMDDHH = '%Y%m%d%H'
TIME_STYLE_YYYYMMDDHHMM = '%Y%m%d%H%M'
TIME_STYLE_YYYYMMDD = '%Y%m%d'
TIME_STYLE_YYYY_MM_DD = '%Y-%m-%d'
TIME_STYLE_YYYY_MM_DD_H = '%Y-%m-%d %H'
TIME_STYLE_YYYYMM = '%Y%m'
TIME_STYLE_HH = '%H'


def time_set_now(out_time_type, input_time_type=None, input_time=None):
    """
    返回自定义格式的时间格式
    :param out_time_type: 时间格式类型  全局变量
    :param input_time_type: 输入的时间类型
    :param input_time: 如果输入自定义时间,按照设置时间返回,否则按照当前时间返回
    :return:
    """
    if input_time is not None:
        return datetime.datetime.strptime(input_time, input_time_type).strftime(out_time_type)
    else:
        return datetime.datetime.now().strftime(out_time_type)


def time_local():  # 获取当前时间
    """
    #获取当前时间
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def time_wai_beijing_time():  # 获取外网北京时间
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
            return beijing_time
    except:
        return time_local()


def time_nei_beijing_time():  # 获取内网北京时间
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
            return beijing_time
    except:
        return time_local()


def get_yesterday():
    """
    获取昨天日期
    :return:    返回格式   2024-01-04
    """
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return str(yesterday)


def get_before_riqi(day_num: int = 1):
    """
    获取之前的日期  默认为昨天
    :type day_num: int 往前之间的天数
    :return: 格式 2024-11-27
    """
    today = datetime.date.today()
    oneday = datetime.timedelta(days=day_num)
    yesterday = today - oneday
    return yesterday


def get_timestamp(input_time=None):
    """
    生成13位时间戳返回 文本格式
    :param input_time: 可选参数，格式为文本格式的日期时间字符串
    :return: 时间戳 注意文本格式
    """
    if input_time is None:
        # 生成当前时间的时间戳
        return str(int(round(time.time() * 1000)))
    else:
        # 将输入的日期时间字符串解析为时间戳
        dt = datetime.datetime.strptime(input_time, '%Y-%m-%d %H:%M:%S')
        timestamp = int(dt.timestamp() * 1000)
        return str(timestamp)


def get_time_now_riqi(input_time=None):
    """
    获取当前的日期.
    1.如果不输入input_time则返回当前日期
    2.输入input_time 则使用当前日期进行计算
    1:param input_time:
    :return:
    """
    if input_time is None:
        return datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        today = datetime.date.today()
        oneday = datetime.timedelta(days=input_time)
        yesterday = today + oneday
        return yesterday


def date_time_day_hors_seconds(s):  # date 转 返回 天 小时 秒
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


def get_time_datatime(input_time=None):  # 获取当前时间
    """
    #获取当前时间
    返回字典 注意返回的value 格式为 int
    {'年': 2024, '月': 6, '日': 1, '小时': 22, '分钟': 24, '秒': 36, '毫秒': 479489, '星期': 5, '星期几': 'Saturday'}
    """
    if input_time:
        data_time = datetime.datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
    else:
        data_time = datetime.datetime.now()

    week_dict = {
        "Monday": "一",
        "Tuesday": "二",
        "Wednesday": "三",
        "Thursday": "四",
        "Friday": "五",
        "Saturday": "六",
        "Sunday": "日"
    }

    time_dict = {
        '年': data_time.year,
        '月': data_time.month,
        '日': data_time.day,
        '小时': data_time.hour,
        '分钟': data_time.minute,
        '秒': data_time.second,
        '毫秒': data_time.microsecond,
        '星期': data_time.weekday(),
        '星期几': week_dict[data_time.strftime('%A')],
    }
    return time_dict


def get_day_of_month(input_time=None):
    """
    如果input_time 输入则计算输入时间计算
    否则按照当前时间计算
    获取本月 月初/昨天/今天/明天/月末的日期  格式 %Y-%m-%d
    :return: dict {月初 昨天 今天 明天 月末}
    """
    # 解析日期字符串为 datetime 对象
    if input_time:
        date_obj = datetime.datetime.strptime(input_time, "%Y-%m-%d")
    else:
        date_obj = datetime.datetime.now()

    # 获取该月的第一天
    first_day_of_month = date_obj.replace(day=1)

    # 获取下个月的第一天，然后减去一天得到该月的最后一天
    last_day_of_month = (date_obj.replace(day=1) + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)

    # 将日期对象格式化为字符串
    first_day_formatted = first_day_of_month.strftime("%Y-%m-%d")
    last_day_formatted = last_day_of_month.strftime("%Y-%m-%d")

    today = datetime.datetime.today()
    one_days_ago = today - datetime.timedelta(days=1)
    one_days = today - datetime.timedelta(days=-1)
    time_dict = {
        '月初': first_day_formatted,
        '昨天': one_days_ago.strftime("%Y-%m-%d"),
        '今天': date_obj.strftime("%Y-%m-%d"),
        '明天': one_days.strftime("%Y-%m-%d"),
        '月末': last_day_formatted,
    }
    # print(time_dict)
    return time_dict


def get_now_time():  # 获取当前时间
    """
    #获取当前时间
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def time_comparison(new_time, olt_time):
    """
    判断new_time时间是否在olt_time之前。

    :param new_time: 被比较对象,字符串格式的时间，例如 "2023-04-05 12:34:56"
    :param olt_time: 比较对象,字符串格式的时间，例如 "2023-04-05 12:34:56"
    :return: 如果jszs在time_today之前，则返回True；否则返回False。
    """
    # 解析时间字符串到datetime对象
    jszs_dt = datetime.datetime.strptime(new_time, "%Y-%m-%d %H:%M:%S")
    time_today_dt = datetime.datetime.strptime(olt_time, "%Y-%m-%d %H:%M:%S")

    # 比较两个datetime对象
    return jszs_dt < time_today_dt


def convert_str_to_13_digit_timestamp(time_str, format_str="%Y-%m-%d %H:%M:%S"):
    """
    将给定的日期时间字符串转换为13位的时间戳。

    参数:
    time_str (str): 需要转换的日期时间字符串
    format_str (str): 字符串的时间格式，默认为"%Y-%m-%d %H:%M:%S"

    返回:
    int: 13位的时间戳
    """
    # 将字符串转换为datetime对象
    dt = datetime.datetime.strptime(time_str, format_str)

    # 转换为Unix时间戳（秒）
    timestamp = int(dt.timestamp() * 1000)

    # 添加毫秒数
    timestamp += dt.microsecond // 1000

    return timestamp


# 测试函数
if __name__ == "__main__":
    # 创建一个时间字符串
    #time_str = "2023-04-01 12:00:00"
    #print(get_day_of_month(get_day_of_month()['昨天']))
    print(get_before_riqi(4))
