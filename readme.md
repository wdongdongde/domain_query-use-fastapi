
# 课二

## 整体需求
将dcq程序重构封装成一个库模块，提供给应用程序调用使用。

### 需求细化
1. 设计对应的API接口，需要实现单域名查询，多域名查询，批量域名查询
2. 能满足同步或异步调用需求
3. 其他

其它要求：
1. 优化性能：使用多线程来优化性能，比如内存换时间（缓存），提升并发度
2. API接口单元测试

### 接口设计（供其他模块调用）
1. 单个域名查询接口

输入：

| domain          | query_info                 |
| --------------- | -------------------------- |
| 查询的域名：str | 需要查询的信息：DomainInfo |

返回：DomainQueryResult 单条查询记录

| domain     | status_code  | err_info       | result               |
| ---------- | ------------ | -------------- | -------------------- |
| 查询的域名 | 查询是否成功 | 失败的错误信息 | 查询结果：DomainInfo |

2. 多个域名查询接口（以上两个接口整合成了一个）

输入：

| domains                 | query_info                 |
| ----------------------- | -------------------------- |
| 查询的域名：DomainQuery | 需要查询的信息：DomainInfo |

返回：一个记录的列表：List(DomainQueryResult)每条记录为：查询成功还是失败，失败原因，查询结果（失败为空[])

3. 批量查询异步接口

3.1 开启查询接口

输入：

| domains                 | query_info                 |
| ----------------------- | -------------------------- |
| 查询的域名：DomainQuery | 需要查询的信息：DomainInfo |

| status_code      | task_id |
| ---------------- | ------- |
| 接口响应是否成功 | 任务id  |

3.2 异步查询结果接口

输入：

| task_id    |
| ---------- |
| 任务id:str |

返回：

| task_id | submit_time | status   | finished_time | submit_count   | success_count | data             |
| ------- | ----------- | -------- | ------------- | -------------- | ------------- | ---------------- |
| 任务id  | 提交时间    | 完成状态 | 完成时间      | 查询的域名数量 | 成功的数量    | 多域名的查询结果 |

### 接口使用与测试
1. 运行dcq_api.py
2. 在浏览器中输入：http://127.0.0.1:8000/docs
3. 测试web接口及接口文档
4. 单元测试见tests.py
----------
# 课一
## 一、整体需求
设计一个dcq程度，通过控制台命令行接收用户输入域名，并打印出该域名对应的主办单位名称

## 二、需求细化与实现
### 语言与环境
- python 3.4及以上版本
- 第三方包：

```
pip3 install beautifulsoup4
pip3 install aiohttp
```

- windows 
### 功能
控制台命令行输入:
- 单个域名 ： dcq 域名 
```
python3 dcq.py  baidu.com
```

- 多个域名 ： dcq 域名1 域名2 域名3 ...
```
python3 dcq.py  baidu.com sangfor.com
```

- 通过文件指定域名 ： dcq -f 文件名（一行一个域名） 
```
python3 dcq.py  -f domains.txt
```

### 健壮性
- 尝试从多个第三方api来获取信息保证程序的输出
  - 从以下两个网站获取域名查询结果："http://icp.chinaz.com/", "http://www.ce8.com/assistor/icp/"
  - 因api调用有时候会失效，且大部分需要收费，所以统一采用爬虫的方式来获取结果

- 严格的参数校验和异常处理
  - 对函数的入参进行了校验
  - 对域名的合法性进行了校验
  - 考虑了上述网站失效的情况
### 可调试性
- 调试日志  dcq.log

### 性能
在使用domains.txt测试的情况下
- 使用requests 耗时：3.42366623878479s
- 使用aiohttp 耗时：1.1887516975402832s
