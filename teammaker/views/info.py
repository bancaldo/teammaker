# -*- coding: utf-8 -*-#
import wx
import wx.html as wxhtml


STYLE = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | \
    wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN


class AboutFrame(wx.Frame):
    def __init__(self, parent, title):
        super(AboutFrame, self).__init__(parent=parent, title=title)
        self.parent = parent
        self.text = """
        <html>
        <center><h1>teammaker</h1> version 2.1<br>
        by Bancaldo</td></center><br><br>
        <b>teammaker</b> is a simple App to create balanced teams<br>
        <br>
        python modules:</b><br>
        - <b>wxPython</b> for Graphics<br>
        - <b>django</b> for database and ORM<br>
        <br>
        <b>useful links:</b><br>
        web-site: www.bancaldo.wordpress.com<br>
        web-site: www.bancaldo.altervista.org<br>
        <br>
        <b>last revision:</b> Aug 22, 2017</p><br>
        <b>author:</b> bancaldo
        </html>
        """
        self.SetSize((400, 600))
        html = wxhtml.HtmlWindow(self)
        html.SetPage(self.text)
        self.btn_quit = wx.Button(self, -1, 'quit', (25, 150), (150, -1))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_quit, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Centre()
        self.Show()

        # Bind
        self.Bind(wx.EVT_BUTTON, self.on_quit, self.btn_quit)

    # noinspection PyUnusedLocal
    def on_quit(self, event):
        self.parent.Enable()
        self.Destroy()


class HelpFrame(wx.Frame):
    def __init__(self, parent, title):
        super(HelpFrame, self).__init__(parent=parent, title=title)
        self.parent = parent
        self.text = """
        <html>
        <center><b>teammaker</b> help.</center><br><br>

        <center><b>How to handle players</b></center><br><br>

        <b>1)</b> Save players to database with <b>players</b>->
                  <em>New Player</em> menu<br>
        <b>2)</b> set values : Surname, name, value (skills), health
                    and role<br>
        <b>3)</b> edit player values from <b>players</b>->
                            <em>Edit Player</em> menu<br>
        <b>4)</b> A summary of player existing in database is available from
                    <b>players</b>-> <em>Player Summary</em> menu<br><br>

        <center><b>Team composition</b></center><br><br>

        <b>1)</b> Select players and click 'generate' button.<br>
        &nbsp&nbsp&nbsp If player number is odd, a NULL player
        is added<br>
        &nbsp&nbsp&nbsp The app will attempt 5000 times to stay
        under GAP set. If it's not possible to create balanced teams<br>
        &nbsp&nbsp&nbsp with actual GAP you need to increase GAP from
        <b>GAP</b>-> <em>Change GAP</em> menu<br>
        </html>
        """
        self.SetSize((700, 400))
        html = wxhtml.HtmlWindow(self)
        html.SetPage(self.text)
        self.btn_quit = wx.Button(self, -1, 'quit', (25, 150), (150, -1))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_quit, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Centre()
        self.Show()

        # Bind
        self.Bind(wx.EVT_BUTTON, self.on_quit, self.btn_quit)

    # noinspection PyUnusedLocal
    def on_quit(self, event):
        self.parent.Enable()
        self.Destroy()
