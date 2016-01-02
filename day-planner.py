# -*- coding: utf-8 -*-

__author__ = 'srebrny'
__copyright__ = u'Copyright (c) 2010 Tomasz Świderski'

import Image, ImageDraw, ImageFont, ImageColor
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

dc = {
    "PRZYGOTOWANIE": ImageColor.getrgb("#00ccff"),
    "FIRMA": ImageColor.getrgb("#6666fc"),
    "PRACA i Obiad": ImageColor.getrgb("#ff3299"),
    "SPRZATANIE/OBIAD/ODPOCZYNEK": ImageColor.getrgb("#013461"),
    "DZHK": ImageColor.getrgb("#ff9899"),
    "SEN": ImageColor.getrgb("#039d01"),
    "FIRMA - ROZWÓJ": ImageColor.getrgb("#6666fc"),

}

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
        self.marginsHeader = {"left": 20, "top": 25, "right": 25, "bottom": 25}
        self.marginsRows = {"left": 25, "top": 52, "right": 25, "bottom": 25}
        self.padding_cols = 18

        # FOR TRANSLATE COLORS
        self.colors = ImageColor

        self.header_bg_color = self.colors.getrgb("#3e35e8")

        #
        # Font Settings
        #
        self.HeaderFont = ImageFont.truetype("./fonts/NotoSans-BoldItalic.ttf", 20)
        self.TextFont = ImageFont.truetype("./fonts/NotoSans-Regular.ttf", 15)

        self.TextFontFill_hour = self.colors.getrgb("#fff")
        self.TextFontFill_text = self.colors.getrgb("#fff")

    def setData(self, *kargs):
        self.col_i = 0
        for day in kargs:

            column_x_pos = (self.marginsCols["size"] * self.col_i)

            HeaderBox = [
                (
                    self.marginsHeader["left"] + column_x_pos,
                    self.marginsHeader["top"]
                ),
                (
                    self.marginsHeader["left"] + column_x_pos + 300 + 5,
                    52
                )
            ]
            size_x, size_y = self.draw.textsize(day["header"].decode("utf-8"), font=self.HeaderFont)

            size_col_x = self.marginsHeader["left"] + column_x_pos + 300 + 5

            padding_size = column_x_pos + (size_col_x - column_x_pos - size_x) / 2

            HeaderPos = (
                self.marginsHeader["left"] + padding_size,
                23)

            # Border for hour coll
            self.draw.rectangle(HeaderBox, fill=self.colors.getrgb("#fff"), outline=(128, 128, 128))
            self.draw.text(HeaderPos,
                           day["header"].decode("utf-8"), font=self.HeaderFont,
                           fill=self.header_bg_color)

            self.row_i = 0
            for row in day["hours"]:
                RowNumPos = (
                    self.marginsRows["left"] + column_x_pos,
                    self.marginsRows["top"] + (self.row_i * 22)
                )

                RowTexPos = (
                    self.marginsRows["left"] + 30 + column_x_pos,
                    self.marginsRows["top"] + (self.row_i * 22)
                )

                self.draw_row(row["hour"], row["text"], background=dc.get(row["text"]),
                              RowNumPos=RowNumPos, RowTexPos=RowTexPos, justify=True)
                self.row_i += 1

            self.col_i += 1
            # break

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
