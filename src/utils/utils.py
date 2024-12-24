from datetime import datetime, timezone, timedelta
from dateutil import parser
import logging

def format_published_time(time_str):
    """
    格式化发布时间为统一格式 YYYY-MM-DD HH:MM

    参数:
    time_str (str): 输入的时间字符串，可能是多种格式。

    返回:
    str: 格式化后的时间字符串，若解析失败返回空字符串。
    """
    try:
        parsed_time = parser.parse(time_str, fuzzy=True)
    except (ValueError, parser.ParserError):
        time_formats = [
            '%a, %d %b %Y %H:%M:%S %z',
            '%a, %d %b %Y %H:%M:%S GMT',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d'
        ]
        for fmt in time_formats:
            try:
                parsed_time = datetime.strptime(time_str, fmt)
                break
            except ValueError:
                continue
        else:
            logging.warning(f"无法解析时间字符串：{time_str}")
            return ''
    
    if parsed_time.tzinfo is None:
        parsed_time = parsed_time.replace(tzinfo=timezone.utc)
    shanghai_time = parsed_time.astimezone(timezone(timedelta(hours=8)))
    return shanghai_time.strftime('%Y-%m-%d %H:%M')

def replace_non_domain(link: str, blog_url: str) -> str:
    """
    暂未实现
    检测并替换字符串中的非正常域名部分（如 IP 地址或 localhost），替换为 blog_url。
    替换后强制使用 https，且考虑 blog_url 尾部是否有斜杠。

    :param link: 原始地址字符串
    :param blog_url: 替换为的博客地址
    :return: 替换后的地址字符串
    """
    
    # 提取link中的路径部分，无需协议和域名
    # path = re.sub(r'^https?://[^/]+', '', link)
    # print(path)
    
    return link
