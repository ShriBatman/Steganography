import wx
import the_codes as my
from random import *
import Image_Image as theimg
#from time import sleep



class windowClass(wx.Frame):    
    def __init__(self):
        wx.Frame.__init__(self,None,title="Welcome to STEGA")
        panel = wx.Panel(self)
        nb = theNotebook(panel)
        
        sizer = wx.BoxSizer()
        sizer.Add(nb,1,wx.EXPAND)
        panel.SetSizer(sizer)

        menuBar = wx.MenuBar()
        fileButton = wx.Menu()
        importItem = wx.Menu()

        import_img = wx.MenuItem(importItem,wx.ID_ANY,"Cover Image")
        importItem.Append(import_img)
        self.Bind(wx.EVT_MENU,nb.iport,import_img)

        
        conceal_img = wx.MenuItem(importItem,wx.ID_ANY,"Conceal Image")
        importItem.Append(conceal_img)
        self.Bind(wx.EVT_MENU,nb.conimg,conceal_img)

        
        #import_audio = wx.MenuItem(importItem,wx.ID_ANY,"Conceal Audio")
        #importItem.Append(import_audio)
        #self.Bind(wx.EVT_MENU,nb.aport,import_audio)
        
        
        fileButton.Append(wx.ID_ANY,'Import',importItem)
        exitItem = wx.MenuItem(fileButton,wx.ID_EXIT,"Quit\tCtrl+Q")
        fileButton.Append(exitItem)

        menuBar.Append(fileButton,'File')
        
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU,self.Quit,exitItem)
        
        self.SetSize(0,0,770,415)
        self.Centre()
        self.Show(True)


    def Quit(self,e):
        self.Close()


class theNotebook(wx.Notebook):
    
    tb = 0
    tab1 = None
    tab2 = None
    tab3 = None
    path = "gfh.jpg"
    con_path = ""
    
    def __init__(self,parent):
        wx.Notebook.__init__(self,parent,id=wx.ID_ANY,style=wx.BK_DEFAULT)
        self.tab1 = Text_Image(self)
        self.tab2 = Image_Image(self)
        #self.tab3 = Audio_Image(self)

        self.AddPage(self.tab1,"TextinImage")
        self.AddPage(self.tab2,"ImageinImage")
        #self.AddPage(self.tab3,"AudioinImage")

        new_img = self.resize(self.path)
        #if self.tb == 1:
        wx.StaticBitmap(self.tab2,-1,wx.Bitmap(new_img),(5,20),(300,300))
        #elif self.tb == 0:
        wx.StaticBitmap(self.tab1,-1,wx.Bitmap(new_img),(5,20),(300,300))
        #elif self.tb == 2:
        #wx.StaticBitmap(self.tab3,-1,wx.Bitmap(new_img),(5,20),(300,300))

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
        

    def iport(self,event):
        openFile = wx.FileDialog(self,"Open","","","All Files |*",wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        if openFile.ShowModal() == wx.ID_OK:
            self.path = openFile.GetPath()
            openFile.Destroy()
            new_img = self.resize(self.path)
            
            if self.tb == 1:
                wx.StaticBitmap(self.tab2,-1,wx.Bitmap(new_img),(5,20),(300,300))
            elif self.tb == 0:
                wx.StaticBitmap(self.tab1,-1,wx.Bitmap(new_img),(5,20),(300,300))
            #elif self.tb == 2:
                #wx.StaticBitmap(self.tab3,-1,wx.Bitmap(new_img),(5,20),(300,300))


    def conimg(self,event):
        openFile = wx.FileDialog(self,"Open","","","All Files |*",wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        if openFile.ShowModal() == wx.ID_OK:
            self.con_path = openFile.GetPath()
            openFile.Destroy()
            new_img = self.resize(self.con_path)
            if self.tb == 1:
                wx.StaticBitmap(self.tab2,-1,wx.Bitmap(new_img),(440,20),(300,300))


    def aport(self,event):
        openFile = wx.FileDialog(self,"Open","","","All Files |*",wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)



    def resize(self,path):
        img = wx.Image(path,wx.BITMAP_TYPE_ANY)
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = 300
            NewH = 300 * H / W
        else:
            NewH = 300
            NewW = 300 * W / H
        new_img = img.Scale(NewW,NewH)
        return new_img
         
    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        self.tb = self.GetSelection()
        #if self.path == "gfh.jpg":
        #    self.setimg()
        #print 'OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, self.tb)
        event.Skip()
 
    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        #print 'OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel)
        event.Skip()
        
        
        
class Image_Image(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        self.basicGUI(parent)

    def onEncrypt(self,event,parent):
        if parent.path == "":
            wx.MessageBox('Please Select an Cover Image','Error',wx.OK | wx.ICON_ERROR)
        elif parent.con_path == "":
            wx.MessageBox('Please Select an Conceal Image','Error',wx.OK | wx.ICON_ERROR)
        else:
            k = theimg.encode(parent.path,parent.con_path)
            if k == 1:
                wx.MessageBox('Encryption Completed','Info',wx.OK)
            elif k == -1:
                wx.MessageBox('Size of the Cover Image is not sufficient. Please select a new Image.','Info',wx.OK)

    def onDecrypt(self,event,parent):
        if parent.path=="":
            wx.MessageBox('Please Select an Cover Image','Error',wx.OK | wx.ICON_ERROR)
        else:
            k = theimg.decode(parent.path)
            if k==1:
                wx.MessageBox('Decryption Completed','Info',wx.OK)
            
        

    def basicGUI(self,parent):
        wx.StaticText(self,-1,'Cover Image:',(8,3))
        wx.StaticText(self,-1,'Conceal Image:',(443,3))

        but_en = wx.Button(self,wx.ID_ANY,'ENCRYPT',(325,90))
        but_en.Bind(wx.EVT_BUTTON, lambda event: self.onEncrypt(event,parent))
        but_de = wx.Button(self,wx.ID_ANY,'DECRYPT',(325,210))
        but_de.Bind(wx.EVT_BUTTON, lambda event: self.onDecrypt(event,parent))


class Audio_Image(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        self.basicGUI(parent)

    def basicGUI(self,parent):
        wx.StaticText(self,-1,'Cover Image:',(8,3))
        but_en = wx.Button(self,wx.ID_ANY,'ENCRYPT',(325,90))
        #but_en.Bind(wx.EVT_BUTTON, self.onEncrypt)
        but_de = wx.Button(self,wx.ID_ANY,'DECRYPT',(325,210))
        #but_de.Bind(wx.EVT_BUTTON, self.onDecrypt)



class Text_Image(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent)

        self.basicGUI(parent)

    def onEncrypt(self,event,parent):
        text = self.the_text.GetValue()
        #print text
        if parent.path == "":
            wx.MessageBox('Please Select an Cover Image','Error',wx.OK | wx.ICON_ERROR)
        elif text == "":
            wx.MessageBox('Please Enter Text','Error',wx.OK | wx.ICON_ERROR)
        else:
            x = randint(1,100)
            #chooseOneBox = wx.SingleChoiceDialog(None,'Cipher','Select Cipher To Encrypt Text:',['None','Ceasar Cipher','PlayFair Cipher'])
            if x%2 == 0:
                #cipher = chooseOneBox.GetStringSelection()
                hide = my.caesar_en(x,text)
            else:
                hide = my.Encrypt(text)
                #print text
            hide = chr(x)+hide+chr(3)
            k = my.stega(parent.path,hide)
            if(k==1):
                wx.MessageBox('Encryption Completed','Info',wx.OK)

    def onDecrypt(self,event,parent):
        #self.the_text.Clear()
        #sleep(7)
        if parent.path == "":
            wx.MessageBox('Please Select an Image','Error',wx.OK | wx.ICON_ERROR)
        else:
            str_ = my.decode(parent.path)
            p = ord(str_[0])
            str_ = str_[1:]
            s=""
            if p%2 == 0:
                x = my.caesar_de(p,str_)
                x = x.upper()
                for i in x:
                    if ord(i)>64 and ord(i)<91:
                        s += i
            else:
                s = my.Decrypt(str_)

            
            #sleep(12)
            self.the_text.SetValue(s)
            if(s!=""):
                wx.MessageBox('Decryption Completed','Info',wx.OK)

    
    def basicGUI(self,parent):
        wx.StaticText(self,-1,'Cover Image:',(8,3))
        wx.StaticText(self,-1,'Conceal Text:',(443,3))

        self.the_text = wx.TextCtrl(self,pos=(440,20),size=(300,300),style = wx.TE_MULTILINE)

        but_en = wx.Button(self,wx.ID_ANY,'ENCRYPT',(325,90))
        but_en.Bind(wx.EVT_BUTTON, lambda event: self.onEncrypt(event,parent))
        but_de = wx.Button(self,wx.ID_ANY,'DECRYPT',(325,210))
        but_de.Bind(wx.EVT_BUTTON, lambda event: self.onDecrypt(event,parent))
        

def main():
    app = wx.App()
    windowClass()
    app.MainLoop()

main()
