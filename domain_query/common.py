# coding=utf8

import re
import logging
from logging import handlers

pattern = re.compile(
    r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
    r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
)


class DcqException(Exception):
    """
    域名查询异常基类
    """
    pass


class ParamException(DcqException):
    """
    参数异常类
    """
    pass


def check_param_type(param, param_name, expected_type_obj):
    """
    校验参数是否为字符串:单个字符串，或多个字符串的列表
    :param param:要校验的参数
    :param param_name:参数的名字，表明参数是什么
    :param expected_type_obj:期望的类型的对象
    """
    if isinstance(param, list):
        for data in param:
            if not isinstance(data, type(expected_type_obj)):
                LOG.error('参数错误:{}必须为{},实际类型为{}'.format(type(expected_type_obj), param_name, type(data)))
                raise ParamException('参数错误:{}必须为{}'.format(param_name, type(expected_type_obj)))
    elif not isinstance(param, type(expected_type_obj)):
        LOG.error('参数错误:{}必须为{},实际类型为{}'.format(param_name, type(expected_type_obj), type(param)))
        raise ParamException('参数错误:{}必须为{}'.format(param_name, type(expected_type_obj)))


def validate_domain(domain):
    """
    校验域名是否合法
    :param domains:
    :return:
    """
    return True if pattern.match(domain) else False


class Logger(object):
    """
    日志
    """
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, filename, level='info', when='D', backCount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        # 设置日志格式
        format_str = logging.Formatter(fmt)
        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))
        # 往屏幕上输出
        sh = logging.StreamHandler()
        # 设置屏幕上显示的格式
        sh.setFormatter(format_str)
        # 往文件里写入
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount, encoding='utf-8')
        # 设置文件里写入的格式
        th.setFormatter(format_str)
        # 把对象加到logger里
        # self.logger.addHandler(sh)
        self.logger.addHandler(th)


LOG = Logger('dcq.log').logger
