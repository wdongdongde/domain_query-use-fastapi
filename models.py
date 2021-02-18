# coding=utf-8
"""
数据库模型
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base  # 已声明的数据库


class DomainInfo(Base):
    """
    域名信息
    """
    __tablename__ = "domain_info"
    domain_name = Column(String)
    company_name = Column(String)
    company_type = Column(String)
    main_page = Column(String)
    site_name = Column(String)
    site_license = Column(String)
    verify_time = Column(String)
    # 在引用父表的子表上放置一个外键
    #  relationship() 然后在父级上指定，作为引用由子级表示的项集合：
    # 要在一对多中建立双向关系，“反向”端是多对一，请指定一个附加的 relationship() 然后用 relationship.back_populates 参数
    result_id = Column(ForeignKey("domain_query_result.id"), primary_key=True)


class DomainQueryResult(Base):
    """
    域名查询结果
    """
    __tablename__ = "domain_query_result"

    id = Column(String, index=True, primary_key=True)
    state_code = Column(Integer)
    err_info = Column(String)
    task_id = Column(ForeignKey("domain_query_task.task_id"))

    # Domainresult会有多个domainInfo
    result = relationship("DomainInfo", uselist=False)


class DomainQueryTask(Base):
    """
    异步任务的保存结果
    只有全部查询完了的时候才会保存
    """
    __tablename__ = "domain_query_task"
    task_id = Column(String, index=True, primary_key=True)
    status = Column(Integer)
    submit_time = Column(Integer)
    # TODO为下面的内容赋予默认值
    finished_time = Column(Integer)
    # 查询的个数
    submit_count = Column(Integer)
    # 查询成功的个数
    success_count = Column(Integer)

    data = relationship("DomainQueryResult")


if __name__ == '__main__':
    domain_info = DomainInfo()
    print(domain_info)
