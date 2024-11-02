import tkinter
from pathlib import Path
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pyperclip
import random
import json
import smtplib
import os

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets")
ASSETS_LECTURES_LIST_PATH = OUTPUT_PATH / Path(r"./assets/lectures_list")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
def relative_to_assets_lectures_list(path: str) -> Path:
    return ASSETS_LECTURES_LIST_PATH / Path(path)

NOW_STUDENT = []
NOW_LECTURER = []
FEEDBACK_EMAIL = os.getenv("FEEDBACK_EMAIL")
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

#TODO === STUDENT INTERFACE
class MainPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Education Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.main_page_frame = Frame(self.window, width=500, height=500)
        self.main_page_frame.pack()

        self.canvas = Canvas(self.main_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=5)

        self.welcome_label = Label(self.main_page_frame, text="WELCOME TO IYTE UBYS")
        self.welcome_label.place(x=177, y=180)

        self.email_label = Label(self.main_page_frame, text="Email:")
        self.email_label.place(x=50, y=250)

        self.email_entry = Entry(self.main_page_frame, width=36)
        self.email_entry.place(x=130, y=250)
        self.email_entry.focus()
        self.email_entry.insert(0, "username@std.iyte.edu.tr")

        self.password_label = Label(self.main_page_frame, text="Password:")
        self.password_label.place(x=47, y=290)

        self.password_entry = Entry(self.main_page_frame, width=36, show="*")
        self.password_entry.place(x=130, y=290)

        self.login_button = Button(self.main_page_frame, text="LOGIN", width=13, command=self.login_button_function)
        self.login_button.place(x=143, y=325)

        self.signup_button = Button(self.main_page_frame, text="SIGN UP", width=30, command=self.signup_button_function)
        self.signup_button.place(x=143, y=355)

        self.send_feedback_button = Button(self.main_page_frame, text="Feedback", width=10, command=self.send_feedback_button_function)
        self.send_feedback_button.place(x=10, y=465)

        self.admin_button = Button(self.main_page_frame, width=0.01, command=self.admin_button_function)
        self.admin_button.place(x=490, y=490)

        self.forgot_password_button = Button(self.main_page_frame, text="Forgot Password?", width=30,
                                             command=self.forgot_password_button_function)
        self.forgot_password_button.place(x=143, y=385)

        self.lecturer_login_button = Button(self.main_page_frame, text="Lecturer LOGIN", width=15,
                                            command=self.lecturer_login_button_function)
        self.lecturer_login_button.place(x=233, y=325)

        self.window.mainloop()
    def admin_button_function(self):
        self.window.destroy()
        AdminPageFrame()
    def signup_button_function(self):
        for widget in self.main_page_frame.winfo_children():
            widget.destroy()
        self.window.destroy()
        SignupPageFrame()

    def forgot_password_button_function(self):
        self.window.destroy()
        ForgotPasswordPageFrame()

    def lecturer_login_button_function(self):
        self.window.destroy()
        LecturerLoginPageFrame()

    def login_button_function(self):
        try:
            with open(relative_to_assets("data.json"), "r") as student_data:
                data = json.load(student_data)

                if len(self.password_entry.get()) == 0 or len(self.email_entry.get()) == 0:
                    messagebox.showerror("Error", "Please don't leave any fields empty !!")

                elif self.email_entry.get() in data:
                    if self.password_entry.get() == data[self.email_entry.get()]["password"]:
                        NOW_STUDENT.append(data[self.email_entry.get()])
                        self.window.destroy()
                        LoginPageFrame()
                    else:
                        messagebox.showerror("Error", "Check your password and try again.")

                else:
                    messagebox.showerror("Error", "Check your email and try again.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Check your email and try again.")

    def send_feedback_button_function(self):
        self.window.destroy()
        FeedbackPageFrame()

class FeedbackPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Education Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.feedback_page_frame = Frame(self.window, width=500, height=500)
        self.feedback_page_frame.pack()

        self.canvas = Canvas(self.feedback_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=5)

        self.back_button = Button(self.feedback_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

        self.name_entry = Entry(self.feedback_page_frame, width=36)
        self.name_entry.place(x=130, y=210)
        self.name_entry.focus_force()

        self.name_label = Label(self.feedback_page_frame, text="Name:")
        self.name_label.place(x=78, y=210)

        self.email_entry = Entry(self.feedback_page_frame, width=36)
        self.email_entry.place(x=130, y=250)

        self.email_label = Label(self.feedback_page_frame, text="Email:")
        self.email_label.place(x=79, y=250)


        self.text = Text(self.feedback_page_frame, width=27)
        self.text.place(x=130, y=300, height=100)

        self.text.insert("1.0","Type your feedback here ❤️")

        self.text.bind("<FocusIn>",self.is_focused)

        self.send_feedback_button = Button(self.feedback_page_frame,text="Send", width=18, command=self.send_feedback_button_function)
        self.send_feedback_button.place(x=180, y=450)

    def send_feedback_button_function(self):
        if len(self.name_entry.get()) == 0 or len(self.email_entry.get()) == 0:
            messagebox.showerror("Error", "Please don't leave any fields empty !!")
        else:
            try:
                with smtplib.SMTP("smtp.gmail.com", port = 587) as connection:
                    connection.starttls()
                    connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                    connection.sendmail(from_addr=MY_EMAIL, to_addrs=FEEDBACK_EMAIL,
                                        msg=f"Subject:FEEDBACK\n\n{self.name_entry.get()}\n\n{self.email_entry.get()}\n\n{self.text.get("1.0", END)}")
            except TimeoutError:
                messagebox.showerror("Timeout Error",
                                     "Timed out while sending \n\n*Check your internet connection and try again")
            else:
                messagebox.showinfo("Successful", "Feedback sent successfully\n\nTHANKS FOR YOUR FEEDBACK ❤️")
            finally:
                self.window.destroy()
                MainPageFrame()

    def is_focused(self, event):

        self.text.delete('1.0', END)



    def go_back(self):
        self.window.destroy()
        MainPageFrame()

class LoginPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.login_page_frame = Frame(self.window, width=500, height=500)
        self.login_page_frame.pack()

        self.canvas = Canvas(self.login_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=0)

        self.my_lectures_button = Button(self.login_page_frame, text="MY LECTURES", width=30,
                                         command=self.my_lectures_button_function)
        self.my_lectures_button.place(x=155, y=260)

        self.my_profile_button = Button(self.login_page_frame, text="MY PROFILE", width=30,
                                        command=self.my_profile_button_function)
        self.my_profile_button.place(x=155, y=220)

        self.logout_button = Button(self.login_page_frame, text="LOGOUT", width=30, command=self.logout_button_function)
        self.logout_button.place(x=155, y=300)

        self.student_info_label = Label(self.login_page_frame, text=f"Welcome {NOW_STUDENT[0]["name"]}")
        self.student_info_label.place(x=180, y=180)

    def my_profile_button_function(self):
        self.window.destroy()
        MyProfilePageFrame()

    def my_lectures_button_function(self):
        self.window.destroy()
        MyLecturesPageFrame()

    def logout_button_function(self):
        global NOW_STUDENT
        NOW_STUDENT = []
        self.window.destroy()
        MainPageFrame()

class MyProfilePageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.my_profile_page_frame = Frame(self.window, width=500, height=500)
        self.my_profile_page_frame.pack()

        self.canvas = Canvas(self.my_profile_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=0)

        self.name_label = Label(self.my_profile_page_frame, text=f"Name: {NOW_STUDENT[0]['name']}")
        self.name_label.place(x=185, y=210)

        self.email_label = Label(self.my_profile_page_frame, text=f"Email: {NOW_STUDENT[0]['email']}")
        self.email_label.place(x=165, y=250)

        self.recovery_email_label = Label(self.my_profile_page_frame,
                                          text=f"Recovery Email: {NOW_STUDENT[0]['recovery_email']}")
        self.recovery_email_label.place(x=145, y=290)

        self.password_change = Button(self.my_profile_page_frame, text="Change My Password", width=20,
                                      command=self.password_change_button_function)
        self.password_change.place(x=110, y=330)

        self.recovery_email_change = Button(self.my_profile_page_frame, text="Change My Recovery Email", width=25,
                                            command=self.recovery_email_change_button_function)
        self.recovery_email_change.place(x=250, y=330)

        self.back_button = Button(self.my_profile_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

    def password_change_button_function(self):
        self.window.destroy()
        ChangePassPageFrame()

    def recovery_email_change_button_function(self):
        self.window.destroy()
        ChangeRecoveryEmailPageFrame()

    def go_back(self):
        self.window.destroy()
        LoginPageFrame()

class ChangePassPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.change_password_page_frame = Frame(self.window, width=500, height=500)
        self.change_password_page_frame.pack()

        self.canvas = Canvas(self.change_password_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=0)

        self.back_button = Button(self.change_password_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

        self.current_password_label = Label(self.change_password_page_frame, text=f"Current Password: ")
        self.current_password_label.place(x=35, y=250)

        self.new_password_label = Label(self.change_password_page_frame, text=f"New Password: ")
        self.new_password_label.place(x=40, y=290)

        self.confirm_new_password_label = Label(self.change_password_page_frame, text=f"Confirm New Password: ")
        self.confirm_new_password_label.place(x=20, y=330)

        self.current_password_entry = Entry(self.change_password_page_frame, width=36)
        self.current_password_entry.place(x=195, y=250)
        self.current_password_entry.focus_force()

        self.new_password_entry = Entry(self.change_password_page_frame, width=36)
        self.new_password_entry.place(x=195, y=290)

        self.confirm_new_password_entry = Entry(self.change_password_page_frame, width=36)
        self.confirm_new_password_entry.place(x=195, y=330)

        self.submit_button = Button(self.change_password_page_frame, text="Submit", width=30, command=self.submit)
        self.submit_button.place(x=195, y=370)

    def submit(self):
        if len(self.new_password_entry.get()) == 0 or len(self.confirm_new_password_entry.get()) == 0 or len(
                self.current_password_entry.get()) == 0:
            messagebox.showerror(title="Oops", message="Please don't leave any fields empty !!")
        elif self.new_password_entry.get() != self.confirm_new_password_entry.get():
            messagebox.showerror(title="Oops", message="Passwords don't match !!")
        elif self.current_password_entry.get() != NOW_STUDENT[0]["password"]:
            messagebox.showerror(title="Oops", message="Current Password doesn't match !!")
        else:
            messagebox.showinfo(title="Success", message="Your Password has been changed !!")
            new_data = {
                NOW_STUDENT[0]["email"]: {
                    "name": NOW_STUDENT[0]['name'],
                    "email": NOW_STUDENT[0]['email'],
                    "recovery_email": NOW_STUDENT[0]['recovery_email'],
                    "password": self.new_password_entry.get(),
                }
            }

            with open(relative_to_assets("data.json"), 'r') as file:
                data = json.load(file)
            data.update(new_data)
            with open(relative_to_assets("data.json"), "w") as file:
                json.dump(data, file, indent=4)
                NOW_STUDENT[0]["password"] = self.new_password_entry.get()

            self.window.destroy()
            MyProfilePageFrame()

    def go_back(self):
        self.window.destroy()
        MyProfilePageFrame()

class ChangeRecoveryEmailPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.change_recovery_email_page_frame = Frame(self.window, width=500, height=500)
        self.change_recovery_email_page_frame.pack()

        self.canvas = Canvas(self.change_recovery_email_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=0)

        self.back_button = Button(self.change_recovery_email_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

        self.new_recovery_email_label = Label(self.change_recovery_email_page_frame, text=f"New Recovery Email: ")
        self.new_recovery_email_label.place(x=40, y=250)
        self.confirm_new_recovery_email_label = Label(self.change_recovery_email_page_frame,
                                                      text=f"Confirm New Recovery Email: ")
        self.confirm_new_recovery_email_label.place(x=20, y=290)

        self.new_recovery_email_entry = Entry(self.change_recovery_email_page_frame, width=36)
        self.new_recovery_email_entry.place(x=195, y=250)
        self.new_recovery_email_entry.focus_force()
        self.new_recovery_email_entry.insert(0, "username@gmail.com")

        self.confirm_new_recovery_email_entry = Entry(self.change_recovery_email_page_frame, width=36)
        self.confirm_new_recovery_email_entry.place(x=195, y=290)
        self.confirm_new_recovery_email_entry.insert(0, "")

        self.submit_button = Button(self.change_recovery_email_page_frame, text="Submit", width=30, command=self.submit)
        self.submit_button.place(x=195, y=330)
        self.window.mainloop()


    def submit(self):
        if len(self.new_recovery_email_entry.get()) == 0 or len(self.confirm_new_recovery_email_entry.get()) == 0:
            messagebox.showerror(title="Oops", message="Please don't leave any fields empty !!")
        elif self.confirm_new_recovery_email_entry.get() != self.new_recovery_email_entry.get():
            messagebox.showerror(title="Oops", message="Emails don't match !!")
        else:
            messagebox.showinfo(title="Success", message="Your Recovery Email Has Changed Successfully!")
            new_data = {
                NOW_STUDENT[0]["email"]: {
                    "name": NOW_STUDENT[0]['name'],
                    "email": NOW_STUDENT[0]['email'],
                    "recovery_email": self.new_recovery_email_entry.get(),
                    "password": NOW_STUDENT[0]['password'],
                }
            }
            with open(relative_to_assets("data.json"), 'r') as file:
                data = json.load(file)
            data.update(new_data)
            with open(relative_to_assets("data.json"), "w") as file:
                json.dump(data, file, indent=4)
                NOW_STUDENT[0]["recovery_email"] = self.new_recovery_email_entry.get()

            self.window.destroy()
            MyProfilePageFrame()

    def go_back(self):
        self.window.destroy()
        MyProfilePageFrame()

class MyLecturesPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.my_lectures_page_frame = Frame(self.window, width=500, height=500)
        self.my_lectures_page_frame.pack()

        self.canvas = Canvas(self.my_lectures_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=5)

        self.lectures = []
        self.added_lectures = []

        for lecture in os.listdir(relative_to_assets("lectures_list")):
            lecture_name = lecture.removesuffix(".json")
            with open(relative_to_assets_lectures_list(f"{lecture_name}.json"), "r") as lecture_file:
                already_enrolled = json.load(lecture_file)
                if NOW_STUDENT[0]["email"] in already_enrolled[lecture_name]["students_enrolled"]:
                    self.added_lectures.append(lecture_name)
                else:
                    self.lectures.append(lecture_name)



        self.choicesvar = StringVar(value=self.lectures)
        self.listbox = Listbox(self.my_lectures_page_frame, width=15, height=11, listvariable=self.choicesvar, highlightthickness=0, borderwidth=0)
        self.listbox.place(x=40, y=225)

        self.scrollbar = Scrollbar(self.my_lectures_page_frame, orient=VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(x=115, y=225, height=176)

        self.my_choicesvar = StringVar(value=self.added_lectures)
        self.my_listbox = Listbox(self.my_lectures_page_frame, width=15, height=11, listvariable=self.my_choicesvar, highlightthickness=0, borderwidth=0)
        self.my_listbox.place(x=375, y=225)

        self.my_scrollbar = Scrollbar(self.my_lectures_page_frame, orient=VERTICAL, command=self.listbox.yview)
        self.my_listbox.configure(yscrollcommand=self.my_scrollbar.set)
        self.my_scrollbar.place(x=450, y=225, height=176)

        self.add_button = Button(self.my_lectures_page_frame, text="Add Selected Lectures", width=25, command=self.add_button_function)
        self.add_button.place(x=5, y=420)

        self.remove_button = Button(self.my_lectures_page_frame, text="Remove Selected Lectures", width=25, command=self.remove_button_function)
        self.remove_button.place(x=335, y=420)

        self.back_button = Button(self.my_lectures_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

        self.done_button = Button(self.my_lectures_page_frame, text="DONE", width=25, command=self.done_button_function)
        self.done_button.place(x=169, y=460)

        self.available_courses_label = Label(text="Available Lectures")
        self.available_courses_label.place(x=30, y=195)

        self.my_courses_label = Label(text="My Lectures")
        self.my_courses_label.place(x=375, y=195)



    def add_button_function(self):
        for i in self.listbox.curselection():
            lecture = self.listbox.get(i)
            with open(relative_to_assets_lectures_list(f"{lecture}.json")) as file:
                data = json.load(file)
                students_list = data[lecture]["students_enrolled"]
                students_list.append(NOW_STUDENT[0]["email"])
            new_data = {
                lecture: {
                    "lecturer_name": data[lecture]["lecturer_name"],
                    "lecturer_email": data[lecture]["lecturer_email"],
                    "students_enrolled": students_list,
                }

            }
            with open(relative_to_assets_lectures_list(f"{lecture}.json"), 'w') as file:
                json.dump(new_data, file, indent=4)
            self.my_listbox.insert(END, self.listbox.get(i))
            self.listbox.delete(self.listbox.curselection()[0])
    def remove_button_function(self):
        for i in self.my_listbox.curselection():
            lecture = self.my_listbox.get(i)
            with open(relative_to_assets_lectures_list(f"{lecture}.json")) as file:
                data = json.load(file)
                students_list = data[lecture]["students_enrolled"]
                students_list.remove(NOW_STUDENT[0]["email"])

            new_data = {
                lecture: {
                    "lecturer_name": data[lecture]["lecturer_name"],
                    "lecturer_email": data[lecture]["lecturer_email"],
                    "students_enrolled": students_list,
                }

            }
            with open(relative_to_assets_lectures_list(f"{lecture}.json"), 'w') as file:
                json.dump(new_data, file, indent=4)
            self.listbox.insert(END, self.my_listbox.get(i))
            self.my_listbox.delete(self.my_listbox.curselection()[0])
    def done_button_function(self):
        is_ok = messagebox.askokcancel(title="Selected Lectures",
                                       message="ARE YOU SURE?")
        if is_ok:
            self.window.destroy()
            LoginPageFrame()
    def go_back(self):
        self.window.destroy()
        LoginPageFrame()

class SignupPageFrame:

    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.signup_page_frame = Frame(self.window, width=500, height=500)
        self.signup_page_frame.pack()

        self.canvas = Canvas(self.signup_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=135, y=0)

        self.welcome_label = Label(self.signup_page_frame, text="SIGN-UP PAGE")
        self.welcome_label.place(x=197, y=180)

        self.name_label = Label(self.signup_page_frame, text="Full Name:")
        self.name_label.place(x=30, y=210)


        self.name_entry = Entry(self.signup_page_frame, width=36)
        self.name_entry.place(x=130, y=210)
        self.name_entry.focus_force()

        self.email_label = Label(self.signup_page_frame, text="Email:")
        self.email_label.place(x=44, y=250)

        self.email_entry = Entry(self.signup_page_frame, width=36)
        self.email_entry.place(x=130, y=250)
        self.email_entry.insert(0, "username@std.iyte.edu.tr")

        self.recovery_email_label = Label(self.signup_page_frame, text="Recovery Email:")
        self.recovery_email_label.place(x=20, y=290)

        self.recovery_email_entry = Entry(self.signup_page_frame, width=36)
        self.recovery_email_entry.place(x=130, y=290)
        self.recovery_email_entry.insert(0, "username@gmail.com")

        self.password_label = Label(self.signup_page_frame, text="Password:")
        self.password_label.place(x=34, y=330)

        self.password_entry = Entry(self.signup_page_frame, width=36)
        self.password_entry.place(x=130, y=330)

        self.confirm_password_label = Label(self.signup_page_frame, text="Confirm Password:")
        self.confirm_password_label.place(x=15, y=370)

        self.confirm_password_entry = Entry(self.signup_page_frame, width=36)
        self.confirm_password_entry.place(x=130, y=370)

        self.signup_button = Button(self.signup_page_frame, text="SIGN-UP", width=30, command=self.signup_button)
        self.signup_button.place(x=143, y=410)

        self.generate_password_button = Button(text="Generate Password", command=self.generate_password)
        self.generate_password_button.place(x=360, y=330)

        self.back_button = Button(self.signup_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

        self.window.mainloop()

    def generate_password(self):
        self.password_entry.delete(0, END)
        self.confirm_password_entry.delete(0, END)

        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                   'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        nr_letters = random.randint(8, 10)
        nr_symbols = random.randint(2, 4)
        nr_numbers = random.randint(2, 4)

        password_letters = [random.choice(letters) for _ in range(nr_letters)]
        password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
        password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

        password_list = password_letters + password_numbers + password_symbols

        random.shuffle(password_list)

        password = "".join(password_list)
        self.password_entry.insert(0, password)
        self.confirm_password_entry.insert(0, password)
        pyperclip.copy(password)
        messagebox.showinfo("Password copied to clipboard", "Password copied to clipboard")

    def signup_button(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        recovery_email = self.recovery_email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        new_data = {
            email: {
                "name": name,
                "email": email,
                "recovery_email": recovery_email,
                "password": password,
            }
        }
        if password != confirm_password:
            messagebox.showerror("Warning", "Passwords do not match")
        elif len(email) == 0 or len(recovery_email) == 0 or len(password) == 0 or len(confirm_password) == 0 or len(
                name) == 0:
            messagebox.showerror(title="Oops", message="Please don't leave any fields empty !!")
        else:
            try:
                with open(relative_to_assets("data.json"), "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open(relative_to_assets("data.json"), "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                if email in data:
                    messagebox.showerror("Warning", "Email already taken")
                elif "@std.iyte.edu.tr" not in email:
                    messagebox.showerror("Error", "Email should end with @std.iyte.edu.tr")
                else:
                    is_ok = messagebox.askokcancel(title=email,
                                                   message=f"These are the details entered: \n\nEmail: {email} \nRecovery Email: {recovery_email}\nPassword: {password} \n\nIs it ok to save?")
                    if is_ok:
                        data.update(new_data)
                        with open(relative_to_assets("data.json"), "w") as data_file:
                            json.dump(data, data_file, indent=4)
                        messagebox.showinfo(title="SUCCESS", message="You have successfully signed up!")
                        self.window.destroy()
                        MainPageFrame()

    def go_back(self):
        self.window.destroy()
        MainPageFrame()

class ForgotPasswordPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.forget_password_page_frame = Frame(self.window, width=500, height=500)
        self.forget_password_page_frame.pack()

        self.canvas = Canvas(self.forget_password_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=155, y=0)

        self.welcome_label = Label(self.forget_password_page_frame, text="FORGOT PASSWORD PAGE")
        self.welcome_label.place(x=185, y=180)

        self.recovery_email_label = Label(self.forget_password_page_frame, text="Recovery Email:")
        self.recovery_email_label.place(x=40, y=290)

        self.recovery_email_entry = Entry(self.forget_password_page_frame, width=36)
        self.recovery_email_entry.place(x=150, y=290)
        self.recovery_email_entry.focus_force()
        self.recovery_email_entry.insert(0, "username@gmail.com")

        self.password_send_button = Button(self.forget_password_page_frame, text="Send My Password", width=30,
                                           command=self.send_password)
        self.password_send_button.place(x=159, y=340)

        self.back_button = Button(self.forget_password_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

        self.window.mainloop()

    def send_password(self):
        email = self.recovery_email_entry.get()
        try:
            with open(relative_to_assets("data.json"), "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showerror("Error", "Email not found.")

        else:
            message = ""
            emails = []
            l_emails = []
            for lecturer in data:
                r_email = data[lecturer]["recovery_email"]
                emails.append(r_email)
                l_emails.append(r_email)
                l_emails.append(lecturer)

            if email in emails:

                for key in data[l_emails[l_emails.index(email) + 1]]:
                    message += f"{key} : {data[l_emails[l_emails.index(email) + 1]][key]}"
                    message += "\n"
                try:
                    with smtplib.SMTP("smtp.gmail.com", port = 587) as connection:
                        connection.starttls()
                        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                        connection.sendmail(from_addr=MY_EMAIL, to_addrs=email,
                                            msg=f"Subject:YOUR PASSWORD\n\n{message}")
                except TimeoutError:
                    messagebox.showerror("Timeout Error",
                                         "Timed out while sending email\n\n*Check your email and try again\n*Check your internet connection and try again")
                else:
                    messagebox.showinfo("Successful", "Email sent successfully\nCheck your email for the password")
                finally:
                    self.window.destroy()
                    MainPageFrame()
            else:
                messagebox.showerror("Error", "Email not found.\nCheck your email and try again")

    def go_back(self):
        self.window.destroy()
        MainPageFrame()

#TODO === ADMIN INTERFACE
class AdminPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Education Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.admin_page_frame = Frame(self.window, width=500, height=500)
        self.admin_page_frame.pack()

        self.canvas = Canvas(self.admin_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=5)

        self.welcome_label = Label(self.admin_page_frame, text="WELCOME TO IYTE UBYS")
        self.welcome_label.place(x=177, y=180)

        self.email_label = Label(self.admin_page_frame, text="Email:")
        self.email_label.place(x=50, y=250)

        self.email_entry = Entry(self.admin_page_frame, width=36)
        self.email_entry.place(x=130, y=250)
        self.email_entry.focus_force()

        self.password_label = Label(self.admin_page_frame, text="Password:")
        self.password_label.place(x=47, y=290)

        self.password_entry = Entry(self.admin_page_frame, width=36, show="*")
        self.password_entry.place(x=130, y=290)

        self.login_button = Button(self.admin_page_frame, text="LOGIN", width=30, command=self.login_button_function)
        self.login_button.place(x=143, y=325)

        self.back_button = Button(self.admin_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)



    def login_button_function(self):

        with open(relative_to_assets("admin_data.json"), "r") as admin_data_file:
            data = json.load(admin_data_file)
            ADMIN_PASSWORD = data["admin"]["password"]
            ADMIN_EMAIL = data["admin"]         ["email"]

            if len(self.password_entry.get()) == 0 or len(self.email_entry.get()) == 0:
                messagebox.showerror("Error", "Please don't leave any fields empty !!")

            elif self.password_entry.get() == ADMIN_PASSWORD and self.email_entry.get() == ADMIN_EMAIL:
                self.window.destroy()
                AdminLoginPageFrame()
            else:
                messagebox.showerror("Error", "Check your password and email.")

    def go_back(self):

        self.window.destroy()
        MainPageFrame()

class AdminLoginPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.admin_login_page_frame = Frame(self.window, width=500, height=500)
        self.admin_login_page_frame.pack()

        self.canvas = Canvas(self.admin_login_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=0)

        self.show_students_button = Button(self.admin_login_page_frame, text="Show Students", width=30, command=self.show_students_button_function)
        self.show_students_button.place(x=155, y=300)

        self.show_lecturers_button = Button(self.admin_login_page_frame, text="Show Lecturers", width=30 ,command=self.show_lecturers_button_function)
        self.show_lecturers_button.place(x=155, y=340)

        self.show_lectures_button = Button(self.admin_login_page_frame, text="Show Lectures", width=30 ,command=self.show_lectures_button_function)
        self.show_lectures_button.place(x=155, y=260)

        self.admin_settings_button = Button(self.admin_login_page_frame, text="Admin Settings", width=30, command=self.admin_settings_button_function)
        self.admin_settings_button.place(x=155, y=220)

        self.logout_button = Button(self.admin_login_page_frame, text="LOGOUT", width=30, command=self.logout_button_function)
        self.logout_button.place(x=155, y=380)

        self.student_info_label = Label(self.admin_login_page_frame, text=f"Welcome ADMIN")
        self.student_info_label.place(x=197, y=180)

    def admin_settings_button_function(self):
        self.window.destroy()
        AdminSettingsPageFrame()

    def show_students_button_function(self):
        self.window.destroy()
        ShowStudentsPageFrame()

    def show_lecturers_button_function(self):
        self.window.destroy()
        ShowLecturersPageFrame()

    def show_lectures_button_function(self):
        self.window.destroy()
        ShowLecturesPageFrame()

    def logout_button_function(self):
        self.window.destroy()
        MainPageFrame()

class AdminSettingsPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.admin_settings_page_frame = Frame(self.window, width=500, height=500)
        self.admin_settings_page_frame.pack()

        self.canvas = Canvas(self.admin_settings_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=0)

        self.email_change = Button(self.admin_settings_page_frame, text="Change Admin-Email", width=25, command=self.email_change_button_function)
        self.email_change.place(x=165, y=210)

        self.password_change = Button(self.admin_settings_page_frame, text="Change Admin-Password", width=25, command=self.password_change_button_function)
        self.password_change.place(x=165, y=240)

        self.back_button = Button(self.admin_settings_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

    def email_change_button_function(self):
        self.window.destroy()
        AdminEmailChangePageFrame()

    def password_change_button_function(self):
        self.window.destroy()
        AdminChangePassPageFrame()

    def go_back(self):
        self.window.destroy()
        AdminLoginPageFrame()

class AdminChangePassPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.admin_change_password_page_frame = Frame(self.window, width=500, height=500)
        self.admin_change_password_page_frame.pack()

        self.canvas = Canvas(self.admin_change_password_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=0)

        self.back_button = Button(self.admin_change_password_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

        self.current_password_label = Label(self.admin_change_password_page_frame, text=f"Current Password: ")
        self.current_password_label.place(x=35, y=250)

        self.new_password_label = Label(self.admin_change_password_page_frame, text=f"New Password: ")
        self.new_password_label.place(x=40, y=290)

        self.confirm_new_password_label = Label(self.admin_change_password_page_frame, text=f"Confirm New Password: ")
        self.confirm_new_password_label.place(x=20, y=330)

        self.current_password_entry = Entry(self.admin_change_password_page_frame, width=36)
        self.current_password_entry.place(x=195, y=250)
        self.current_password_entry.focus_force()

        self.new_password_entry = Entry(self.admin_change_password_page_frame, width=36)
        self.new_password_entry.place(x=195, y=290)

        self.confirm_new_password_entry = Entry(self.admin_change_password_page_frame, width=36)
        self.confirm_new_password_entry.place(x=195, y=330)

        self.submit_button = Button(self.admin_change_password_page_frame, text="Submit", width=30, command=self.submit)
        self.submit_button.place(x=195, y=370)

    def submit(self):
            with open(relative_to_assets("admin_data.json"), "r") as admin_data_file:
                data = json.load(admin_data_file)
                ADMIN_PASSWORD = data["admin"]["password"]
                ADMIN_EMAIL = data["admin"]["email"]
            if len(self.new_password_entry.get()) == 0 or len(self.confirm_new_password_entry.get()) == 0 or len(
                    self.current_password_entry.get()) == 0:
                messagebox.showerror(title="Oops", message="Please don't leave any fields empty !!")
            elif self.new_password_entry.get() != self.confirm_new_password_entry.get():
                messagebox.showerror(title="Oops", message="Passwords don't match !!")
            elif self.current_password_entry.get() != ADMIN_PASSWORD:
                messagebox.showerror(title="Oops", message="Current Password doesn't match !!")
            else:
                messagebox.showinfo(title="Success", message="Your Password has been changed !!")
                new_data = {
                    "admin": {
                        "email": f"{ADMIN_EMAIL}",
                        "password": f"{self.new_password_entry.get()}"
                    }
                }
                with open(relative_to_assets("admin_data.json"), 'r') as file:
                    admin_data = json.load(file)
                admin_data.update(new_data)
                with open(relative_to_assets("admin_data.json"), "w") as file:
                    json.dump(admin_data, file, indent=4)


                self.window.destroy()
                AdminSettingsPageFrame()

    def go_back(self):

        self.window.destroy()
        AdminSettingsPageFrame()

class AdminEmailChangePageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.change_recovery_email_page_frame = Frame(self.window, width=500, height=500)
        self.change_recovery_email_page_frame.pack()

        self.canvas = Canvas(self.change_recovery_email_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=0)

        self.new_recovery_email_label = Label(self.change_recovery_email_page_frame, text=f"New Email: ")
        self.new_recovery_email_label.place(x=40, y=250)
        self.confirm_new_recovery_email_label = Label(self.change_recovery_email_page_frame, text=f"Confirm New Email: ")
        self.confirm_new_recovery_email_label.place(x=20, y=290)

        self.new_email_entry = Entry(self.change_recovery_email_page_frame, width=36)
        self.new_email_entry.place(x=195, y=250)
        self.new_email_entry.focus_force()

        self.confirm_new_email_entry = Entry(self.change_recovery_email_page_frame, width=36)
        self.confirm_new_email_entry.place(x=195, y=290)
        self.confirm_new_email_entry.insert(0, "")

        self.back_button = Button(self.change_recovery_email_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

        self.submit_button = Button(self.change_recovery_email_page_frame, text="Submit", width=30, command=self.submit)
        self.submit_button.place(x=195, y=330)
        self.window.mainloop()

    def submit(self):
        if len(self.new_email_entry.get()) == 0 or len(self.confirm_new_email_entry.get()) == 0:
            messagebox.showerror(title="Oops", message="Please don't leave any fields empty !!")
        elif self.confirm_new_email_entry.get() != self.new_email_entry.get():
            messagebox.showerror(title="Oops", message="Emails don't match !!")
        else:
            messagebox.showinfo(title="Success", message="Your Email Has Changed Successfully!")


            with open(relative_to_assets("admin_data.json"), 'r') as file:
                admin_data = json.load(file)
                new_data = {
                    "admin": {
                        "email": f"{self.new_email_entry.get()}",
                        "password": f"{admin_data["admin"]['password']}"
                    }
                }
            admin_data.update(new_data)
            with open(relative_to_assets("admin_data.json"), "w") as file:
                json.dump(admin_data, file, indent=4)
            self.window.destroy()
            AdminSettingsPageFrame()

    def go_back(self):
        self.window.destroy()
        AdminSettingsPageFrame()

class ShowLecturesPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.show_lectures_page_frame = Frame(self.window, width=500, height=500)
        self.show_lectures_page_frame.pack()

        self.canvas = Canvas(self.show_lectures_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=0)

        self.back_button = Button(self.show_lectures_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

        self.lectures_list = []
        for lecture in os.listdir(relative_to_assets("lectures_list")):
            lecture_name = lecture.removesuffix(".json")
            self.lectures_list.append(lecture_name)


        self.choice_var = StringVar(value= self.lectures_list)
        self.lectures_listbox = Listbox(self.show_lectures_page_frame, width=15, height=17, listvariable=self.choice_var, justify="center", exportselection=False)
        self.lectures_listbox.place(x=380, y=220)

        self.scrollbar = Scrollbar(self.show_lectures_page_frame, orient=VERTICAL, command=self.lectures_listbox.yview)
        self.lectures_listbox.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(x=473, y=219, height=280)

        self.new_lecture_entry = Entry(self.show_lectures_page_frame, width=15)
        self.new_lecture_entry.place(x=160, y=250)
        self.new_lecture_entry.focus_force()

        self.new_lecture_label = Label(self.show_lectures_page_frame, text=f"New Lecture's name: ")
        self.new_lecture_label.place(x=10, y=250)

        self.existing_lectures_label = Label(self.show_lectures_page_frame, text="Existing Lectures")
        self.existing_lectures_label.place(x=382, y=190)


        self.new_lecture_which_lecturer_label = Label(self.show_lectures_page_frame, text=f"Which Lecturer: ")
        self.new_lecture_which_lecturer_label.place(x=20, y=290)
        self.lecturers = []
        with open(relative_to_assets("lecturers.json"), 'r') as file:
            lecturers_info = json.load(file)
            for lecturer in lecturers_info:
                self.lecturers.append(lecturers_info[lecturer]['name'])


        self.lecturers_combobox = lecturers = Combobox(self.show_lectures_page_frame, values=self.lecturers, state="readonly")
        self.lecturers_combobox.place(x=140, y=290)

        self.add_lecture_button = Button(self.show_lectures_page_frame, text="Add Lecture", width=38, command=self.add_lecture_button_function)
        self.add_lecture_button.place(x=90, y=330)

        self.remove_selected_lecture_button = Button(self.show_lectures_page_frame, text="Remove Selected Lecture", width=38, command=self.remove_selected_lecture_button_function)
        self.remove_selected_lecture_button.place(x=90, y=370)


    def remove_selected_lecture_button_function(self):
        i = self.lectures_listbox.curselection()

        if len(i) >= 1:
            is_ok = messagebox.askokcancel("BE CAREFUL!!!", "Are You Sure?")
            if is_ok:
                selected_lecture = self.lectures_listbox.get(i)
                if f"{selected_lecture}.json" in os.listdir(relative_to_assets("lectures_list")):


                    Path.unlink(relative_to_assets_lectures_list(f"{selected_lecture}.json"))
                    self.window.destroy()
                    ShowLecturesPageFrame()
        elif len(i) == 0:
            messagebox.showerror("Error", "No Lectures Selected")

    def add_lecture_button_function(self):

        if len(self.new_lecture_entry.get()) == 0:
            messagebox.showerror("Error", "Please don't leave any fields empty !!")
        elif len(self.lecturers_combobox.get()) == 0:
            messagebox.showerror("Error", "Please select a lecturer")
        elif f"{self.new_lecture_entry.get()}.json" in os.listdir(relative_to_assets("lectures_list")):
            messagebox.showerror("Error", "Lecture already exists")
        else:
            with open(relative_to_assets("lecturers.json"), 'r') as file1:
                lecturers_info = json.load(file1)
                lecturer_name = []
                lecturer_email = []
                for lecturer in lecturers_info:
                    lecturer_name.append(lecturers_info[lecturer]["name"])
                    lecturer_email.append(lecturers_info[lecturer]["email"])

                idx = lecturer_name.index(self.lecturers_combobox.get())


                with open(relative_to_assets_lectures_list(f"{self.new_lecture_entry.get()}.json"), 'w') as file:
                    new_data = {
                        f"{self.new_lecture_entry.get()}": {
                            "lecturer_name": f"{self.lecturers_combobox.get()}",
                            "lecturer_email":f"{lecturer_email[idx]}" ,
                            "students_enrolled": [],
                        }

                    }
                    json.dump(new_data, file, indent=4)
                self.window.destroy()
                ShowLecturesPageFrame()

    def go_back(self):
        self.window.destroy()
        AdminLoginPageFrame()

class ShowStudentsPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.show_students_page_frame = Frame(self.window, width=500, height=500)
        self.show_students_page_frame.pack()

        self.canvas = Canvas(self.show_students_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=0)

        self.back_button = Button(self.show_students_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

        self.students_list = []
        self.students_emails = []
        with open(relative_to_assets("data.json"), "r") as students_file:
            self.students_data = json.load(students_file)
            for student in self.students_data:
                self.students_list.append(self.students_data[student]["name"])
                self.students_emails.append(self.students_data[student]["email"])


        self.choice_var = StringVar(value= self.students_list)
        self.students_listbox = Listbox(self.show_students_page_frame, width=15, height=17, listvariable=self.choice_var, justify="center", exportselection=False)
        self.students_listbox.place(x=380, y=220)

        self.scrollbar = Scrollbar(self.show_students_page_frame, orient=VERTICAL, command=self.students_listbox.yview)
        self.students_listbox.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(x=473, y=219, height=280)


        self.existing_students_label = Label(self.show_students_page_frame, text="Existing Students")
        self.existing_students_label.place(x=382, y=190)


        self.add_student_button = Button(self.show_students_page_frame, text="Add Student", width=38, command=self.add_student_button_function)
        self.add_student_button.place(x=75, y=300)

        self.remove_selected_student_button = Button(self.show_students_page_frame, text="Remove Selected Student", width=38, command=self.remove_selected_student_button_function)
        self.remove_selected_student_button.place(x=75, y=340)

    def add_student_button_function(self):
        self.window.destroy()
        AdminSignupPageFrame()

    def remove_selected_student_button_function(self):
        i = self.students_listbox.curselection()

        if len(i) >= 1:
            is_ok = messagebox.askokcancel("BE CAREFUL!!!", "Are You Sure?")
            if is_ok:
                selected_student = self.students_listbox.get(i)

                if selected_student in self.students_list:
                    idx = self.students_list.index(selected_student)
                    selected_students_email = self.students_emails[idx]
                    with open(relative_to_assets("data.json")) as json_file:
                        data = json.load(json_file)
                        data.pop(selected_students_email)
                        with open(relative_to_assets("data.json"), 'w') as outfile:
                            json.dump(data, outfile, indent=4)
                    self.window.destroy()
                    ShowStudentsPageFrame()

        elif len(i) == 0:
            messagebox.showerror("Error", "No Students Selected")


    def go_back(self):
        self.window.destroy()
        AdminLoginPageFrame()

class AdminSignupPageFrame:

    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.signup_page_frame = Frame(self.window, width=500, height=500)
        self.signup_page_frame.pack()

        self.canvas = Canvas(self.signup_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=135, y=0)

        self.welcome_label = Label(self.signup_page_frame, text="STUDENT SIGN-UP PAGE")
        self.welcome_label.place(x=170, y=180)

        self.name_label = Label(self.signup_page_frame, text="Full Name:")
        self.name_label.place(x=30, y=210)

        self.name_entry = Entry(self.signup_page_frame, width=36)
        self.name_entry.place(x=130, y=210)
        self.name_entry.focus_force()

        self.email_label = Label(self.signup_page_frame, text="Email:")
        self.email_label.place(x=44, y=250)

        self.email_entry = Entry(self.signup_page_frame, width=36)
        self.email_entry.place(x=130, y=250)
        self.email_entry.insert(0, "username@std.iyte.edu.tr")

        self.recovery_email_label = Label(self.signup_page_frame, text="Recovery Email:")
        self.recovery_email_label.place(x=20, y=290)

        self.recovery_email_entry = Entry(self.signup_page_frame, width=36)
        self.recovery_email_entry.place(x=130, y=290)
        self.recovery_email_entry.insert(0, "username@gmail.com")

        self.password_label = Label(self.signup_page_frame, text="Password:")
        self.password_label.place(x=34, y=330)

        self.password_entry = Entry(self.signup_page_frame, width=36)
        self.password_entry.place(x=130, y=330)

        self.confirm_password_label = Label(self.signup_page_frame, text="Confirm Password:")
        self.confirm_password_label.place(x=15, y=370)

        self.confirm_password_entry = Entry(self.signup_page_frame, width=36)
        self.confirm_password_entry.place(x=130, y=370)

        self.signup_button = Button(self.signup_page_frame, text="SIGN-UP", width=30, command=self.signup_button)
        self.signup_button.place(x=143, y=410)

        self.generate_password_button = Button(text="Generate Password", command=self.generate_password)
        self.generate_password_button.place(x=360, y=330)

        self.back_button = Button(self.signup_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

        self.window.mainloop()

    def generate_password(self):
        self.password_entry.delete(0, END)
        self.confirm_password_entry.delete(0, END)

        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                   'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        nr_letters = random.randint(8, 10)
        nr_symbols = random.randint(2, 4)
        nr_numbers = random.randint(2, 4)

        password_letters = [random.choice(letters) for _ in range(nr_letters)]
        password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
        password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

        password_list = password_letters + password_numbers + password_symbols

        random.shuffle(password_list)

        password = "".join(password_list)
        self.password_entry.insert(0, password)
        self.confirm_password_entry.insert(0, password)

    def signup_button(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        recovery_email = self.recovery_email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        new_data = {
            email: {
                "name": name,
                "email": email,
                "recovery_email": recovery_email,
                "password": password,
            }
        }
        if password != confirm_password:
            messagebox.showerror("Warning", "Passwords do not match")
        elif len(email) == 0 or len(recovery_email) == 0 or len(password) == 0 or len(confirm_password) == 0 or len(
                name) == 0:
            messagebox.showerror(title="Oops", message="Please don't leave any fields empty !!")
        else:
            try:
                with open(relative_to_assets("data.json"), "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open(relative_to_assets("data.json"), "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                if email in data:
                    messagebox.showerror("Warning", "Email already taken")
                elif "@std.iyte.edu.tr" not in email:
                    messagebox.showerror("Error", "Email should end with @std.iyte.edu.tr")
                else:
                    is_ok = messagebox.askokcancel(title=email,
                                                   message=f"These are the details entered: \n\nEmail: {email} \nRecovery Email: {recovery_email}\nPassword: {password} \n\nIs it ok to save?")
                    if is_ok:
                        data.update(new_data)
                        with open(relative_to_assets("data.json"), "w") as data_file:
                            json.dump(data, data_file, indent=4)
                        messagebox.showinfo(title="SUCCESS", message="You have successfully Added a Student")
                        self.window.destroy()
                        ShowStudentsPageFrame()
    def go_back(self):
        self.window.destroy()
        ShowStudentsPageFrame()

class AdminLecturerSignupPageFrame:

    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.signup_page_frame = Frame(self.window, width=500, height=500)
        self.signup_page_frame.pack()

        self.canvas = Canvas(self.signup_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=135, y=0)

        self.welcome_label = Label(self.signup_page_frame, text="LECTURER SIGN-UP PAGE")
        self.welcome_label.place(x=165, y=180)

        self.name_label = Label(self.signup_page_frame, text="Full Name:")
        self.name_label.place(x=30, y=210)

        self.name_entry = Entry(self.signup_page_frame, width=36)
        self.name_entry.place(x=130, y=210)
        self.name_entry.focus_force()

        self.email_label = Label(self.signup_page_frame, text="Email:")
        self.email_label.place(x=44, y=250)

        self.email_entry = Entry(self.signup_page_frame, width=36)
        self.email_entry.place(x=130, y=250)
        self.email_entry.insert(0, "username@iyte.edu.tr")

        self.recovery_email_label = Label(self.signup_page_frame, text="Recovery Email:")
        self.recovery_email_label.place(x=20, y=290)

        self.recovery_email_entry = Entry(self.signup_page_frame, width=36)
        self.recovery_email_entry.place(x=130, y=290)
        self.recovery_email_entry.insert(0, "username@gmail.com")

        self.password_label = Label(self.signup_page_frame, text="Password:")
        self.password_label.place(x=34, y=330)

        self.password_entry = Entry(self.signup_page_frame, width=36)
        self.password_entry.place(x=130, y=330)

        self.confirm_password_label = Label(self.signup_page_frame, text="Confirm Password:")
        self.confirm_password_label.place(x=15, y=370)

        self.confirm_password_entry = Entry(self.signup_page_frame, width=36)
        self.confirm_password_entry.place(x=130, y=370)

        self.signup_button = Button(self.signup_page_frame, text="SIGN-UP", width=30, command=self.signup_button)
        self.signup_button.place(x=143, y=410)

        self.generate_password_button = Button(text="Generate Password", command=self.generate_password)
        self.generate_password_button.place(x=360, y=330)

        self.back_button = Button(self.signup_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

        self.window.mainloop()

    def generate_password(self):
        self.password_entry.delete(0, END)
        self.confirm_password_entry.delete(0, END)

        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                   'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        nr_letters = random.randint(8, 10)
        nr_symbols = random.randint(2, 4)
        nr_numbers = random.randint(2, 4)

        password_letters = [random.choice(letters) for _ in range(nr_letters)]
        password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
        password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

        password_list = password_letters + password_numbers + password_symbols

        random.shuffle(password_list)

        password = "".join(password_list)
        self.password_entry.insert(0, password)
        self.confirm_password_entry.insert(0, password)

    def signup_button(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        recovery_email = self.recovery_email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        new_data = {
            email: {
                "name": name,
                "email": email,
                "recovery_email": recovery_email,
                "password": password,
            }
        }
        if password != confirm_password:
            messagebox.showerror("Warning", "Passwords do not match")
        elif len(email) == 0 or len(recovery_email) == 0 or len(password) == 0 or len(confirm_password) == 0 or len(
                name) == 0:
            messagebox.showerror(title="Oops", message="Please don't leave any fields empty !!")
        else:
            try:
                with open(relative_to_assets("lecturers.json"), "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open(relative_to_assets("lecturers.json"), "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                if email in data:
                    messagebox.showerror("Warning", "Email already taken")
                elif "@iyte.edu.tr" not in email:
                    messagebox.showerror("Error", "Email should end with @iyte.edu.tr")
                else:
                    is_ok = messagebox.askokcancel(title=email,
                                                   message=f"These are the details entered: \n\nEmail: {email} \nRecovery Email: {recovery_email}\nPassword: {password} \n\nIs it ok to save?")
                    if is_ok:
                        data.update(new_data)
                        with open(relative_to_assets("lecturers.json"), "w") as data_file:
                            json.dump(data, data_file, indent=4)
                        messagebox.showinfo(title="SUCCESS", message="You have successfully Added a Lecturer")
                        self.window.destroy()
                        ShowLecturersPageFrame()
    def go_back(self):
        self.window.destroy()
        ShowLecturersPageFrame()

class ShowLecturersPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.show_lecturers_page_frame = Frame(self.window, width=500, height=500)
        self.show_lecturers_page_frame.pack()

        self.canvas = Canvas(self.show_lecturers_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=0)

        self.back_button = Button(self.show_lecturers_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

        self.lecturers_list = []
        self.lecturers_emails = []
        with open(relative_to_assets("lecturers.json"), "r") as lecturers_file:
            self.lecturers_data = json.load(lecturers_file)
            for lecturer in self.lecturers_data:
                self.lecturers_list.append(self.lecturers_data[lecturer]["name"])
                self.lecturers_emails.append(self.lecturers_data[lecturer]["email"])

        self.choice_var = StringVar(value=self.lecturers_list)
        self.lecturers_listbox = Listbox(self.show_lecturers_page_frame, width=15, height=17,
                                        listvariable=self.choice_var, justify="center", exportselection=False)
        self.lecturers_listbox.place(x=380, y=220)

        self.scrollbar = Scrollbar(self.show_lecturers_page_frame, orient=VERTICAL, command=self.lecturers_listbox.yview)
        self.lecturers_listbox.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(x=473, y=219, height=280)

        self.existing_students_label = Label(self.show_lecturers_page_frame, text="Existing Lecturers")
        self.existing_students_label.place(x=382, y=190)

        self.add_student_button = Button(self.show_lecturers_page_frame, text="Add Lecturer", width=38,
                                         command=self.add_lecturer_button_function)
        self.add_student_button.place(x=75, y=300)

        self.remove_selected_student_button = Button(self.show_lecturers_page_frame, text="Remove Selected Lecturer",
                                                     width=38, command=self.remove_selected_lecturer_button_function)
        self.remove_selected_student_button.place(x=75, y=340)

    def add_lecturer_button_function(self):
        self.window.destroy()
        AdminLecturerSignupPageFrame()

    def remove_selected_lecturer_button_function(self):
        i = self.lecturers_listbox.curselection()

        if len(i) >= 1:
            is_ok = messagebox.askokcancel("BE CAREFUL!!!", "Are You Sure?")
            if is_ok:
                selected_student = self.lecturers_listbox.get(i)

                if selected_student in self.lecturers_list:
                    idx = self.lecturers_list.index(selected_student)
                    selected_students_email = self.lecturers_emails[idx]
                    with open(relative_to_assets("lecturers.json")) as json_file:
                        data = json.load(json_file)
                        data.pop(selected_students_email)
                        with open(relative_to_assets("lecturers.json"), 'w') as outfile:
                            json.dump(data, outfile, indent=4)
                    self.window.destroy()
                    ShowLecturersPageFrame()

        elif len(i) == 0:
            messagebox.showerror("Error", "No Lecturers Selected")


    def go_back(self):
        self.window.destroy()
        AdminLoginPageFrame()

#TODO === LECTURER INTERFACE
class LecturerLoginPageFrame:

    def __init__(self):
        self.window = Tk()
        self.window.title("Education Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.lecturer_login_page_frame = Frame(self.window, width=500, height=500)
        self.lecturer_login_page_frame.pack()

        self.canvas = Canvas(self.lecturer_login_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=5)

        self.welcome_label = Label(self.lecturer_login_page_frame, text="WELCOME TO IYTE UBYS")
        self.welcome_label.place(x=177, y=180)

        self.email_label = Label(self.lecturer_login_page_frame, text="Email:")
        self.email_label.place(x=50, y=250)

        self.email_entry = Entry(self.lecturer_login_page_frame, width=36)
        self.email_entry.place(x=130, y=250)
        self.email_entry.focus_force()
        self.email_entry.insert(0, "username@iyte.edu.tr")

        self.password_label = Label(self.lecturer_login_page_frame, text="Password:")
        self.password_label.place(x=47, y=290)

        self.password_entry = Entry(self.lecturer_login_page_frame, width=36, show="*")
        self.password_entry.place(x=130, y=290)

        self.login_button = Button(self.lecturer_login_page_frame, text="LOGIN", width=30,
                                   command=self.login_button_function)
        self.login_button.place(x=143, y=325)

        self.forgot_password_button = Button(self.lecturer_login_page_frame, text="Forgot Password?", width=30,
                                             command=self.forgot_password_button_function)
        self.forgot_password_button.place(x=143, y=355)

        self.back_button = Button(self.lecturer_login_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

        self.window.mainloop()

    def forgot_password_button_function(self):
        self.window.destroy()
        LecturerForgotPasswordPageFrame()

    def go_back(self):
        self.window.destroy()
        MainPageFrame()

    def login_button_function(self):
        with open(relative_to_assets("lecturers.json"), "r") as lecturer_data:
            l_data = json.load(lecturer_data)
            if len(self.password_entry.get()) == 0 or len(self.email_entry.get()) == 0:
                messagebox.showerror("Error", "Please don't leave any fields empty !!")

            elif self.email_entry.get() in l_data:
                if self.password_entry.get() == l_data[self.email_entry.get()]["password"]:
                    NOW_LECTURER.append(l_data[self.email_entry.get()])
                    self.window.destroy()
                    LecturerLoginButtonFrame()
                else:
                    messagebox.showerror("Error", "Check your password and try again.")

            else:
                messagebox.showerror("Error", "Check your email and try again.")

class LecturerLoginButtonFrame:

    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.lecturer_login_page_frame = Frame(self.window, width=500, height=500)
        self.lecturer_login_page_frame.pack()

        self.canvas = Canvas(self.lecturer_login_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=0)

        self.my_lectures_button = Button(self.lecturer_login_page_frame, text="MY LECTURES", width=30,
                                         command=self.lecturer_my_lectures_button_function)
        self.my_lectures_button.place(x=155, y=260)

        self.my_profile_button = Button(self.lecturer_login_page_frame, text="MY PROFILE", width=30,
                                        command=self.lecturer_my_profile_button_function)
        self.my_profile_button.place(x=155, y=220)

        self.logout_button = Button(self.lecturer_login_page_frame, text="LOGOUT", width=30,
                                    command=self.logout_button_function)
        self.logout_button.place(x=155, y=300)

        self.student_info_label = Label(self.lecturer_login_page_frame, text=f"Welcome {NOW_LECTURER[0]["name"]}")
        self.student_info_label.place(x=180, y=180)

    def lecturer_my_profile_button_function(self):
        self.window.destroy()
        LecturerMyProfilePageFrame()

    def lecturer_my_lectures_button_function(self):
        self.window.destroy()
        LecturerMyLecturesPageFrame()

    def logout_button_function(self):
        global NOW_LECTURER
        NOW_LECTURER = []
        self.window.destroy()
        LecturerLoginPageFrame()

class LecturerMyProfilePageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.lecturer_my_profile_page_frame = Frame(self.window, width=500, height=500)
        self.lecturer_my_profile_page_frame.pack()

        self.canvas = Canvas(self.lecturer_my_profile_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=0)

        self.name_label = Label(self.lecturer_my_profile_page_frame, text=f"Name: {NOW_LECTURER[0]['name']}")
        self.name_label.place(x=185, y=210)

        self.email_label = Label(self.lecturer_my_profile_page_frame, text=f"Email: {NOW_LECTURER[0]['email']}")
        self.email_label.place(x=165, y=250)

        self.recovery_email_label = Label(self.lecturer_my_profile_page_frame,
                                          text=f"Recovery Email: {NOW_LECTURER[0]['recovery_email']}")
        self.recovery_email_label.place(x=145, y=290)

        self.password_change = Button(self.lecturer_my_profile_page_frame, text="Change My Password", width=20,
                                      command=self.password_change_button_function)
        self.password_change.place(x=110, y=330)

        self.recovery_email_change = Button(self.lecturer_my_profile_page_frame, text="Change My Recovery Email", width=25,
                                            command=self.recovery_email_change_button_function)
        self.recovery_email_change.place(x=250, y=330)

        self.back_button = Button(self.lecturer_my_profile_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

    def password_change_button_function(self):
        self.window.destroy()
        LecturerChanePassPageFrame()

    def recovery_email_change_button_function(self):
        self.window.destroy()
        LecturerChangeRecoveryEmailPageFrame()

    def go_back(self):
        self.window.destroy()
        LecturerLoginButtonFrame()

class LecturerChanePassPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.lecturer_change_password_page_frame = Frame(self.window, width=500, height=500)
        self.lecturer_change_password_page_frame.pack()

        self.canvas = Canvas(self.lecturer_change_password_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=0)

        self.back_button = Button(self.lecturer_change_password_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

        self.current_password_label = Label(self.lecturer_change_password_page_frame, text=f"Current Password: ")
        self.current_password_label.place(x=35, y=250)

        self.new_password_label = Label(self.lecturer_change_password_page_frame, text=f"New Password: ")
        self.new_password_label.place(x=40, y=290)

        self.confirm_new_password_label = Label(self.lecturer_change_password_page_frame, text=f"Confirm New Password: ")
        self.confirm_new_password_label.place(x=20, y=330)

        self.current_password_entry = Entry(self.lecturer_change_password_page_frame, width=36)
        self.current_password_entry.place(x=195, y=250)
        self.current_password_entry.focus_force()

        self.new_password_entry = Entry(self.lecturer_change_password_page_frame, width=36)
        self.new_password_entry.place(x=195, y=290)

        self.confirm_new_password_entry = Entry(self.lecturer_change_password_page_frame, width=36)
        self.confirm_new_password_entry.place(x=195, y=330)

        self.submit_button = Button(self.lecturer_change_password_page_frame, text="Submit", width=30, command=self.submit)
        self.submit_button.place(x=195, y=370)

    def submit(self):
        if len(self.new_password_entry.get()) == 0 or len(self.confirm_new_password_entry.get()) == 0 or len(
                self.current_password_entry.get()) == 0:
            messagebox.showerror(title="Oops", message="Please don't leave any fields empty !!")
        elif self.new_password_entry.get() != self.confirm_new_password_entry.get():
            messagebox.showerror(title="Oops", message="Passwords don't match !!")
        elif self.current_password_entry.get() != NOW_LECTURER[0]["password"]:
            messagebox.showerror(title="Oops", message="Current Password doesn't match !!")
        else:
            messagebox.showinfo(title="Success", message="Your Password has been changed !!")
            new_data = {
                NOW_LECTURER[0]["email"]: {
                    "name": NOW_LECTURER[0]['name'],
                    "email": NOW_LECTURER[0]['email'],
                    "recovery_email": NOW_LECTURER[0]['recovery_email'],
                    "password": self.new_password_entry.get(),
                }
            }

            with open(relative_to_assets("lecturers.json"), 'r') as file:
                data = json.load(file)
            data.update(new_data)
            with open(relative_to_assets("lecturers.json"), "w") as file:
                json.dump(data, file, indent=4)
                NOW_LECTURER[0]["password"] = self.new_password_entry.get()

            self.window.destroy()
            LecturerMyProfilePageFrame()

    def go_back(self):
        self.window.destroy()
        LecturerMyProfilePageFrame()

class LecturerChangeRecoveryEmailPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.lecturer_change_recovery_email_page_frame = Frame(self.window, width=500, height=500)
        self.lecturer_change_recovery_email_page_frame.pack()

        self.canvas = Canvas(self.lecturer_change_recovery_email_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=0)

        self.back_button = Button(self.lecturer_change_recovery_email_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

        self.new_recovery_email_label = Label(self.lecturer_change_recovery_email_page_frame, text=f"New Recovery Email: ")
        self.new_recovery_email_label.place(x=40, y=250)
        self.confirm_new_recovery_email_label = Label(self.lecturer_change_recovery_email_page_frame,
                                                      text=f"Confirm New Recovery Email: ")
        self.confirm_new_recovery_email_label.place(x=20, y=290)

        self.new_recovery_email_entry = Entry(self.lecturer_change_recovery_email_page_frame, width=36)
        self.new_recovery_email_entry.place(x=195, y=250)
        self.new_recovery_email_entry.focus_force()
        self.new_recovery_email_entry.insert(0, "username@gmail.com")

        self.confirm_new_recovery_email_entry = Entry(self.lecturer_change_recovery_email_page_frame, width=36)
        self.confirm_new_recovery_email_entry.place(x=195, y=290)
        self.confirm_new_recovery_email_entry.insert(0, "")

        self.submit_button = Button(self.lecturer_change_recovery_email_page_frame, text="Submit", width=30, command=self.submit)
        self.submit_button.place(x=195, y=330)

    def submit(self):
        if len(self.new_recovery_email_entry.get()) == 0 or len(self.confirm_new_recovery_email_entry.get()) == 0:
            messagebox.showerror(title="Oops", message="Please don't leave any fields empty !!")
        elif self.confirm_new_recovery_email_entry.get() != self.new_recovery_email_entry.get():
            messagebox.showerror(title="Oops", message="Emails don't match !!")
        else:
            messagebox.showinfo(title="Success", message="Your Recovery Email Has Changed Successfully!")
            new_data = {
                NOW_LECTURER[0]["email"]: {
                    "name": NOW_LECTURER[0]['name'],
                    "email": NOW_LECTURER[0]['email'],
                    "recovery_email": self.new_recovery_email_entry.get(),
                    "password": NOW_LECTURER[0]['password'],
                }
            }
            with open(relative_to_assets("lecturers.json"), 'r') as file:
                data = json.load(file)
            data.update(new_data)
            with open(relative_to_assets("lecturers.json"), "w") as file:
                json.dump(data, file, indent=4)
                NOW_LECTURER[0]["recovery_email"] = self.new_recovery_email_entry.get()

            self.window.destroy()
            LecturerMyProfilePageFrame()

    def go_back(self):
        self.window.destroy()
        LecturerMyProfilePageFrame()

class LecturerMyLecturesPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.lecturer_my_lectures_page_frame = Frame(self.window, width=500, height=500)
        self.lecturer_my_lectures_page_frame.pack()

        self.my_lectures_label = Label(self.lecturer_my_lectures_page_frame, text="My Lectures")
        self.my_lectures_label.place(x=410, y=200)


        self.canvas = Canvas(self.lecturer_my_lectures_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=145, y=0)

        self.back_button = Button(self.lecturer_my_lectures_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)


        self.lectures = []
        for lecture in os.listdir(relative_to_assets("lectures_list")):
            lecture_name = lecture.removesuffix(".json")
            with open(relative_to_assets_lectures_list(f"{lecture_name}.json"), "r") as lecture_file:
                already_enrolled = json.load(lecture_file)
                if NOW_LECTURER[0]["email"] in already_enrolled[lecture_name]["lecturer_email"]:
                    self.lectures.append(lecture_name)



        self.choicesvar = StringVar(value=self.lectures)
        self.listbox = Listbox(self.lecturer_my_lectures_page_frame, width=15, height=11, listvariable=self.choicesvar,
                               highlightthickness=0, borderwidth=0, justify="center", exportselection=False)
        self.listbox.place(x=400, y=225)
        self.listbox.selection_set(first=0)

        self.listbox.bind("<<ListboxSelect>>", self.students_list)


    def students_list(self, event=None):

        self.enrolled_students_label = Label(self.lecturer_my_lectures_page_frame, text="Enrolled Students")
        self.enrolled_students_label.place(x=270, y=200)

        i = self.listbox.curselection()
        self.selected_lecture = self.listbox.get(i)
        self.students_names = []
        self.students_emails = []

        with open(relative_to_assets_lectures_list(f"{self.selected_lecture}.json"), "r") as lecture_file:
            already_enrolled = json.load(lecture_file)
            self.students = already_enrolled[self.selected_lecture]["students_enrolled"]
            for f in self.students:
                with open(relative_to_assets("data.json"), "r") as file:
                    students_names = json.load(file)
                    self.students_names.append(students_names[f]["name"])
                    self.students_emails.append(students_names[f]["email"])


        def edit_info_label(event=None):
            self.info_label = Label(self.lecturer_my_lectures_page_frame)
            self.info_label.place(x=70, y=250)

            self.enrolled_students_email_label = Label(self.lecturer_my_lectures_page_frame, text="Student's email")
            self.enrolled_students_email_label.place(x=90, y=200)


            index = self.students_listbox.curselection()
            self.info_label.config(text=self.students_emails[index[0]])





        self.choicesvar = StringVar(value=self.students_names)
        self.students_listbox = Listbox(self.lecturer_my_lectures_page_frame, width=22, height=11, listvariable=self.choicesvar,
                               highlightthickness=0, borderwidth=0, justify="center")
        self.students_listbox.place(x=250, y=225)

        self.students_listbox.bind("<<ListboxSelect>>", edit_info_label)








    def go_back(self):
        self.window.destroy()
        LecturerLoginButtonFrame()

class LecturerForgotPasswordPageFrame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Student Management System")
        self.window.geometry("500x500+500+100")
        self.window.resizable(False, False)

        self.forget_password_page_frame = Frame(self.window, width=500, height=500)
        self.forget_password_page_frame.pack()

        self.canvas = Canvas(self.forget_password_page_frame, width=200, height=200)
        self.logo_img = ImageTk.PhotoImage(Image.open(relative_to_assets("iyte_logo.png")))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.place(x=155, y=0)

        self.welcome_label = Label(self.forget_password_page_frame, text="FORGOT PASSWORD PAGE")
        self.welcome_label.place(x=185, y=180)

        self.recovery_email_label = Label(self.forget_password_page_frame, text="Recovery Email:")
        self.recovery_email_label.place(x=40, y=290)

        self.recovery_email_entry = Entry(self.forget_password_page_frame, width=36)
        self.recovery_email_entry.place(x=150, y=290)
        self.recovery_email_entry.focus_force()
        self.recovery_email_entry.insert(0, "username@gmail.com")

        self.password_send_button = Button(self.forget_password_page_frame, text="Send My Password", width=30,
                                           command=self.send_password)
        self.password_send_button.place(x=159, y=340)

        self.back_button = Button(self.forget_password_page_frame, text="Go Back", width=10, command=self.go_back)
        self.back_button.place(x=10, y=10)

        self.window.mainloop()

    def send_password(self):
        email = self.recovery_email_entry.get()
        try:
            with open(relative_to_assets("lecturers.json"), "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showerror("Error", "Email not found.")

        else:
            message = ""
            emails = []
            l_emails = []
            for lecturer in data:
                r_email = data[lecturer]["recovery_email"]
                emails.append(r_email)
                l_emails.append(r_email)
                l_emails.append(lecturer)

            if email in emails:

                for key in data[l_emails[l_emails.index(email) + 1]]:
                    message += f"{key} : {data[l_emails[l_emails.index(email) + 1]][key]}"
                    message += "\n"
                try:
                    with smtplib.SMTP("smtp.gmail.com", port = 587) as connection:
                        connection.starttls()
                        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                        connection.sendmail(from_addr=MY_EMAIL, to_addrs=email,
                                            msg=f"Subject:YOUR PASSWORD\n\n{message}")
                except TimeoutError:
                    messagebox.showerror("Timeout Error",
                                         "Timed out while sending email\n\n*Check your email and try again\n*Check your internet connection and try again")
                else:
                    messagebox.showinfo("Successful", "Email sent successfully\nCheck your email for the password")
                finally:
                    self.window.destroy()
                    LecturerLoginPageFrame()
            else:
                messagebox.showerror("Error", "Email not found.\nCheck your email and try again")

    def go_back(self):
        self.window.destroy()
        LecturerLoginPageFrame()

MainPageFrame()


