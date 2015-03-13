# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# Copyright (C) 2009 Free Software Fundation

# auteur : pzia <paparazzia@gmail.com>

import Tkinter
import re
import NlconverterLib
import os

class Gui(Tkinter.Frame):
    """Basic Gui using NlconverterLib"""
    def __init__(self):
        Tkinter.Frame.__init__(self)
        self.master.title("Lotus Notes Converter")
        self.defaultOpenPath = '.'
        self.defaultSaveName = "old_lotus_notes"
        self.nsfPath = None
        self.destMbox = None
        self.checked = False
        self.dbNotes = None

        #Source chooser
        self.chooseNsfButton = Tkinter.Button(self.master, text="Select SOURCE nsf file", command= self.openNsfFile, relief =Tkinter.GROOVE)
        self.chooseNsfButton.grid(row=1,column=1, sticky=Tkinter.E+Tkinter.W)

        #Destination chooser
        self.chooseDestButton = Tkinter.Button(self.master, text="Select DESTINATION mbox file", command= self.openDestination, relief =Tkinter.GROOVE)
        self.chooseDestButton.grid(row=1,column=2, sticky=Tkinter.E+Tkinter.W)

        #Password
        Tkinter.Label(self.master, text="Enter Lotus Notes password").grid(row=2, column=1, sticky=Tkinter.W)
        self.entryPassword = Tkinter.Entry(self.master, relief =Tkinter.GROOVE) #, show="*")
        self.entryPassword.insert(0, "Enter Lotus Notes password")
        self.entryPassword.grid(row=2,column=1, sticky=Tkinter.E+Tkinter.W)
        self.entryPassword.bind("<FocusIn>", self.bindEntry)

        #Action button
        self.startButton = Tkinter.Button(self.master, text="Check parameters", command= self.doConvert, relief =Tkinter.GROOVE)
        self.startButton.grid(row=2,column=2, sticky=Tkinter.E+Tkinter.W)
        
        #Message Area
        frame = Tkinter.Frame(self.master)
        frame.grid(row=5, column=1, columnspan=2)
        self.messageWidget = Tkinter.Text(frame, width=60, height=10, state = Tkinter.DISABLED, wrap=Tkinter.NONE)
        scrollY = Tkinter.Scrollbar(frame, orient = Tkinter.VERTICAL, command = self.messageWidget.yview)
        self.messageWidget['yscrollcommand'] = scrollY.set
        scrollY.pack(side=Tkinter.RIGHT,expand=Tkinter.NO,fill=Tkinter.Y)
        scrollX = Tkinter.Scrollbar(frame, orient = Tkinter.HORIZONTAL, command = self.messageWidget.xview)
        self.messageWidget['xscrollcommand'] = scrollX.set
        scrollX.pack(side=Tkinter.BOTTOM,expand=Tkinter.NO,fill=Tkinter.X)

        self.messageWidget.pack(side=Tkinter.RIGHT,expand=Tkinter.YES,fill=Tkinter.BOTH)
        self.log("INFO: Visit http://code.google.com/p/nlconverter/ for docs.\n")

    def bindEntry(self, foo= "bar"):
        """Blank the pasword field and set it in password mode"""
        self.entryPassword.delete(0, Tkinter.END)
        self.entryPassword.config(show="*")
        self.entryPassword.unbind("<FocusIn>") #not needed anymore

    def debug(self):
        """Debug"""
        print self.nsfPath
        print self.entryPassword.get()
        print self.destMbox
        print self.dbNotes
        print self.checked

    def configWidgets(self, **kargs):
        self.chooseNsfButton.config(**kargs)
        self.chooseDestButton.config(**kargs)
        self.entryPassword.config(**kargs)
        self.startButton.config(**kargs)

    def realConvert(self):
        """Perform the translation from nsf to mbox"""
        c = 0 #compteur de documents
        e = 0 #compteur d'erreur à la conversion
        tl = self.winfo_toplevel()

        mc = NlconverterLib.NotesToMboxConverter(self.destMbox)
        self.log("INFO: Populating mbox file : %s" % self.destMbox)
        mc.log = self.log
        #ic = NlconverterLib.NotesToIcalConverter(notesNsfPath+".ics")
        all = self.dbNotes.AllDocuments
        ac = all.Count
        doc = all.GetFirstDocument()
        
        self.log("INFO: Starting Convert")
        self.configWidgets(state = Tkinter.DISABLED)
        while doc and e < 100 : #stop after 100 exceptions...
            try:
                mc.addDocument(doc)                
                #ic.addDocument(doc)
        
            except Exception, ex:
                e += 1 #compte les exceptions
                self.log("ERROR: Exception for message %d (%s - see below) :" % (c, ex))
                mc.debug(doc)
        
            finally:
                doc = all.GetNextDocument(doc)
                c+=1
                if (c % 100) == 0:
                    tl.title("Lotus Notes Converter - Running (%.1f%%)" % float(100.*c/ac))
                    self.update()
                    
        self.log("\nINFO: Exceptions a traiter manuellement: %d ... Documents OK : %d" % (e, c))
        mc.close()
        #ic.close()
        self.log("INFO: End of convert")
        tl.title("Lotus Notes Converter")
        self.configWidgets(state = Tkinter.NORMAL)
        self.unchecked()

    def doConvert(self):
        if self.checked:
            self.realConvert()
        else : #Check if all is OK
            try :
                self.dbNotes = NlconverterLib.getNotesDb(self.nsfPath, self.entryPassword.get())
                all=self.dbNotes.AllDocuments
                ac = all.Count
                self.log("INFO: Documents in %s : %d" % (self.dbNotes, ac) )
            except:
                self.log("ERROR: Could not connect to Notes !")
                self.registerDll()
                self.dbNotes = None
            self.check()

    def registerDll(self):
        if NlconverterLib.registerNotesDll():
            self.log("INFO: NotesDll registered")
            return True
        else :
            self.log("ERROR : Could not find and register the dll (see the documentation)")
            return False

    def check(self):
        check = self.dbNotes != None and self.nsfPath != None and self.entryPassword.get() != ""
        if check :
            self.startButton.config(text = "Convert")
            self.checked = True
            self.log("INFO: Parameters OK")
        else :
            self.unchecked()
            self.log("ERROR : Check your input")
            #self.debug()
        return self.checked   

    def openNsfFile(self):
        types = "{ {Lotus Notes Database} {.nsf} TEXT } { {All} * }"
        filename = self.tk.call('tk_getOpenFile','-filetypes',types,'-initialdir',self.defaultOpenPath)
        if filename != "" and type(filename) is not tuple:
            self.nsfPath = "%s" % filename
            self.chooseNsfButton.config(text = "Source file is : %s" % self.nsfPath)
            self.unchecked()

    def openDestination(self):
        repname = self.tk.call('tk_getSaveFile','-initialdir',self.defaultOpenPath, "-initialfile", self.defaultSaveName)
        if repname != "" and type(repname) is not tuple and str(repname) != "":
            self.destMbox = str(repname)
            self.chooseDestButton.config(text = "Write mbox to %s" % self.destMbox)
            self.unchecked()

    def unchecked(self):
        self.startButton.config(text = "Check")
        self.checked = False        

    def updateProgress(self, ratio):
        pass

    def log(self, message = ""):
        self.messageWidget.config(state = Tkinter.NORMAL)
        self.messageWidget.insert(Tkinter.END, message+"\n")
        self.messageWidget.config(state = Tkinter.DISABLED)
        self.messageWidget.yview(Tkinter.END)
        self.update()

if __name__ == '__main__':

    Gui().mainloop()
