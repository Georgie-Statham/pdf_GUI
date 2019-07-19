import os
import wx
from PyPDF4 import PdfFileReader, PdfFileWriter

pdfs = "pdf files (*.pdf)|*.pdf|"


class RotatePanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self.input_path = None
        self.degrees_list = ['90', '180', '270']

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        open_button = wx.Button(self, 5, "Choose file...")
        open_button.Bind(wx.EVT_BUTTON, self.OpenButton)
        main_sizer.Add(open_button, 0, wx.ALL, 5)

        text = wx.StaticText(self, label="Selected:")
        main_sizer.Add(text, 0, wx.LEFT, 5)

        self.selected = wx.TextCtrl(self, 0, style=wx.TE_READONLY)
        main_sizer.Add(
            self.selected, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)

        text2 = wx.StaticText(self, label="How many degrees clockwise?")
        main_sizer.Add(text2, 0, wx.LEFT, 5)

        self.set_degrees = wx.RadioBox(
            self,
            0,
            "",
            wx.DefaultPosition,
            wx.DefaultSize,
            self.degrees_list,
            3,
            wx.RA_SPECIFY_COLS
        )
        main_sizer.Add(self.set_degrees, 0, wx.LEFT, 20)

        button_sizer = wx.GridSizer(2)

        clear_button = wx.Button(self, 0, "Clear")
        clear_button.Bind(wx.EVT_BUTTON, self.Clear_Button)
        button_sizer.Add(clear_button, 0,
            wx.ALIGN_LEFT|wx.LEFT|wx.BOTTOM|wx.RIGHT, 5)

        save_button = wx.Button(self, 0, "Rotate and save")
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
            self.selected.AppendText(file_name)
            dlg.Destroy()


    def SaveButton(self, event):
        dlg = wx.FileDialog(
            self,
            message="Save file as...",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=pdfs,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )

        if dlg.ShowModal() == wx.ID_OK:

            selection = self.set_degrees.GetSelection()
            degrees = int(self.degrees_list[selection])
            output_path = dlg.GetPath()
            pdf_writer = PdfFileWriter()
            pdf_reader = PdfFileReader(self.input_path)

            for page in range(pdf_reader.getNumPages()):
                original = pdf_reader.getPage(page)
                pdf_writer.addPage(original.rotateClockwise(degrees))

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


class RotateFrame(wx.Frame):
    def __init__(self):
        super().__init__(
            None,
            title="Rotate a pdf",
            size=(400, 170),
        )
        panel = RotatePanel(self)
        self.SetSizeHints(400, 170, 400, 170)
        self.Show()

if __name__ == "__main__":
    app = wx.App()
    frame = RotateFrame()
    app.MainLoop()
