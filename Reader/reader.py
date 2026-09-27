import pandas as pd
import openpyxl
import json
from pathlib import Path
from tkinter import filedialog

SHEET = filedialog.askopenfilename(filetypes=[('Excel表格', 'xlsx')])
# print(SHEET)
OUTPUT = Path(__file__) / '..' / 'class.json'

BASE_MODE = HIGH_MODE = 0

_s = openpyxl.load_workbook(SHEET)
sheet_style = _s.active
sheet_data = pd.read_excel(SHEET, header=0)
CODE = str(sheet_data.iloc[2, 18])


def check_base(code): pass
def check_high(code): pass


WRITE = {
    "schedules": [],
    "names": [],
    "styles": {
        "formats": [],
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
            cl = None
            fill = sheet_style[f'N{x}'].fill  # type:ignore
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

            WRITE['formats'].append({'fg': cl if cl else '000000'})

        WRITE['before'] = sheet_data.iloc[]


with open(OUTPUT, 'w', encoding='utf-8') as fp:
    json.dump(WRITE, fp, ensure_ascii=False, indent=4)
