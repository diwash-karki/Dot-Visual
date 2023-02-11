import json
import os,shutil
from tkinter.messagebox import *


def build(folder, fwidth, fheight):
    print(os.getcwd())
    try:
        folders = os.listdir("output")
        if folder in folders:
            shutil.rmtree("output/" + folder)

        os.mkdir("output/" + folder)
        file = open("output/{}/main.py".format(folder), "w")
        with open("init/import.txt", "r") as df:
            lines = df.readlines()
            for n, line in enumerate(lines):
                if 'geometry' in line:
                    file.writelines(line.format(fwidth, fheight))
                elif 'title' in line:
                    file.writelines(line.format(folder))
                else:
                    file.writelines(line)
        df.close()
        file.close()

        widgetjson = open("data/" + folder + "/main.json", "r")
        file = open("output/{}/main.py".format(folder), "a")
        widgets = json.load(widgetjson)

        for n, widget in enumerate(widgets):
            if widget == "canvas":

                widgettext = "frame=Frame(root,bg='{}',height={},width={}).place(x=0,y=0)\n".format(
                    widgets[widget]["color"], widgets[widget]["height"], widgets[widget]["width"])

            else:

                widtitle = widgets[widget]
                wtype = widtitle["type"]
                text = widtitle["text"]
                fg = widtitle["fg"]
                bg = widtitle["bg"]
                font = widtitle["font"]
                fontsize = widtitle["fontsize"]
                weight = widtitle["weight"]
                x = widtitle["x"]
                y = widtitle["y"]
                height = widtitle["height"]
                width = widtitle["width"]
                border = widtitle["border"]

                if wtype == "Label":
                    widgettext = "Label(frame,text='{}',fg='{}',bg='{}',font=('{}',{},'{}')).place(x={},y={},height={},width={})\n".format(
                        text, fg, bg, font, fontsize, weight, x, y, height, width)

                elif wtype == "Button":
                    widgettext = "Button(frame,text='{}',fg='{}',bg='{}',border={},font=('{}',{},'{}')).place(x={},y={},height={},width={})\n".format(
                        text, fg, bg, border, font, fontsize, weight, x, y, height, width)

                elif wtype == "Entry":
                    widgettext = "Entry(frame,fg='{}',bg='{}',border={},font=('{}',{},'{}')).place(x={},y={},height={},width={})\n".format(
                        fg, bg, border, font, fontsize, weight, x, y, height, width)

                elif wtype == "Image":

                    if "img" not in os.listdir("output/" + folder):
                        os.mkdir("output/"+folder+"/img")
                    shutil.copy(text,"output/{}/img".format(folder))
                    widgettext = "src{} = img_src('{}',({},{}))\n".format(n, "img/"+text.split("/")[-1], width, height)
                    widgettext += "img{} = Label(frame,image=src{} ,bg='{}',border={},highlightthickness={})\n".format(
                        n, n, bg, border, border)
                    widgettext += "img{}.image = src{}\n".format(n, n)
                    widgettext += "img{}.place(x={},y={})\n".format(n, x, y)

                elif wtype == "Rectangle":
                    widgettext = "Label(frame,fg='{}',bg='{}').place(x={},y={},height={},width={})\n".format(
                        fg, bg, x, y, height, width)

                elif wtype == "Checkbox":
                    widgettext = "Checkbutton(frame,text='{}',fg='{}',bg='{}',onvalue=1,offvalue=0,border={},font=('{}',{},'{}'),height={},width={}).place(x={},y={})\n".format(
                        text, fg, bg, border, font, fontsize, weight, height, width, x, y)

                elif wtype == "Optionmenu":
                    widgettext = "om{} = OptionMenu(frame,StringVar(),'{}')\n".format(
                        n,text)
                    widgettext +="om{}.configure(fg='{}',bg='{}',border={},highlightthickness={},font=('{}',{},'{}'))\n".format(
                        n, fg, bg, border, border, font, fontsize, weight)
                    widgettext +="om{}.place(x={},y={},height={},width={})\n".format(n,x, y, height, width)

                elif wtype == "Radio":
                    widgettext = "Radiobutton(frame,text='{}',fg='{}',bg='{}',border={},font=('{}',{},'{}')).place(x={},y={},height={},width={})\n".format(
                        text, fg, bg, border, font, fontsize, weight, x, y, height, width)
                elif wtype == "Slider":
                    widgettext = "Scale(frame, from_=0, to=100,fg='{}',bg='{}', orient=HORIZONTAL,highlightthickness='{}',relief='ridge',tickinterval=1,showvalue=False, troughcolor='{}',border={},font=('{}',{},'{}')).place(x={},y={},height={},width={})\n".format(
                        fg, bg, border,fg,border, font, fontsize, weight, x, y, height, width)

            file.write(widgettext)
        file.write("\nroot.mainloop()")
        file.close()
        widgetjson.close()
        showinfo("Success","Build Successfully.")

    except Exception as e:

        showerror("Build failed",e)


