__author__ = 'Administrator'
from multiprocessing import Process,Queue
from multiprocessing.managers import BaseManager
import time
from UrlManager import UrlManager
from DataOutput import DataOutput


class NodeManager(object):


    def start_Manager(self,url_q,result_q):
        '''
        创建一个分布式管理器
        :param url_q:url队列
        :param result_q: 结果队列
        :return:
        '''
        # 把创建的两个队列注册在网络上，利用register方法,callable参数关联了Queue对象
        # 将Queue对象在网络中暴露
        BaseManager.register("get_task_queue",callable=lambda:url_q)
        BaseManager.register("get_result_queue",callable=lambda:result_q)
        # 绑定端口5000,设置验证口令'abc',这个相当于对象的初始化
        manager=BaseManager(address=("127.0.0.1",5000),authkey=b'abc')
        # 返回manager对象
        return manager

    # url_q队列是URL管理进程将URL传递给爬虫节点的通道
    # result_q队列是爬虫节点将数据返回给数据提取进程的通道
    # conn_q队列是数据提取进程将新的URL数据提交给URL管理进程的通道
    # store_q队列是数据提取进程将获取到的数据交给数据存储进程的通道
    def url_manager_proc(self,url_q,conn_q,root_url):
        url_manager=UrlManager()
        url_manager.add_new_url(root_url)
        while True:
            while (url_manager.has_new_url()):
                # 从URL管理器获取新的url
                new_url=url_manager.get_new_url()
                # 将新的URL发给工作节点
                url_q.put(new_url)
                print("old_url=",url_manager.old_url_size())
            # 加一个判断条件，当爬取了2000条URL就关闭，并保存进度
                if(url_manager.old_url_size()>2000):
                #通知爬行节点工作结束
                    print("爬取工作结束")
                    url_manager.save_progress("new_urls.txt",url_manager.new_urls)
                    url_manager.save_progress("old_urls.txt",url_manager.old_urls)
                    return
            # 将从result_solve_proc获取到的urls添加到URL管理器中
            try:
                if not conn_q.empty():
                    urls=conn_q.get()
                    print(urls)
                    url_manager.add_new_urls(urls)
            except BaseException as e:
                time.sleep(0.1)#延时休息

    def result_solve_proc(self,result_q,conn_q,store_q):
        while (True):
            try:
                if not result_q.empty():
                    content=result_q.get(True)
                    #print(content)
                    if content["new_urls"]=="end":
                        print("结果分析进程接受通知然后结束")
                        store_q.put('end')
                        return
                    conn_q.put(content["new_urls"])#url为set类型
                    store_q.put(content["data"])#解释出来的数据为dict
                else:
                    time.sleep(0.1)#延时休息
            except BaseException as e:
                time.sleep(0.1)

    def store_proc(self,store_q):
        output=DataOutput()
        while True:
            if not store_q.empty():
                data=store_q.get()
                if data=='end':
                    print("储存进程接受通知然后结束")
                    output.output_end(output.filepath)
                    return
                output.store_data(data)
            else:
                time.sleep(0.1)
        pass


if __name__=="__main__":
    # 暴露给所有slave节点的URL队列
    url_q=Queue()
    # 暴露给所有slave节点的数据队列，提供给slave返回数据储存
    result_q=Queue()
    # master节点的储存队列
    store_q=Queue()
    # urls集合队列
    conn_q=Queue()
    node=NodeManager()
    manager=node.start_Manager(url_q,result_q)

    url_manager_proc=Process(target=node.url_manager_proc,args=(url_q,conn_q,'http://baike.baidu.com/view/284853.html',))

    result_solve_proc=Process(target=node.result_solve_proc,args=(result_q,conn_q,store_q,))

    store_proc=Process(target=node.store_proc,args=(store_q,))
	
    url_manager_proc.start()
    result_solve_proc.start()
    store_proc.start()
    manager.get_server().serve_forever()
