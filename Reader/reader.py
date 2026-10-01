import pandas as pd
import openpyxl
import json
from pathlib import Path
from tkinter import filedialog, messagebox as mb
import ntplib
from datetime import datetime
from time import time
from uuid import uuid5, UUID

KEYPATH = Path(__file__)/'..'/'myKey.key'
SHEET = filedialog.askopenfilename(filetypes=[('Excel表格', 'xlsx')])
# print(SHEET)
OUTPUT = Path(__file__) / '..' / 'class.json'

BASE_MODE = HIGH_MODE = 0
STYLES = 'styles'

_s = openpyxl.load_workbook(SHEET)
sheet_style = _s.active
sheet_data = pd.read_excel(SHEET, header=0)
CODE = str(sheet_data.iloc[2, 18])


def get_time_stamp():
    try:
        client = ntplib.NTPClient()
        response = client.request('time.windows.com', version=3, timeout=5)
        tmstamp = response.tx_time
    except:
        tmstamp = time()
    return tmstamp


def check_code(code: str):
    global HIGH_MODE, BASE_MODE
    with open(KEYPATH, encoding='utf-8')as keyfp:
        KEY = keyfp.read().upper()
    tmstmp = get_time_stamp()
    code = code.replace('-', '')
    # print(code)
    if len(code) != 25:
        mb.showerror('错误', '激活码不合法')
        return
    key = code[:8]
    mode = code[8]
    disabled = int(code[9:20])
    valid = code[20:]
    inited = code[:20]
    # print(key, mode, disabled, valid)
    if key != KEY[:8]:
        mb.showerror('错误', '激活码不合法')
        return
    if valid != str(uuid5(UUID(KEY), inited))[:5].upper():

        mb.showerror('错误', '激活码被篡改')
        return
    if tmstmp > disabled:
        mb.showerror('错误', '激活码已过期')
        return
    if mode == 'A':
        HIGH_MODE = BASE_MODE = 1
        scs = '高级版'
    elif mode == 'B':
        BASE_MODE = 1
        scs = '基础版'
    else:
        mb.showerror('错误', '激活码不合法')
        return
    mb.showinfo('成功', f'{scs}激活成功，有效期还剩{((disabled-tmstmp)/3600):.1f}小时')


WRITE = {
    "schedules": [],
    "names": [],
    "styles": {
        "formats": {},
        "before": 'white',
        "now": 'green',
        "after": 'gray'
    },
    "times": []
}


def intx(x, y):
    value = sheet_data.iloc[x, y]
    if pd.isna(value):
        return 0
    try:
        return int(float(str(value).strip()))
    except (ValueError, TypeError):
        return 0


code = str(sheet_data.iloc[0, 18])
check_code(code)


def get_fill_color(name, none='000000'):
    cl = None
    fill = sheet_style[name].fill  # type:ignore
    if fill.fill_type != 'solid':
        cl = None
        print(0)
    else:
        fg = fill.fgColor
        if not fg:
            cl = None
        elif isinstance(fg.rgb, str):
            cl = fg.rgb[2:]
        elif fg.type == 'theme':
            cl = {
                0: 'E0E0E0',
                1: '000000',
                2: 'DBDADA',
                3: '4B5C74',
                4: '4B7DD5',
                5: 'FF8937',
                6: 'B4B4B4',
                7: 'FFD001',
                8: '64A9E7',
                9: '7BBC4E',
            }[fg.theme]
    return cl if cl else none


if BASE_MODE:

    j = 2
    for x in sheet_data.iloc[2:, 0]:
        WRITE['names'].append(str(x) if pd.notna(x) else '')
        j += 1

    for k in range(2, j):
        t0 = intx(k, 1)*60+intx(k, 2)
        t1 = intx(k, 3)*60+intx(k, 4)
        WRITE['times'].append([t0, t1])

    for x in range(7):
        WRITE['schedules'].append(
            [str(i) if pd.notna(i) else '' for i in sheet_data.iloc[2:, 5+x]])

    if HIGH_MODE:

        for x in range(4, j+1):
            WRITE[STYLES]['formats'][x-4] = get_fill_color(f'N{x}')

        WRITE[STYLES]['before'] = get_fill_color('O4', 'F2F2F2')
        WRITE[STYLES]['now'] = get_fill_color('P4', '008000')
        WRITE[STYLES]['after'] = get_fill_color('Q4', '757171')


with open(OUTPUT, 'w', encoding='utf-8') as fp:
    json.dump(WRITE, fp, ensure_ascii=False, indent=4)
