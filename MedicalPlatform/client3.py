import socket
import threading
import json  
import tkinter
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText  
import time
from tkinter import filedialog

IP = ''
PORT = ''
user = ''
listbox1 = ''  # 显示在线用户
ii = 0  
users = []  # 在线用户列表
chat = '群聊'  # 聊天对象, 默认为群聊


# 登陆界面
root1 = tkinter.Tk()
root1.title('登录')
root1['height'] = 110
root1['width'] = 270
root1.resizable(0, 0)  

IP1 = tkinter.StringVar()
IP1.set('127.0.0.1:54321') 
User = tkinter.StringVar()
User.set('')

labelIP = tkinter.Label(root1, text='服务器地址')
labelIP.place(x=20, y=10, width=100, height=20)

entryIP = tkinter.Entry(root1, width=80, textvariable=IP1)
entryIP.place(x=120, y=10, width=130, height=20)

labelUser = tkinter.Label(root1, text='账号')
labelUser.place(x=30, y=40, width=80, height=20)

entryUser = tkinter.Entry(root1, width=80, textvariable=User)
entryUser.place(x=120, y=40, width=130, height=20)


# 登录按钮
def login(*args):
    global IP, PORT, user
    IP, PORT = entryIP.get().split(':')  
    PORT = int(PORT)                     
    user = entryUser.get()
    if not user:
        tkinter.messagebox.showerror('用户名类型错误', message=' 空用户名')
    else:
        root1.destroy()                  


root1.bind('<Return>', login)           
but = tkinter.Button(root1, text='登录', command=login)
but.place(x=100, y=70, width=70, height=30)

root1.mainloop()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
if user:
    s.send(user.encode()) 
else:
    s.send('no'.encode()) 

addr = s.getsockname()
addr = addr[0] + ':' + str(addr[1])
if user == '':
    user = addr

# 聊天窗口
root = tkinter.Tk()
root.title(user) 
root['height'] = 400
root['width'] = 580
root.resizable(0, 0)  

listbox = ScrolledText(root)
listbox.place(x=135, y=0, width=570, height=320)

listbox.tag_config('red', foreground='red')
listbox.tag_config('blue', foreground='blue')
listbox.tag_config('green', foreground='green')
listbox.tag_config('pink', foreground='pink')
listbox.insert(tkinter.END, '欢迎使用远程医疗系统!', 'blue')

# 表情包
b1 = ''
b2 = ''
b3 = ''

p1 = tkinter.PhotoImage(file='./emoji/mingbai.png')
p2 = tkinter.PhotoImage(file='./emoji/bumiao.png')
p3 = tkinter.PhotoImage(file='./emoji/zhengtinghao.png')

dic = {'mingbai*': p1, 'bumiao*': p2, 'zhengtinghao*': p3}
ee = 0  


def mark(exp):  
    global ee
    mes = exp + ':;' + user + ':;' + chat
    s.send(mes.encode())
    b1.destroy()
    b2.destroy()
    b3.destroy()
    ee = 0

def bb1():
    mark('mingbai*')

def bb2():
    mark('bumiao*')

def bb3():
    mark('zhengtinghao*')

def express():
    global b1, b2, b3, ee
    if ee == 0:
        ee = 1
        b1 = tkinter.Button(root, command=bb1, image=p1,
                            relief=tkinter.FLAT, bd=0)
        b2 = tkinter.Button(root, command=bb2, image=p2,
                            relief=tkinter.FLAT, bd=0)
        b3 = tkinter.Button(root, command=bb3, image=p3,
                            relief=tkinter.FLAT, bd=0)

        b1.place(x=5, y=248)
        b2.place(x=105, y=248)
        b3.place(x=225, y=248)
    else:
        ee = 0
        b1.destroy()
        b2.destroy()
        b3.destroy()


# 表情按钮
eBut = tkinter.Button(root, text='表情', command=express)
eBut.place(x=140, y=320, width=60, height=30)


# 图片功能

def fileGet(name):
    PORT3 = 54323
    ss2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss2.connect((IP, PORT3))
    message = 'get ' + name
    ss2.send(message.encode())
    fileName = '.\\Cimage\\' + name
    print('开始下载图片！')
    with open(fileName, 'wb') as f:
        while True:
            data = ss2.recv(1024)
            if data == 'EOF'.encode():
                print('下载完成！')
                break
            f.write(data)
    time.sleep(0.1)
    ss2.send('quit'.encode())


def filePut(fileName):
    PORT3 = 54323
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.connect((IP, PORT3))
    print(fileName)
    name = fileName.split('/')[-1]
    print(name)
    message = 'put ' + name
    ss.send(message.encode())
    time.sleep(0.1)
    print('开始上传图片!')
    with open(fileName, 'rb') as f:
        while True:
            a = f.read(1024)
            if not a:
                break
            ss.send(a)
        time.sleep(0.1)  
        ss.send('EOF'.encode())
        print('上传成功！')
    ss.send('quit'.encode())
    time.sleep(0.1)
    
    mes = '``#' + name + ':;' + user + ':;' + chat
    s.send(mes.encode())


def picture():
    fileName = tkinter.filedialog.askopenfilename(title='请选择上传图片')
    if fileName:   
        filePut(fileName)


# 创建发送图片按钮
pBut = tkinter.Button(root, text='图片', command=picture)
pBut.place(x=200, y=320, width=60, height=30)



# 文件功能

list2 = ''  
label = ''  
upload = ''  
close = ''  


def fileClient():
    PORT2 = 54322  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT2))

    
    root['height'] = 390
    root['width'] = 760

    
    list2 = tkinter.Listbox(root)
    list2.place(x=580, y=25, width=175, height=325)

    # 打印接收到的目录文件列表
    def recvList(enter, lu):
        s.send(enter.encode())
        data = s.recv(4096)
        data = json.loads(data.decode())
        list2.delete(0, tkinter.END)  
        lu = lu.split('\\')
        if len(lu) != 1:
            list2.insert(tkinter.END, '返回上一级')
            list2.itemconfig(0, fg='green')
        for i in range(len(data)):
            list2.insert(tkinter.END, ('' + data[i]))
            if '.' not in data[i]:
                list2.itemconfig(tkinter.END, fg='orange')
            else:
                list2.itemconfig(tkinter.END, fg='blue')

    # 创建标签显示服务端工作目录
    def lab():
        global label
        data = s.recv(1024)  
        lu = data.decode()
        try:
            label.destroy()
            label = tkinter.Label(root, text=lu)
            label.place(x=580, y=0, )
        except:
            label = tkinter.Label(root, text=lu)
            label.place(x=580, y=0, )
        recvList('dir', lu)

    # cd指定目录
    def cd(message):
        s.send(message.encode())

    # 刷新
    cd('cd same')
    lab()

    # 接收下载文件(get)
    def get(message):
        # print(message)
        name = message.split(' ')
        # print(name)
        name = name[1]        
        fileName = tkinter.filedialog.asksaveasfilename(title='保存文件至', initialfile=name)
        if fileName:
            s.send(message.encode())
            with open(fileName, 'wb') as f:
                while True:
                    data = s.recv(1024)
                    if data == 'EOF'.encode():
                        tkinter.messagebox.showinfo(title='Message',
                                                    message='下载成功')
                        break
                    f.write(data)

    # 创建用于绑定在列表框上的函数
    def run(*args):
        indexs = list2.curselection()
        index = indexs[0]
        content = list2.get(index)
        if '.' in content:
            content = 'get ' + content
            get(content)
            cd('cd same')
        elif content == '返回上一级':
            content = 'cd ..'
            cd(content)
        else:
            content = 'cd ' + content
            cd(content)
        lab()  

    # 在列表框上设置绑定事件
    list2.bind('<ButtonRelease-1>', run)

    # 上传客户端所在文件夹中指定的文件到服务端, 在函数中获取文件名, 不用传参数
    def put():
        fileName = tkinter.filedialog.askopenfilename(title='选择上传文件')
        if fileName:
            name = fileName.split('/')[-1]
            message = 'put ' + name
            s.send(message.encode())
            with open(fileName, 'rb') as f:
                while True:
                    a = f.read(1024)
                    if not a:
                        break
                    s.send(a)
                time.sleep(0.1)
                s.send('EOF'.encode())
                tkinter.messagebox.showinfo(title='Message',
                                            message='上传完毕!')
        cd('cd same')
        lab()  

    # 创建上传按钮, 并绑定上传文件功能
    upload = tkinter.Button(root, text='上传文件', command=put)
    upload.place(x=600, y=353, height=30, width=80)

    # 关闭文件管理器
    def closeFile():
        root['height'] = 390
        root['width'] = 580
        # 关闭连接
        s.send('quit'.encode())
        s.close()

    # 创建关闭按钮
    close = tkinter.Button(root, text='关闭', command=closeFile)
    close.place(x=685, y=353, height=30, width=70)


# 创建文件按钮
fBut = tkinter.Button(root, text='文件上传', command=fileClient)
fBut.place(x=260, y=320, width=60, height=30)

# 创建多行文本框, 显示在线用户
listbox1 = tkinter.Listbox(root)
listbox1.place(x=5, y=0, width=130, height=320)

# 隐藏控件
def hide():
    global listbox1, ii
    if ii == 1:
        listbox1.place(x=5, y=0, width=130, height=320)
        ii = 0
    else:
        listbox1.place_forget() 
        ii = 1


# 查看在线用户按钮
button1 = tkinter.Button(root, text='查看在线用户', command=hide)
button1.place(x=5, y=320, width=90, height=30)

# 创建输入文本框和关联变量
a = tkinter.StringVar()
a.set('')
entry = tkinter.Entry(root, width=120, textvariable=a)
entry.place(x=5, y=350, width=570, height=40)



def send(*args):
    users.append('群聊')  
    print(chat)
    if chat not in users:
        tkinter.messagebox.showerror('Send error', message='没人和你说话哦!')
        return
    if chat == user:
        tkinter.messagebox.showerror('Send error', message='不要和自己说话哦!')
        return
    mes = entry.get() + ':;' + user + ':;' + chat 
    s.send(mes.encode())
    a.set('')  # 


# 创建发送按钮
button = tkinter.Button(root, text='发送', command=send)
button.place(x=515, y=353, width=60, height=30)
root.bind('<Return>', send) 


# 私聊功能
def private(*args):
    global chat
   
    indexs = listbox1.curselection()
    index = indexs[0]
    if index > 0:
        chat = listbox1.get(index)
        
        if chat == '群聊':
            root.title(user)
            return
        ti = user + '  -->  ' + chat
        root.title(ti)


# 在显示用户列表框上设置绑定事件
listbox1.bind('<ButtonRelease-1>', private)


# 用于时刻接收服务端发送的信息并打印
def recv():
    global users
    while True:
        data = s.recv(1024)
        data = data.decode()
        
        try:
            data = json.loads(data)
            users = data
            listbox1.delete(0, tkinter.END) 
            number = ('   在线用户: ' + str(len(data)))
            listbox1.insert(tkinter.END, number)
            listbox1.itemconfig(tkinter.END, fg='green', bg="#f0f0ff")
            listbox1.insert(tkinter.END, '群聊')
            listbox1.itemconfig(tkinter.END, fg='blue')
            for i in range(len(data)):
                listbox1.insert(tkinter.END, (data[i]))
                listbox1.itemconfig(tkinter.END, fg='green')
        except:
            data = data.split(':;')
            data1 = data[0].strip()
            data2 = data[1]
            data3 = data[2]

            markk = data1.split('：')[1]
            # 图片
            pic = markk.split('#')
            # 表情
            if (markk in dic) or pic[0] == '``':
                data4 = '\n' + data2 + '：'  
                if data3 == '群聊':
                    if data2 == user:  
                        listbox.insert(tkinter.END, data4, 'blue')
                    else:
                        listbox.insert(tkinter.END, data4, 'green')  
                elif data2 == user or data3 == user:  
                    listbox.insert(tkinter.END, data4, 'red')  
                if pic[0] == '``':
                   
                    fileGet(pic[1])
                else:
                
                    listbox.image_create(tkinter.END, image=dic[markk])
            else:
                data1 = '\n' + data1
                if data3 == '群聊':
                    if data2 == user:  
                        listbox.insert(tkinter.END, data1, 'blue')
                    else:
                        listbox.insert(tkinter.END, data1, 'green')  
                    if len(data) == 4:
                        listbox.insert(tkinter.END, '\n' + data[3], 'pink')
                elif data2 == user or data3 == user:  
                    listbox.insert(tkinter.END, data1, 'red')  
            listbox.see(tkinter.END)  


r = threading.Thread(target=recv)
r.start()  

root.mainloop()
s.close()  
