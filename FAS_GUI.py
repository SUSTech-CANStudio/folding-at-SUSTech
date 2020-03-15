from tkinter import *
import os
import subprocess
from login import *

global login_ok
login_ok = False

# window for login 
def login_clicked():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("登录")
    login_screen.geometry("300x250")
    login_screen.iconbitmap("icon.ico")
    Label(login_screen, text="SUSTech CAS身份认证").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="用户名 * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    username_login_entry.focus()
    Label(login_screen, text="").pack()
    Label(login_screen, text="密码 * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    btn = Button(login_screen, text="登录", width=10, height=1, command=login_verify).pack()

# Implementing event on login button 
def login_verify():
    global username
    global password
    username = username_verify.get()
    password = password_verify.get()
    # Generate hash code
    hash_code = GetHashCode(username)

    # Try login
    if not Login(username, password, hash_code):
        login_failure()
    else:
        config = GetConfig(hash_code)
        if not config:
            config_failure()
        else:
            global login_ok
            login_ok = True
            delete_main_screen()
            print("正在写入配置文件...")
            WriteConfig(config)
            print("配置文件写入成功，开始运行")

# Designing popup for login invalid password
def login_failure():
    global login_failure_screen
    login_failure_screen = Toplevel(login_screen)
    login_failure_screen.title("认证信息无效！")
    login_failure_screen.geometry("300x66")
    login_failure_screen.iconbitmap("icon.ico")
    Label(login_failure_screen, text="请检查用户名和密码").pack()
    Button(login_failure_screen, text="确定", command=delete_login_failure).pack()

# Designing popup for config_failure
def config_failure():
    global config_failure_screen
    config_failure_screen = Toplevel(login_screen)
    config_failure_screen.title("Failed to get config file.")
    config_failure_screen.geometry("300x66")
    config_failure_screen.iconbitmap("icon.ico")
    Label(config_failure_screen, text="Failed to get config file.").pack()
    Button(config_failure_screen, text="OK", command=delete_config_failure).pack()

# Deleting popups
def delete_main_screen():
    main_screen.destroy()

def delete_login_failure():
    login_failure_screen.destroy()

def delete_config_failure():
    config_failure_screen.destroy()

# Designing Main(first) window
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x150")
    main_screen.title("Folding@SUSTech")
    main_screen.iconbitmap("icon.ico")
    Label(text="Folding@SUSTech", bg="blue", fg="white", width="300", height="2", font=("Calibri Bold", 13)).pack()
    Label(text="").pack()
    Button(text="认证身份", height="2", width="30", command=login_clicked).pack()

    main_screen.mainloop()



fah_client_ref = None

# Designing FAS window
def fas_screen():
    global paused
    global fah_client_ref
    paused = False
    fah_client_ref = subprocess.Popen("FAHClient")
    global fas_screen
    fas_screen = Tk()
    fas_screen.geometry("300x150")
    fas_screen.title("Folding@SUSTech")
    fas_screen.iconbitmap("icon.ico")
    Label(text="Folding@SUSTech", bg="blue", fg="white", width="300", height="2", font=("Calibri Bold", 13)).pack()
    Label(text="").pack()
    global btn_txt
    btn_txt = StringVar()
    btn = Button(textvariable=btn_txt, height="2", width="30", command=toggleFolding).pack()
    unpause()

    fas_screen.mainloop()

def toggleFolding():
    unpause() if paused else pause()

def unpause():
    subprocess.Popen("FAHClient --send-unpause")
    global paused
    # print("Unpausing!!! - {}".format(paused))
    paused = False
    global btn_txt
    btn_txt.set("正在运行，点击暂停")

def pause():
    subprocess.Popen("FAHClient --send-pause")
    global paused
    # print("pausing!!! - {}".format(paused))
    paused = True
    global btn_txt
    btn_txt.set("已暂停，点击继续")

if __name__ == "__main__":
    main_account_screen()
    if login_ok:
        fas_screen()
        print("退出")
        fah_client_ref.terminate()
