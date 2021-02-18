# coding=utf-8
"""
域名查询器，每个从不同的外部接口查询域名信息
"""
from bs4 import BeautifulSoup

from domain_query.queries.base_query import BaseDomainQuery
from schemas import DomainInfo


class ChinazDomainQuery(BaseDomainQuery):
    """
    从icp.chinaz.com获取域名信息
    """

    def __init__(self, query_info):
        BaseDomainQuery.__init__(self, query_info)
        self.url = "http://icp.chinaz.com/"

    def parse_from_html(self, res_html):
        """
        从html结果中获取域名备案信息
        :return:有结果时返回结果，未查询到结果时返回None
        """
        domain_info = DomainInfo()
        soup = BeautifulSoup(res_html, 'html.parser')
        for li in soup.find_all(name='li'):
            for span in li.find_all(name='span'):
                if span.string == '主办单位名称':
                    try:
                        domain_info.company_name = li.find(name='a').string
                    except AttributeError:
                        pass
                if span.string == '主办单位性质':
                    try:
                        domain_info.company_type = li.find(name='strong').string
                    except AttributeError:
                        pass
                if span.string == '网站备案/许可证号':
                    try:
                        domain_info.site_license = li.find(name='font').string
                    except AttributeError:
                        pass
                if span.string == '网站名称':
                    try:
                        domain_info.site_name = li.find(name='p').string
                    except AttributeError:
                        pass
                if span.string == '网站首页网址':
                    try:
                        domain_info.main_page = li.find(name='p').string
                    except AttributeError:
                        pass
                if span.string == '审核时间':
                    try:
                        domain_info.verify_time = li.find(name='p').string
                    except AttributeError:
                        pass
        return domain_info


class Ce8DomainQuery(BaseDomainQuery):
    """
    从www.ce8.com/assistor/icp/获取域名信息
    """

    def __init__(self, query_info):
        BaseDomainQuery.__init__(self, query_info)
        self.url = "http://www.ce8.com/assistor/icp/"

    def parse_from_html(self, res_html):
        """
        从html结果中获取域名备案信息
        :return:有结果时返回结果，未查询到结果时返回None
        """
        domain_info = DomainInfo()
        soup = BeautifulSoup(res_html, 'html.parser')
        for li in soup.find_all(name='li'):
            for span in li.find_all(name='span'):
                if span.string == '主办单位名称':
                    try:
                        domain_info.company_name = li.find(name='a').string
                    except AttributeError:
                        pass
                if span.string == '主办单位性质':
                    try:
                        domain_info.company_type = li.find(name='strong').string
                    except AttributeError:
                        pass
                if span.string == '网站备案/许可证号':
                    try:
                        domain_info.site_license = li.find(name='font').string
                    except AttributeError:
                        pass
                if span.string == '网站名称':
                    try:
                        domain_info.site_name = li.find(name='p').string
                    except AttributeError:
                        pass
                if span.string == '网站首页网址':
                    try:
                        domain_info.main_page = li.find(name='p').string
                    except AttributeError:
                        pass
                if span.string == '审核时间':
                    try:
                        domain_info.verify_time = li.find(name='p').string
                    except AttributeError:
                        pass
        return domain_info

