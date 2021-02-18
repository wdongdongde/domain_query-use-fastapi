# coding=utf-8
"""
数据库操作
"""
import sqlalchemy
from bson import ObjectId
from sqlalchemy.orm import Session

import models, schemas


def get_task_result(db: Session, task_id: str):
    """
    通过task_id查询任务的结果
    :param db:
    :param task_id:
    :return:
    """
    return db.query(models.DomainQueryTask).filter(models.DomainQueryTask.task_id == task_id).first()


def create_task_result(db: Session, task: schemas.DomainQueryTask):
    """
    写入任务的执行结果
    :param db:
    :param task:
    :return:
    """
    db_domain_query_result_list = []
    # TODO 多层嵌套的情况下，这样写入数据库是否合理
    for domain_query_result in task.data:
        result_id = str(ObjectId())
        domain_query_result.id = result_id
        # domain_info有一个外键时result_id 每个result_id只有一个domain_info
        # 生成domain_info数据库存储内容
        if domain_query_result.result is not None:
            db_domain_info = models.DomainInfo(**domain_query_result.result.dict(), result_id=result_id)
        else:
            db_domain_info = None
        # 生成domain_query_result数据库存储内容
        db_domain_query_result_list.append(
            models.DomainQueryResult(state_code=domain_query_result.state_code,
                                     task_id=task.task_id,
                                     result=db_domain_info,
                                     err_info=domain_query_result.err_info,
                                     id=domain_query_result.id))

    param_dict = task.dict()
    param_dict.pop('data')
    db_task = models.DomainQueryTask(**param_dict, data=db_domain_query_result_list)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
