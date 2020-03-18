from tkinter import *
import os
import subprocess
from login import *
import logging

global GUI_log_here
GUI_log_here = False

class TextHandler(logging.Handler):
    def __init__(self, txtOutput, level=logging.DEBUG, formatter=None):
        logging.Handler.__init__(self, level)
        self.txtOutput = txtOutput

    def emit(self, record):
        global GUI_log_here
        if GUI_log_here:
            insertLog(self.txtOutput, self.format(record))


global login_ok
login_ok = False

file_handler = logging.FileHandler(filename='FASLog.txt')
file_handler.setLevel(logging.DEBUG)

global formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - "%(message)s" in - %(funcName)s - Line:%(lineno)s')
file_handler.setFormatter(formatter)

b_logger = logging.getLogger('test')
b_logger.setLevel(logging.DEBUG)
b_logger.addHandler(file_handler)

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

    b_logger.info("Initializing Login Window...")


# Implementing event on login button 
def login_verify():
    global username
    global password
    username = username_verify.get()
    password = password_verify.get()

    b_logger.debug("username: {}".format(username))
    b_logger.info("Verifying username and password...")

    # Generate hash code
    hash_code = GetHashCode(username)
    b_logger.debug("generated hashcode = {}".format(hash_code))

    # Try login
    if not Login(username, password, hash_code):
        login_failure()
        b_logger.warning("login failure.")
    else:
        config = GetConfig(hash_code, b_logger)
        if not config:
            config_failure()
            b_logger.warning("pulling config failure.")
        else:
            global login_ok
            login_ok = True
            b_logger.debug("Login successful, exiting window...")
            delete_main_screen()
            print("正在写入配置文件...")
            b_logger.info("Writing config file")
            WriteConfig(config)
            print("配置文件写入成功，开始运行")
            b_logger.info("Config file written, starting execution...")

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
    b_logger.info("Initializing Main Window...")
    main_screen.mainloop()

fah_client_ref = None

# Designing FAS window
def fas_screen():
    global paused
    global fah_client_ref
    paused = False
    b_logger.info("Starting FAHClient with config.xml...")
    #fah_client_ref = subprocess.Popen("FAHClient --config ./config.xml")
    fah_client_ref = launchWithoutConsole("FAHClient --config ./config.xml")
    global fas_screen
    fas_screen = Tk()
    fas_screen.geometry("600x300")
    fas_screen.title("Folding@SUSTech")
    fas_screen.iconbitmap("icon.ico")
    Label(text="Folding@SUSTech", bg="blue", fg="white", width="300", height="2", font=("Calibri Bold", 13)).pack()
    Label(text="").pack()
    global btn_txt
    btn_txt = StringVar()
    btn = Button(textvariable=btn_txt, height="2", width="30", command=toggleFolding).pack()
    b_logger.info("Initializing FAHCLient with a pre-unpause signal...")
    
    Label(text="").pack()

    txtFrame = Frame(fas_screen, borderwidth=1, relief="sunken")
    txtOutput = Text(txtFrame, wrap=NONE, height=10, width=70, borderwidth=0, bg="black", fg="white", state=DISABLED)
    vscroll = Scrollbar(txtFrame, orient=VERTICAL, command=txtOutput.yview)
    txtOutput['yscroll'] = vscroll.set
    vscroll.pack(side="right", fill="y")
    txtOutput.pack(side="left", fill="both", expand=True)
    txtFrame.pack()

    global formatter
    th = TextHandler(txtOutput)
    th.setFormatter(formatter)
    b_logger.addHandler(th)

    global GUI_log_here
    GUI_log_here = True
    unpause()
    fas_screen.mainloop()

def insertLog(txtOutput, str):
    txtOutput.config(state=NORMAL)
    txtOutput.insert(END, str + "\n")
    txtOutput.config(state=DISABLED)
    txtOutput.yview_moveto(1)
    

def toggleFolding():
    unpause() if paused else pause()

def unpause():
    #subprocess.Popen("FAHClient --send-unpause")
    launchWithoutConsole("FAHClient --send-unpause")
    global paused
    # print("Unpausing!!! - {}".format(paused))
    paused = False
    global btn_txt
    btn_txt.set("正在运行，点击暂停")
    b_logger.debug("Unpaused")

def pause():
    #subprocess.Popen("FAHClient --send-pause")
    launchWithoutConsole("FAHClient --send-pause")
    global paused
    # print("pausing!!! - {}".format(paused))
    paused = True
    global btn_txt
    btn_txt.set("已暂停，点击继续")
    b_logger.debug("Paused")

def launchWithoutConsole(command):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.Popen(command, startupinfo=startupinfo)

if __name__ == "__main__":
    main_account_screen()
    if login_ok:
        fas_screen()
        GUI_log_here = False
        print("退出")
        b_logger.info("Finish")
        fah_client_ref.terminate()
