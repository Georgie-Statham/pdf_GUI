import os
import wx
import wx.adv
from PyPDF4 import PdfFileReader, PdfFileWriter

pdfs = "pdf files (*.pdf)|*.pdf|"


class JoinPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self.files_and_paths = {}
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        open_button = wx.Button(self, 5, "Choose files...")
        open_button.Bind(wx.EVT_BUTTON, self.OpenButton)
        main_sizer.Add(open_button, 0, wx.TOP|wx.LEFT, 5)

        self.input_files = wx.adv.EditableListBox(
            self, 0, "Selected:", style=wx.adv.EL_ALLOW_DELETE)
        main_sizer.Add(
            self.input_files, 5, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5)

        button_sizer = wx.GridSizer(2)

        clear_button = wx.Button(self, 0, "Clear")
        clear_button.Bind(wx.EVT_BUTTON, self.Clear_Button)
        button_sizer.Add(clear_button, 0,
            wx.ALIGN_LEFT|wx.LEFT|wx.BOTTOM|wx.RIGHT, 5)

        save_button = wx.Button(self, 0, "Join and save")
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
                wx.FD_MULTIPLE |
                wx.FD_CHANGE_DIR |
                wx.FD_FILE_MUST_EXIST |
                wx.FD_PREVIEW
        )

        if dlg.ShowModal() == wx.ID_OK:
            for file, path in zip(dlg.GetFilenames(), dlg.GetPaths()):
                self.files_and_paths[file] = path
            self.input_files.SetStrings([
                file for file in self.files_and_paths
            ])

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
            output_path = dlg.GetPath()
            input_paths = (
                self.files_and_paths[file]
                for file in self.input_files.GetStrings()
            )

            pdf_writer = PdfFileWriter()

            for path in input_paths:
                pdf_reader = PdfFileReader(path)
                for page in range(pdf_reader.getNumPages()):
                    pdf_writer.addPage(pdf_reader.getPage(page))

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


    def Clear_Button(self, event):
        self.clear_func()


    def clear_func(self):
        self.files_and_paths = {}
        self.input_files.SetStrings([""])


class JoinFrame(wx.Frame):
    def __init__(self):
        super().__init__(
            None,
            title="Join pdfs",
            size=(400, 250),
        )
        panel = JoinPanel(self)
        self.SetSizeHints(400, 250, 400, 250)
        self.Show()

if __name__ == "__main__":
    app = wx.App()
    frame = JoinFrame()
    app.MainLoop()


