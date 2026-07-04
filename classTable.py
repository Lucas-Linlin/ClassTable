'''
Copyright (c) 2026 zhilin.tang@qq.com. All right reserved.
我把课表文件放到了我的网站上
这是联网加载的课程表
足够炒掉任何在黑板上每天写课表的人
'''
import requests as rq
import json
from tkinter import Tk, Canvas, Button, Frame
from time import localtime
from datetime import datetime, timedelta
import sys
from pathlib import Path


URL = 'https://qiihmzijbqinlnfnkhrg.supabase.co/storage/v1/object/public/schedule/class.json'
LOCAL = Path(__file__).parent / 'class.json'
with open(LOCAL, encoding='utf-8') as fp:
    FILE_IN = json.load(fp)
    data = FILE_IN['schedules']
    schedule = FILE_IN['times']

text_size = 75


def refresh():
    global data
    r = rq.get(URL)
    data = json.loads(r.content)
    with open(LOCAL, encoding='utf-8', mode='w') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)
    display_class()


root = Tk()

w_w = root.winfo_screenwidth()
w_h = root.winfo_screenheight()
ww = 200
wh = w_h

root.geometry(f'{ww}x{wh}+{w_w-ww}+0')
root.overrideredirect(True)
root.resizable(False, False)
root.grid_columnconfigure(0, weight=1)


c = Canvas(root, width=ww, height=wh-200)
c.pack()
Button(root, text="关闭", command=root.quit).pack(fill='x')
texts = []


def get_now_min():
    a = localtime()
    return a.tm_hour*60+a.tm_min


def current_class():
    n = get_now_min()
    print(n)
    for i, (start, end) in enumerate(schedule):
        if start <= n and n < end:
            color = 'green'
        elif n >= end:
            color = 'gray'
        else:
            color = 'white'

        c.create_rectangle(
            (ww-3*text_size)/2,
            (i*1.1-0.5)*text_size+0.1*wh,
            (ww+3*text_size)/2,
            (i*1.1+0.5)*text_size+0.1*wh,
            outline=color, fill=color
        )
        c.update()

    display_class()
    root.after(10000, current_class)


def display_class():
    for i in texts:
        c.delete(i)
    y = 0.1*wh
    wkd = datetime.now().weekday()
    for i, j in enumerate(data[wkd]):
        clr = 'black'
        if i > 8:
            cls = ' '
        elif i == 4:
            cls = ' '
            clr = 'red'
        elif i > 4:
            cls = str(i)
        else:
            cls = str(i+1)
        cls += ' '
        if i == 2 or i == 7:
            y += text_size*1.1
        texts.append(c.create_text(ww//2, y, text=cls + j,
                                   fill=clr, font=f"Kaiti {text_size}"))
        y += text_size*1.1


current_class()
display_class()
root.bind('<r>', lambda _: refresh())
root.mainloop()
