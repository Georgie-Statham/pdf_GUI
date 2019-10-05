import os
import wx
from PyPDF4 import PdfFileReader, PdfFileWriter

pdfs = "pdf files (*.pdf)|*.pdf|"

class AddPagesPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self.input_path = None
        self.input_file = None

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        open_button = wx.Button(self, 5, "Choose file...")
        open_button.Bind(wx.EVT_BUTTON, self.OpenButton)
        main_sizer.Add(open_button, 0, wx.ALL, 5)

        text = wx.StaticText(self, label="Selected:")
        main_sizer.Add(text, 0, wx.LEFT, 5)

        self.selected = wx.TextCtrl(self, 0, style=wx.TE_READONLY)
        main_sizer.Add(
            self.selected, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)

        text2 = wx.StaticText(self, label="How many pages would you like to add?")
        main_sizer.Add(text2, 0, wx.LEFT, 5)

        self.no_pages = wx.TextCtrl(self, 0)
        main_sizer.Add(
            self.no_pages, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)

        button_sizer = wx.GridSizer(2)

        clear_button = wx.Button(self, 0, "Clear")
        clear_button.Bind(wx.EVT_BUTTON, self.Clear_Button)
        button_sizer.Add(clear_button, 0,
            wx.ALIGN_LEFT|wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.TOP, 5)

        save_button = wx.Button(self, 0, "Add pages and save")
        save_button.Bind(wx.EVT_BUTTON, self.SaveButton)
        button_sizer.Add(save_button, 0,
            wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM|wx.TOP, 5)
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
            self.input_file = dlg.GetFilename()
            self.selected.AppendText(self.input_file)
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


    def SaveButton(self, event):
        dlg = wx.FileDialog(
            self,
            message="Save file as...",
            defaultDir=os.getcwd(),
            defaultFile=self.input_file + "+" + self.no_pages.GetValue(),
            wildcard=pdfs,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )

        if not self.input_path:
            self.error_message("Please select a pdf")

        elif dlg.ShowModal() == wx.ID_OK:
            output_path = dlg.GetPath()
            pdf_writer = PdfFileWriter()
            pdf_reader = PdfFileReader(self.input_path)
            try:
                blank_pages = int(self.no_pages.GetValue())
            except ValueError:
                self.error_message("The number of pages added must be an integer")
            pdf_writer.appendPagesFromReader(pdf_reader)
            for _ in range(blank_pages):
                pdf_writer.addBlankPage()

            with open(output_path, 'wb') as output:
                pdf_writer.write(output)

            success_dlg = wx.MessageDialog(self,
                f"""You created {dlg.GetFilename()} and saved it at
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
        self.selected.Clear()


    def Clear_Button(self, event):
        self.clear_func()


class AddPagesFrame(wx.Frame):
    def __init__(self, title, parent=None):
        wx.Frame.__init__(
            self,
            parent=parent,
            title=title,
            size=(400, 170),
        )
        panel = AddPagesPanel(self)
        self.SetSizeHints(400, 170, 400, 170)
        self.Show()

if __name__ == "__main__":
    app = wx.App()
    frame = AddPagesFrame()
    app.MainLoop()
