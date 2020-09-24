# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 09:57:53 2020

@author: Lenovo
"""

from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print ('运行任务 %s ，子进程号为(%s)...' % (name, os.getpid()))
    
    print ("我就是子进程号为(%s)处理的内容" % (os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print ('任务 %s 运行了 %0.2f 秒.' % (name, (end - start)))
    return 200

if __name__=='__main__':
    print ('父进程号为 %s.' % os.getpid())
    rst = []
    p = Pool(4)  #进程池中含有4个子进程
    for i in range(5): #4个子进程完成5个任务，所以有一个任务是需要等某个进程空闲再处理
        a = p.apply_async(long_time_task, args=(i,)) #a是进程处理函数long_time_task的返回结果
        rst.append(a)  #将次得到的结果添加到数组rst中去
    print ('等待所有子进程结束...')
    p.close()
    p.join()#等待所有子进程执行完毕。调用join()之前必须先调用close()，调用close()之后就不能继续添加新的Process了。
    print ('所有子进程结束...')
    


from multiprocessing import Process, freeze_support

def foo():
    print ('hello')

if __name__ == '__main__':
    freeze_support()
    p = Process(target=foo)
    p.start()



from multiprocessing import Process
import os

# 子进程要执行的代码
def run_proc(name):
    print ('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print ('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print ('Process will start.')
    p.start()
    p.join()
    print ('Process end.')

















