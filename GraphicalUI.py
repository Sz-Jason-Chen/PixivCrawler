# -*- coding: utf-8 -*-


import wx
import wx.xrc
import userIllustsTagsAnalysis


class MyFrame1(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(576, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer1.Add(self.m_staticText1, 0, wx.ALL, 5)

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_textCtrl1, 0, wx.ALL, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_button1, 0, wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_textCtrl1.Bind(wx.EVT_TEXT, self.text1)
        self.m_button1.Bind(wx.EVT_BUTTON, self.button1event)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def text1(self, event):
        event.Skip()

    def button1event(self, event):
        userIllustsTagsAnalysis.main(self.m_textCtrl1.Value)
        event.Skip()


if __name__ == "__main__":
    app = wx.App()
    frm = MyFrame1(None)
    frm.Show()
    app.MainLoop()
