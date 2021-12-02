import threading
import time


def movie():
    print('this is movie')
    time.sleep(5)


def movie1():
    print('this is movie1')
    time.sleep(4)


def movie2():
    print('this is movie2')
    time.sleep(3)


threads = []
t1 = threading.Thread(target=movie)
threads.append(t1)
t2 = threading.Thread(target=movie1)
threads.append(t2)
t3 = threading.Thread(target=movie2)
threads.append(t3)

if __name__ == '__main__':

    for i in threads:
        i.start()
    for i in threads:
        i.join()

    print('线程执行结束了')