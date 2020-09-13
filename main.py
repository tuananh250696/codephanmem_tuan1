from tkinter import *
import sqlite3
import tkinter as tk
import tkinter.messagebox
from datetime import date
import os
from tkinter import ttk
import math
import datetime
import cv2
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import imutils
import shutil
from fpdf import FPDF
import webbrowser

today = date.today()
date = datetime.datetime.now().date()
# temporary lists like sessions
products_list = []
product_price = []
product_quantity = []
product_id = []

# list for labels
root = Tk()
root.title("COMPANY BOSSCCOM")
root.geometry("1360x786+0+0")
labels_list = []
image = PhotoImage(file="ngang1.png")
img_resize = image.subsample(1, 1)
var = IntVar()
var1 = IntVar()
c = StringVar()
c1 = StringVar()



class Application:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        # frame
        self.left1 = Frame(master, width=1024, height=60, bg='white')
        self.left1.pack(side=TOP)
        Label(self.left1, image=img_resize, bg="white", relief=SUNKEN).pack(pady=5)

        self.left = Frame(master, width=260, height=1000, bg='white')
        self.left.pack(side=LEFT)

        # components
        self.date_l = Label(self.left,
                            text="Today's Date: " + str(today.day) + "-" + str(today.month) + "-" + str(today.year),
                            font=('arial 14 bold'), bg='lightblue',
                            fg='white')
        self.date_l.place(x=20, y=0)

        # button
        self.bt_st_catalog = Button(self.left, text="Hồ sơ bệnh nhân", width=15, height=2, font=('arial 18 bold'),
                                    bg='orange', command=self.ajax)
        self.bt_st_catalog.place(x=8, y=45)

        self.bt_st_form = Button(self.left, text="Nội soi", width=15, height=2, font=('arial 18 bold'), bg='orange',
                                 command=self.endoscopy)
        self.bt_st_form.place(x=8, y=135)

        self.bt_patient = Button(self.left, text="Biểu mẫu in", width=15, height=2, font=('arial 18 bold'), bg='orange',
                                 command=self.add_to_bn)
        self.bt_patient.place(x=8, y=225)

        self.bt_endoscop = Button(self.left, text="Danh mục khám", width=15, height=2, font=('arial 18 bold'),
                                  bg='orange', command=self.createNewWindow)
        self.bt_endoscop.place(x=8, y=315)

        self.bt_exit1 = Button(self.left, text="Thoát", width=15, height=2, font=('arial 18 bold'), bg='orange',
                               command=self.quit)
        self.bt_exit1.place(x=8, y=405)

    def Search(self, *args, **kwargs):
        # =====================================Table WIDGET=========================================
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect("db_member.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM `member` WHERE `name` LIKE ? AND `job` LIKE ? AND `address` LIKE ? AND `age` LIKE ?",
            ('%' + str(self.name_infos.get()) + '%', '%' + str(self.from_jobs.get()) + '%',
             '%' + str(self.from_addss.get()) + '%', '%' + str(self.born_agess.get()) + '%'))
        fetch = cursor.fetchall()
        for data in fetch:
            self.tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        self.name_infos.delete(0, tk.END)
        self.from_jobs.delete(0, tk.END)
        self.from_addss.delete(0, tk.END)
        self.born_agess.delete(0, tk.END)

    def ajax(self, *args, **kwargs):

        self.right = Frame(root, width=1100, height=75, bg='white')
        self.right.pack(side=TOP)

        self.bottom = Frame(root, width=1100, height=220, bg='lightblue')
        self.bottom.pack(side=TOP)

        self.bottom1 = Frame(root, width=1100, height=80, bg='yellow')
        self.bottom1.pack(side=TOP)

        self.bottom2 = Frame(root, width=1100, height=550, bg='lightblue')
        self.bottom2.pack(side=TOP)

        self.Top = Frame(self.bottom2, width=1000, bd=2, relief=SOLID)
        self.Top.pack(side=TOP)
        self.MidFrame = Frame(self.bottom2, width=1000)
        self.MidFrame.pack(side=TOP)
        self.RightForm = Frame(self.MidFrame, width=1100)
        self.RightForm.pack(side=RIGHT)

        self.bt_add_patient = Button(self.right, text="Lưu hồ sơ", width=14, height=3, font=('arial 12 bold'),
                                     bg='white', command=self.get_itemsdatabase)
        self.bt_add_patient.place(x=0, y=0)

        self.bt_open_file = Button(self.right, text="Mở hồ sơ", width=14, height=3, font=('arial 12 bold'), bg='white',
                                   command=self.create_pdf1)
        self.bt_open_file.place(x=150, y=0)
        #
        self.bt_save_file = Button(self.right, text="Làm mới", width=14, height=3, font=('arial 12 bold'), bg='white',
                                   command=self.delete_text)
        self.bt_save_file.place(x=300, y=0)
        #
        self.bt_delele1 = Button(self.right, text="Xóa", width=14, height=3, font=('arial 12 bold'), bg='white',
                                 command=self.Deletedata)
        # command=self.Deletedata)
        self.bt_delele1.place(x=450, y=0)
        #
        self.bt_thoat = Button(self.right, text="Đóng", width=14, height=3, font=('arial 12 bold'), bg='white',
                               command=self.add_to_cart)

        self.bt_thoat.place(x=600, y=0)
        self.bt_thoat = Button(self.right, text="Khôi phục cài đặt gốc", width=14, height=3, font=('arial 12 bold'),
                               bg='white',command=self.Deletealldata)
        self.bt_thoat.place(x=750, y=0)

        self.tenbenhnhan = Label(self.bottom, text="Tên bệnh nhân:", font=('arial 12 bold'), fg='black', bg='lightblue')
        self.tenbenhnhan.place(x=15, y=5)

        self.name_p = Entry(self.bottom, font=('arial 24 bold'), width=20)
        self.name_p.place(x=5, y=30)
        self.name_p.focus()

        self.adr = Label(self.bottom, text="Địa chỉ:", font=('arial 12 bold'), fg='black', bg='lightblue')
        self.adr.place(x=15, y=75)

        self.adr_p = Entry(self.bottom, font=('arial 24 bold'), width=20)
        self.adr_p.place(x=5, y=100)

        self.year_b = Label(self.bottom, text="Năm sinh:", font=('arial 12 bold'), fg='black', bg='lightblue')
        self.year_b.place(x=15, y=150)

        self.y_b = Entry(self.bottom, font=('arial 24 bold'), width=20)
        self.y_b.place(x=5, y=175)

        self.job = Label(self.bottom, text="Nghề nghiệp:", font=('arial 12 bold'), fg='black', bg='lightblue')
        self.job.place(x=425, y=5)
        self.jobw = Entry(self.bottom, font=('arial 24 bold'), width=20)
        self.jobw.place(x=410, y=30)

        self.st = Label(self.bottom, text="Triệu chứng:", font=('arial 12 bold'), fg='black', bg='lightblue')
        self.st.place(x=420, y=75)
        self.stom = Entry(self.bottom, font=('arial 24 bold'), width=20)
        self.stom.place(x=410, y=100)

        self.sbh = Label(self.bottom, text="Số bảo hiểm:", font=('arial 12 bold'), fg='black', bg='lightblue')
        self.sbh.place(x=420, y=150)
        self.nbh = Entry(self.bottom, font=('arial 24 bold'), width=20)
        self.nbh.place(x=410, y=175)

        # self.enteride = Entry(self.bottom, width=25, font=('arial 18 bold'), bg='lightblue')
        # self.enteride.place(x=800, y=175)
        # self.enteride.focus()

        self.droplist = OptionMenu(self.bottom, c, 'NAM', 'NỮ')
        self.droplist.pack()
        self.menu = self.droplist.nametowidget(self.droplist.menuname)
        self.menu.configure(font=('arial 20 bold'))
        c.set('NAM')
        self.droplist.config(width=10, font=('arial 18 bold'))
        self.droplist.place(x=800, y=30)

        self.seachinfo = Button(self.bottom1, text="Tìm kiếm", width=15, height=1, font=('arial 18 bold'), bg='orange',
                                command=self.Search)
        self.seachinfo.place(x=800, y=5)

        self.name_info = Label(self.bottom1, text="Tên:", font=('arial 12 bold'), fg='black', bg='lightblue')
        self.name_info.place(x=5, y=10)

        self.name_infos = Entry(self.bottom1, width=18, font=('arial 20 bold'), bg='white')
        self.name_infos.place(x=5, y=38)

        self.job_s = Label(self.bottom1, text="Nghề nghiệp:", font=('arial 12 bold'), fg='black', bg='lightblue')
        self.job_s.place(x=290, y=10)
        self.from_jobs = Entry(self.bottom1, font=('arial 20 bold'), width=12)
        self.from_jobs.place(x=290, y=38)

        self.aadd_s = Label(self.bottom1, text="Địa Chỉ:", font=('arial 12 bold'), fg='black', bg='lightblue')
        self.aadd_s.place(x=485, y=10)
        self.from_addss = Entry(self.bottom1, font=('arial 20 bold'), width=10)
        self.from_addss.place(x=485, y=38)

        self.born_s2 = Label(self.bottom1, text="Năm sinh:", font=('arial 12 bold'), fg='black', bg='lightblue')
        self.born_s2.place(x=650, y=10)
        self.born_agess = Entry(self.bottom1, font=('arial 20 bold'), width=5)
        self.born_agess.place(x=650, y=38)

        self.scrollbarx = Scrollbar(self.RightForm, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(self.RightForm, orient=VERTICAL)
        self.tree = ttk.Treeview(self.RightForm, columns=("Id", "Name", "Job", "Address", "Age"),
                                 selectmode="extended",
                                 height=400, yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set)
        self.scrollbary.config(command=self.tree.yview)
        self.scrollbary.pack(side=RIGHT, fill=Y)
        self.scrollbarx.config(command=self.tree.xview)
        self.scrollbarx.pack(side=BOTTOM, fill=X)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=30)
        self.tree.column('#2', stretch=NO, minwidth=0, width=300)
        self.tree.column('#3', stretch=NO, minwidth=0, width=250)
        self.tree.column('#4', stretch=NO, minwidth=0, width=250)

        self.tree.pack()
        self.tree.heading('Id', text="Id", anchor=W)
        self.tree.heading('Name', text="Name", anchor=W)
        self.tree.heading('Job', text="Job", anchor=W)
        self.tree.heading('Address', text="Address", anchor=W)
        self.tree.heading('Age', text="Age", anchor=W)

    def Deletedata(self):

        conn = sqlite3.connect("db_member.db")
        cursor = conn.cursor()
        for selected_item in self.tree.selection():
            print(selected_item)  # it prints the selected row id
            cursor.execute("DELETE FROM member WHERE id=?", (self.tree.set(selected_item, '#1'),))
            self.tree.delete(selected_item)
        conn.commit()
        conn.close()

    def Deletealldata(self):
        shutil.rmtree("anh")
        conn = sqlite3.connect("db_member.db")
        cur = conn.cursor()
        sql = 'DELETE FROM member'
        cur.execute(sql)
        conn.commit()

    def get_itemsdatabase(self, *args, **kwargs):

        conn = sqlite3.connect("db_member.db")
        cursor = conn.cursor()

        if self.name_p.get() == '' or self.adr_p.get() == '' or self.y_b.get() == '' or self.jobw.get() == '' or self.stom.get() == '' or self.nbh.get() == '' or c.get() == '':
            tkinter.messagebox.showinfo("Error", "Điền đầy đủ thông tin.")
        else:

            cursor.execute('INSERT INTO member (name, address, age, job, symptom,sbh,sex ) VALUES(?,?,?,?,?,?,?)', (
            self.name_p.get(), self.adr_p.get(), self.y_b.get(), self.jobw.get(), self.stom.get(), self.nbh.get(),
            c.get()))
            conn.commit()
            self.endoscopy()
            # textbox insert
            # tkinter.messagebox.showinfo("Success", "Successfully added to the database")


    def add_to_cart(self, *args, **kwargs):
        self.right.destroy()
        self.bottom.destroy()
        self.bottom1.destroy()
        self.bottom2.destroy()

    def delete_text(self, *args, **kwargs):

        self.name_p.delete(0, END)
        self.adr_p.delete(0, END)
        self.y_b.delete(0, END)
        self.jobw.delete(0, END)
        self.stom.delete(0, END)
        self.nbh.delete(0, END)

    def database_print(self, *args, **kwargs):

        namepk = self.adr2_p.get()
        name_dt = self.doctor_p.get()
        address_pk = self.n2_p.get()
        conn = sqlite3.connect("db_member.db")
        cursor = conn.cursor()
        if namepk == '' or name_dt == '' or address_pk == '':
            tkinter.messagebox.showinfo("Error", "Điền đầy đủ thông tin.")
        else:
            cursor.execute("DELETE FROM print_dt WHERE id=1")
            cursor.execute('CREATE TABLE IF NOT EXISTS print_dt (name_pk TEXT,dt_name TEXT,address TEXT)')
            cursor.execute('INSERT INTO print_dt (name_pk,dt_name,address) VALUES(?,?,?)',
                           (namepk, name_dt, address_pk))
            tkinter.messagebox.showinfo("Success", "Đã thêm thông tin")
            conn.commit()
            cursor.close()

    def add_to_bn(self, *args, **kwargs):
        addWindow = Toplevel(root)
        addWindow.title("Set form print")
        addWindow.geometry("1200x600")
        self.rightw2 = Frame(addWindow, width=550, height=600, bg='lightblue')
        self.rightw2.pack(side=RIGHT)
        self.rightw3 = Frame(addWindow, width=600, height=600, bg='lightblue')
        self.rightw3.pack(side=LEFT)

        self.adr2 = Label(self.rightw3, text="Phòng khám:", font=('arial 16 bold'), fg='black', bg='lightblue')
        self.adr2.place(x=10, y=10)
        self.adr2_p = Entry(self.rightw3, font=('arial 18 bold'), width=32)
        self.adr2_p.place(x=150, y=10)

        self.doctor = Label(self.rightw3, text=" Bác sĩ :", font=('arial 16 bold'), fg='black', bg='lightblue')
        self.doctor.place(x=10, y=85)

        self.doctor_p = Entry(self.rightw3, font=('arial 18 bold'), width=32)
        self.doctor_p.place(x=150, y=75)

        self.n2 = Label(self.rightw3, text="Địa chỉ:", font=('arial 16 bold'), fg='black', bg='lightblue')
        self.n2.place(x=10, y=150)

        self.n2_p = Entry(self.rightw3, font=('arial 18 bold'), width=32)
        self.n2_p.place(x=150, y=150)

        self.add_dt = Button(self.rightw3, text="Cập nhật", width=12, height=2, font=('arial 18 bold'), bg='orange',
                             command=self.database_print)
        self.add_dt.place(x=10, y=260)

        self.add_dl = Button(self.rightw3, text="Xóa", width=12, height=2, font=('arial 18 bold'), bg='orange',
                             command=self.Deletedata_print)
        self.add_dl.place(x=200, y=260)

        self.add_dltd = Button(self.rightw3, text="Đóng", width=12, height=2, font=('arial 18 bold'), bg='orange',
                               command=self.quit_print2)
        self.add_dltd.place(x=390, y=260)

        self.scrollbarx = Scrollbar(self.rightw2, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(self.rightw2, orient=VERTICAL)
        self.tree1 = ttk.Treeview(self.rightw2, columns=("Id", "Phòng khám", "Bác sĩ", "Địa chỉ"),
                                  selectmode="extended",
                                  height=400, yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set)
        self.scrollbary.config(command=self.tree1.yview)
        self.scrollbary.pack(side=RIGHT, fill=Y)
        self.scrollbarx.config(command=self.tree1.xview)
        self.scrollbarx.pack(side=BOTTOM, fill=X)
        self.tree1.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree1.column('#1', stretch=NO, minwidth=0, width=30)
        self.tree1.column('#2', stretch=NO, minwidth=0, width=250)
        self.tree1.column('#3', stretch=NO, minwidth=0, width=150)
        self.tree1.column('#4', stretch=NO, minwidth=0, width=150)

        self.tree1.pack()
        self.tree1.heading('Id', text="Id", anchor=W)
        self.tree1.heading('Phòng khám', text="Phòng khám", anchor=W)
        self.tree1.heading('Bác sĩ', text="Bác sĩ", anchor=W)
        self.tree1.heading('Địa chỉ', text="Địa chỉ", anchor=W)
        self.tree1.pack()

        conn = sqlite3.connect("db_member.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `print_dt`")
        fetch = cursor.fetchall()
        for data in fetch:
            self.tree1.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

    def Deletedata_print(self):
        conn = sqlite3.connect("db_member.db")
        cursor = conn.cursor()
        for selected_item1 in self.tree1.selection():
            print(selected_item1)  # it prints the selected row id
            cursor.execute("DELETE FROM print_dt WHERE id=?", (self.tree1.set(selected_item1, '#1'),))
            conn.commit()
            self.tree1.delete(selected_item1)
        conn.commit()
        cursor.close()

    def Chosedata_print(self):
        conn = sqlite3.connect("db_member.db")
        cursor = conn.cursor()
        for selected_item1 in self.tree1.selection():
            print(selected_item1)  # it prints the selected row id
            cursor.execute("DELETE FROM print_dt WHERE id=?", (self.tree1.set(selected_item1, '#1'),))
            conn.commit()
            self.tree1.delete(selected_item1)
        conn.commit()
        cursor.close()

    def database_print111(self, *args, **kwargs):
        nameadd22 = c1.get()
        name_dt22 = self.ad_if2.get()

        conn = sqlite3.connect("db_member.db")
        cursor = conn.cursor()
        if nameadd22 == '' or name_dt22 == '':
            tkinter.messagebox.showinfo("Error", "điền đầy đủ thông tin!.")

        else:
            cursor.execute('CREATE TABLE IF NOT EXISTS print_dt22 (name_pk22 TEXT,dt_name22 TEXT)')
            cursor.execute('INSERT INTO print_dt22 (name_pk22,dt_name22) VALUES(?,?)',
                           (nameadd22, name_dt22))
            tkinter.messagebox.showinfo("Success", "Đã thêm thông tin")
            conn.commit()
            cursor.close()

    def createNewWindow(self, *args, **kwarg):
        newWindowaddf = Toplevel(root)
        newWindowaddf.title("add infomation")
        newWindowaddf.geometry("800x500")

        self.rightw2 = Frame(newWindowaddf, width=500, height=500, bg='lightblue')
        self.rightw2.pack(side=RIGHT)
        self.rightw3 = Frame(newWindowaddf, width=290, height=500, bg='lightblue')
        self.rightw3.pack(side=LEFT)

        self.n3 = Label(self.rightw3, text="Chẩn Đoán:", font=('arial 14 bold'), fg='black', bg='lightblue')
        self.n3.place(x=10, y=10)

        self.ad_if2 = Entry(self.rightw3, font=('arial 20 bold'), width=16)
        self.ad_if2.place(x=10, y=40)

        self.n4 = Label(self.rightw3, text="Danh Mục:", font=('arial 14 bold'), fg='black', bg='lightblue')
        self.n4.place(x=10, y=90)

        self.droplist = OptionMenu(self.rightw3, c1, 'TAI', 'MŨI', 'HỌNG')
        self.droplist.pack()

        self.menu = self.droplist.nametowidget(self.droplist.menuname)
        self.menu.configure(font=('arial 28 bold'))
        c1.set('HỌNG')

        self.droplist.config(width=16, height=2, font=('arial 18 bold'))
        self.droplist.place(x=5, y=120)

        self.add_ifmt = Button(self.rightw3, text="Cập nhật", width=14, height=2, font=('arial 20 bold'), bg='orange',
                               command=self.database_print111)
        self.add_ifmt.place(x=5, y=200)

        self.add_dltifmt = Button(self.rightw3, text="Xóa", width=14, height=2, font=('arial 20 bold'),
                                  bg='orange', command=self.Deletedata_NewWindow)
        self.add_dltifmt.place(x=5, y=300)

        self.add_dltd = Button(self.rightw3, text="Đóng", width=14, height=2, font=('arial 20 bold'),
                               bg='orange', command=self.quit_print1)
        self.add_dltd.place(x=5, y=400)
        scrollbary = Scrollbar(self.rightw2, orient=VERTICAL)
        scrollbarx = Scrollbar(self.rightw2, orient=HORIZONTAL)
        self.tree2 = ttk.Treeview(self.rightw2, columns=("Diagnostic", "Firstname"),
                                  selectmode="extended", height=500, yscrollcommand=scrollbary.set,
                                  xscrollcommand=scrollbarx.set)
        scrollbary.config(command=self.tree2.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=self.tree2.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        self.tree2.heading('Diagnostic', text="Diagnostic", anchor=W)
        self.tree2.heading('Firstname', text="Firstname", anchor=W)
        self.tree2.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree2.column('#1', stretch=NO, minwidth=0, width=200)
        self.tree2.column('#2', stretch=NO, minwidth=0, width=300)
        self.tree2.pack()

        conn = sqlite3.connect("db_member.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `print_dt22`")
        fetch = cursor.fetchall()
        for data in fetch:
            self.tree2.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

    def Deletedata_NewWindow(self):
        conn = sqlite3.connect("db_member.db")
        cursor = conn.cursor()
        for selected_item1 in self.tree2.selection():
            print(selected_item1)  # it prints the selected row id
            cursor.execute("DELETE FROM print_dt22 WHERE name_pk22=?", (self.tree2.set(selected_item1, '#1'),))
            conn.commit()
            self.tree2.delete(selected_item1)
        conn.commit()
        cursor.close()

    def quit(self):
        root.withdraw()
        root.destroy()

    def quit_print1(self):
        tkinter.messagebox.showinfo("Success", "Thoát cài đặt danh mục")

    def quit_print2(self):
        tkinter.messagebox.showinfo("Success", "Thoát cài đặt biểu mẫu")

    def hide(self):
        root.withdraw()

    def show(self):
        root.update()
        root.deiconify()

    def create_pdf1(self):
        # Set up a logo
        conn = sqlite3.connect("db_member.db")
        conn.row_factory = sqlite3.Row
        for selected_item in self.tree.selection():
            print(selected_item)
        cur = conn.cursor()
        cur.execute("SELECT * FROM `member` WHERE id=?", (self.tree.set(selected_item, '#1'),))
        rows = cur.fetchall()
        for row in rows:
            print("%s" % (row["id"]))
        webbrowser.open_new(r'doccument\%s.pdf' % ("a" + str(row["id"])))

    def endoscopy(self):
        class tehseencode(QDialog):
            def __init__(self):

                super(tehseencode, self).__init__()
                loadUi("untitled2.ui", self)
                self.logic = 0
                self.value = 1
                self.SHOW.clicked.connect(self.onClicked)
                self.TEXT.setText("Kindly Press 'Show' to connect with webcam.")
                self.CAPTURE.clicked.connect(self.CaptureClicked)
                self.NEXT_3.clicked.connect(self.create_pdf2)
                self.CAPTURE_2.clicked.connect(self.f2vrec)
                self.NEXT_2.clicked.connect(self.w1)
                self.NEXT_7.clicked.connect(self.w1)

            @pyqtSlot()
            def onClicked(self):
                self.TEXT.setText('Kindly Press "Capture Image " to Capture image')
                cap = cv2.VideoCapture(0)
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                op = cv2.VideoWriter('Sample1.avi', fourcc, 11.0, (560, 560))
                self.value=0
                while (cap.isOpened()):
                    ret, frame = cap.read()
                    frame = imutils.resize(frame, width=560, height=560)
                    frame1 = imutils.resize(frame, width=80, height=60)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    if ret == True:
                        self.displayImage(frame, 1)
                        cv2.waitKey()
                        if (self.logic == 2):
                            self.value = self.value + 1
                            conn = sqlite3.connect("db_member.db")
                            conn.row_factory = sqlite3.Row
                            cur = conn.cursor()
                            cur.execute("SELECT max(id) FROM member")
                            rows = cur.fetchall()
                            directory = "anh/"
                            if not os.path.exists(directory):
                                os.makedirs(directory)
                            for row in rows:
                                print("%s" % (row["max(id)"]))
                            cv2.imwrite('anh\%s.png' % ("a" + str(row["max(id)"]) + "a" + str(self.value)), frame1)
                            self.TEXT.setText('your Image have been Saved')

                            conn.commit()
                            conn.close()
                            self.logic = 1

                        if (self.logic == 3):
                            op.write(frame)
                        if (self.logic == 4):
                            cap.release()
                            break

                    else:
                        print('not found')
                cap.release()
                cv2.destroyAllWindows()

            def CaptureClicked(self):
                self.logic = 2

            def displayImage(self, img, window=1):
                qformat = QImage.Format_Indexed8
                if len(img.shape) == 3:
                    if (img.shape[2]) == 4:
                        qformat = QImage.Format_RGBA888
                    else:
                        qformat = QImage.Format_RGB888
                img = QImage(img, img.shape[1], img.shape[0], qformat)
                img = img.rgbSwapped()
                self.imgLabel.setPixmap(QPixmap.fromImage(img))
                self.imgLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignLeft)

            def f2vrec(self):
                self.logic = 3

            def w1(self):
                #self.logic = 4
                window.close()

            def create_pdf2(self):
                # Set up a logo
                conn = sqlite3.connect("db_member.db")
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute("SELECT max(id) FROM member")
                rows = cur.fetchall()
                for row in rows:
                    print("%s" % (row["max(id)"]))

                cur2 = conn.cursor()
                cur2.execute("SELECT name_pk FROM print_dt")
                cur3 = conn.cursor()
                cur3.execute("SELECT address FROM print_dt")
                cur4 = conn.cursor()
                cur4.execute("SELECT dt_name FROM print_dt")
                cur5 = conn.cursor()
                cur5.execute("SELECT * FROM `member`")

                rows5 = cur5.fetchall()
                rows4 = cur4.fetchall()
                rows3 = cur3.fetchall()
                rows2 = cur2.fetchall()

                for row5 in rows5:
                    row5[6]
                for row2 in rows2:
                    row2["name_pk"]

                for row3 in rows3:
                    row3["address"]

                for row4 in rows4:
                    row4["dt_name"]



                t = row2["name_pk"]
                t1 = row3["address"]
                t2 = "BS: " + row4["dt_name"]

                pdf = FPDF()
                pdf.set_font("Arial", size=12)
                pdf.add_page()

                pdf.image('demo.png', 8, 10, 25)
                pdf.add_font('DejaVu', '', 'DejaVuSerif-Italic.ttf', uni=True)
                pdf.set_font('DejaVu', '', 16)
                pdf.set_text_color(0, 70, 255)
                pdf.cell(35)
                pdf.cell(0, 5, t, ln=1)
                pdf.set_font('DejaVu', '', 14)

                pdf.cell(70)
                pdf.cell(0, 10, t2, ln=1)
                pdf.set_font('DejaVu', '', 14)
                pdf.set_text_color(0, 70, 255)
                pdf.cell(30)

                pdf.cell(0, 0, "ĐC:", ln=1)
                pdf.set_font('DejaVu', '', 12)
                pdf.set_text_color(0, 0, 0)
                pdf.cell(40)
                pdf.cell(0, 0, t1, ln=1)
                pdf.set_draw_color(0, 0, 0)
                pdf.set_line_width(1)
                pdf.line(30, 30, 180, 30)

                pdf.set_font('DejaVu', '', 16)
                pdf.set_text_color(255, 0, 40)
                pdf.cell(35)
                pdf.cell(0, 5, ' ', ln=1)

                pdf.set_font('DejaVu', '', 16)
                pdf.set_text_color(255, 0, 40)
                pdf.cell(35)
                pdf.cell(0, 15, 'PHIẾU KHÁM NỘI SOI TAI-MŨI-HỌNG', ln=1)

                pdf.set_font('DejaVu', '', 12)
                pdf.set_text_color(0, 70, 255)
                pdf.cell(75)
                pdf.cell(0, 0, 'Số Phiếu : ' + str(row5[0]), ln=1)

                pdf.set_font('DejaVu', '', 16)
                pdf.set_text_color(0, 70, 255)
                pdf.cell(0, 8, ' ', ln=1)

                pdf.set_font('DejaVu', '', 10)
                pdf.cell(5)
                pdf.cell(0, 0, 'Tên bệnh nhân : ' + str(row5[1]), ln=1)
                pdf.cell(85)
                pdf.cell(0, 0, 'Tuổi : ' + str(row5[4]), ln=1)
                pdf.cell(135)
                pdf.cell(0, 0, 'Giới tính : ' + str(row5[6]), ln=1)

                pdf.set_font('DejaVu', '', 10)
                pdf.set_text_color(0, 70, 255)
                pdf.cell(0, 8, ' ', ln=1)
                pdf.cell(5)
                pdf.cell(0, 0, 'Địa chỉ : ' + str(row5[3]), ln=1)
                pdf.cell(85)
                pdf.cell(0, 0, 'Số bảo hiểm : ' + str(row5[7]), ln=1)
                pdf.cell(135)
                pdf.cell(0, 0, 'Nghề nghiệp : ' + str(row5[2]), ln=1)

                pdf.set_font('DejaVu', '', 10)
                pdf.set_text_color(0, 70, 255)
                pdf.cell(0, 8, ' ', ln=1)
                pdf.cell(5)
                pdf.cell(0, 0, 'Triệu chứng : ' + str(row5[5]), ln=1)
                pdf.cell(85)
                pdf.cell(0, 0, 'Số bảo hiểm : ' + str(row5[7]), ln=1)
                pdf.cell(135)
                pdf.cell(0, 0, 'Nghề nghiệp : ' + str(row5[2]), ln=1)

                pdf.set_font('DejaVu', '', 14)
                pdf.cell(0, 15, ' ', ln=1)
                pdf.cell(70)
                pdf.cell(0, 0, 'HÌNH ẢNH NỘI SOI ', ln=1)
                #
                file_name =  ('anh\%s.png' % ("a" + str(row["max(id)"]) + "a" + str(2)))
                file_name1 = ('anh\%s.png' % ("a" + str(row["max(id)"]) + "a" + str(3)))
                file_name2 = ('anh\%s.png' % ("a" + str(row["max(id)"]) + "a" + str(4)))
                file_name3 = ('anh\%s.png' % ("a" + str(row["max(id)"]) + "a" + str(5)))
                file_name4 = ('anh\%s.png' % ("a" + str(row["max(id)"]) + "a" + str(6)))
                file_name5 = ('anh\%s.png' % ("a" + str(row["max(id)"]) + "a" + str(7)))
                #
                pdf.image(file_name, 12, 90, 60)
                pdf.image(file_name1, 12, 150, 60)
                pdf.image(file_name2, 74, 90, 60)
                pdf.image(file_name3, 74, 150, 60)
                pdf.image(file_name4, 136, 90, 60)
                pdf.image(file_name5, 136, 150, 60)

                pdf.set_font('DejaVu', '', 16)
                pdf.cell(0, 132, ' ', ln=1)
                pdf.cell(60)
                pdf.cell(0, 0, 'MÔ TẢ KẾT QUẢ NỘI SOI ', ln=1)
                pdf.set_font('DejaVu', '', 12)
                pdf.cell(0, 8, ' ', ln=1)
                pdf.cell(12)
                pdf.cell(0, 7, 'Chẩn đoán : ', ln=1)
                pdf.cell(12)
                pdf.cell(0, 7, 'Điều trị : ', ln=1)
                pdf.cell(12)
                pdf.cell(0, 7, 'Chỉ định bác sĩ : ', ln=1)

                pdf.set_x(120)
                pdf.cell(0, 10, " Ngày " + str(today.day) + " Tháng " + str(today.month) + " Năm " + str(today.year),
                         ln=1)
                pdf.set_x(145)
                pdf.cell(0, 6, 'Bác sĩ : ', ln=1)
                pdf.cell(0, 15, ' ', ln=1)
                pdf.set_x(126)
                pdf.cell(0, 0, t2, ln=1)
                directory1 = "doccument/"
                if not os.path.exists(directory1):
                    os.makedirs(directory1)
                pdf.output('doccument\%s.pdf' %("a" + str(row["max(id)"])))
                webbrowser.open_new(r'doccument\%s.pdf' %("a" + str(row["max(id)"])))
                conn.commit()
                cur.close()

        window = tehseencode()
        window.show()
        try:
            sys.exit(app.exec_())
        except:
            print('excitng')


app = QApplication(sys.argv)
b = Application(root)

root.geometry("1024x600+0+0")
root.mainloop()

