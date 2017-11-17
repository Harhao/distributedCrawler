# distributedCrawler
- 基于multiprocessing多进程的Managers模块的进程队列消息共享
利用多进程实现简单分布式通信
- distributedCrawler的Master主要分为三部份：
    - UrlManager.py爬取url种子处理类
    - NodeManager.py主从模式的master启动文件
    - DataOutput.py爬取的数据输出处理类
- distributedCrawler的Slave主要分为三部份:
    - HtmlDownloader.py页面源码下载器类
    - HtmlParser.py提取数据处理类
    - SpiderWork.py Slave节点获取Master节点分发URL种子程序
- 使用方式：
    - 进入distributedCrawler的MasterNode目录运行命令：
    ```
    $ python NodeManager.py
    ```
    - 进入distributedCrawler的SlaveNode目录运行命令：
    ```
    $ python SpiderWork.py
    ```
- 运行环境: Linux（Ubuntu16.7）
