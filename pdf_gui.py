import wx

from join import JoinFrame
from split import SplitFrame
from rotate import RotateFrame
from add_pages import AddPagesFrame


class MainPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)

        main_sizer = wx.GridSizer(2, 2, 5)

        join_button = wx.Button(self, 5, 'Join')
        join_button.Bind(wx.EVT_BUTTON, self.get_join_frame)
        main_sizer.Add(join_button, 1, wx.TOP|wx.LEFT|wx.EXPAND, 5)

        split_button = wx.Button(self, 5, 'Split')
        split_button.Bind(wx.EVT_BUTTON, self.get_split_frame)
        main_sizer.Add(
            split_button, 1, wx.TOP|wx.RIGHT|wx.EXPAND, 5
        )

        rotate_button = wx.Button(self, 5, 'Rotate')
        rotate_button.Bind(wx.EVT_BUTTON, self.get_rotate_frame)
        main_sizer.Add(
            rotate_button, 1, wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, 5
        )

        add_pages_button = wx.Button(self, 5, 'Add Blank Pages')
        add_pages_button.Bind(
            wx.EVT_BUTTON, self.get_add_pages_frame)
        main_sizer.Add(
            add_pages_button, 1, wx.TOP|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5
        )

        self.SetSizer(main_sizer)

    # def get_other_frame(self, event, frame, title):
    #     frame = frame(
    #         title=title,
    #         parent=wx.GetTopLevelParent(self)
    #     )

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

    def get_add_pages_frame(self, event):
        frame = AddPagesFrame(
            title='Add blank pages',
            parent=wx.GetTopLevelParent(self)
        )


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(
            None,
            title="Manipulate your pdfs!",
            size=(300, 80),
        )
        panel = MainPanel(self)
        self.SetSizeHints(300, 80, 300, 80)
        self.Show()

if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()

