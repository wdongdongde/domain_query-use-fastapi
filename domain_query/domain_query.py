# coding=utf-8
"""
域名查询入口函数，支持同步和异步
"""
import asyncio

from domain_query.common import DcqException
from domain_query.queries.queries import ChinazDomainQuery, Ce8DomainQuery


DCQ_LIST = [ChinazDomainQuery, Ce8DomainQuery]


async def async_query_domain(domain_list, query_info):
    """
    异步查询:需要被异步函数调用
    :param domain_list:
    :param query_info:
    :return:
    """
    # TODO 每一个都抛出异常的情况
    for dcq in DCQ_LIST:
        try:
            dcq_obj = dcq(query_info)
            await dcq_obj.async_get_query_result(domain_list)
            return dcq_obj.query_result
        except DcqException:
            # 接口无法访问的情况
            continue


def request_query_domain(domain_list, query_info):
    """
    同步查询：使用request
    :param domain_list:
    :param query_info:
    :return:
    """
    for dcq in DCQ_LIST:
        try:
            dcq_obj = dcq(query_info)
            dcq_obj.request_get_query_result(domain_list)
            return dcq_obj.query_result
        # TODO 抛出连接不上的异常的情况下再去试下一个
        except DcqException:
            continue


def fast_query_domain(domain_list, query_info):
    """
    可供同步函数调用的接口：使用携程加快查询速度
    :return:
    """
    # TODO 每一个都抛出异常的情况
    loop = asyncio.get_event_loop()
    for dcq in DCQ_LIST:
        try:
            dcq_obj = dcq(query_info)
            loop.run_until_complete(dcq_obj.async_get_query_result(domain_list))
            return dcq_obj.query_result
        except DcqException:
            # 接口无法访问的情况
            continue




