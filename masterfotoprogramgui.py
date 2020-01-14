#!/home/christopher/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
begun on Sun Aug 25 11:24:43 2019

this is the main foto management proram.
@author: christopher rehm
note this program uses the wxPython4.0 and wxWidgets for GUI development,
both must be installed
plase use wxPython 4.0 or higher 

"""
#import sys
import os
import wx 
import shutil
import json
import artmanagementcfg as cfg
from markdown import markdown
import pdfkit

##################################################################################   
def makeList():
    #this function makes a list of all paintings in the file of works
    os.chdir(cfg.myworkingFolder)
    print(os.getcwd())
    os.chdir("./info") #enter info dir, where we keep all info files
    fh = open("./finishedPaintings.txt", "w")
    mylist ={}
    mylist["all"] = searchLevel(cfg.myworkingFolder)
    for k, v in mylist.items():
        fh.write(str(k) + '\n')
        for k1, v1 in v.items():
            fh.write("" + str(k1) + '\n')
            try:
                for k2, v2 in v1.items():
                    fh.write("" + str(k2) +'\n')
            except:
                fh.write("\n")
    fh.close()
    os.chdir("..")   
##################################################################################
def createAllSubfolders():
    os.chdir(cfg.workingDir)
    mylist= os.listdir()
    for each in mylist:
        chkdir = cfg.workingDir + "/" + str(each)
        if os.path.isdir(each) is True:
            os.chdir(chkdir)
            mylist1= os.listdir()
            for each1 in mylist1:
                chkdir1 = chkdir + "/" + str(each1)
                if os.path.isdir(each1) is True:
                    os.chdir(chkdir1)
                    for every in cfg.dirlist:   
                        newdir = chkdir + "/" + str(each1) + "/" + str(every)
                        if os.path.isdir(newdir) is False:
                            os.mkdir(newdir)
                    os.chdir("..")
            os.chdir("..")
##################################################################################  
def moveAllPhotos():
   for each in cfg.paintingPaths:
       os.chdir(each)
       listOfFilesToMove = os.listdir(".")
       for each in listOfFilesToMove:
           if each.endswith(".CR2"):
               shutil.move("./"+each, "./cr2type/"+ each)
           elif each.endswith(".JPG"):
               shutil.move("./"+each, "./jpgtype/"+ each)
           elif each.endswith(".jpg"):
               shutil.move("./"+each, "./oldCamerPics/"+ each)
           else:
               pass  
##################################################################################
def renameFotos():
    pass
##################################################################################
#### recursion search function #####
def searchLevel(myLevel):
    tableofitems ={}
    thisdirlist = os.listdir(myLevel)
    countoffiles = 1
    for each in thisdirlist:
        if os.path.isdir(myLevel +"/" + each) is True:
            mynewlevel = myLevel +"/" + each 
            tableofitems[each] = searchLevel(mynewlevel)
        else:
            tableofitems[countoffiles] = each
            countoffiles +=1
    return tableofitems
##################################################################################

##################################################################################
#GUI APP 
class mainMenu(wx.Frame):   
    
    def __init__(self, parent, id):

        wx.Frame.__init__(self, parent, id, 'Menus', size=(1200, 800))

        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour("blue")
        
        hboxMain =wx.BoxSizer(wx.HORIZONTAL)
        vboxBig = wx.BoxSizer(wx.VERTICAL)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
       
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1a = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        hbox7 = wx.BoxSizer(wx.HORIZONTAL)
       
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        
        hboxr1 = wx.BoxSizer(wx.HORIZONTAL)
        hboxr1aa = wx.BoxSizer(wx.HORIZONTAL)
        hboxr1a = wx.BoxSizer(wx.HORIZONTAL)
        hboxr2 = wx.BoxSizer(wx.HORIZONTAL)
 
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menu2 = wx.Menu()
        menu3 = wx.Menu()
        menu4 = wx.Menu()
        menuItemLoad = menu1.Append(-1, "&Load dir")
        menuItemClose = menu1.Append(-1, "&Close dir")
        menuItemExit = menu1.Append(-1, "&Exit...")
    
        menuItemNewPainting = menu2.Append(-1,"&New Painting")
        menuItemNewSubfolder = menu2.Append(-1,"Create New Subfolder")
    
        menuItemMakeListAll = menu3.Append(-1, "List all works")
        menuItemCreateAllSubfolders = menu3.Append(-1,"Make All Subfolders")
        menuItemMoveFotosToFolders = menu3.Append(-1, "Move Fotos to Subfolders")
        menuItemColate = menu3.Append(-1, "Collate all Info Sheets")
        menuItemRenameAll = menu3.Append(-1, "Rename All Fotos")

        menuItemHelp = menu4.Append(-1,"Help")
        menuItemPref = menu4.Append(-1, "Preferences")
        menuItemAbout = menu4.Append(-1, "&About me")
    
        menuBar.Append(menu1, "&File")
        menuBar.Append(menu2, "&Common Actions")
        menuBar.Append(menu3, "&Other Actions")
        menuBar.Append(menu4, "&Info")
    
        self.SetMenuBar(menuBar)
        self.CreateStatusBar()
        self.SetStatusText("Welcome to art business management")
    
        self.Bind(wx.EVT_MENU, self.OpenFile, menuItemLoad)
        self.Bind(wx.EVT_MENU, self.CloseFile, menuItemClose)
        self.Bind(wx.EVT_MENU, self.OnCloseMe, menuItemExit)
    
        self.Bind(wx.EVT_MENU, self.NewPainting, menuItemNewPainting)
        self.Bind(wx.EVT_MENU, self.AddNewSubFolder, menuItemNewSubfolder)
        self.Bind(wx.EVT_MENU, self.MakeListAllWorks, menuItemMakeListAll)
        self.Bind(wx.EVT_MENU, self.CreateAllSubfolders, menuItemCreateAllSubfolders)
        self.Bind(wx.EVT_MENU, self.MoveFotosToFolders, menuItemMoveFotosToFolders)
        self.Bind(wx.EVT_MENU, self.ColateAllInfoSheets, menuItemColate)
        self.Bind(wx.EVT_MENU, self.RenameAllFotosPicDateNum, menuItemRenameAll)
    
        self.Bind(wx.EVT_MENU, self.GetHelp, menuItemHelp)
        self.Bind(wx.EVT_MENU, self.SetPreferences, menuItemPref)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuItemAbout)
    
        workName ="Name of work"
        catName = "Current Catagory"
    
        self.b1 = wx.Button(panel, label = 'previous work') 
        hbox0.Add(self.b1, 1, wx.ALIGN_LEFT|wx.ALL,5)
    
        self.labelA = wx.StaticText(panel, -1, workName , style = wx.TE_CENTER)
        hbox0.Add(self.labelA, 1, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL,5)
    
        self.b2 = wx.Button(panel, label = 'next work') 
        hbox0.Add(self.b2, 1, wx.ALIGN_LEFT|wx.ALL,5)
    
        self.b3 = wx.Button(panel, label = 'previous catagory') 
        hbox0.Add(self.b3, 1, wx.ALIGN_LEFT|wx.ALL,5)
    
        self.labelB = wx.StaticText(panel, -1, catName ,style = wx.TE_CENTER)
        hbox0.Add(self.labelB, 1, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL,5)
    
        self.b4 = wx.Button(panel, label = 'next catagory') 
        hbox0.Add(self.b4, 1, wx.ALIGN_LEFT|wx.ALL,5)
    
        self.b5 = wx.Button(panel, label = 'EXIT PROGRAM') 
        hbox0.Add(self.b5, 1, wx.ALIGN_RIGHT|wx.ALL,5)
    
        self.b5.Bind(wx.EVT_BUTTON, self.OnQuit)  
        self.b1.Bind(wx.EVT_BUTTON, self.PrevPainting)
        self.b2.Bind(wx.EVT_BUTTON, self.NextPainting)
        self.b3.Bind(wx.EVT_BUTTON, self.PrevCat)
        self.b4.Bind(wx.EVT_BUTTON, self.NextCat)
    
        label1 = wx.StaticText(panel, -1, "Name of work")
        hbox1.Add(label1, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        
        self.t1 = wx.TextCtrl(panel,-1,size=(350,40))
        hbox1.Add(self.t1,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
    
        label2 = wx.StaticText(panel, -1, "Date painted")
        hbox2.Add(label2, 1, wx.ALIGN_LEFT|wx.ALL,5)
    
        self.t2 = wx.TextCtrl(panel,-1,size=(100,40))
        hbox2.Add(self.t2,1,wx.ALIGN_LEFT|wx.ALL,5)
        
        label2a = wx.StaticText(panel, -1, "id number")
        hbox2.Add(label2a, 1, wx.ALIGN_LEFT|wx.ALL,5)
    
        self.t2a = wx.TextCtrl(panel,-1,size=(50,40))
        hbox2.Add(self.t2a,1,wx.ALIGN_LEFT|wx.ALL,5)
        
        label2b = wx.StaticText(panel, -1, "count/year")
        hbox2.Add(label2b, 1, wx.ALIGN_LEFT|wx.ALL,5)
    
        self.t2b = wx.TextCtrl(panel,-1,size=(50,40))
        hbox2.Add(self.t2b,1,wx.ALIGN_LEFT|wx.ALL,5)
    
        label3 = wx.StaticText(panel, -1, "Where painted")
        hbox3.Add(label3, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        
        self.t3 = wx.TextCtrl(panel,-1,size=(350,40))
        hbox3.Add(self.t3,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
    
        label4 = wx.StaticText(panel, -1, "Vertical dim")
        hbox4.Add(label4, 1, wx.ALIGN_LEFT|wx.ALL,5)
        
        self.t4 = wx.TextCtrl(panel,-1,size=(50,40))
        hbox4.Add(self.t4,1,wx.ALIGN_LEFT|wx.ALL,5)
        
        label5 = wx.StaticText(panel, -1, "Horizontal dim")
        hbox4.Add(label5, 1, wx.ALIGN_LEFT|wx.ALL,5)
        
        self.t5 = wx.TextCtrl(panel,-1,size=(50,40))
        hbox4.Add(self.t5,1,wx.ALIGN_LEFT|wx.ALL,5)
    
        label10 = wx.StaticText(panel, -1, cfg.gallery1)
        hbox5.Add(label10, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        
        self.t10 = wx.TextCtrl(panel,-1,size=(50,40))
        hbox5.Add(self.t10,1,wx.ALIGN_LEFT|wx.ALL,5)
        
        label11 = wx.StaticText(panel, -1, cfg.gallery2)
        hbox5.Add(label11, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        
        self.t11 = wx.TextCtrl(panel,-1,size=(50,40))
        hbox5.Add(self.t11,1,wx.ALIGN_LEFT|wx.ALL,5)
        
        label12 = wx.StaticText(panel, -1, cfg.gallery3)
        hbox5.Add(label12, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        
        self.t12 = wx.TextCtrl(panel,-1,size=(50,40))
        hbox5.Add(self.t12,1,wx.ALIGN_LEFT|wx.ALL,5)
        
        label13 = wx.StaticText(panel, -1, cfg.gallery4)
        hbox5.Add(label13, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        
        self.t13 = wx.TextCtrl(panel,-1,size=(50,40))
        hbox5.Add(self.t13,1,wx.ALIGN_LEFT|wx.ALL,5)
        
        label14 = wx.StaticText(panel, -1, cfg.gallery5)
        hbox5.Add(label14, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        
        self.t14 = wx.TextCtrl(panel,-1,size=(50,40))
        hbox5.Add(self.t14,1,wx.ALIGN_LEFT|wx.ALL,5)
       
        label6 = wx.StaticText(panel, -1, "Materials used")
        hbox6.Add(label6, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
    
        label7 = wx.StaticText(panel, -1, "cfg.description")
        hbox7.Add(label7, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
    
        self.t6 = wx.TextCtrl(panel,-1,size=(350,80),style = wx.TE_MULTILINE)
        hbox6.Add(self.t6,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
    
        self.t7 = wx.TextCtrl(panel,-1,size=(350,160),style = wx.TE_MULTILINE)
        hbox7.Add(self.t7,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        
        self.savebtn = wx.Button(panel, label = "save painting data")
        hboxr2.Add(self.savebtn,1,wx.ALIGN_CENTER|wx.ALIGN_BOTTOM|wx.ALL, 5)
        self.savebtn.Bind(wx.EVT_BUTTON, self.onSavePainting)
        
        self.printbtn = wx.Button(panel, label = "print .md and pdf")
        hboxr2.Add(self.printbtn,1,wx.ALIGN_CENTER|wx.ALIGN_BOTTOM|wx.ALL, 5)
        self.printbtn.Bind(wx.EVT_BUTTON, self.MakeMd)
        
        image_size=(500,500)
        
        self.max_size = 400

        img = wx.Image(*image_size)
        self.image_ctrl = wx.StaticBitmap(panel, bitmap=wx.Bitmap(img))

        self.browse_btn = wx.Button(panel, label='Browse')
        
        self.browse_btn.Bind(wx.EVT_BUTTON, self.on_browse)

        self.photo_txt = wx.StaticText(panel, -1 , "this is the file")
        hboxr1aa.Add(self.photo_txt,wx.ALIGN_CENTER|wx.ALIGN_BOTTOM|wx.ALL, 5)
        
        vbox1.Add(hbox1)
        vbox1.Add(hbox1a)
        vbox1.Add(hbox2) 
        vbox1.Add(hbox3)
        vbox1.Add(hbox4)
        vbox1.Add(hbox5)
        vbox1.Add(hbox6)
        vbox1.Add(hbox7)
        
        hboxr1.Add(self.image_ctrl, 1, wx.ALIGN_CENTER|wx.ALL, 5)
        hboxr1a.Add(self.browse_btn, 1, wx.ALIGN_CENTER|wx.ALL, 5)
        vbox2.Add(hboxr1)
        vbox2.Add(hboxr1aa)
        vbox2.Add(hboxr1a)
        vbox2.Add(hboxr2)

        hboxMain.Add(vbox1)
        hboxMain.Add(vbox2)
        
        vboxBig.Add(hbox0)
        vboxBig.Add(hboxMain)
    
        panel.SetSizer(vboxBig)
        panel.Center()
        panel.Show()
        panel.Fit()
        
        self.labelA.SetLabel(cfg.nameOfPaintingfile)
        self.labelB.SetLabel(cfg.nameOfCatagory)
        
        self.t1.SetValue(cfg.nameOfPainting)
        self.t2.SetValue(cfg.datePainted)
        self.t2a.SetValue(str(cfg.idnum))
        self.t2b.SetValue(str(cfg.secid))
        self.t3.SetValue(cfg.wherePainted)
        self.t4.SetValue(cfg.Dims)
        self.t5.SetValue(cfg.hDims)
        self.t6.SetValue(cfg.materialsUsed)
        self.t7.SetValue(cfg.description)
        self.t10.SetValue(str(cfg.gallery1Val))
        self.t11.SetValue(str(cfg.gallery2Val))
        self.t12.SetValue(str(cfg.gallery3Val))
        self.t13.SetValue(str(cfg.gallery4Val))
        self.t14.SetValue(str(cfg.gallery5Val))      
#++++++++++++++++++++++++++++++++++++++++++++++++    
    def dispData(self):
        
        print("in dispData function")
        ptgName = cfg.catDir[cfg.currentCat][cfg.dispPainting][cfg.dispPainting]["pname"]
        ptgDesc = cfg.catDir[cfg.currentCat][cfg.dispPainting][cfg.dispPainting]["desc"]
        ptgDate = cfg.catDir[cfg.currentCat][cfg.dispPainting][cfg.dispPainting]["year"]
        ptgNum = cfg.catDir[cfg.currentCat][cfg.dispPainting][cfg.dispPainting]["number"]
        saatchi= cfg.catDir[cfg.currentCat][cfg.dispPainting][cfg.dispPainting]["saatchi"]
        s6 = cfg.catDir[cfg.currentCat][cfg.dispPainting][cfg.dispPainting]["soc6"]
        try : 
            mysite = cfg.catDir[cfg.currentCat][cfg.dispPainting][cfg.dispPainting]["mysite"]
        except:
            mysite = 0
            pass
        try : 
            secid = cfg.catDir[cfg.currentCat][cfg.dispPainting][cfg.dispPainting]["secid"]
        except:
            secid = 0
            pass
        #displate = cfg.catDir[cfg.currentCat][cfg.dispPainting][cfg.dispPainting]["displate"]
        dev = cfg.catDir[cfg.currentCat][cfg.dispPainting][cfg.dispPainting]["deviant"]
        buzz= cfg.catDir[cfg.currentCat][cfg.dispPainting][cfg.dispPainting]["buzz"]
        dims= cfg.catDir[cfg.currentCat][cfg.dispPainting][cfg.dispPainting]["dims"]
        try:
            cfg.hDims = cfg.catDir[cfg.currentCat][cfg.dispPainting][cfg.dispPainting]["cfg.hDims"]
        except:
            cfg.hDims = "none"
            pass
        try:
            cfg.materialsUsed = cfg.catDir[cfg.currentCat][cfg.dispPainting][cfg.dispPainting]["cfg.materialsUsed"]
        except:
            cfg.materialsUsed = "none"
            pass
        
        self.labelA.SetLabel(cfg.dispPainting)
        self.labelB.SetLabel(cfg.currentCat)
        
        self.t1.SetValue(ptgName)
        self.t2.SetValue(str(ptgDate))
        self.t2a.SetValue(str(ptgNum))
        self.t2b.SetValue(str(secid))
        self.t3.SetValue(cfg.wherePainted)
        self.t4.SetValue(dims)
        self.t5.SetValue(cfg.hDims)
        self.t6.SetValue(cfg.materialsUsed)
        self.t7.SetValue(ptgDesc)
        self.t10.SetValue(str(saatchi))
        self.t11.SetValue(str(dev))
        self.t12.SetValue(str(s6))
        self.t13.SetValue(str(buzz))
        self.t14.SetValue(str(mysite))  
#++++++++++++++++++++++++++++++++++++++++++++++++    
    # WORKING
    def OpenFile(self,event,opt = ""):
        
        self.SetStatusText("Opens the database")
        if opt == "":
            dialog = wx.DirDialog(None, "Choose a directory to work with: ", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
            if dialog.ShowModal() == wx.ID_OK:
                cfg.workingDir = str(dialog.GetPath())
                cfg.myworkingFolder = str(dialog.GetPath())
                os.chdir(str(dialog.GetPath()))
            dialog.Destroy()
        else:
            cfg.workingDir = cfg.myworkingFolder
        cfg.subDirList = os.listdir(cfg.workingDir)
        cfg.subDirList.remove("info")
        for each in cfg.subDirList:
            listOfPaintings = {}
            if True == os.path.isdir(cfg.workingDir + "/" + each):
                cfg.subDirPaths.append(cfg.workingDir + "/" + each)
                os.chdir(cfg.workingDir + "/" + each)
                thePaintings = os.listdir(os.getcwd())
                cfg.dirOfCatandPaintings[each] = thePaintings
                for eacheins in thePaintings:
                    os.chdir(cfg.workingDir + "/" + each + "/" + eacheins + "/info")
                    for theFile in os.listdir("."):
                        if theFile.endswith(".json"):
                            with open(theFile, "r") as content:
                                datastuff = json.load(content)
                                print(datastuff)
                                listOfPaintings[eacheins]= datastuff
                    os.chdir("..")
                    os.chdir("..")

                cfg.catDir[each] = listOfPaintings

        cfg.mylibListOfPaintings = {"list_of_paintings" : cfg.paintingList }
        cfg.mylibOfSubdirectories = {"list_of_subdirectories" : cfg.subDirList}
        cfg.mylibOfSubPaintings = {"list_of_cat_and_paintings": cfg.dirOfCatandPaintings}
        
        jsonData = json.dumps(cfg.mylibOfSubdirectories, sort_keys=True,  indent=4, separators=(",", ": "))
        json1Data = json.dumps(cfg.mylibOfSubPaintings, sort_keys=True,  indent=4, separators=(",", ": "))
        json2Data = json.dumps(cfg.catDir, sort_keys=True,  indent=4, separators=(",", ": "))
        json3Data = json.dumps(cfg.workingDir, sort_keys=True,  indent=4, separators=(",", ": "))

        print("\n")
        print(os.getcwd())
        
        os.chdir(cfg.workingDir + "/" + "info")
        filename = "libOfSubdirs.json"
        with open(filename, 'w') as f:
             f.write(jsonData)
        file2name = "libOfSubsandPaintngs.json"
        with open(file2name, 'w') as f:
             f.write(json1Data)  
        file3name = "alljsondatagrams.json"
        with open(file3name, 'w') as f:
             f.write(json2Data)
        file4name = "fliepathmainfolder.json"
        with open(file4name, 'w') as f:
             f.write(json3Data)
             
        #now load correct stuff to screen.
        
        cfg.listSubs = cfg.mylibOfSubdirectories["list_of_subdirectories"]
        cfg.totalSubs = len(cfg.listSubs)
        cfg.currentCat = cfg.listSubs[1]
        cfg.listPtngs = cfg.mylibOfSubPaintings["list_of_cat_and_paintings"][cfg.currentCat]
        cfg.totalPtngs = len(cfg.listPtngs)     
        cfg.dispPainting = cfg.listPtngs[0]
        
        self.dispData()
#++++++++++++++++++++++++++++++++++++++++++++++++ 
    #WORKING       
    def CloseFile(self,event):
        self.SetStatusText("Closes the database")
        wx.MessageBox("This closes the file ",
                      "fileloader", wx.OK | wx.ICON_INFORMATION, self)
#++++++++++++++++++++++++++++++++++++++++++++++++   
    #WORKING
    def OnAbout(self, event):
        self.SetStatusText("About me")
        wx.MessageBox("This program manages data and files for an artist.\n See the user manual for more info.\n if you use regularly a 10 € contribution to my paypal account is suggested.",
                      "About Art Biz Manager", wx.OK | wx.ICON_INFORMATION, self)   
#++++++++++++++++++++++++++++++++++++++++++++++++    
    #WORKING    
    def OnCloseMe(self, event):
        self.Close() 
#++++++++++++++++++++++++++++++++++++++++++++++++        
    #WORKING
    def OnQuit(self, event):
        self.Close()  
#++++++++++++++++++++++++++++++++++++++++++++++++
    #working
    def on_browse(self, event):
        """
        Browse for an image file
        @param event: The event object
        """
        wildcard = "JPEG files (*.jpg)|*.jpg"
        with wx.FileDialog(None, "Choose a file",
                           wildcard=wildcard,
                           style=wx.ID_OPEN) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.photo_txt.SetLabel(dialog.GetPath())
                self.load_image()
#++++++++++++++++++++++++++++++++++++++++++++++++
    #working
    def load_image(self):
        """
        Load the image and display it to the user
        """
        filepath = self.photo_txt.GetLabel()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.max_size
            NewH = self.max_size * H / W
        else:
            NewH = self.max_size
            NewW = self.max_size * W / H
        img = img.Scale(NewW,NewH)
        
        self.image_ctrl.SetBitmap(wx.Bitmap(img))
        self.Refresh()    
#++++++++++++++++++++++++++++++++++++++++++++++++    
    #WORKING
    def NewPainting(self, event):
        
        self.SetStatusText("Create a New Painting")
        dialog = wx.DirDialog(None, "Choose a directory for your painting: ", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            print(dialog.GetPath())
            os.chdir(str(dialog.GetPath()))
            cfg.currentCat=os.getcwd()
            tmpcat = cfg.currentCat
        dialog.Destroy()
        dlg = wx.TextEntryDialog(None, "What is the new painting named",'Name of new painting', 'new painting')
        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetValue()
            os.mkdir("./" + response)
            os.chdir("./" + response)
            for each in cfg.dirlist:
                os.mkdir("./" + each) 
            os.chdir("info")
            cfg.dispPainting = response
            tempPainting = cfg.dispPainting

            ptgname = ""
            ptgDate =""
            numb = 0
            secid =0
            cfg.wherePainted = ""
            vertDim = ""
            horizDim = ""
            cfg.materialsUsed = ""
            ptgDesc = ""
            gal1 = 0
            gal2 = 0
            gal3 = 0
            gal4 = 0
            gal5 = 0
                   
            mydata = {cfg.dispPainting:{"pname": ptgname,"cfg.wherePainted":cfg.wherePainted,"secid":secid, "mysite":gal1,"buzz":gal2,"deviant":gal3,"saatchi":gal4,"soc6":gal5,"number": numb,"secid":secid, "year" : ptgDate, "dims": vertDim, "cfg.hDims": horizDim, "desc" : ptgDesc, "materials": cfg.materialsUsed}}
            jsonData = json.dumps(mydata, sort_keys=True,  indent=4, separators=(",", ": "))
            print(os.getcwd())
            filename = cfg.dispPainting + ".json"
            with open(filename, 'w') as f:
                 f.write(jsonData)     
            self.OpenFile(event = "none",opt = cfg.myworkingFolder)
            cfg.currentCat = tmpcat
            cfg.dispPainting =tempPainting
            self.dispData()         
#++++++++++++++++++++++++++++++++++++++++++++++++    #WORKING
    def AddNewSubFolder(self, event):
        self.SetStatusText("Add a new catagory to database")
        dlg = wx.TextEntryDialog(None, "What is the new catagory named",'Name of new folder', 'new folder')
        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetValue()
            os.chdir(cfg.myworkingFolder)
            os.mkdir(response)
        dlg.Destroy()
        self.OpenFile(event = "none",opt = cfg.myworkingFolder) 
#++++++++++++++++++++++++++++++++++++++++++++++++        
    #should be working watch for bugs
    def onSavePainting(self,event):
        
        self.SetStatusText("saving painting data to json file")
        ptgname =self.t1.GetValue()
        ptgDate =self.t2.GetValue()
        numb = self.t2a.GetValue()
        secid =self.t2b.GetValue()
        cfg.wherePainted = self.t3.GetValue()
        vertDim = self.t4.GetValue()
        horizDim = self.t5.GetValue()
        cfg.materialsUsed = self.t6.GetValue()
        ptgDesc = self.t7.GetValue()
        gal1 = self.t10.GetValue()
        gal2 =self.t11.GetValue()
        gal3 =self.t12.GetValue()
        gal4 =self.t13.GetValue()
        gal5 =self.t14.GetValue()
               
        mydata = {cfg.dispPainting:{"pname": ptgname,"cfg.wherePainted":cfg.wherePainted,"secid":secid, "mysite":gal1,"buzz":gal2,"deviant":gal3,"saatchi":gal4,"soc6":gal5,"number": numb,"secid":secid, "year" : ptgDate, "dims": vertDim, "cfg.hDims": horizDim, "desc" : ptgDesc, "materials": cfg.materialsUsed}}
        jsonData = json.dumps(mydata, sort_keys=True,  indent=4, separators=(",", ": "))
        os.chdir(cfg.workingDir + "/" + cfg.currentCat + "/"+ cfg.dispPainting +  "/info") 
        filename = cfg.dispPainting + ".json"
        with open(filename, 'w') as f:
             f.write(jsonData)
#++++++++++++++++++++++++++++++++++++++++++++++++
    #SHOULD BE WORKING        
    def MakeListAllWorks(self, event):
        self.SetStatusText("Make a list of all works")
        makeList()     
#++++++++++++++++++++++++++++++++++++++++++++++++        
    def CreateAllSubfolders(self, event):
        self.SetStatusText("Create all subfolders, not normally used")
        createAllSubfolders()
#++++++++++++++++++++++++++++++++++++++++++++++++       
    #Should be working not tested yet
    def MoveFotosToFolders(self, event):
        self.SetStatusText("Move fotos to correct picture folders")
        moveAllPhotos()
#++++++++++++++++++++++++++++++++++++++++++++++++        
    #WORKING
    def ColateAllInfoSheets(self,event):
        self.SetStatusText("Collate all info sheets in one folder")
        for each in cfg.paintingPaths:
            os.chdir(each + "/info")
            for eachone in os.listdir():
                if eachone.endswith(".odt"):
                    shutil.copy(eachone, cfg.workingDir + "/info/odtFiles/")
                elif eachone.endswith("lr.pdf"):
                    shutil.copy(eachone, cfg.workingDir + "/info/lrpdfFiles/")
                else:
                    shutil.copy(eachone, cfg.workingDir + "/info/pdfFiles/")
#++++++++++++++++++++++++++++++++++++++++++++++++    
    def RenameAllFotosPicDateNum(self, event):
        self.SetStatusText("Rename all fotos to name date index")
        renameFotos()
#++++++++++++++++++++++++++++++++++++++++++++++++    
    def DisplayWork(self,event):
        self.SetStatusText("Display a work")
        pass  
#++++++++++++++++++++++++++++++++++++++++++++++++
    def GetHelp(self, event):
        self.SetStatusText("Help")
        pass
#++++++++++++++++++++++++++++++++++++++++++++++++    
    def SetPreferences(self, event):
        self.SetStatusText("Set up preferences")
        pass
#++++++++++++++++++++++++++++++++++++++++++++++++
    def MakeMd(self, event):
        print("in makeMd")
        filename = cfg.dispPainting + ".html"
        output_filename =cfg.dispPainting + ".pdf"
        ptgname =self.t1.GetValue()
        ptgDate =self.t2.GetValue()
        wherePainted = self.t3.GetValue()
        vertDim = self.t4.GetValue()
        horizDim = self.t5.GetValue()
        materialsUsed = self.t6.GetValue()
        ptgDesc = self.t7.GetValue()
       
        data = ["\n\n\n\n\n\n\n\n\n\n",ptgname + "\n\n",ptgDate + "\n\n",wherePainted + "\n\n",vertDim + "  *  " + horizDim + "\n\n",materialsUsed + "\n\n", ptgDesc]
        
        print(os.getcwd())
        with open(filename, 'w+') as f:
            for each in data:
                f.write(each)
                
        with open(filename, 'r') as f:
            test.html = markdown(f.read(), output_format='html')

        pdfkit.from_file(test.html, output_filename)
        f.close()  
#++++++++++++++++++++++++++++++++++++++++++++++++       
    #WORKING
    def PrevPainting(self,event):
        cfg.ptngIndex -= 1
        if cfg.ptngIndex < 0:
            cfg.ptngIndex = (cfg.totalPtngs-1)
        #load new painting
        cfg.dispPainting = cfg.listPtngs[cfg.ptngIndex]
        self.dispData()
        self.SetStatusText("back one painting")    
#++++++++++++++++++++++++++++++++++++++++++++++
    #WORKING    
    def NextPainting(self,event):
        cfg.ptngIndex += 1
        if cfg.ptngIndex > (cfg.totalPtngs-1):
            cfg.ptngIndex =0
        #load new painting
        cfg.dispPainting = cfg.listPtngs[cfg.ptngIndex]
        self.dispData()
        self.SetStatusText("forward one painting")    
#+++++++++++++++++++++++++++++++++++++++++++++++++++
    #WORKING    
    def PrevCat(self,event):
        cfg.catIndex -= 1
        if cfg.catIndex < 0:
            cfg.catIndex = cfg.totalSubs-1
        cfg.currentCat = cfg.listSubs[cfg.catIndex]
        cfg.listPtngs = cfg.mylibOfSubPaintings["list_of_cat_and_paintings"][cfg.currentCat]
        cfg.totalPtngs = len(cfg.listPtngs)
        cfg.dispPainting = cfg.listPtngs[0]
        self.dispData()
####++++++++++++++++++++++++++++++++++++++++++++++++
    #WORKING    
    def NextCat(self, event):
        cfg.catIndex = cfg.catIndex + 1
        if cfg.catIndex > (cfg.totalSubs-1):
            cfg.catIndex = 0   
        cfg.currentCat = cfg.listSubs[cfg.catIndex]
        cfg.listPtngs = cfg.mylibOfSubPaintings["list_of_cat_and_paintings"][cfg.currentCat]
        cfg.totalPtngs = len(cfg.listPtngs)
        cfg.dispPainting = cfg.listPtngs[0]
        self.dispData()
##################################################################################
class App(wx.App):
    def OnInit(self):
         self.frame = mainMenu(parent=None, id = -1)
         self.frame.Center()
         self.frame.Show()
         self.frame.Fit()
         self.SetTopWindow(self.frame)
         return True
##################################################################################
if __name__ == '__main__':
    app = App()
    app.MainLoop()

    print("Ending program.")       
##################################################################################
