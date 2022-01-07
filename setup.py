from pymouse import PyMouse
from win32api import GetSystemMetrics
from random import randint
from time import sleep

# import threading
from threading import Timer,Thread
from tkinter import *
from tkinter.messagebox import *

min_t = 5
max_t = 60
cycle = 30
width = GetSystemMetrics(0)
heigth = GetSystemMetrics(1)

class Window(Frame):
    def __init__(self, master):
        self.root=master
        self.root.title('禁止休眠小助手')

        self.root.label = Label(self.root,text = "执行周期(10~60)")
        self.root.timeEntry = Entry(self.root, show = None)#显示成明文形式
        self.root.timeEntry.insert(0,'30')
        self.root.s_unit = Label(self.root,text = "s")
        self.root.label.grid(row=0,column=0)
        self.root.timeEntry.grid(row=0,column=1)
        self.root.s_unit.grid(row=0,column=2)

        self.root.run_btn = Button(self.root, text='开始', width=10, command= self.setTimerAndStart)

        self.root.stop_btn = Button(self.root, text='结束', width=10, command=self.stopTimer)

        self.root.run_btn.grid(row=1,column=2)
        self.root.stop_btn.grid(row=2,column=2)

        self.screen_width = self.root.winfo_screenwidth()#获得屏幕宽度
        self.screen_height = self.root.winfo_screenheight()  #获得屏幕高度
        self.root.update_idletasks()#刷新GUI
        self.root.withdraw() #暂时不显示窗口来移动位置
        self.root.geometry('%dx%d+%d+%d' % (self.root.winfo_width(), self.root.winfo_height() ,(self.screen_width - self.root.winfo_width()) / 2,(self.screen_height - self.root.winfo_height()) / 2))  # center window on desktop
        self.root.deiconify()     

    # 确认输入是否为整型数字
    def isNumber(self,s):
        try:
            int(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    # 设置定时器并启动
    def setTimerAndStart(self):
        inputtime = self.root.timeEntry.get()
        if self.isNumber(inputtime):
            cycle = int(inputtime)
            if cycle > max_t:
                cycle = max_t
            elif cycle < min_t:
                cycle = min_t
            self.cycle = cycle
            self.m = PyMouse()
        else:
            pass
    
        self.timer_threadobj = Thread(target = self.stratTimer)
        self.run = True
        showinfo('提示','鼠标漫步已开始')
        self.timer_threadobj.start()

    # 定时器执行程序
    def stratTimer(self):
        while self.run:
            x = randint(0, self.screen_width)
            y = randint(0, self.screen_height)
            self.m.move(x, y)
            sleep(self.cycle)
            
    # TODO 目前释放时间为10s,待优化
    def stopTimer(self):
        if self.timer_threadobj:
            self.run = False
            self.timer_threadobj.join()
            showinfo('提示','鼠标漫步已结束')
        else:
            print("error")
 
if __name__=='__main__':
    root=Tk()
    root.iconbitmap('icon.ico')
    Window(root)
    root.mainloop()