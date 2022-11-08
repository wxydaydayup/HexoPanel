import tkinter as tk  # 导入Tkinter
from tkinter.scrolledtext import ScrolledText  # 导入ScrolledText
import webbrowser
import sys
import os
import subprocess
import signal

rootDir = "F:/MyBlog" #这个需要改成自己Hexo的根目录

class StdoutRedirector(object):  # Print重定向类
    def __init__(self, ScrolledText):
        self.text_space = ScrolledText
        # 备份
        self.stdoutbak = sys.stdout
        self.stderrbak = sys.stderr
    def write(self, str):
        self.text_space.insert(tk.END, str)
        self.text_space.see(tk.END)
        # 刷新显示
        self.text_space.update() 
    # 还原
    def restoreStd(self):
        sys.stdout = self.stdoutbak
        sys.stderr = self.stderrbak
    # 这个类必须得有，不然会报错
    def flush(self):
        pass

def sh(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) 
    #如需要将打印信息打印到tkinter，则取消下面注释。若出现乱码问题，换为GDK编码
    # lines = []
    # for line in iter(p.stdout.readline, b''):
    #     line = line.strip().decode("utf-8","ignore")
    #     print(">>>", line)
    #     lines.append(line)
    # return lines

def killPort(port): # 关闭进程
    r = os.popen("netstat -ano | findstr "+port)
    text = r.read()
    arr=text.split("\n")
    for text0 in arr:
        arr2=text0.split(" ")
        if len(arr2)>1:
            pid=arr2[len(arr2)-1]
            print('kill '+pid)
            if(pid == '0'):
                break
            os.system("taskkill /PID "+pid+" /T /F")
            break
    r.close()  
    
def btnfunc01():  # 刷新 
    output = sys.stdout
    sys.stdout = StdoutRedirector(textMess)
    killPort('4000')
    os.chdir(rootDir)
    sh("hexo clean")
    sh("hexo s")
    print("刷新成功")
    sys.stdout = output
    
def btnfunc02(): # 打开网址
    output = sys.stdout
    sys.stdout = StdoutRedirector(textMess)
    webbrowser.open("http://localhost:4000/")
    print("打开网址成功")
    sys.stdout = output
    
def btnfunc03():  # 发布
    output = sys.stdout
    sys.stdout = StdoutRedirector(textMess)
    os.chdir(rootDir)
    sh("hexo clean")
    sh("hexo d")
    print("已发布到Github")
    sys.stdout = output
    
def new():       # 新建
    last = NameEntry.get()                    # 获取输入框内容
    output = sys.stdout                       # 备份
    sys.stdout = StdoutRedirector(textMess)   # Print重定向类
    os.chdir(rootDir) 
    sh("hexo new "+last)
    print(last+" 新建成功")
    sys.stdout = output                       # 恢复到备份

def newDraft():  # 新建草稿
    last = NameEntry.get()                    # 获取输入框内容
    output = sys.stdout                       # 备份
    sys.stdout = StdoutRedirector(textMess)   # Print重定向类
    os.chdir(rootDir) 
    sh("hexo new draft"+last)
    print(last+" 新建草稿成功")
    sys.stdout = output                        # 恢复到备份

def clearMess():  # 清空打印
    global textMess
    textMess.delete(1.0, tk.END)

if __name__ == '__main__':
    # 建立主窗口
    root = tk.Tk()
    mytitle = 'hexo控制台'
    root.title(mytitle)
    root.geometry('{}x{}+{}+{}'.format(700, 600, 400, 100))
    
    # 新建文件输入框
    frame = tk.Frame(root)
    lb = tk.Label(frame, text='新建文件名:',font=('楷体',12), width=13, height=1)
    NameEntry = tk.Entry(frame, font=('楷体',12), width=23)
    # 确定按钮与草稿按钮
    updateButton = tk.Button(frame, text='确定', font=('楷体', 10), width=5, height=1)
    draftButton = tk.Button(frame, text='草稿', font=('楷体', 10), width=5, height=1)
    updateButton['command'] = lambda: new()
    draftButton['command'] = lambda: newDraft()
    # 新建文件输入框、确定按钮与草稿按钮的布局
    lb.pack(side=tk.LEFT)
    NameEntry.pack(side=tk.LEFT)
    updateButton.pack(side=tk.LEFT,padx=5)
    draftButton.pack(side=tk.LEFT)
    frame.pack(side=tk.TOP, fill=tk.BOTH)
    
    # 设置按钮的样式和位置
    frame1 = tk.Frame(root)
    global button1,button2,button3,button4
    button1 = tk.Button(frame1, text='刷新', bg='green', font=('楷体', 11), width=7, height=1)
    button2 = tk.Button(frame1, text='网址', bg='green', font=('楷体', 11), width=7, height=1)
    button3 = tk.Button(frame1, text='发布', bg='green', font=('楷体', 11), width=7, height=1)
    button4 = tk.Button(frame1, text='打开文件位置', font=('楷体', 12), width=12, height=1)
    button1.pack(side=tk.LEFT,padx=5)
    button2.pack(side=tk.LEFT,padx=5)
    button3.pack(side=tk.LEFT,padx=5)
    button4.pack(side=tk.RIGHT)
    frame1.pack(side=tk.TOP, fill=tk.BOTH)
    # 为按钮设置功能
    button1['command'] = lambda: btnfunc01()                                           # 刷新
    button2['command'] = lambda: btnfunc02()                                           # 打开网址
    button3['command'] = lambda: btnfunc03()                                           # 新建
    button4['command'] = lambda: btnfunc04(rootDir)                                    # 打开文件分配位置

    #为信息框设置一个容器作为信息输出窗口
    global textMess
    frame2 = tk.LabelFrame(root, text='打印信息', height=2)
    textMess = ScrolledText(frame2, bg='white', height=10)
    textMess.pack(fill=tk.BOTH, expand=1)
    clearMessbutton = tk.Button(frame2, text='清空信息', font=('楷体', 12), width=7, height=1)
    clearMessbutton.pack(anchor='se')
    clearMessbutton['command'] = lambda: clearMess()                                   #清空打印
    frame2.pack(fill=tk.BOTH, expand=1)

    # 进入Tkinter消息循环
    root.mainloop()