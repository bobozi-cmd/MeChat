import threading
import time

class ReadWriteLock:
    def __init__(self):
        self.lock = threading.Lock()
        self.readers = 0
        self.writers = 0
        self.cv = threading.Condition(self.lock)
    
    def acquire_read(self):
        with self.lock:
            while self.writers > 0:
                self.cv.wait()
            self.readers += 1
    
    def release_read(self):
        with self.lock:
            self.readers -= 1
            self.cv.notify_all()
    
    def acquire_write(self):
        with self.lock:
            self.writers += 1
            while self.readers > 0 or self.writers > 1:
                self.cv.wait()
    
    def release_write(self):
        with self.lock:
            self.writers -= 1
            self.cv.notify_all()

if __name__ == "__main__":
    # 公共变量
    count = 0

    # 创建读写锁
    rw_lock = ReadWriteLock()

    def read():
        global count
        while True:
            # 获取读锁
            rw_lock.acquire_read()
            print(f"Read count: {count}")
            # 模拟读取操作
            time.sleep(1)
            # 释放读锁
            rw_lock.release_read()

    def write():
        global count
        while True:
            # 获取写锁
            rw_lock.acquire_write()
            count += 1
            print(f"Write count: {count}")
            # 模拟写入操作
            time.sleep(2)
            # 释放写锁
            rw_lock.release_write()

    # 创建多个读线程和写线程
    threads = []
    for _ in range(5):
        t = threading.Thread(target=read)
        threads.append(t)
        t.start()

    for _ in range(2):
        t = threading.Thread(target=write)
        threads.append(t)
        t.start()

    # 等待所有线程执行完成
    for t in threads:
        t.join()