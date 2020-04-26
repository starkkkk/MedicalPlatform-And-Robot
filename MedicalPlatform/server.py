import socket
import threading
import queue
import json  
import time
import os
import os.path
import sys
import tkinter
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText  

IP = ''
PORT = 54321
que = queue.Queue()                             # 存放客户端发送信息的队列
users = []                                      # 用于存放在线用户的信息  [conn, user, addr]
lock = threading.Lock()                        





root = tkinter.Tk()
root.title('服务端')  
root['height'] = 400
root['width'] = 580
root.resizable(0, 0)  


listbox = ScrolledText(root)
listbox.place(x=5, y=5, width=570, height=390)
listbox.tag_config('red', foreground='red')
listbox.tag_config('blue', foreground='blue')
listbox.tag_config('green', foreground='green')
listbox.tag_config('pink', foreground='pink')
listbox.insert(tkinter.END, '开始监视！', 'pink')




# 将在线用户存入online列表并返回
def onlines():
    online = []
    for i in range(len(users)):
        online.append(users[i][1])
    return online


class ChatServer(threading.Thread):
    global users, que, lock

    def __init__(self, port):
        threading.Thread.__init__(self)
        self.ADDR = ('', port)
        os.chdir(sys.path[0])
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 用于接收所有客户端发送信息的函数
    def tcp_connect(self, conn, addr):
        user = conn.recv(1024)                                    
        user = user.decode()

        for i in range(len(users)):
            if user == users[i][1]:
                e11 = '\n' + '用户已经登录' 
                listbox.insert(tkinter.END, e11,'red') 
#                print('用户已经登录')
                user = '' + user + '_2'

        if user == 'no':
            user = addr[0] + ':' + str(addr[1])
        users.append((conn, user, addr))
        
        u1 = '\n' + user + '上线了'
        listbox.insert(tkinter.END, u1,'green')
                
        d = onlines()
        # 保存信息到队列                                                  
        self.recv(d, addr)
        try:
            while True:
                data = conn.recv(1024)
                data = data.decode()
                self.recv(data, addr)                       
            conn.close()
        except:
            e12 = '\n' + user + '下线了' 
            listbox.insert(tkinter.END, e12,'green')
#            print(user + ' 下线了')
            self.delUsers(conn, addr)                            
            conn.close()

    # 刷新客户端的在线用户显示
    def delUsers(self, conn, addr):
        a = 0
        for i in users:
            if i[0] == conn:
                users.pop(a)
#                print(' 剩余在线用户： ', end='')        
                d = onlines()
                self.recv(d, addr)                
#                print(d)
                break
            a += 1

    # 接收到的信息存入que队列
    def recv(self, data, addr):
        lock.acquire()
        try:
            que.put((addr, data))
        finally:
            lock.release()

    # 将队列que中的消息发送给所有连接到的用户
    def sendData(self):
        while True:
            if not que.empty():
                data = ''
                message = que.get()                              
                if isinstance(message[1], str):                   
                    for i in range(len(users)):
                        for j in range(len(users)):
                            if message[0] == users[j][2]:

                                data = ' ' + users[j][1] + '：' + message[1]
                                break      
                        users[i][0].send(data.encode())
                data = data.split(':;')[0]
#                print(data)
                u4 = '\n' + data
                listbox.insert(tkinter.END, u4,'blue')                 
                

                if isinstance(message[1], list):  
 
                    data = json.dumps(message[1])
                    for i in range(len(users)):
                        try:
                            users[i][0].send(data.encode())
                        except:
                            pass

    def run(self):

        self.s.bind(self.ADDR)
        self.s.listen(3)
        
        k1 = '\n' + '聊天服务器正在启动...' 
        listbox.insert(tkinter.END, k1,'green') 
        
        q = threading.Thread(target=self.sendData)
        q.start()
        while True:
            conn, addr = self.s.accept()
            t = threading.Thread(target=self.tcp_connect, args=(conn, addr))
            t.start()
        self.s.close()

################################################################


class FileServer(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.ADDR = ('', port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.first = r'.\resources'
        os.chdir(self.first)                                     

    def tcp_connect(self, conn, addr):        
        while True:
            data = conn.recv(1024)
            data = data.decode()
            if data == 'quit':
                print('断开连接 {0}'.format(addr))
                break
            order = data.split(' ')[0]                            
            self.recv_func(order, data, conn)
                
        conn.close()

    # 传输当前目录列表
    def sendList(self, conn):
        listdir = os.listdir(os.getcwd())
        listdir = json.dumps(listdir)
        conn.sendall(listdir.encode())

    # 发送文件函数
    def sendFile(self, message, conn):
        name = message.split()[1]                               
        fileName = r'./' + name
        with open(fileName, 'rb') as f:    
            while True:
                a = f.read(1024)
                if not a:
                    break
                conn.send(a)
        time.sleep(0.1)                                         
        conn.send('EOF'.encode())

    # 保存上传的文件到当前工作目录
    def recvFile(self, message, conn):
        name = message.split()[1]                             
        fileName = r'./' + name
        with open(fileName, 'wb') as f:
            while True:
                data = conn.recv(1024)
                if data == 'EOF'.encode():
                    break
                f.write(data)

    # 切换工作目录
    def cd(self, message, conn):
        message = message.split()[1]                         
     
        if message != 'same':
            f = r'./' + message
            os.chdir(f)
        
        path = os.getcwd().split('\\')                     
        for i in range(len(path)):
            if path[i] == 'resources':
                break
        pat = ''
        for j in range(i, len(path)):
            pat = pat + path[j] + ' '
        pat = '\\'.join(pat.split())
        if 'resources' not in path:
            f = r'./resources'
            os.chdir(f)
            pat = 'resources'
        conn.send(pat.encode())

    # 判断输入的命令并执行对应的函数
    def recv_func(self, order, message, conn):
        if order == 'get':
            return self.sendFile(message, conn)
        elif order == 'put':
            return self.recvFile(message, conn)
        elif order == 'dir':
            return self.sendList(conn)
        elif order == 'cd':
            return self.cd(message, conn)

    def run(self):
        
        k2 = '\n' + '文件服务器正在启动...' 
        listbox.insert(tkinter.END, k2,'green') 
#        print('文件服务器正在启动...')
        
        self.s.bind(self.ADDR)
        self.s.listen(3)
        while True:
            conn, addr = self.s.accept()
            t = threading.Thread(target=self.tcp_connect, args=(conn, addr))
            t.start()
        self.s.close()

#############################################################################


class PictureServer(threading.Thread):

    def __init__(self, port):
        threading.Thread.__init__(self)
        self.ADDR = ('', port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        os.chdir(sys.path[0])
        self.folder = '.\\Simage\\'  

    def tcp_connect(self, conn, addr):
        while True:
            data = conn.recv(1024)
            data = data.decode()
            if data == 'quit':
                break
            order = data.split()[0]  
            self.recv_func(order, data, conn)
        conn.close()

    # 发送文件函数
    def sendFile(self, message, conn):
        e13 = '\n' + message 
        listbox.insert(tkinter.END, e13 , 'green')
#        print(message)
        name = message.split()[1]                  
        fileName = self.folder + name               
        f = open(fileName, 'rb')
        while True:
            a = f.read(1024)
            if not a:
                break
            conn.send(a)
        time.sleep(0.1)             # 延时，不然不完整                             
        conn.send('EOF'.encode())
#        print('图片发送 !')

    # 保存上传的文件到当前工作目录
    def recvFile(self, message, conn):
#        print(message)

        name = message.split(' ')[1]                  
        fileName = self.folder + name                 
#        print(fileName)
#        print('正在保存 ！')
        f = open(fileName, 'wb+')
        while True:
            data = conn.recv(1024)
            if data == 'EOF'.encode():
                p1 = '\n' + '图片发送成功' 
                listbox.insert(tkinter.END, p1,'green') 
#                print('保存成功 !')
                break
            f.write(data)

    # 判断输入的命令并执行对应的函数
    def recv_func(self, order, message, conn):
        if order == 'get':
            return self.sendFile(message, conn)
        elif order == 'put':
            return self.recvFile(message, conn)

    def run(self):
        self.s.bind(self.ADDR)
        self.s.listen(5)
        
        k3 = '\n' + '图片服务器正在启动...' 
        listbox.insert(tkinter.END, k3,'green') 
        
#        print('图片服务器正在启动...')
        while True:
            conn, addr = self.s.accept()
            t = threading.Thread(target=self.tcp_connect, args=(conn, addr))
            t.start()
        self.s.close()

####################################################################################


if __name__ == '__main__':
    cserver = ChatServer(PORT)
    fserver = FileServer(PORT + 1)
    pserver = PictureServer(PORT + 2)
    cserver.start()
    fserver.start()
    pserver.start()
    
    root.mainloop()
    while True:
        time.sleep(1)
        if not cserver.isAlive():
            e1 = '\n' + '聊天服务器丢失...' 
            listbox.insert(tkinter.END, e1,'red') 
#            print("Chat connection lost...")
            sys.exit(0)
        if not fserver.isAlive():
            e2 = '\n' + '文件服务器丢失...' 
            listbox.insert(tkinter.END, e2,'red') 
#            print("File connection lost...")
            sys.exit(0)
        if not pserver.isAlive():
            e3 = '\n' + '图片服务器丢失...' 
            listbox.insert(tkinter.END, e3,'red') 
#            print("Picture connection lost...")
            sys.exit(0)
