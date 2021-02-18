# coding=utf-8
"""
基础域名查询器，支持同步和异步
"""
import aiohttp
import asyncio
import requests

from domain_query.common import validate_domain, DcqException, LOG
from schemas import DomainQueryResult


class BaseDomainQuery():
    """
    域名查询基类
    """

    def __init__(self, query_info):
        self.url = None
        self.query_result = []
        self.query_info = query_info

    async def async_get_query_result(self, domains: list):
        """
        从域名获取需要的信息
        :return:
        """
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.ensure_future(self._get_query_result(session, domain)) for domain in domains]
            await asyncio.wait(tasks)

    def request_get_query_result(self, domains):
        """
        :param domains:
        :return:
        """
        for domain in domains:
            if not validate_domain(domain):
                domain_query_result = DomainQueryResult(state_code=-1, err_info="非合法的域名！")
            else:
                url = "".join([self.url, domain])
                content = requests.get(url).content
                res_html = content.decode()
                domain_info = self.parse_from_html(res_html)
                if not self._check_query_result(domain_info):
                    domain_query_result = DomainQueryResult(state_code=-1, err_info="无法查询到域名相关信息！")
                else:
                    domain_info.domain_name = domain
                    # 查询得到正常结果
                    domain_query_result = DomainQueryResult(result=domain_info)
            self.query_result.append(domain_query_result)

    def parse_from_html(self, res_html):
        """
        从html中解析出域名相关注册信息
        子类需要实现该函数
        :param res_html: 请求返回的html
        :return: 返回DomainInfo
        """
        pass

    async def _get_query_result(self, session, domain: str):
        """
        :param session:
        :param domain:
        :return:
        """
        try:
            url = "".join([self.url, domain])
            async with session.get(url, verify_ssl=False, timeout=2) as response:
                if validate_domain(domain):
                    content = await response.content.read()
                    res_html = content.decode()
                    domain_info = self.parse_from_html(res_html)
                    if not self._check_query_result(domain_info):
                        domain_query_result = DomainQueryResult(state_code=-1, err_info="无法查询到域名相关信息！")
                    else:
                        domain_info.domain_name = domain
                        # 查询得到正常结果
                        domain_query_result = DomainQueryResult(result=domain_info)
                else:
                    # 域名不正确
                    domain_query_result = DomainQueryResult(state_code=-1, err_info="非合法的域名！")
                self.query_result.append(domain_query_result)
        except (aiohttp.ClientConnectorError, asyncio.TimeoutError):
            LOG.error("域名查询接口无法访问,{}".format(url))
            raise DcqException("域名查询接口无法访问")

    def _check_query_result(self, query_result):
        """
        :param query_result:
        :return:
        """
        is_ok = True
        for key, val in self.query_info:
            if val:
                # 需要返回的字段没有则查询失败
                if getattr(query_result, key) is None:
                    is_ok = False
            else:
                # 不需要查询的字段设为空
                setattr(query_result, key, None)
        return is_ok
