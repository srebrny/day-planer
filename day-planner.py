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
        self.size = (1000, 794)

        self.im = Image.new("RGB", self.size, self.__configuration["background"])
        self.draw = ImageDraw.Draw(self.im)
        # margins Left, upper, right, bottom
        self.marginsCols = {"size": 320}
        self.marginsHeader = {"left": 20, "top": 75, "right": 25, "bottom": 25}
        self.marginsRows = {"left": 25, "top": 100, "right": 25, "bottom": 25}
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
            size_x, size_y = self.draw.textsize(day["header"].decode("utf-8"), font=self.HeaderFont)

            size_col_x = self.marginsHeader["left"] + column_x_pos + 300 + 5

            padding_size = column_x_pos + (size_col_x - column_x_pos - size_x) / 2

            HeaderPos = (
                self.marginsHeader["left"] + padding_size,
                self.marginsHeader["top"])

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

                self.drawRow(row["hour"], row["text"], background=self.__configuration["procedures"].get(row["text"]),
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

    def drawPlanHeader(self, text, background=None, justify=None, pos=(0, 0), margins=None):
        if not margins:
            margins = {"left": 0, "top": 0, "right": 0, "bottom": 0}

        HeaderBox = [
            (margins["left"], margins["top"]),
            (self.size[0] - margins["right"], margins["bottom"])
        ]

        self.draw.rectangle(HeaderBox, fill=self.colors.getrgb("#fff"), outline=(128, 128, 128))
        self.draw.text(
            pos,
            text,
            font=self.TextFont,
            fill=self.TextFontFill_text
        )

    def save(self):
        self.im.save(self.filename)


if __name__ == '__main__':
    dp = DayPlan()

    stream = file("./myday.yml", "r")
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
    dp.drawPlanHeader("PLAN", background=conf["name"]["background"], pos=conf["name"]["pos"],margins=conf["name"]["margins"])

    for day in days_data:
        dp.addDay(day)
    dp.save()
