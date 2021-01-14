
##################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs
from fpdf import FPDF

# Own modules


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

#################################################################################################################


class PDF(FPDF):

    def build_layout(self):
        self.width = 210
        self.height = 300

        self.x_margin = 20
        self.top_margin = 10
        self.bottom_margin = 20

        self.text_width = self.width - 2 * self.x_margin

        self.y_tracker = 10

        self.font = "Arial"

    def reset_layout(self):
        self.y_tracker = 10

        self.add_line(8.0)
        self.add_line(290.0)

    # =======================================================================================================

    def add_chapter(self, text, align="C", style="B"):

        self.y_tracker += 40

        self.set_xy(0, self.y_tracker)
        self.set_font(self.font, style, 28)

        self.cell(w=0, h=0, align=align, txt=text, border=0)

    def add_title(self, text, height=5, align="", style="B"):

        self.y_tracker += 10

        self.set_xy(self.x_margin, self.y_tracker)
        self.set_font(self.font, style, 18)

        self.cell(w=self.text_width, h=height, align=align, txt=text, border=0)

        self.y_tracker += 5

    def add_subtitle(self, text, height=5, align="", style=""):

        self.y_tracker += 10

        self.set_xy(self.x_margin, self.y_tracker)
        self.set_font(self.font, style, 16)

        self.cell(w=self.text_width, h=height, align=align, txt=text, border=0)

        self.y_tracker += 5

    def add_subsubtitle(self, text, height=5, align="", style="B"):

        self.y_tracker += 5

        self.set_xy(self.x_margin, self.y_tracker)
        self.set_font(self.font, style, 11)

        self.cell(w=self.text_width, h=height, align=align, txt=text, border=0)

    # =======================================================================================================

    def add_text(self, text, height=5, align="", style=""):

        self.y_tracker += 5

        self.set_xy(self.x_margin, self.y_tracker)
        self.set_font(self.font, style, 11)

        self.multi_cell(w=self.text_width, h=height, align=align, txt=text, border=0)

    def add_image(self, image, height=0, width=0):

        self.y_tracker += 7

        self.set_xy(self.x_margin, self.y_tracker)
        self.image(image, link="", type="", h=height, w=width)

    def add_dataframe(self, dataframe, ):
        return

    # =======================================================================================================

    def add_textbox(self, text, x_origin, y_origin, height=40, width=210, align="", style=""):

        self.set_xy(x_origin, y_origin)
        self.set_font(self.font, style, 11)

        self.cell(w=width, h=height, align=align, txt=text, border=0)

    def add_floating_image(self, image, x_origin, y_origin, height=0, width=0):

        self.set_xy(x_origin, y_origin)
        self.image(image, link="", type="", h=height, w=width)

        self.y_tracker += 7

    # =======================================================================================================

    def adjust_space(self, space):
        self.y_tracker += space

    def add_line(self, y):

        self.set_line_width(0.0)
        self.line(self.x_margin, y, self.width-self.x_margin, y)