"""
Copyright (c) 2026-2027 zhilin.tang@qq.com.
我把课表文件放到了我的网站上
这是联网加载的课程表
足够炒掉任何在黑板上每天写课表的人
"""
import requests as rq
import json
from tkinter import Tk, Canvas, Button, Toplevel
from time import localtime
from datetime import datetime, timedelta
import sys
from pathlib import Path

_HARD_CODE = """{
    
    "names": [
        "1",
        "2",
        "",
        "3",
        "4",
        "考",
        "6",
        "",
        "7",
        "8",
        "1",
        "2"
    ],
    "times": [
        [
            480,
            520
        ],
        [
            535,
            575
        ],
        [
            575,
            605
        ],
        [
            605,
            645
        ],
        [
            660,
            700
        ],
        [
            730,
            770
        ],
        [
            770,
            865
        ],
        [
            865,
            895
        ],
        [
            895,
            935
        ],
        [
            950,
            985
        ],
        [
            990,
            1045
        ],
        [
            1050,
            1110
        ]
    ]
}"""
holidays = json.loads(
    rq.get(
        f'https://publicapi.xiaoai.me/holiday/year?date={str(datetime.now().year)}'
    ).content
)

URL = 'https://qiihmzijbqinlnfnkhrg.supabase.co/storage/v1/object/public/schedule/class.json'
LOCAL = Path(__file__).parent / 'class.json'
try:
    with open(LOCAL, encoding='utf-8') as fp:
        FILE_IN = json.load(fp)
        data = FILE_IN['schedules']
        schedule = FILE_IN['times']
        names = FILE_IN['names']
        formats = FILE_IN['formats']
except FileNotFoundError:
    try:
        r = rq.get(URL)
        data = json.loads(r.content)
        with open(LOCAL, encoding='utf-8', mode='w') as fp:
            json.dump(data, fp, ensure_ascii=False, indent=4)
    except:
        with open(LOCAL, encoding='utf-8', mode='w') as fp:
            fp.write(_HARD_CODE)
    with open(LOCAL, encoding='utf-8') as fp:
        FILE_IN = json.load(fp)
        data = FILE_IN['schedules']
        schedule = FILE_IN['times']
        names = FILE_IN['names']
        formats = FILE_IN['formats']


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
ww = int(w_w / 16.7)
wh = w_h

zk = datetime(2027, 6, 21)
text_size = int(w_w / 50.2)

rect_h = 0.59  # * 2 * text_size

text_offset_y = 1.25
d = datetime

root.geometry(f'{ww}x{wh}+{w_w-ww}+0')
root.overrideredirect(True)
root.resizable(False, False)
root.grid_columnconfigure(0, weight=1)


c = Canvas(root, width=ww, height=wh - 200)
c.pack()
Button(root, text='关闭', command=root.quit).pack(fill='x')
texts = []


def get_now_min():
    a = localtime()
    return a.tm_hour * 60 + a.tm_min


def current_class():
    n = get_now_min()
    for i, (start, end) in enumerate(schedule):
        if start <= n < end:
            color = 'green'
        elif n >= end:
            color = 'gray'
        else:
            color = 'white'

        c.create_rectangle(
            0,
            (i * text_offset_y - rect_h) * text_size + 0.1 * wh,
            ww,
            (i * text_offset_y + rect_h) * text_size + 0.1 * wh,
            outline=color,
            fill=color,
        )
        c.update()

    display_class()
    root.after(10000, current_class)


def display_class():
    for i in texts:
        c.delete(i)
    y = 0.1 * wh
    wkd = datetime.now().weekday()
    for i, j in enumerate(data[wkd]):
        cls = names[i]
        clr = '#'+formats[i]['fg']
        cls += ' ' if cls else ''
        texts.append(
            c.create_text(
                ww//2, y, text=cls + j, fill=clr, font=f'Kaiti {text_size}'
            )
        )
        y += text_size * text_offset_y


def school_day(day: datetime) -> bool:
    if day.weekday() > 4:
        return False
    elif (d(2026, 7, 15) <= day <= d(2026, 8, 31)) or (
        d(2027, 1, 15) <= day <= d(2027, 2, 28)
    ):
        return False
    else:
        return True


def get_days_school():
    s = 0
    i = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
    while i <= zk:
        if school_day(i):
            s += 1
        i += timedelta(days=1)
    i = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
    for j in holidays['data']:
        if str(i)[:10] == j['date'] and i <= d(2027, 6, 21):
            s -= j['rest']
        i += timedelta(1)
    return s


t_ww = w_w - ww
t_wh = int(w_h / 43.2)

timeDown = Toplevel(root)
timeDown.geometry(f'{t_ww}x{t_wh}+0+0')
timeDown.overrideredirect(True)
timeDown.resizable(False, False)
t_c = Canvas(timeDown, width=t_ww, height=t_wh)
t_c.pack()
td_text1 = '距中考还有     天，在校     天'
days_all = (zk - datetime.now()).days
days_school = get_days_school()
td_text2 = f'        {days_all:03}          {days_school:03}'
t_c.create_text(
    t_ww / 2,
    0,
    text=td_text1,
    fill='black',
    anchor='n',
    font=f'Kaiti {text_size//2}',
)
t_c.create_text(
    t_ww / 2,
    0,
    text=td_text2,
    fill='red',
    anchor='n',
    font=f'Kaiti {text_size//2}',
)

current_class()
root.bind('<r>', lambda _: refresh())
root.mainloop()
