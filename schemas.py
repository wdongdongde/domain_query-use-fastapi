# coding=utf-8
from typing import List
from pydantic import BaseModel


class QueryDomainInfo(BaseModel):
    """
    要查询的域名信息
    """
    site_name: bool = False
    company_name: bool = True
    company_type: bool = False
    main_page: bool = False
    site_license: bool = False
    verify_time: bool = False


class DomainInfo(BaseModel):
    """
    域名对应的信息
    """
    # 默认可以不需要
    domain_name: str = None
    company_name: str = None
    company_type: str = None
    main_page: str = None
    site_name: str = None
    site_license: str = None
    verify_time: str = None

    class Config:
        orm_mode = True


class DomainQueryResult(BaseModel):
    """
    单个域名查询结果返回结构
    """
    # 域名查询是成功还是失败,默认0为成功
    state_code: int = 0
    # 调用失败的原因
    err_info: str = None
    # 结果的id
    id: str = None
    result: DomainInfo = None

    class Config:
        orm_mode = True


class AsyncDomainQueryResult(BaseModel):
    """
    异步域名查询直接返回结果的结构
    """
    status_code: int = 0
    task_id: str = None


class DomainQueryTask(BaseModel):
    """
    异步域名查询返回的查询结果结构
    """
    task_id: str
    # 完成状态（已完成和未完成）
    status: int = 0
    submit_time: int = None
    # TODO为下面的内容赋予默认值
    finished_time: int = None
    # 查询的个数
    submit_count: int = None
    # 查询成功的个数 暂未统计
    success_count: int = None
    data: List[DomainQueryResult] = []

    class Config:
        orm_mode = True


class DomainQuery(BaseModel):
    """
    域名查询的输入参数结构
    """
    domains: List[str]


if __name__ == '__main__':
    res = DomainQueryTask(task_id="1")
    for d in res.data:
        print(d.result)
