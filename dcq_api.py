# coding=utf-8
"""
域名查询对外接口
"""
import time
from functools import partial

from bson import ObjectId

from crud import create_task_result, get_task_result
from database import SessionLocal, engine
from domain_query.common import DcqException, LOG
from domain_query.domain_query import request_query_domain, async_query_domain, fast_query_domain
from schemas import DomainQuery, QueryDomainInfo, DomainQueryResult, AsyncDomainQueryResult, DomainQueryTask
from typing import List
import asyncio
import models
from fastapi import FastAPI, HTTPException

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
SYNC_MAX_QUERY_NUM = 50
ASYNC_MAX_QUERY_NUM = 500


@app.post("/domains", response_model=List[DomainQueryResult], response_model_exclude_none=True)
def query_domains(domains: DomainQuery, query_info: QueryDomainInfo) -> List[DomainQueryResult]:
    """
    同步查询单个或多个域名
    """
    if len(domains.domains) > SYNC_MAX_QUERY_NUM:
        raise HTTPException(status_code=400, detail="查询的域名数量超过限制！")
    res = request_query_domain(domains.domains, query_info)
    return res


def sync_fast_query_domains(domains: DomainQuery, query_info: QueryDomainInfo) -> List[DomainQueryResult]:
    """
    同步查询多个域名：使用协程加速  模块接口
    """
    if len(domains.domains) > SYNC_MAX_QUERY_NUM:
        raise DcqException("查询的域名数量超过限制!")
    res = fast_query_domain(domains.domains, query_info)
    return res


@app.post("/domains/fast", response_model=List[DomainQueryResult], response_model_exclude_none=True)
async def fast_query_domains(domains: DomainQuery, query_info: QueryDomainInfo) -> List[DomainQueryResult]:
    """
    同步查询多个域名：使用协程加速  web接口
    """
    if len(domains.domains) > SYNC_MAX_QUERY_NUM:
        raise HTTPException(status_code=400, detail="查询的域名数量超过限制！")
    res = await async_query_domain(domains.domains, query_info)
    return res


@app.post("/batchdomains", response_model=AsyncDomainQueryResult, response_model_exclude_none=True)
async def async_query_domains(domains: DomainQuery, query_info: QueryDomainInfo) -> AsyncDomainQueryResult:
    """
    异步批量查询
    """
    if len(domains.domains) > ASYNC_MAX_QUERY_NUM:
        raise HTTPException(status_code=400, detail="查询的域名数量超过限制！")
    res = AsyncDomainQueryResult()
    try:
        task = asyncio.ensure_future(async_query_domain(domains.domains, query_info))
        task_id = str(ObjectId())
        res.task_id = task_id
        # 添加回调：用于将查询得到的结果保存到数据库
        # TODO 暂时全查询完到内存，然后再写入数据库，后续优化减小内存占用
        task.add_done_callback(
            partial(callback, task_id=task_id, submit_time=time.time(), submit_count=len(domains.domains)))
    except Exception as err:
        res.status_code = -1
        res.err_info = str(err)
    return res


@app.get("/batchdomains/{task_id}", response_model=DomainQueryTask, response_model_exclude_none=True)
def get_async_query_result(task_id: str) -> DomainQueryTask:
    """
    异步批量查询结果返回
    """
    return get_task_result(db=SessionLocal(), task_id=task_id)


def callback(future, task_id, submit_time, submit_count):
    """
    异步查询的回调函数:将查询结果写入数据库
    :param future:
    :param task_id:
    :param submit_time:
    :param submit_count:
    :return:
    """
    LOG.info('future done: {}，task_id:{},submit_time:{},submit_count:{}'.format(future.result(), task_id, submit_time,
                                                                                submit_count))
    # 异步查询的结果 List[DomainQueryResult]
    domain_query_result = future.result()
    task_result = DomainQueryTask(task_id=task_id, submit_time=submit_time, submit_count=submit_count, status=0)
    task_result.data = domain_query_result
    task_result.finished_time = time.time()
    # 将结果保存到数据库
    create_task_result(SessionLocal(), task_result)
    LOG.info("callback down!")


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
