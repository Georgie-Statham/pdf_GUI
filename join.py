import os
import wx
from PyPDF4 import PdfFileReader, PdfFileWriter

pdfs = "pdf files (*.pdf)|*.pdf|"

class JoinPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        open_button = wx.Button(self, 5, "Select pdfs")
        open_button.Bind(wx.EVT_BUTTON, self.OpenButton)
        main_sizer.Add(open_button, 0, wx.ALL, 5)

        header = wx.StaticText(self, 0, "Selected:")
        main_sizer.Add(header, 0)

        self.input_pdfs = wx.TextCtrl(self, 0)
        self.input_pdfs.Disable()
        main_sizer.Add(self.input_pdfs, 5, wx.ALIGN_CENTER|wx.ALL, 5)

        join_button = wx.Button(self, 0, "Join")
        main_sizer.Add(join_button, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        save_button = wx.Button(self, 0, "Save as...")
        save_button.Bind(wx.EVT_BUTTON, self.SaveButton)
        main_sizer.Add(save_button, 0,  wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(main_sizer)

    def OpenButton(self, event):
        dlg = wx.FileDialog(
            self,
            message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=pdfs,
            style=wx.FD_OPEN |
                wx.FD_MULTIPLE |
                wx.FD_CHANGE_DIR |
                wx.FD_FILE_MUST_EXIST |
                wx.FD_PREVIEW
        )

        if dlg.ShowModal() == wx.ID_OK:
            input_paths = dlg.GetPaths() # pass to textctrl
            dlg.Destroy()

    # list


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
            path = dlg.GetPath()

        # with open(path, 'wb') as output:
        #         pdf_writer = PdfFileWriter()

        # for path in input_paths: # get from interactive list
        #     pdf_reader = PdfFileReader(path)
        #     for page in range(pdf_reader.getNumPages()):
        #         pdf_writer.addPage(pdf_reader.getPage(page))

        # pdf_writer.write(output)
        dlg.Destroy()

class JoinFrame(wx.Frame):
    def __init__(self):
        super().__init__(
            None,
            title="Join pdfs",
            size=(200, 250),
        )
        panel = JoinPanel(self)
        self.SetSizeHints(200, 250, 200, 250)
        self.Show()

if __name__ == "__main__":
    app = wx.App()
    frame = JoinFrame()
    app.MainLoop()


