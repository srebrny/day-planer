# -*- coding: utf-8 -*-

__author__ = 'srebrny'
__copyright__ = u'Copyright (c) 2010 Tomasz Świderski'

import Image, ImageDraw, ImageFont
import sys

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
    "hours": {
        5: "PRZYGOTOWANIE",
        6: "FIRMA",
        7: "FIRMA",
        8: "PRACA i Obiad",
        9: "PRACA i Obiad",
        10: "PRACA i Obiad",
        11: "PRACA i Obiad",
        12: "PRACA i Obiad",
        13: "PRACA i Obiad",
        14: "PRACA i Obiad",
        15: "PRACA i Obiad",
        16: "PRACA i Obiad",
        17: "PRACA i Obiad",
        18: "SPRZATANIE/OBIAD/ODPOCZYNEK",
        19: "DZHK",
        20: "FIRMA",
        21: "FIRMA",
        22: "PRZYGOTOWANIE",
        23: "SEN",
        00: "SEN",
        01: "SEN",
        02: "SEN",
        03: "SEN",
        04: "SEN",
    }
}

day2 = {
    "header": "Plan dnia - Soboty",
    "hours": {
        5: "SEN",
        6: "SEN",
        7: "SEN",
        8: "SEN",
        9: "PRZYGOTOWANIE",
        10: "SPRZATANIE/OBIAD/ODPOCZYNEK",
        11: "PRACA i Obiad",
        12: "PRACA i Obiad",
        13: "PRACA i Obiad",
        14: "PRACA i Obiad",
        15: "PRACA i Obiad",
        16: "PRACA i Obiad",
        17: "SPRZATANIE/OBIAD/ODPOCZYNEK",
        18: "DZHK",
        19: "DZHK",
        20: "DZHK",
        21: "DZHK",
        22: "DZHK",
        23: "DZHK",
        00: "DZHK",
        01: "PRZYGOTOWANIE",
        02: "SEN",
        03: "SEN",
        04: "SEN",
    }
}

day3 = day2.copy()
day3["header"] = "Plan dnia - Święta"


class DayPlan(object):
    __hours = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 00, 01, 02, 03, 04]

    def __init__(self, filename="./day-plan-1.png"):
        self.filename = filename

        self.im = Image.new("RGB", (1000, 794), "black")
        self.draw = ImageDraw.Draw(self.im)
        # margins Left, upper, right, bottom
        self.marginsCols = {"size": 320}
        self.marginsHeader = {"left": 55, "top": 52, "right": 25, "bottom": 25}
        self.marginsRows = {"left": 25, "top": 52, "right": 25, "bottom": 25}
        self.padding_cols = 18

        self.HeaderFont = ImageFont.truetype("./NotoSans-BoldItalic.ttf", 20)
        self.TextFont = ImageFont.truetype("./NotoSans-Regular.ttf", 15)

    def setData(self, *kargs):
        cols = 0
        for day in kargs:
            HeaderPos = (
                self.marginsHeader["left"] + (self.marginsCols["size"] * cols + 20 + self.marginsHeader["right"]), 23)
            print("Marginesy dla kolumny %i " % cols, HeaderPos)

            self.draw.text(HeaderPos,
                           day["header"].decode("utf-8"), font=self.HeaderFont,
                           fill=(240, 240, 0))
            row_i = 0
            for hour, text in day["hours"].iteritems():
                RowNumPos = (
                    self.marginsRows["left"] + (self.marginsCols["size"] * cols),
                    self.marginsRows["top"] + (row_i * 22)
                )
                RoWTexPos = (
                    self.marginsRows["left"] + 50 + (self.marginsCols["size"] * cols),
                    self.marginsRows["top"] + (row_i * 22)
                )

                print("Marginesy dla kolumny %i Numer: %s, Text: %s  " % (cols, RowNumPos, RoWTexPos))
                self.draw.text(RowNumPos,
                               str("%s%s" % ("  ", hour)).decode("utf-8"),
                               font=self.TextFont,
                               fill=(240, 240, 0))
                self.draw.text(RoWTexPos, text.decode("utf-8"), font=self.TextFont,
                               fill=(240, 240, 0))
                row_i += 1

            cols += 1

    # # Każda linia ma mieć odstęp od góry - 5 px + font size + 2px, Boki 10px + TextFont.getSize(t)+ 10px
    #     #
    #     # draw.rectangle([margins["left"], 23 + (i * 22), 50, 50], fill=(255, 0, 0), outline=(0, 255, 0))
    #     # write hour cell
    #     draw.text((margins["left"], 23 + (i * 22)), str("%s%s" % ("  ", h)).decode("utf-8"), font=TextFont,
    #               fill=(240, 240, 0))
    #
    #     # Write text cell
    #     draw.text((margins["left"] + 50, 23 + (i * 22)), t.decode("utf-8"), font=TextFont, fill=(240, 240, 0))
    #
    #     print(h, " => ", t)
    #     i += 1
    #
    # del draw

    def draw_row(hour, text):
        pass

    def save(self):
        self.im.save(self.filename)


if __name__ == '__main__':
    dp = DayPlan()
    dp.setData(day1, day2, day3)
    dp.save()
