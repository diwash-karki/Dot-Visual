from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.font import Font
import os, json, random, datetime
from PIL import ImageTk, Image
from build.buildlogic import build


def unhash(hv):
    hash = ""
    t = hv.split('`')
    for i in t:
        if i.isdigit():
            x = int(int(i) / 7338)
            hash += str(x) + "-"
    return hash[:-1]


def check_hash():
    date = str(datetime.datetime.today()).split(" ")[0]
    y = date.split("-")[0]
    m = date.split("-")[1]
    d = date.split("-")[2]
    chck = open("binaries/bn_hash.json", "r")
    jsdata = json.load(chck)
    unhashdate = unhash(jsdata["app"]["donotedit"])
    yy = unhashdate.split("-")[0]
    mm = unhashdate.split("-")[1]
    dd = unhashdate.split("-")[2]
    chck.close()

    if y <= yy:
        if m <= mm:
            if d <= dd:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def showframe(frame):
    print(frame)
    if str(frame) == ".!frame3":
        r_f = Frame(root, bg="white")
        r_f.grid(row=0, column=0, sticky="nsew")
        mainui.home(r_f)
        frame = r_f
    frame.tkraise()


def expired_page(frame):
    Label(frame, text="Your trial has been expired.", bg="#303030", fg="white", font=("Arial", 20, "bold")).pack(
        anchor="center", pady=(300, 50))
    Button(frame, text="EXIT", height=2, width=20, bd=0, command=quit, font=("Arial", 10, "bold")).pack()


class UI:
    def __init__(self):
        self.height = 0
        self.width = 0
        self.folder = ""
        self.canvascolor = "#F1F1F1"
        self.color_var = StringVar()
        self.height_var = IntVar()
        self.width_var = IntVar()
        self.txtvar = StringVar()
        self.widheight_var = IntVar()
        self.widwidth_var = IntVar()
        self.fg_var = StringVar()
        self.bg_var = StringVar()
        self.fontsize_var = IntVar()
        self.weight_var = StringVar()
        self.border_var = IntVar()
        self.posx_var = IntVar()
        self.posy_var = IntVar()
        self.font_var = StringVar()
        self.activewidget = ""
        self.memorywidget = ""
        self.activetype = ""

    def welcomepage(self, frame):
        root.title("Dot Visual > Welcome")
        canvas = Canvas(frame, height=611, width=766, bg="#363636", highlightthickness=0)
        myFont = Font(family="Segoe UI", size=45, weight="bold")
        btnfont = Font(family="Segoe UI", size=18, weight="bold")
        fontsmall = Font(family="Segoe UI", size=15)
        title = Label(frame, text="New Project", bg="#363636", fg="#707070", font=myFont)
        w = Entry(frame, bg="#303030", fg="white", border=0, font=("monospace", 35), width=5)
        h = Entry(frame, bg="#303030", fg="white", border=0, font=("monospace", 35), width=5)
        wl = Label(frame, text="Width", bg="#363636", fg="#707070", font=fontsmall)
        hl = Label(frame, text="Height", bg="#363636", fg="#707070", font=fontsmall)
        canvas.create_rectangle(170, 235, 302, 238, fill="white", width=0)
        canvas.create_rectangle(430, 235, 562, 238, fill="white", width=0)
        folder = Entry(frame, bg="#303030", fg="white", border=0, font=("monospace", 35), width=15)
        folderl = Label(frame, text="Project Name", bg="#363636", fg="#707070", font=fontsmall)
        canvas.create_rectangle(170, 366, 562, 369, fill="white", width=0)
        save = Button(frame, text="Create", height=0, width=27, font=btnfont, fg="#423F3F", bg="#FFBB00", border=0,
                      command=lambda: self.createnewproject(w, h, folder))

        load = Button(frame, text="Load", height=0, width=27, font=btnfont, fg="#423F3F", bg="#FF6800", border=0,
                      command=lambda: self.loadpreviousdata(askdirectory()))
        canvas.create_window(210, 30, window=title, anchor=NW)
        canvas.create_window(170, 180, window=w, anchor=NW)
        canvas.create_window(430, 180, window=h, anchor=NW)
        canvas.create_window(170 + 35, 250, window=wl, anchor=NW)
        canvas.create_window(430 + 35, 250, window=hl, anchor=NW)
        canvas.create_window(170, 310, window=folder, anchor=NW)
        canvas.create_window(310, 370, window=folderl, anchor=NW)
        canvas.create_window(174, 440, window=save, anchor=NW)
        canvas.create_window(174, 510, window=load, anchor=NW)
        canvas.pack(pady=(95, 0))

    def createnewproject(self, w, h, folder):
        try:
            print("create")
            self.width = w.get()
            self.height = h.get()
            self.folder = folder.get()
            self.color_var.set("#F1F1F1")
            self.height_var.set(int(h.get()))
            self.width_var.set(int(w.get()))

            os.mkdir("data/" + self.folder)
            data = open("data/{}/main.json".format(self.folder), "w")
            print("nope")
            canvassetting = {"canvas":
                                 {"width": int(self.width),
                                  "height": int(self.height),
                                  "color": "#F1F1F1"
                                  }}
            canvassetting = json.dumps(canvassetting, indent=4)
            data.write(canvassetting)
            data.close()

            self.loadpreviousdata(self.folder)
        except Exception as e:
            showerror("Error", str(e) + "\t Create Project")

    def loadpreviousdata(self, path):
        try:

            print(path.split("/")[-1])
            try:
                folder = path.split('/')[-1]
            except:
                print("gg")
                folder = path
            rcnt = open(f"data/{folder}/main.json")
            x = json.load(rcnt)
            self.height = x["canvas"]["height"]
            self.width = x["canvas"]["width"]
            self.canvascolor = x["canvas"]["color"]
            self.folder = folder
            self.color_var.set(self.canvascolor)
            self.height_var.set(int(self.height))
            self.width_var.set(int(self.width))
            rcnt.close()
            showframe(homef)

            for wi in x:

                if wi != "canvas":
                    self.memorywidget = wi
                    self.previouswidget(wi, x[wi]["text"], x[wi]["fg"], x[wi]["bg"], x[wi]["x"], x[wi]["y"],
                                        x[wi]["fontsize"], x[wi]["font"], x[wi]["weight"], x[wi]["border"],
                                        x[wi]["height"], x[wi]["width"], x[wi]["type"])
            self.memorywidget = ""

        except Exception as e:
            showerror("Error", str(e) + "\t Load Previous")
            showframe(welcomef)

    def home(self, frame):
        root.title("Dot Visual >> " + self.folder)
        topframe = Frame(frame, bg="#2B2B2B", height=123, width=960)

        hl = Label(topframe, text="height", bg="#2B2B2B", fg="white", font=("arial", 10, "bold"))
        hl.place(x=20, y=2)
        hp = Entry(topframe, border=0, bg="#817D7D", fg="white", width=5, font=("arial", 15, "bold"),
                   textvariable=self.widheight_var)
        hp.place(x=20, y=25)
        hl = Label(topframe, text="width", bg="#2B2B2B", fg="white", font=("arial", 10, "bold"))
        hl.place(x=20, y=60)
        wp = Entry(topframe, border=0, bg="#817D7D", fg="white", width=5, font=("arial", 15, "bold"),
                   textvariable=self.widwidth_var)
        wp.place(x=20, y=83)

        hl = Label(topframe, text="text", bg="#2B2B2B", fg="white", font=("arial", 10, "bold"))
        hl.place(x=100, y=2)
        txtp = Entry(topframe, border=0, bg="#817D7D", fg="white", width=5, font=("arial", 15, "bold"),
                     textvariable=self.txtvar)
        txtp.place(x=100, y=25)
        hl = Label(topframe, text="fgcolor", bg="#2B2B2B", fg="white", font=("arial", 10, "bold"))
        hl.place(x=100, y=60)
        fgp = Entry(topframe, border=0, bg="#817D7D", fg="white", width=5, font=("arial", 15, "bold"),
                    textvariable=self.fg_var)
        fgp.place(x=100, y=83)

        hl = Label(topframe, text="bg color", bg="#2B2B2B", fg="white", font=("arial", 10, "bold"))
        hl.place(x=180, y=2)
        bgp = Entry(topframe, border=0, bg="#817D7D", fg="white", width=5, font=("arial", 15, "bold"),
                    textvariable=self.bg_var)
        bgp.place(x=180, y=25)
        hl = Label(topframe, text="font size", bg="#2B2B2B", fg="white", font=("arial", 10, "bold"))
        hl.place(x=180, y=60)
        fsp = Entry(topframe, border=0, bg="#817D7D", fg="white", width=5, font=("arial", 15, "bold"),
                    textvariable=self.fontsize_var)
        fsp.place(x=180, y=83)

        hl = Label(topframe, text="weight", bg="#2B2B2B", fg="white", font=("arial", 10, "bold"))
        hl.place(x=260, y=2)
        weightp = Entry(topframe)
        weightp.configure(border=0, bg="#817D7D", fg="white", width=5, font=("arial", 15, "bold"),
                          textvariable=self.weight_var)
        weightp.place(x=260, y=25)
        hl = Label(topframe, text="border", bg="#2B2B2B", fg="white", font=("arial", 10, "bold"))
        hl.place(x=260, y=60)
        bordp = Entry(topframe, border=0, bg="#817D7D", fg="white", width=5, font=("arial", 15, "bold"),
                      textvariable=self.border_var)
        bordp.place(x=260, y=83)

        hl = Label(topframe, text="positionX", bg="#2B2B2B", fg="white", font=("arial", 10, "bold"))
        hl.place(x=340, y=2)
        posxp = Entry(topframe, text="image")
        posxp.configure(border=0, bg="#817D7D", fg="white", width=5, font=("arial", 15, "bold"),
                        textvariable=self.posx_var)
        posxp.place(x=340, y=25)
        bxd = Button(topframe, text="-", command=self.posxdec)
        bxd.configure(border=0, bg="#6D6B6B", fg="white", height=1, width=2, font=("arial", 11, "bold"))
        bxd.place(x=400, y=24)
        bxd.bind("<Left>", lambda event=None: bxd.invoke())

        bxi = Button(topframe, text="+", command=self.posxinc)
        bxi.configure(border=0, bg="#6D6B6B", fg="white", height=1, width=2, font=("arial", 11, "bold"))
        bxi.place(x=428, y=24)
        bxi.bind("<Right>", lambda event=None: bxi.invoke())

        hl = Label(topframe, text="positionY", bg="#2B2B2B", fg="white", font=("arial", 10, "bold"))
        hl.place(x=340, y=60)
        posyp = Entry(topframe, border=0, bg="#817D7D", fg="white", width=5, font=("arial", 15, "bold"),
                      textvariable=self.posy_var)
        posyp.place(x=340, y=83)

        byd = Button(topframe, text="-", command=self.posydec)
        byd.configure(border=0, bg="#6D6B6B", fg="white", height=1, width=2, font=("arial", 11, "bold"))
        byd.place(x=400, y=82)
        byd.bind("<Down>", lambda event=None: byd.invoke())

        byi = Button(topframe, text="+", command=self.posyinc)
        byi.configure(border=0, bg="#6D6B6B", fg="white", height=1, width=2, font=("arial", 11, "bold"))
        byi.place(x=428, y=82)
        byi.bind("<Up>", lambda event=None: byi.invoke())
        topframe.place(x=240, y=0)

        hl = Label(topframe, text="fonts", bg="#2B2B2B", fg="white", font=("arial", 10, "bold"))
        hl.place(x=473, y=2)
        opmp = Entry(topframe)
        opmp.configure(border=0, bg="#817D7D", fg="white", width=5, font=("arial", 15, "bold"),
                       textvariable=self.font_var)
        opmp.place(x=473, y=24)

        for bevent in (hp, wp, txtp, fgp, bgp, fsp, weightp, bordp, posxp, posyp, opmp):
            bevent.bind('<Return>', lambda event=None: done.invoke())

        done = Button(topframe, text="Done")
        done.configure(border=0, bg="#3891EB", fg="#FBFBFB", width=15, height=2, font=("arial", 10, "bold"),
                       command=lambda: self.widgetproperty(hp.get(), wp.get(), txtp.get(), fgp.get(), bgp.get(),
                                                           fsp.get(), weightp.get(), bordp.get(), posxp.get(),
                                                           posyp.get(), opmp.get(), self.activetype))
        done.place(x=800, y=15)

        h = Button(topframe, text="Delete")
        h.configure(border=0, bg="#D94444", fg="#FBFBFB", width=15, height=2, font=("arial", 10, "bold"),
                    command=self.removewidget)
        h.place(x=800, y=65)

        myfont = Font(family="Segoe UI", size=16)
        font1 = Font(family="Segoe UI", size=28, weight="bold")
        lframe = Frame(frame, bg="black", width=252)

        txt = Label(lframe, text="Background", fg="white", bg="black", font=font1)
        txt.pack(pady=(10, 0))
        bgcolor = Entry(lframe, border=0, textvariable=self.color_var, fg="white", bg="#232323")
        bgcolor.pack(pady=(5, 0), ipadx=(35), ipady=(10))
        txt = Label(lframe, text="COLOR", fg="white", bg="black", font=myfont)
        txt.pack()
        hght = Entry(lframe, border=0, fg="white", bg="#232323", textvariable=self.height_var)
        hght.configure(width=15)
        hght.place(x=27, y=150, height=30)
        txt = Label(lframe, text="HEIGHT", fg="#707070", bg="black", font=("arial", 8, "bold"))
        txt.place(x=50, y=190)
        wdth = Entry(lframe, border=0, fg="white", bg="#232323", textvariable=self.width_var)
        wdth.configure(width=15)
        wdth.place(x=125, y=150, height=30)
        txt = Label(lframe, text="WIDTH", fg="#707070", bg="black", font=("arial", 8, "bold"))
        txt.place(x=150, y=190)
        aplybtn = Button(lframe, text="Apply", border=0, fg="white", bg="#F98500", font=("arial", 15, "bold"),
                         command=lambda: self.canvassetting(bgcolor, hght, wdth))
        aplybtn.pack(pady=(87, 10), ipadx=(70), ipady=(5))

        for bevent in (bgcolor, hght, wdth):
            bevent.bind('<Return>', lambda event=None: aplybtn.invoke())

        btn = Button(lframe, text="Button", bg="#484848", fg="#707070", border=0, font=myfont,
                     command=lambda: self.button("Button", "black", "grey", int(self.width / 2), int(self.height / 2),
                                                 15, "arial", "normal", 1, 40, 90))
        btn.configure(width=20, height=1)
        btn.pack(pady=(1))
        btn = Button(lframe, text="Label", bg="#484848", fg="#707070", border=0, font=myfont,
                     command=lambda: self.text("New Text", "black", "white", int(self.width / 2), int(self.height / 2),
                                               15, "arial", "normal", 20, 100))
        btn.configure(width=20, height=1)
        btn.pack(pady=(1))
        btn = Button(lframe, text="Entry", bg="#484848", fg="#707070", border=0, font=myfont,
                     command=lambda: self.entry("", "black", "grey", int(self.width / 2), int(self.height / 2), 15,
                                                "arial", "normal", 1, 40, 90))
        btn.configure(width=20, height=1)
        btn.pack(pady=(1))
        btn = Button(lframe, text="Rectangle", bg="#484848", fg="#707070", border=0, font=myfont,
                     command=lambda: self.rectangle("", "black", "red", int(self.width / 2), int(self.height / 2), 15,
                                                    "arial", "normal", 1, 40, 90))
        btn.configure(width=20, height=1)
        btn.pack(pady=(1))
        btn = Button(lframe, text="Image", bg="#484848", fg="#707070", border=0, font=myfont,
                     command=lambda: self.image("empty__img__", "black", "white", int(self.width / 2),
                                                int(self.height / 2), 15, "arial", "normal", 1, 100, 100))
        btn.configure(width=20, height=1)
        btn.pack(pady=(1))
        btn = Button(lframe, text="Checkbox", bg="#484848", fg="#707070", border=0, font=myfont,
                     command=lambda: self.checkbox("New check", "black", "grey", int(self.width / 2),
                                                   int(self.height / 2), 15,
                                                   "arial", "normal", 1, 0, 0))
        btn.configure(width=20, height=1)
        btn.pack(pady=(1))

        btn = Button(lframe, text="Option", bg="#484848", fg="#707070", border=0, font=myfont,
                     command=lambda: self.option("New Option", "black", "grey", int(self.width / 2),
                                                 int(self.height / 2), 15,
                                                 "arial", "normal", 1, 35, 60))
        btn.configure(width=20, height=1)
        btn.pack(pady=(1))

        btn = Button(lframe, text="Radio", bg="#484848", fg="#707070", border=0, font=myfont,
                     command=lambda: self.radio("New check", "black", "grey", int(self.width / 2), int(self.height / 2),
                                                15,
                                                "arial", "normal", 1, 35, 150))
        btn.configure(width=20, height=1)
        btn.pack(pady=(1))
        btn = Button(lframe, text="Slider", bg="#484848", fg="#707070", border=0, font=myfont,
                     command=lambda: self.slider("", "black", "grey", int(self.width / 2), int(self.height / 2), 15,
                                                 "arial", "normal", 1, 14, 150))
        btn.configure(width=20, height=1)
        btn.pack(pady=(1))
        btn = Button(lframe, text="BUILD", bg="#32BD86", fg="white", border=0, font=myfont,
                     command=lambda: build(self.folder, self.width, self.height))
        btn.configure(width=20, height=1)
        btn.pack(pady=(1))
        lframe.pack(side=LEFT, fill=Y)

        mainfholder = Frame(frame, bg="#303030", height=677, width=954)
        self.rframe = Frame(mainfholder, highlightthickness=0, bg=self.canvascolor, height=self.height,
                            width=self.width)
        self.rframe.place(x=10, y=10)
        self.rframe.bind("<Button-1>", self.fr_start)
        self.rframe.bind("<B1-Motion>", self.fr_motion)

        mainfholder.place(x=246, y=123)

    ############################################################################

    def fr_start(self, event):
        print("Start")
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def fr_motion(self, event):
        widget = event.widget
        x = widget.winfo_x() - widget._drag_start_x + event.x
        y = widget.winfo_y() - widget._drag_start_y + event.y
        widget.place(x=x, y=y)

    ##################################################

    def widgetposition(self, x, y):
        try:
            data = open("data/{}/temp.json".format(self.folder), "a")
            tmp = open("data/{}/main.json".format(self.folder), "r")
            tmpd = json.load(tmp)
            title = self.widtotitle()
            tmpd[title]["x"] = int(x)
            tmpd[title]["y"] = int(y)
            tmpd = json.dumps(tmpd, indent=4)
            data.write(tmpd)
            tmp.close()
            data.close()
            os.remove("data/{}/main.json".format(self.folder))
            os.rename("data/{}/temp.json".format(self.folder), "data/{}/main.json".format(self.folder))
        except Exception as e:
            showerror("Error", str(e) + "\t Remove Widget")

    def posxinc(self):
        inc = self.posx_var.get()
        inc += 1
        self.posx_var.set(inc)
        self.activewidget.place(x=inc, y=self.posy_var.get())
        self.widgetposition(inc, self.posy_var.get())

    def posxdec(self):
        dec = self.posx_var.get()
        dec -= 1
        self.posx_var.set(dec)
        self.activewidget.place(x=dec, y=self.posy_var.get())
        self.widgetposition(dec, self.posy_var.get())

    def posyinc(self):
        inc = self.posy_var.get()
        inc += 1
        self.posy_var.set(inc)
        self.activewidget.place(x=self.posx_var.get(), y=inc)
        self.widgetposition(self.posx_var.get(), inc)

    def posydec(self):
        dec = self.posy_var.get()
        dec -= 1
        self.posy_var.set(dec)
        self.activewidget.place(x=self.posx_var.get(), y=dec)
        self.widgetposition(self.posx_var.get(), dec)

    def widgetproperty(self, hp, wp, txtp, fgp, bgp, fsp, weightp, bordp, posxp, posyp, opmp, type):
        try:
            print(str(self.activewidget).split(".")[-1])
            ac = str(self.activewidget).split(".")[-1]

            if type == "Label":
                newfont = Font(family=opmp, size=int(fsp), weight=weightp)
                self.activewidget.configure(text=txtp, fg=fgp, bg=bgp, font=newfont)
                self.activewidget.place(x=posxp, y=posyp, height=hp, width=wp)
                data = open("data/{}/temp.json".format(self.folder), "a")
                tmp = open("data/{}/main.json".format(self.folder), "r")
                tmpd = json.load(tmp)

                if self.memorywidget != "":
                    tmpd[self.widtotitle()] = tmpd.pop(self.memorywidget)

                title = self.widtotitle()
                widg = {title: {
                    "type": "Label",
                    "height": int(hp),
                    "width": int(wp),
                    "border": int(bordp),
                    "text": txtp,
                    "fg": fgp,
                    "bg": bgp,
                    "fontsize": int(fsp),
                    "font": opmp,
                    "weight": weightp,
                    "x": posxp,
                    "y": posyp
                }}
                tmpd.update(widg)
                tmpd = json.dumps(tmpd, indent=4)
                data.write(tmpd)
                tmp.close()
                data.close()
                os.remove("data/{}/main.json".format(self.folder))
                os.rename("data/{}/temp.json".format(self.folder), "data/{}/main.json".format(self.folder))

            elif type == "Button":

                newfont = Font(family=opmp, size=int(fsp), weight=weightp)
                self.activewidget.configure(text=txtp, fg=fgp, bg=bgp, font=newfont, border=bordp)
                self.activewidget.place(x=posxp, y=posyp, height=hp, width=wp)
                data = open("data/{}/temp.json".format(self.folder), "a")
                tmp = open("data/{}/main.json".format(self.folder), "r")
                tmpd = json.load(tmp)
                if self.memorywidget != "":
                    tmpd[self.widtotitle()] = tmpd.pop(self.memorywidget)
                title = self.widtotitle()
                widg = {title: {
                    "type": "Button",
                    "height": int(hp),
                    "width": int(wp),
                    "border": int(bordp),
                    "text": txtp,
                    "fg": fgp,
                    "bg": bgp,
                    "fontsize": int(fsp),
                    "font": opmp,
                    "weight": weightp,
                    "x": posxp,
                    "y": posyp
                }}
                tmpd.update(widg)
                tmpd = json.dumps(tmpd, indent=4)
                data.write(tmpd)
                tmp.close()
                data.close()
                os.remove("data/{}/main.json".format(self.folder))
                os.rename("data/{}/temp.json".format(self.folder), "data/{}/main.json".format(self.folder))

            elif type == "Entry":

                newfont = Font(family=opmp, size=int(fsp), weight=weightp)
                self.activewidget.configure(fg=fgp, bg=bgp, font=newfont, border=bordp)
                self.activewidget.place(x=posxp, y=posyp, height=hp, width=wp)
                data = open("data/{}/temp.json".format(self.folder), "a")
                tmp = open("data/{}/main.json".format(self.folder), "r")
                tmpd = json.load(tmp)
                if self.memorywidget != "":
                    tmpd[self.widtotitle()] = tmpd.pop(self.memorywidget)
                title = self.widtotitle()
                widg = {title: {
                    "type": "Entry",
                    "height": int(hp),
                    "width": int(wp),
                    "border": int(bordp),
                    "text": txtp,
                    "fg": fgp,
                    "bg": bgp,
                    "fontsize": int(fsp),
                    "font": opmp,
                    "weight": weightp,
                    "x": posxp,
                    "y": posyp
                }}
                tmpd.update(widg)
                tmpd = json.dumps(tmpd, indent=4)
                data.write(tmpd)
                tmp.close()
                data.close()
                os.remove("data/{}/main.json".format(self.folder))
                os.rename("data/{}/temp.json".format(self.folder), "data/{}/main.json".format(self.folder))

            elif type == "Image":
                self.activewidget.place(x=posxp, y=posyp)
                img = self.img_src(txtp, [int(wp), int(hp)])
                self.activewidget.configure(image=img, highlightthickness=bordp, border=bordp, bg=bgp)
                self.activewidget.image = img

                data = open("data/{}/temp.json".format(self.folder), "a")
                tmp = open("data/{}/main.json".format(self.folder), "r")
                tmpd = json.load(tmp)

                if self.memorywidget != "":
                    tmpd[self.widtotitle()] = tmpd.pop(self.memorywidget)
                widg = {self.widtotitle(): {
                    "type": "Image",
                    "height": int(hp),
                    "width": int(wp),
                    "border": int(bordp),
                    "text": txtp,
                    "fg": fgp,
                    "bg": bgp,
                    "fontsize": int(fsp),
                    "font": opmp,
                    "weight": weightp,
                    "x": posxp,
                    "y": posyp
                }}
                tmpd.update(widg)
                tmpd = json.dumps(tmpd, indent=4)
                data.write(tmpd)
                tmp.close()
                data.close()
                os.remove("data/{}/main.json".format(self.folder))
                os.rename("data/{}/temp.json".format(self.folder), "data/{}/main.json".format(self.folder))

            elif type == "Rectangle":

                self.activewidget.configure(fg=fgp, bg=bgp)
                self.activewidget.place(x=posxp, y=posyp, height=hp, width=wp)
                data = open("data/{}/temp.json".format(self.folder), "a")
                tmp = open("data/{}/main.json".format(self.folder), "r")
                tmpd = json.load(tmp)

                if self.memorywidget != "":
                    tmpd[self.widtotitle()] = tmpd.pop(self.memorywidget)

                title = self.widtotitle()
                widg = {title: {
                    "type": "Rectangle",
                    "height": int(hp),
                    "width": int(wp),
                    "border": int(bordp),
                    "text": txtp,
                    "fg": fgp,
                    "bg": bgp,
                    "fontsize": int(fsp),
                    "font": opmp,
                    "weight": weightp,
                    "x": posxp,
                    "y": posyp
                }}
                tmpd.update(widg)
                tmpd = json.dumps(tmpd, indent=4)
                data.write(tmpd)
                tmp.close()
                data.close()
                os.remove("data/{}/main.json".format(self.folder))
                os.rename("data/{}/temp.json".format(self.folder), "data/{}/main.json".format(self.folder))

            elif type == "Checkbox":
                newfont = Font(family=opmp, size=fsp, weight=weightp)
                self.activewidget.configure(fg=fgp, bg=bgp, text=txtp, border=bordp, height=hp, width=wp, font=newfont)
                self.activewidget.place(x=posxp, y=posyp)
                data = open("data/{}/temp.json".format(self.folder), "a")
                tmp = open("data/{}/main.json".format(self.folder), "r")
                tmpd = json.load(tmp)

                if self.memorywidget != "":
                    tmpd[self.widtotitle()] = tmpd.pop(self.memorywidget)

                title = self.widtotitle()
                widg = {title: {
                    "type": "Checkbox",
                    "height": int(hp),
                    "width": int(wp),
                    "border": int(bordp),
                    "text": txtp,
                    "fg": fgp,
                    "bg": bgp,
                    "fontsize": int(fsp),
                    "font": opmp,
                    "weight": weightp,
                    "x": posxp,
                    "y": posyp
                }}
                tmpd.update(widg)
                tmpd = json.dumps(tmpd, indent=4)
                data.write(tmpd)
                tmp.close()
                data.close()
                os.remove("data/{}/main.json".format(self.folder))
                os.rename("data/{}/temp.json".format(self.folder), "data/{}/main.json".format(self.folder))

            elif type == "Optionmenu":
                newfont = Font(family=opmp, size=fsp, weight=weightp)
                self.activewidget.configure(fg=fgp, bg=bgp, text=txtp, border=bordp, font=newfont,
                                            highlightthickness=bordp)
                self.activewidget.place(x=posxp, y=posyp, height=hp, width=wp)
                data = open("data/{}/temp.json".format(self.folder), "a")
                tmp = open("data/{}/main.json".format(self.folder), "r")
                tmpd = json.load(tmp)

                if self.memorywidget != "":
                    tmpd[self.widtotitle()] = tmpd.pop(self.memorywidget)

                title = self.widtotitle()
                widg = {title: {
                    "type": "Optionmenu",
                    "height": int(hp),
                    "width": int(wp),
                    "border": int(bordp),
                    "text": txtp,
                    "fg": fgp,
                    "bg": bgp,
                    "fontsize": int(fsp),
                    "font": opmp,
                    "weight": weightp,
                    "x": posxp,
                    "y": posyp
                }}
                tmpd.update(widg)
                tmpd = json.dumps(tmpd, indent=4)
                data.write(tmpd)
                tmp.close()
                data.close()
                os.remove("data/{}/main.json".format(self.folder))
                os.rename("data/{}/temp.json".format(self.folder), "data/{}/main.json".format(self.folder))

            elif type == "Radio":
                newfont = Font(family=opmp, size=fsp, weight=weightp)
                self.activewidget.configure(fg=fgp, bg=bgp, text=txtp, border=bordp, font=newfont)
                self.activewidget.place(x=posxp, y=posyp, height=hp, width=wp)
                data = open("data/{}/temp.json".format(self.folder), "a")
                tmp = open("data/{}/main.json".format(self.folder), "r")
                tmpd = json.load(tmp)

                if self.memorywidget != "":
                    tmpd[self.widtotitle()] = tmpd.pop(self.memorywidget)

                title = self.widtotitle()
                widg = {title: {
                    "type": "Radio",
                    "height": int(hp),
                    "width": int(wp),
                    "border": int(bordp),
                    "text": txtp,
                    "fg": fgp,
                    "bg": bgp,
                    "fontsize": int(fsp),
                    "font": opmp,
                    "weight": weightp,
                    "x": posxp,
                    "y": posyp
                }}
                tmpd.update(widg)
                tmpd = json.dumps(tmpd, indent=4)
                data.write(tmpd)
                tmp.close()
                data.close()
                os.remove("data/{}/main.json".format(self.folder))
                os.rename("data/{}/temp.json".format(self.folder), "data/{}/main.json".format(self.folder))

            elif type == "Slider":
                newfont = Font(family=opmp, size=fsp, weight=weightp)
                self.activewidget.configure(troughcolor=fgp, bg=bgp, highlightthickness=bordp, border=bordp,
                                            font=newfont)
                self.activewidget.place(x=posxp, y=posyp, height=hp, width=wp)
                data = open("data/{}/temp.json".format(self.folder), "a")
                tmp = open("data/{}/main.json".format(self.folder), "r")
                tmpd = json.load(tmp)

                if self.memorywidget != "":
                    tmpd[self.widtotitle()] = tmpd.pop(self.memorywidget)

                title = self.widtotitle()
                widg = {title: {
                    "type": "Slider",
                    "height": int(hp),
                    "width": int(wp),
                    "border": int(bordp),
                    "text": txtp,
                    "fg": fgp,
                    "bg": bgp,
                    "fontsize": int(fsp),
                    "font": opmp,
                    "weight": weightp,
                    "x": posxp,
                    "y": posyp
                }}
                tmpd.update(widg)
                tmpd = json.dumps(tmpd, indent=4)
                data.write(tmpd)
                tmp.close()
                data.close()
                os.remove("data/{}/main.json".format(self.folder))
                os.rename("data/{}/temp.json".format(self.folder), "data/{}/main.json".format(self.folder))

        except Exception as e:
            showerror("Error", str(e) + "\t Widget Property")

    def widtotitle(self):
        try:
            title = "."
            for i in str(self.activewidget).split("!")[2:]:
                title += "!" + i
            return title
        except Exception as e:
            showerror("Error", str(e) + "\t Widget to Title")

    def removewidget(self):
        try:
            data = open("data/{}/temp.json".format(self.folder), "a")
            tmp = open("data/{}/main.json".format(self.folder), "r")
            tmpd = json.load(tmp)

            tmpd.pop(self.widtotitle())
            tmpd = json.dumps(tmpd, indent=4)
            data.write(tmpd)
            tmp.close()
            data.close()
            os.remove("data/{}/main.json".format(self.folder))
            os.rename("data/{}/temp.json".format(self.folder), "data/{}/main.json".format(self.folder))
            self.activewidget.destroy()
            self.fillpropertyclear()
        except Exception as e:
            showerror("Error", str(e) + "\t Remove Widget")

    def fillproperty(self):
        try:
            tmp = open("data/{}/main.json".format(self.folder), "r")
            tmpd = json.load(tmp)
            title = self.widtotitle()
            self.txtvar.set(tmpd[title]["text"])
            self.widheight_var.set(tmpd[title]["height"])
            self.widwidth_var.set(tmpd[title]["width"])
            self.fg_var.set(tmpd[title]["fg"])
            self.bg_var.set(tmpd[title]["bg"])
            self.fontsize_var.set(tmpd[title]["fontsize"])
            self.weight_var.set(tmpd[title]["weight"])
            self.border_var.set(tmpd[title]["border"])
            self.posx_var.set(tmpd[title]["x"])
            self.posy_var.set(tmpd[title]["y"])
            self.font_var.set(tmpd[title]["font"])
            tmp.close()
        except Exception as e:
            showerror("Error", str(e) + "\t Fill Property")

    def fillpropertyclear(self):
        try:
            self.txtvar.set("")
            self.widheight_var.set("")
            self.widwidth_var.set("")
            self.fg_var.set("")
            self.bg_var.set("")
            self.fontsize_var.set("")
            self.weight_var.set("")
            self.border_var.set("")
            self.posx_var.set("")
            self.posy_var.set("")
            self.font_var.set("")
        except Exception as e:
            showerror("Error", str(e) + "\t Clear Property")

    def canvassetting(self, color, height, width):
        try:
            self.rframe.configure(bg="{}".format(color.get()), height=height.get(), width=width.get())
            self.canvascolor = color.get()
            self.height = int(height.get())
            self.width = int(width.get())
            data = open("data/{}/temp.json".format(self.folder), "w")
            tmp = open("data/{}/main.json".format(self.folder), "r")
            tmpd = json.load(tmp)
            tmpd["canvas"]["color"] = color.get()
            tmpd["canvas"]["height"] = int(height.get())
            tmpd["canvas"]["width"] = int(width.get())
            tmpd = json.dumps(tmpd, indent=4)
            data.write(tmpd)
            tmp.close()
            data.close()
            os.remove("data/{}/main.json".format(self.folder))
            os.rename("data/{}/temp.json".format(self.folder), "data/{}/main.json".format(self.folder))


        except Exception as e:
            showerror("Error", str(e) + "\t Background Setting")

    def widtotype(self):
        try:
            tmp = open("data/{}/main.json".format(self.folder), "r")
            tmpd = json.load(tmp)
            typeo = tmpd[self.widtotitle()]["type"]
            tmp.close()
            return typeo
        except Exception as e:
            showerror("Error", str(e) + "\t Widget to Type")

    ############################################################################

    def on_drag_start(self, event):
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def on_drag_motion(self, event):
        widget = event.widget
        x = widget.winfo_x() - widget._drag_start_x + event.x
        y = widget.winfo_y() - widget._drag_start_y + event.y
        widget.place(x=x, y=y)

    def on_drag_release(self, event):
        self.widgetposition(event.widget.winfo_x(), event.widget.winfo_y())
        self.fillproperty()

    ##################################################

    def combfunction(self, e):
        self.on_drag_start(e)
        self.getwidget(e)

    def getwidget(self, e):
        try:

            self.activewidget = e.widget
            self.activetype = self.widtotype()
            self.fillproperty()
        except Exception as e:
            showerror("Error", str(e) + "\t Get Widget")

    def img_src(self, src, imgsize):
        try:
            openimg = ImageTk.Image.open(src)
            w, h = openimg.size
            if sum(imgsize) > 1:
                openimg = openimg.resize(imgsize, Image.CUBIC)
            timg = ImageTk.PhotoImage(openimg)
            return timg
        except Exception as e:
            showerror("Error", str(e) + "\t Src to Image")

    def previouswidget(self, e, txtv, fgv, bgv, xv, yv, fons, fon, wei, bord, hei, wid, type):
        try:

            if type == "Label":
                self.activetype = type
                self.text(txtv, fgv, bgv, xv, yv, fons, fon, wei, hei, wid)
            elif type == "Button":
                self.activetype = type
                self.button(txtv, fgv, bgv, xv, yv, fons, fon, wei, bord, hei, wid)
            elif type == "Entry":
                self.activetype = type
                self.entry(txtv, fgv, bgv, xv, yv, fons, fon, wei, bord, hei, wid)
            elif type == "Image":
                self.activetype = type
                self.image(txtv, fgv, bgv, xv, yv, fons, fon, wei, bord, hei, wid)
            elif type == "Rectangle":
                self.activetype = type
                self.rectangle(txtv, fgv, bgv, xv, yv, fons, fon, wei, bord, hei, wid)
            elif type == "Checkbox":
                self.activetype = type
                self.checkbox(txtv, fgv, bgv, xv, yv, fons, fon, wei, bord, hei, wid)
            elif type == "Optionmenu":
                self.activetype = type
                self.option(txtv, fgv, bgv, xv, yv, fons, fon, wei, bord, hei, wid)
            elif type == "Radio":
                self.activetype = type
                self.radio(txtv, fgv, bgv, xv, yv, fons, fon, wei, bord, hei, wid)
            elif type == "Slider":
                self.activetype = type
                self.slider(txtv, fgv, bgv, xv, yv, fons, fon, wei, bord, hei, wid)
        except Exception as e:
            showerror("Error", str(e) + "\t Previous Widget")

    #######################################  Widget #######################################

    def button(self, txtv, fgv, bgv, xv, yv, fons, fon, wei, bord, height, width):
        try:
            newfont = Font(family=fon, size=fons, weight=wei)
            lbl = Button(self.rframe,
                         text=txtv, fg=fgv, bg=bgv, font=newfont)
            lbl.configure(border=bord)
            lbl.place(x=xv, y=yv, height=height, width=width)
            lbl.bind('<Button-1>', self.combfunction)
            lbl.bind("<B1-Motion>", self.on_drag_motion)
            lbl.bind("<ButtonRelease-1>", self.on_drag_release)
            self.activewidget = lbl
            self.widgetproperty(height, width, txtv, fgv, bgv, fons, wei, bord, xv, yv, fon, "Button")
            self.fillproperty()
        except Exception as e:
            showerror("Error", str(e) + "\t Button")

    def text(self, txtv, fgv, bgv, xv, yv, fons, fon, wei, hv, wv):
        try:
            newfont = Font(family=fon, size=fons, weight=wei)
            lbl = Label(self.rframe,
                        text=txtv, fg=fgv, bg=bgv, font=newfont)

            lbl.place(x=xv, y=yv, height=hv, width=wv)
            lbl.bind('<Button-1>', self.combfunction)
            lbl.bind("<B1-Motion>", self.on_drag_motion)
            lbl.bind("<ButtonRelease-1>", self.on_drag_release)
            self.activewidget = lbl

            self.widgetproperty(hv, wv, txtv, fgv, bgv, fons, wei, 0, xv, yv, fon, "Label")
            self.fillproperty()
        except Exception as e:
            showerror("Error", str(e) + "\t Label")

    def entry(self, txtv, fgv, bgv, xv, yv, fons, fon, wei, bord, height, width):
        try:
            newfont = Font(family=fon, size=fons, weight=wei)
            lbl = Entry(self.rframe, fg=fgv, bg=bgv, font=newfont)
            lbl.configure(border=bord)
            lbl.place(x=xv, y=yv, height=height, width=width)
            lbl.bind('<Button-1>', self.combfunction)
            lbl.bind("<B1-Motion>", self.on_drag_motion)
            lbl.bind("<ButtonRelease-1>", self.on_drag_release)
            self.activewidget = lbl

            self.widgetproperty(height, width, txtv, fgv, bgv, fons, wei, bord, xv, yv, fon, "Entry")
            self.fillproperty()
        except Exception as e:
            showerror("Error", str(e) + "\t Entry")

    def image(self, txtv, fgv, bgv, xv, yv, fons, fon, wei, bord, height, width):
        try:
            if txtv == "empty__img__":
                imag = askopenfilename()
            else:
                imag = txtv
            if imag != "":
                txtv = imag

                img = self.img_src(txtv, [width, height])
                lbl = Label(self.rframe, image=img, bg=bgv)
                lbl.image = img
                lbl.place(x=xv, y=yv)
                lbl.bind('<Button-1>', self.combfunction)
                lbl.bind("<B1-Motion>", self.on_drag_motion)
                lbl.bind("<ButtonRelease-1>", self.on_drag_release)
                self.activewidget = lbl

                self.widgetproperty(height, width, txtv, fgv, bgv, fons, wei, bord, xv, yv, fon, "Image")
                self.fillproperty()
        except Exception as e:
            showerror("Error", str(e) + "\t Image")

    def rectangle(self, txtv, fgv, bgv, xv, yv, fons, fon, wei, bord, height, width):
        try:
            lbl = Label(self.rframe, fg=fgv, bg=bgv)

            lbl.place(x=xv, y=yv, height=height, width=width)
            lbl.bind('<Button-1>', self.combfunction)
            lbl.bind("<B1-Motion>", self.on_drag_motion)
            lbl.bind("<ButtonRelease-1>", self.on_drag_release)
            self.activewidget = lbl

            self.widgetproperty(height, width, txtv, fgv, bgv, fons, wei, bord, xv, yv, fon, "Rectangle")
            self.fillproperty()

        except Exception as e:
            showerror("Error", str(e) + "\t Rectangle")

    def checkbox(self, txtv, fgv, bgv, xv, yv, fons, fon, wei, bord, height, width):
        try:
            newfont = Font(family=fon, size=fons, weight=wei)
            lbl = Checkbutton(self.rframe, fg=fgv, bg=bgv, onvalue=1, offvalue=0, height=height, width=width,
                              font=newfont)
            lbl.place(x=xv, y=yv)
            lbl.bind('<Button-1>', self.combfunction)
            lbl.bind("<B1-Motion>", self.on_drag_motion)
            lbl.bind("<ButtonRelease-1>", self.on_drag_release)
            self.activewidget = lbl
            self.widgetproperty(height, width, txtv, fgv, bgv, fons, wei, bord, xv, yv, fon, "Checkbox")
            self.fillproperty()

        except Exception as e:
            showerror("Error", str(e) + "\t Checkbox")

    def option(self, txtv, fgv, bgv, xv, yv, fons, fon, wei, bord, height, width):
        try:
            newfont = Font(family=fon, size=fons, weight=wei)
            lbl = OptionMenu(self.rframe, StringVar(), txtv)
            lbl.configure(fg=fgv, bg=bgv, font=newfont, border=bord, highlightthickness=bord)
            lbl.place(x=xv, y=yv, height=height, width=width)
            lbl.bind('<Button-1>', self.combfunction)
            lbl.bind("<B1-Motion>", self.on_drag_motion)
            lbl.bind("<ButtonRelease-1>", self.on_drag_release)
            self.activewidget = lbl
            self.widgetproperty(height, width, txtv, fgv, bgv, fons, wei, bord, xv, yv, fon, "Optionmenu")
            self.fillproperty()

        except Exception as e:
            showerror("Error", str(e) + "\t Option")

    def radio(self, txtv, fgv, bgv, xv, yv, fons, fon, wei, bord, height, width):
        try:
            newfont = Font(family=fon, size=fons, weight=wei)
            lbl = Radiobutton(self.rframe, var=IntVar(), value=0, fg=fgv, bg=bgv, border=bord,
                              font=newfont)
            lbl.place(x=xv, y=yv, height=height, width=width)
            lbl.bind('<Button-1>', self.combfunction)
            lbl.bind("<B1-Motion>", self.on_drag_motion)
            lbl.bind("<ButtonRelease-1>", self.on_drag_release)
            self.activewidget = lbl
            self.widgetproperty(height, width, txtv, fgv, bgv, fons, wei, bord, xv, yv, fon, "Radio")
            self.fillproperty()

        except Exception as e:
            showerror("Error", str(e) + "\t Radio")

    def slider(self, txtv, fgv, bgv, xv, yv, fons, fon, wei, bord, height, width):
        try:
            newfont = Font(family=fon, size=fons, weight=wei)
            lbl = Scale(self.rframe, from_=0, to=100, tickinterval=1, showvalue=False, troughcolor=fgv, bg=bgv,
                        border=bord,
                        font=newfont, orient=HORIZONTAL, highlightthickness=bord, relief="ridge")
            lbl.place(x=xv, y=yv, height=height, width=width)
            lbl.bind('<Button-1>', self.combfunction)
            lbl.bind("<B1-Motion>", self.on_drag_motion)
            lbl.bind("<ButtonRelease-1>", self.on_drag_release)
            self.activewidget = lbl
            self.widgetproperty(height, width, txtv, fgv, bgv, fons, wei, bord, xv, yv, fon, "Slider")
            self.fillproperty()

        except Exception as e:
            showerror("Error", str(e) + "\t Slider")


root = Tk()
root.title("Dot Visual")
root.wm_resizable(height=False, width=False)
tempfr = ""
root.geometry("1200x800")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
expf = Frame(root, bg="#303030")
expf.grid(row=0, column=0, sticky="nsew")
if True:
    welcomef = Frame(root, bg="#303030")
    welcomef.grid(row=0, column=0, sticky="nsew")
    homef = Frame(root, bg="#303030")
    homef.grid(row=0, column=0, sticky="nsew")
    mainui = UI()
    mainui.welcomepage(welcomef)
    showframe(welcomef)

root.mainloop()
