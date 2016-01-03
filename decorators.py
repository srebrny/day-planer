__author__ = 'srebrny'


def BackgroundDecorator(f):
    def wrapper(*argv, **kwargs):
        self = argv[0]
        background = kwargs.get("background", None)

        if background:
            # Draw a background for our hour
            bHour_coords = [
                (
                    self.marginsRows["left"] + (self.marginsCols["size"] * self.col_i) - 5,
                    self.marginsRows["top"] + (self.row_i * 22)
                ),
                (
                    self.marginsRows["left"] + (self.marginsCols["size"] * self.col_i) + 22,
                    self.marginsRows["top"] + (self.row_i * 22) + 22
                )
            ]

            bText_coords = [
                (
                    self.marginsRows["left"] + (self.marginsCols["size"] * self.col_i) + 22,
                    self.marginsRows["top"] + (self.row_i * 22)
                ),
                (
                    self.marginsRows["left"] + (self.marginsCols["size"] * self.col_i) + self.marginsCols["size"] - 20,
                    self.marginsRows["top"] + (self.row_i * 22) + 22
                )
            ]

            # Border for hour coll
            self.draw.rectangle(bHour_coords, fill=background, outline=(128, 128, 128))

            # Border for text coll
            self.draw.rectangle(bText_coords, fill=background, outline=(128, 128, 128))

        return f(*argv, **kwargs)

    return wrapper


def JustifyTextDecorator(f):
    def wrapper(*argv, **kwargs):
        self = argv[0]
        hour = argv[1]
        text = argv[2]
        justify = kwargs.get("justify", False)

        # if we want to justify our text...
        if justify:
            # We grab RowTexPos
            RowTexPos = kwargs.get("RowTexPos", (0, 0))
            # calculate current text length and width ...
            calculate_text_size = self.draw.textsize(text, self.TextFont)
            padding_size = (self.marginsCols["size"] - calculate_text_size[0] - 55) / 2

            # and update the kwargs
            kwargs["RowTexPos"] = (RowTexPos[0] + padding_size , RowTexPos[1])

        return f(*argv, **kwargs)

    return wrapper
