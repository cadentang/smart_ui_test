import datetime,time,random
def make(func):
    def mak(*args,**kwargs):
        try:
            func(*args,**kwargs)
        except Exception as e:
            print(str(e))
            with open('except.txt','a+') as f:
                except_time=datetime.datetime.now()
                f.writelines(except_time.strftime('%Y-%m-%d  %H:%M:%S')+'\n')
                f.close()
            with open('except.txt','rb') as m:
                try:
                    date=m.readlines()[-5].decode('utf-8')
                    ne=(date.split('\r\n')[0])
                    f1=datetime.datetime.strptime(ne,'%Y-%m-%d %H:%M:%S')
                    if (except_time-f1).seconds<6:
                        print('异常！！！fail')
                    else:
                        print('正常！')
                    m.close()
                except:
                    print('越界代表着我们的实验是成功的')
    return mak
@make
def beijing(i,m):
    print(i/m)


class Screen:
    def __init__(self, driver):
        self.driver = driver

    def __call__(self, func):
        def inner(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except:
                import time
                nowtime = time.strftime("%Y_%m_%d_%H_%M_%S")
                self.driver.get_screenshot_as_file("%s.png" % nowtime)
                raise
        return inner



if __name__=="__main__":
    while True:
        f=random.choice([0,1,2,3])
        n=random.choice([0,1,2,3])
        beijing(f,n)
        time.sleep(0.3)