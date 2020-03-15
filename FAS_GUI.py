from tkinter import *
import os
from login import *

global login_status
login_status = False

# window for login 
def login_clicked():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command=login_verify).pack()

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
        login_sucess()

# Designing popup for login success
def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()

# Designing popup for login invalid password
def login_failure():
    global login_failure_screen
    login_failure_screen = Toplevel(login_screen)
    login_failure_screen.title("Wrong user name or password.")
    login_failure_screen.geometry("150x100")
    Label(login_failure_screen, text="Wrong user name or password.").pack()
    Button(login_failure_screen, text="OK", command=delete_login_failure).pack()

# Designing popup for config_failure
def config_failure():
    global config_failure_screen
    config_failure_screen = Toplevel(login_screen)
    config_failure_screen.title("Failed to get config file.")
    config_failure_screen.geometry("150x100")
    Label(config_failure_screen, text="Failed to get config file.").pack()
    Button(config_failure_screen, text="OK", command=delete_config_failure).pack()

# Deleting popups
def delete_main_screen():
    main_screen.destroy()

def delete_login_success():
    login_success_screen.destroy()
    # after success, delete main screen as well
    delete_main_screen()

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
    # main_screen.iconbitmap("icon.ico")
    Label(text="Folding@SUSTech", bg="blue", fg="white", width="300", height="2", font=("Calibri Bold", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command=login_clicked).pack()

    main_screen.mainloop()

if __name__ == "__main__":
    main_account_screen()
    print("username={}".format(username))
    print("password={}".format(password))
