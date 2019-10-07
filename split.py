import os
import wx
from PyPDF4 import PdfFileReader, PdfFileWriter
from pathlib import Path

pdfs = "pdf files (*.pdf)|*.pdf|"

class SplitPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self.input_path = None
        self.options = ['Join segments', 'Split segments']

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        open_button = wx.Button(self, 5, "Choose file...")
        open_button.Bind(wx.EVT_BUTTON, self.OpenButton)
        main_sizer.Add(open_button, 0, wx.ALL, 5)

        text = wx.StaticText(self, label="Selected:")
        main_sizer.Add(text, 0, wx.LEFT, 5)

        self.file_selected = wx.TextCtrl(self, 0, style=wx.TE_READONLY)
        main_sizer.Add(
            self.file_selected, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)

        text2 = wx.StaticText(self, label="Enter the desired page ranges:")
        main_sizer.Add(text2, 0, wx.LEFT, 5)

        self.page_input = wx.TextCtrl(self, 0)
        main_sizer.Add(
            self.page_input, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)

        self.set_option = wx.RadioBox(
            self,
            0,
            "",
            wx.DefaultPosition,
            wx.DefaultSize,
            self.options,
            2,
            wx.RA_SPECIFY_COLS
        )
        main_sizer.Add(self.set_option, 0, wx.LEFT, 20)

        button_sizer = wx.GridSizer(2)

        clear_button = wx.Button(self, 0, "Clear")
        clear_button.Bind(wx.EVT_BUTTON, self.Clear_Button)
        button_sizer.Add(clear_button, 0,
            wx.ALIGN_LEFT|wx.LEFT|wx.BOTTOM|wx.RIGHT, 5)

        save_button = wx.Button(self, 0, "Split and save")
        save_button.Bind(wx.EVT_BUTTON, self.SaveButton)
        button_sizer.Add(save_button, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 5)
        main_sizer.Add(button_sizer, 0, wx.EXPAND)

        self.SetSizer(main_sizer)


    def OpenButton(self, event):
        dlg = wx.FileDialog(
            self,
            message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=pdfs,
            style=wx.FD_OPEN |
                wx.FD_CHANGE_DIR |
                wx.FD_FILE_MUST_EXIST |
                wx.FD_PREVIEW
        )

        if dlg.ShowModal() == wx.ID_OK:
            self.input_path = dlg.GetPath()
            file_name = dlg.GetFilename()
            self.file_selected.AppendText(file_name)
            dlg.Destroy()


    def error_message(self, message):
        error_dlg = wx.MessageDialog(
            self,
            message,
            "Something went wrong...",
            wx.OK | wx.ICON_ERROR
        )
        error_dlg.ShowModal()
        error_dlg.Destroy()


    def check_ranges(self, start, stop):
        try:
            start, stop = int(start) - 1, int(stop)
            return (start, stop)
        except ValueError:
                self.error_message("Please select a valid page range")


    def format_range(self, pages):
        """
        Converts strings of form "n-m" or "n" into
        format required for python range function.
        """
        try:
            start, stop = pages.split('-')
            return self.check_ranges(start, stop)

        except ValueError:
            return self.check_ranges(pages, pages)


    def add_pages(self, pages, writer, reader):
        start, stop = self.format_range(pages)
        try:
            for page in range(start, stop):
                writer.addPage(reader.getPage(page))
            return writer
        except IndexError:
            self.error_message(
                "The page range you have selected exceeds the length "
                "of the pdf.\n" # This works, but then file is saved and
                # success message pops up. Need to figure out how to return
                # to split window at this point
            )


    def save_file(self, output, writer):
        with open(output, 'wb') as output_pdf:
            writer.write(output_pdf)


    def SaveButton(self, event):
        dlg = wx.FileDialog(
            self,
            message="Save file as...",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=pdfs,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )

        if not self.input_path:
            self.error_message("Please select a pdf to split")

        elif dlg.ShowModal() == wx.ID_OK:
            page_ranges = self.page_input.GetValue().split(',')
            selection = self.set_option.GetSelection()
            join_or_split = self.options[selection]
            output_path = dlg.GetPath()
            output_name = Path(dlg.GetFilename())
            pdf_reader = PdfFileReader(self.input_path)
            if join_or_split == 'Split segments':
                for page_range in page_ranges:
                    pdf_writer = PdfFileWriter()
                    self.add_pages(page_range, pdf_writer, pdf_reader)
                    output = (
                        f"{output_name.with_suffix('')}"
                        f"_p{page_range.strip()}.pdf"
                    )
                    self.save_file(output, pdf_writer)
            else:
                pdf_writer = PdfFileWriter()
                for page_range in page_ranges:
                    self.add_pages(page_range, pdf_writer, pdf_reader)
                self.save_file(output_path, pdf_writer)

            success_dlg = wx.MessageDialog(self,
                f"""Your file/s {dlg.GetFilename()} are saved at
{dlg.GetPath()}.""",
                "Success!",
                wx.OK | wx.ICON_INFORMATION
                )
            success_dlg.ShowModal()
            success_dlg.Destroy()
            dlg.Destroy()
            self.clear_func()


    def clear_func(self):
        self.input_path = None
        self.file_selected.Clear()
        self.page_input.Clear()


    def Clear_Button(self, event):
        self.clear_func()


class SplitFrame(wx.Frame):
    def __init__(self, title, parent=None):
        wx.Frame.__init__(
            self,
            parent=parent,
            title=title,
            size=(400, 200),
        )
        panel = SplitPanel(self)
        self.SetSizeHints(400, 200, 400, 200)
        self.Show()

if __name__ == "__main__":
    app = wx.App()
    frame = SplitFrame()
    app.MainLoop()
