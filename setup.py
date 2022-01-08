from pymouse import PyMouse
from win32api import GetSystemMetrics
from random import randint
from time import ctime,time

# import threading
from threading import Timer,Thread
from tkinter import *
from tkinter.messagebox import *

from MyThread import thread_with_exception

min_t = 3
max_t = 60
width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

class Window(Frame):
    def __init__(self, master):
        self.root=master
        self.root.title('禁止休眠小助手')

        self.cycle = 30
        self.root.label = Label(self.root,width=15,text = "执行周期 (5~60) ")
        self.root.timeEntry = Entry(self.root,width=10, show = None,textvariable=self.cycle)#显示成明文形式
        
        self.root.timeEntry.insert(0,'30')
        self.root.s_unit = Label(self.root,text = "秒", width=10, anchor = 'w')
        self.root.label.grid(row=0,column=0)
        self.root.timeEntry.grid(row=0,column=1)
        self.root.s_unit.grid(row=0,column=2)

        self.root.run_btn = Button(self.root, text='开始[Space]', width=10, command= self.startTimer)

        self.root.stop_btn = Button(self.root, text='结束[Esc]', width=10, command=self.stopTimer)

        self.root.run_btn.grid(row=1,column=2)
        self.root.stop_btn.grid(row=2,column=2)

        self.screen_width = width#获得屏幕宽度
        self.screen_height = height  #获得屏幕高度
        self.root.update_idletasks()
        self.root.withdraw() #暂时不显示窗口来移动位置
        self.root.geometry('%dx%d+%d+%d' % (self.root.winfo_width(), self.root.winfo_height() ,(self.screen_width - self.root.winfo_width()) / 2,(self.screen_height - self.root.winfo_height()) / 2))  # center window on desktop
        self.root.deiconify()

        # 设置快捷方式，关闭软件前强制检查线程是否释放
        self.root.bind_all("<Return>", self.startTimer_handler)
        self.root.bind_all("<Escape>", self.stopTimer_handler)
        self.root.protocol('WM_DELETE_WINDOW', self.exit_stopTimer)

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

    # 检查输入值
    def cycleNumberCheck(self,cycle_string):
        cycle = int(cycle_string)
        if cycle > max_t:
            cycle = max_t
        elif cycle < min_t:
            cycle = min_t
        self.cycle = cycle

    # 设置定时器并启动
    def startTimer(self):
        inputtime_string = self.root.timeEntry.get()
        if self.isNumber(inputtime_string):
            self.cycleNumberCheck(inputtime_string)            
            self.m = PyMouse()
            self.no_sleep_timer_thread = thread_with_exception(self.cycle)  # 新建一个禁止休眠进程
            self.no_sleep_timer_thread.start()# 启动线程
            print("thread start %s" %  ctime(time()))
            showinfo('提示','鼠标漫步开始')
        else:
            pass
    
    def startTimer_handler(self,event):
        self.startTimer()

    # 关闭定时器
    def stopTimer(self):
        if 'no_sleep_timer_thread' in dir(self):
            self.no_sleep_timer_thread.stop_thread()
            showinfo('提示','鼠标漫步已结束')
        else:
            print("无定时器线程")
            pass

    def stopTimer_handler(self,event):
        self.stopTimer()
    
    def exit_stopTimer(self):
        self.stopTimer()
        root.destroy()
 
if __name__=='__main__':
    root=Tk()
    root.iconbitmap('icon.ico')
    Window(root)
    root.mainloop()