import wx

from join import JoinFrame
from split import SplitFrame
from rotate import RotateFrame


class MainPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        join_button = wx.Button(self, 5, 'Join')
        join_button.Bind(wx.EVT_BUTTON, self.get_join_frame)
        main_sizer.Add(
            join_button, 1, wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, 5
        )

        split_button = wx.Button(self, 5, 'Split')
        split_button.Bind(wx.EVT_BUTTON, self.get_split_frame)
        main_sizer.Add(
            split_button, 1, wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, 5
        )

        rotate_button = wx.Button(self, 5, 'Rotate')
        rotate_button.Bind(wx.EVT_BUTTON, self.get_rotate_frame)
        main_sizer.Add(
            rotate_button, 1, wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5
        )

        self.SetSizer(main_sizer)


    def get_join_frame(self, event):
        frame = JoinFrame(
            title='Join pdfs',
            parent=wx.GetTopLevelParent(self)
        )

    def get_split_frame(self, event):
        frame = SplitFrame(
            title='Split a pdf',
            parent=wx.GetTopLevelParent(self)
        )

    def get_rotate_frame(self, event):
        frame = RotateFrame(
            title='Rotate a pdf',
            parent=wx.GetTopLevelParent(self)
        )


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(
            None,
            title="Manipulate your pdfs!",
            size=(300, 60),
        )
        panel = MainPanel(self)
        self.SetSizeHints(300, 60, 300, 60)
        self.Show()

if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()

