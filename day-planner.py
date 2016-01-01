# -*- coding: utf-8 -*-

__author__ = 'srebrny'
__copyright__ = u'Copyright (c) 2010 Tomasz Świderski'

import Image, ImageDraw, ImageFont
import sys

from decorators import BackgroundDecorator, JustifyTextDecorator

SEN = []
PRACA_I_OBIAD = []
FIRMA = []
FIRMA_ROZWOJ = []
DZHK = []
PRZYGOTOWANIE_RANO = []
PRZYGOTOWANIE_WIECZOR = []
SOO = []  # sprzątanie / obiad / odpoczynek

day1 = {
    "header": "Plan dnia - Normalny",
    "hours": [
        {"hour": "05", "text": "PRZYGOTOWANIE"},
        {"hour": "06", "text": "FIRMA"},
        {"hour": "07", "text": "FIRMA"},
        {"hour": "08", "text": "PRACA i Obiad"},
        {"hour": "09", "text": "PRACA i Obiad"},
        {"hour": "10", "text": "PRACA i Obiad"},
        {"hour": "11", "text": "PRACA i Obiad"},
        {"hour": "12", "text": "PRACA i Obiad"},
        {"hour": "13", "text": "PRACA i Obiad"},
        {"hour": "14", "text": "PRACA i Obiad"},
        {"hour": "15", "text": "PRACA i Obiad"},
        {"hour": "16", "text": "PRACA i Obiad"},
        {"hour": "17", "text": "PRACA i Obiad"},
        {"hour": "18", "text": "SPRZATANIE/OBIAD/ODPOCZYNEK"},
        {"hour": "19", "text": "DZHK"},
        {"hour": "20", "text": "FIRMA"},
        {"hour": "21", "text": "FIRMA"},
        {"hour": "22", "text": "PRZYGOTOWANIE"},
        {"hour": "23", "text": "SEN"},
        {"hour": "00", "text": "SEN"},
        {"hour": "01", "text": "SEN"},
        {"hour": "02", "text": "SEN"},
        {"hour": "03", "text": "SEN"},
        {"hour": "04", "text": "SEN"},
    ]
}

day2 = {
    "header": "Plan dnia - Soboty",
    "hours": [
        {"hour": "05", "text": "SEN"},
        {"hour": "06", "text": "SEN"},
        {"hour": "07", "text": "SEN"},
        {"hour": "08", "text": "SEN"},
        {"hour": "09", "text": "PRZYGOTOWANIE"},
        {"hour": "10", "text": "SPRZATANIE/OBIAD/ODPOCZYNEK"},
        {"hour": "11", "text": "FIRMA"},
        {"hour": "12", "text": "FIRMA"},
        {"hour": "13", "text": "FIRMA"},
        {"hour": "14", "text": "FIRMA"},
        {"hour": "15", "text": "FIRMA"},
        {"hour": "16", "text": "FIRMA"},
        {"hour": "17", "text": "SPRZATANIE/OBIAD/ODPOCZYNEK"},
        {"hour": "18", "text": "DZHK"},
        {"hour": "19", "text": "DZHK"},
        {"hour": "20", "text": "DZHK"},
        {"hour": "21", "text": "DZHK"},
        {"hour": "22", "text": "DZHK"},
        {"hour": "23", "text": "DZHK"},
        {"hour": "00", "text": "DZHK"},
        {"hour": "01", "text": "PRZYGOTOWANIE"},
        {"hour": "02", "text": "SEN"},
        {"hour": "03", "text": "SEN"},
        {"hour": "04", "text": "SEN"},
    ]
}

day3 = {
    "header": "Plan dnia - Święta",
    "hours": [
        {"hour": "05", "text": "SEN"},
        {"hour": "06", "text": "SEN"},
        {"hour": "07", "text": "SEN"},
        {"hour": "08", "text": "SEN"},
        {"hour": "09", "text": "PRZYGOTOWANIE"},
        {"hour": "10", "text": "SPRZATANIE/OBIAD/ODPOCZYNEK"},
        {"hour": "11", "text": "FIRMA - ROZWÓJ"},
        {"hour": "12", "text": "FIRMA - ROZWÓJ"},
        {"hour": "13", "text": "FIRMA - ROZWÓJ"},
        {"hour": "14", "text": "FIRMA - ROZWÓJ"},
        {"hour": "15", "text": "FIRMA - ROZWÓJ"},
        {"hour": "16", "text": "FIRMA - ROZWÓJ"},
        {"hour": "17", "text": "SPRZATANIE/OBIAD/ODPOCZYNEK"},
        {"hour": "18", "text": "DZHK"},
        {"hour": "19", "text": "DZHK"},
        {"hour": "20", "text": "DZHK"},
        {"hour": "21", "text": "DZHK"},
        {"hour": "22", "text": "DZHK"},
        {"hour": "23", "text": "DZHK"},
        {"hour": "00", "text": "DZHK"},
        {"hour": "01", "text": "PRZYGOTOWANIE"},
        {"hour": "02", "text": "SEN"},
        {"hour": "03", "text": "SEN"},
        {"hour": "04", "text": "SEN"},
    ]
}


class DayPlan(object):
    __hours = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 00, 01, 02, 03, 04]

    def __init__(self, filename="./day-plan-1.png"):
        self.filename = filename

        self.im = Image.new("RGB", (1000, 794), "black")
        self.draw = ImageDraw.Draw(self.im)
        # margins Left, upper, right, bottom
        self.marginsCols = {"size": 320}
        self.marginsHeader = {"left": 15, "top": 52, "right": 25, "bottom": 25}
        self.marginsRows = {"left": 25, "top": 52, "right": 25, "bottom": 25}
        self.padding_cols = 18

        #
        # Font Settings
        #
        self.HeaderFont = ImageFont.truetype("./fonts/NotoSans-BoldItalic.ttf", 20)
        self.TextFont = ImageFont.truetype("./fonts/NotoSans-Regular.ttf", 15)

        self.TextFontFill_hour = (255, 255, 255)
        self.TextFontFill_text = (255, 255, 255)

    def setData(self, *kargs):
        self.col_i = 0
        for day in kargs:
            HeaderPos = (
                self.marginsHeader["left"] + (self.marginsCols["size"] * self.col_i + 20 + self.marginsHeader["right"]),
                23)
            print("Marginesy dla kolumny %i " % self.col_i, HeaderPos)

            self.draw.text(HeaderPos,
                           day["header"].decode("utf-8"), font=self.HeaderFont,
                           fill=(240, 240, 0))
            self.row_i = 0
            for row in day["hours"]:
                RowNumPos = (
                    self.marginsRows["left"] + (self.marginsCols["size"] * self.col_i),
                    self.marginsRows["top"] + (self.row_i * 22)
                )

                RowTexPos = (
                    self.marginsRows["left"] + 30 + (self.marginsCols["size"] * self.col_i),
                    self.marginsRows["top"] + (self.row_i * 22)
                )

                self.draw_row(row["hour"], row["text"], background=(0, 0, 128),
                              RowNumPos=RowNumPos, RowTexPos=RowTexPos, justify=True)
                self.row_i += 1
                # break

            self.col_i += 1

    @BackgroundDecorator
    @JustifyTextDecorator
    def draw_row(self, hour, text, background=None, justify=None, RowNumPos=(0, 0), RowTexPos=(0, 0)):

        print("Marginesy dla kolumny %i Numer: %s, Text: %s  " % (self.col_i, RowNumPos, RowTexPos))

        self.draw.text(
            RowNumPos,
            hour.decode("utf-8"),
            font=self.TextFont,
            fill=self.TextFontFill_hour
        )

        self.draw.text(
            RowTexPos,
            text.decode("utf-8"),
            font=self.TextFont,
            fill=self.TextFontFill_text
        )

    def save(self):
        self.im.save(self.filename)


if __name__ == '__main__':
    dp = DayPlan()
    dp.setData(day1, day2, day3)
    dp.save()
