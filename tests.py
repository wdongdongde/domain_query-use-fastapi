# coding=utf-8

import unittest

from dcq_api import query_domains, sync_fast_query_domains
from schemas import QueryDomainInfo, DomainQuery


class TestQueryDomains(unittest.TestCase):
    # 测试前的准备工作 常用来做一些初始化， 非必需方法
    def setUp(self):
        self.normal_domains = ['baidu.com', 'sina.com', 'sangfor.com', 'tencent.com', 'huawei.com']
        self.bad_domains = ['ddf', 'ggt.']
        self.unknown_domains = ['google.com']

        print("setup starting...")

    def test_query_domains(self):
        """
        测试查询多个域名的接口
        :return:
        """
        # 正常域名
        res_list = query_domains(DomainQuery(domains=self.normal_domains), QueryDomainInfo(company_name=True))
        # 查询是成功的
        for res in res_list:
            self.assertEqual(res.state_code, 0)
        # 异常域名
        res_list = query_domains(DomainQuery(domains=self.bad_domains), QueryDomainInfo(company_name=True))
        # 查询是失败的
        for res in res_list:
            self.assertEqual(res.state_code, -1)
            self.assertEqual(res.err_info, "非合法的域名！")
        # 不存在的域名
        res_list = query_domains(DomainQuery(domains=self.unknown_domains), QueryDomainInfo(company_name=True))
        # 查询是失败的
        for res in res_list:
            self.assertEqual(res.state_code, -1)
            self.assertEqual(res.err_info, "无法查询到域名相关信息！")

    def test_sync_fast_query_domains(self):
        """
        测试查询多个域名的接口:使用协程加速
        :return:
        """
        # 正常域名
        res_list = sync_fast_query_domains(DomainQuery(domains=self.normal_domains), QueryDomainInfo(company_name=True))
        # 查询是成功的
        for res in res_list:
            self.assertEqual(res.state_code, 0)
        # 异常域名
        res_list = sync_fast_query_domains(DomainQuery(domains=self.bad_domains), QueryDomainInfo(company_name=True))
        # 查询是失败的
        for res in res_list:
            self.assertEqual(res.state_code, -1)
            self.assertEqual(res.err_info, "非合法的域名！")
        # 不存在的域名
        res_list = sync_fast_query_domains(DomainQuery(domains=self.unknown_domains),
                                           QueryDomainInfo(company_name=True))
        # 查询是失败的
        for res in res_list:
            self.assertEqual(res.state_code, -1)
            self.assertEqual(res.err_info, "无法查询到域名相关信息！")

    def test_async_query_domains(self):
        pass

    # 测试完成后的收尾工作
    def tearDown(self):
        print("tearDown starting...")


if __name__ == '__main__':
    unittest.main()
