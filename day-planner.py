# -*- coding: utf-8 -*-

__author__ = 'srebrny'
__copyright__ = u'Copyright (c) 2010 Tomasz Świderski'

import Image, ImageDraw, ImageFont, ImageColor
import sys

from yaml import load_all

from decorators import BackgroundDecorator, JustifyTextDecorator

from yaml import load_all

dc = {
    "PRZYGOTOWANIE": ImageColor.getrgb("#00ccff"),
    "FIRMA": ImageColor.getrgb("#6666fc"),
    "PRACA i Obiad": ImageColor.getrgb("#ff3299"),
    "SPRZATANIE/OBIAD/ODPOCZYNEK": ImageColor.getrgb("#013461"),
    "DZHK": ImageColor.getrgb("#ff9899"),
    "SEN": ImageColor.getrgb("#039d01"),
    "FIRMA - ROZWOJ": ImageColor.getrgb("#6666fc"),
}


class DayPlan(object):
    __hours = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 00, 01, 02, 03, 04]
    __days = 0

    __configuration = None

    def __init__(self, filename="./day-plan-1.png", config=None):
        self.filename = filename
        if config:
            self.setConfig(config)

    def init(self):
        self.size = (1000, 900)

        self.im = Image.new("RGB", self.size, self.__configuration["background"])
        self.draw = ImageDraw.Draw(self.im)
        # margins Left, upper, right, bottom
        self.marginsCols = {"size": 320}
        self.marginsHeader = {"left": 20, "top": 60, "right": 0, "bottom": 25}
        self.marginsRows = {"left": 25, "top": 85, "right": 25, "bottom": 25}
        self.padding_cols = 18

        # FOR TRANSLATE COLORS
        self.colors = ImageColor

        # @todo: fix this it is header font color inside a background color
        self.header_bg_color = self.colors.getrgb("#3e35e8")

        #
        # Font Settings
        #
        self.HeaderFont = ImageFont.truetype("./fonts/NotoSans-BoldItalic.ttf", 20)
        self.TextFont = ImageFont.truetype("./fonts/NotoSans-Regular.ttf", 15)

        self.TextFontFill_hour = self.colors.getrgb("#fff")
        self.TextFontFill_text = self.colors.getrgb("#fff")

    def setConfig(self, conf):
        if type(conf) != dict:
            raise Exception("Missing configuration")

        self.__configuration = conf

    def getConfig(self):
        if not self.__configuration:
            raise Exception("Configuration isn't loaded")
        return self.__configuration

    def addDay(self, *kargs):

        # print (kargs)
        self.col_i = self.__days
        for day in kargs:
            # print (day)
            column_x_pos = (self.marginsCols["size"] * self.col_i)

            HeaderBox = [
                (
                    self.marginsHeader["left"] + column_x_pos,
                    self.marginsHeader["top"]
                ),
                (
                    self.marginsHeader["left"] + column_x_pos + 300 + 5,
                    self.marginsHeader["top"] + 25
                )
            ]
            size_x, size_y = self.draw.textsize(day["header"], font=self.HeaderFont)

            size_col_x = self.marginsHeader["left"] + column_x_pos + 300 + 5

            padding_size = column_x_pos + (size_col_x - column_x_pos - size_x) / 2

            HeaderPos = (
                self.marginsHeader["left"] + padding_size,
                self.marginsHeader["top"])

            # Border for hour coll
            self.draw.rectangle(HeaderBox, fill=self.colors.getrgb("#fff"), outline=(128, 128, 128))
            self.draw.text(HeaderPos,
                           day["header"], font=self.HeaderFont,
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

                self.drawRow(row["hour"], row["text"],
                             background=self.__configuration["procedures"].get(row["text"])["color"],
                             RowNumPos=RowNumPos, RowTexPos=RowTexPos, justify=True)
                self.row_i += 1

            self.col_i += 1
            # break
        self.__days += 1

    @BackgroundDecorator
    @JustifyTextDecorator
    def drawRow(self, hour, text, background=None, justify=None, RowNumPos=(0, 0), RowTexPos=(0, 0)):

        self.draw.text(
            RowNumPos,
            hour,
            font=self.TextFont,
            fill=self.TextFontFill_hour
        )

        self.draw.text(
            RowTexPos,
            text,
            font=self.TextFont,
            fill=self.TextFontFill_text
        )

    def drawProcedureRow(self, name, color, desc, question, background=None, justify=None, pos=[0, 0], font=None):

        # zapis najdłuższej i najszerszej kolumny, do wygenerowania szerokości kolumny.
        width, height = self.draw.textsize(name, font)
        fw_x, fw_y = self.size

        pos_x, pos_y = pos

        if self.max_width < width:
            self.max_width = width

        self.draw.rectangle(
            ((pos_x - 5, pos_y + self.__configuration["procedureTable"]["fontSize"] + 5), (fw_x - 35, pos_y)),
            fill=background, outline=(128, 128, 128))


        # jeżeli nasz desc albo question mają więcej niż 1 linię wtedy mnożymy fontsize +5 px * ilosc linii
        self.draw.text(
            [pos_x, pos_y],
            name,
            font=font,
            fill=self.TextFontFill_text
        )

        pos_x = 240
        self.draw.text(
            [pos_x, pos_y],
            question,
            font=font,
            fill=self.TextFontFill_text
        )

        pos_x = fw_x / 2
        self.draw.text(
            [pos_x, pos_y],
            desc,
            font=font,
            fill=self.TextFontFill_text
        )

    def drawHeader(self, text, background=None, justify=None, pos=[0, 0], margins=None, color=(0, 0, 0), font=None):
        if not margins:
            margins = {"left": 0, "top": 0, "right": 0, "bottom": 0}

        if not font:
            font = self.HeaderFont

        pos_x, pos_y = pos

        HeaderBox = [
            (margins["left"] + pos_x, margins["top"] + pos_y),
            (self.size[0] - margins["right"] - self.marginsHeader["right"], margins["bottom"] + 50 + pos_y)
        ]

        size_x, size_y = self.draw.textsize(text, font=self.TextFont)

        pos_x += margins["left"] + self.marginsHeader["left"]
        pos_y += margins["top"]
        if justify:
            pos_x += (self.size[0] - margins["right"] - self.marginsHeader["right"] - margins["left"] -
                      self.marginsHeader["left"] - size_x) / 2

        self.draw.rectangle(HeaderBox, fill=background, outline=(128, 128, 128))
        self.draw.text(
            [pos_x, pos_y],
            text,
            font=font,
            fill=color
        )

    def showProcedureBook(self):
        procConf = self.__configuration["procedureTable"]

        if procConf and self.__configuration["showProcedureTable"]:
            self.drawHeader("Lista procedur", pos=procConf["pos"], color=procConf["color"],
                            background=procConf["background"],
                            margins=procConf["margins"])

            self.max_width = 0

            pos_x, pos_y = procConf["pos"]

            pos_x += procConf["margins"]["left"] + 5
            pos_y += procConf["margins"]["top"] + 30

            procFont = ImageFont.truetype("./fonts/NotoSans-BoldItalic.ttf", procConf["fontSize"])

            padding = procConf["fontSize"] + 5
            i = 0
            for procedure, params in self.__configuration["procedures"].items():
                color, desc, question = params

                self.drawProcedureRow(procedure, params["color"], params["desc"], params["question"],
                                      pos=[pos_x, pos_y + padding * i], font=procFont,
                                      background=ImageColor.getrgb(params["color"]))
                i += 1

    def save(self):
        self.showProcedureBook()
        self.im.save(self.filename)


if __name__ == '__main__':
    dp = DayPlan()
    import codecs

    with codecs.open("./myday.yml", "r", encoding='utf-8') as stream:
        i = 0
        days_data = []
        for data in load_all(stream):
            if i != 0:
                days_data.append(data)
            else:
                config = data
            i += 1

        dp.setConfig(config)
        dp.init()

        conf = dp.getConfig()

        ImageFont.truetype("./fonts/NotoSans-Regular.ttf", 25)
        dp.drawHeader("PLAN DNIA ROZWOJOWY", background=conf["name"]["background"], pos=conf["name"]["pos"],
                      margins=conf["name"]["margins"], color=conf["name"]["color"], justify=conf["name"]["justify"])

        for day in days_data:
            dp.addDay(day)
        dp.save()
