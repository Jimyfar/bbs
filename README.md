
基于 Flask 的个人论坛
=====================
## 简介
论坛地址：https://www.sapazai.xyz/
测试账号 用户名：密码123  密码：123

- 实现板块分区、话题支持 markdown 渲染和语法高亮、话题浏览排行、回复通知、点赞通知、@ 提醒、邮箱重置密码、更换头像等功能。
- 数据库选择了 MySQL，实现了基于 SQLALchemy 的 ORM，封装 CRUD 接口的基类。
- 编写数据库重置脚本与 Shell 脚本一键部署结合，加快开发测试速率，保证测试数据可控和一致性。
- 使用 Nginx 访问静态资源、做反向代理，同时配合 Gunicorn 实现多进程负载均衡，用 Gevent 开启协程充分利用机器效能。使用 Nginx 配置 SSL 证书，网站入口全部转入 HTTPS 协议。
- 使用 Redis 实现登录 Session 和页面 token 在多进程下的数据共享，和用于缓存计算耗时长的数据结果。
- 使用 Celery 任务队列框架和 Redis 组合模拟高并发应对策略，确保邮箱信息可靠发送。
- 多次使用 A/B Test、 cProfile 和 Graphviz 对影响用户体验较大的路由函数评估，提供调优证据，为优化响应提供方向。

## 运行环境

Ubuntu Server 18.04.1 LTS 64位

Python 3.6

## 一键部署

```
bash deploy.sh
```

## 详细
### 注册 登录 重置密码
- 实现重置邮箱重置密码、登录和注册功能。
![主页](https://github.com/Jimyfar/bbs/blob/master/images/%E7%99%BB%E5%BD%95.gif)

## 话题主页 和 详细页
- 实现板块分区，浏览排行。
- 话题内容支持 markdown 渲染、语法高亮、点赞和回复。
![登录界面](https://github.com/Jimyfar/bbs/blob/master/images/%E8%AF%9D%E9%A2%98.gif)

## 用户主页
- 按时间降序查看创建过的话题和回复过的话题
![ajax](https://github.com/Jimyfar/bbs/blob/master/images/%E5%88%9B%E5%BB%BA%E7%9A%84%E8%AF%9D%E9%A2%98.gif)

## 消息中心
- 发送消息和接收消息
- 查看被回复、被 @ 、和被回复的话题
微博增删改查，微博权限控制（博主可以修改博文和删除博文，博主可以删除评论但不可以修改评论。评论楼主可以修改和删除评论）
![weibo_CRUD_gif](https://github.com/Jimyfar/bbs/blob/master/images/%E6%B6%88%E6%81%AF%E4%B8%AD%E5%BF%83.gif)
## 更新用户信息
- 更新用户名、签名、头像和密码
![注册登录](https://github.com/Jimyfar/bbs/blob/master/images/%E8%AE%BE%E7%BD%AE.gif)


