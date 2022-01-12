#Youtube Downloader Miken et Sriram//
from tkinter import *
from tkinter import font
import tkinter
from tkinter.ttk import Progressbar
from tkinter import filedialog
import threading
import pafy

################################

def VideoUrl():
    TéléchargementBarreTexteLabel.configure(text="")
    TéléchargementLabelRésultat.configure(text="")
    TéléchargementTailleLabelRésultat.configure(text="")
    TéléchargementLabelTempsRestants.configure(text="")
    getdetail = threading.Thread(target=ObtenirVideo)
    getdetail.start()

def ObtenirVideo():
    global streams
    listbox.delete(0,tkinter.END)
    url = TexteURL.get()
    donnée = pafy.new(url)
    streams = donnée.allstreams
    index = 0

    #Conversion
    for i in streams:
        du = '{:0.1f}'.format(i.get_filesize()//(1024*1024))
        datas = str(index) + '.'.ljust(3, ' ') + str(i.quality).ljust(10, ' ') + str(i.extension).ljust(5, ' ') + str(i.mediatype) + ' ' + du.rjust(10, ' ') + "MB"
        listbox.insert(END, datas)
        index += 1

def SelectionDuCurseur(evt):
    global téléchargerindex
    listboxdonnée = listbox.get(listbox.curselection())
    print(listboxdonnée)
    téléchargerstream = listboxdonnée[:3]
    téléchargerindex = int("".join(x for x in téléchargerstream if x.isdigit()))


def TéléchargerVideo():
    ObtenirDonnée = threading.Thread(target=TéléchargerVideoDonnée)
    ObtenirDonnée.start()


def TéléchargerVideoDonnée():
    global téléchargerindex
    fgr = filedialog.askdirectory()
    TéléchargementBarreTexteLabel.configure(text="En cours de téléchargement...")

    def mycallback(total, recvd, ratio, rate, eta):
        global total12
        total = float("{:.5}".format(total/(1024*1024)))
        TéléchargementProgressionBarre.configure(maximum=total)
        recieved1 = "{:.5} mb".format(recvd / (1024 * 1024))
        eta1 = "{:.2f} sec".format(eta)
        TéléchargementTailleLabelRésultat.configure(text=total12)
        TéléchargementLabelRésultat.configure(text=recieved1)
        TéléchargementLabelTempsRestants.configure(text=eta1)
        TéléchargementProgressionBarre["value"] = recvd/(1024*1024)


    streams[téléchargerindex].download(filepath=fgr, quiet=True, callback=mycallback)
    TéléchargementBarreTexteLabel.configure(text="Téléchargé")


################################

root = Tk()
root.title("Youtube Downloader by Miken & Sriram")
root.geometry("780x500")
root.iconbitmap("")
root.configure(bg="grey")
root.resizable(False,False)
téléchargerindex = 0
total12 = 0
streams = ""

#Barre à glisser
BarreGlissement = Scrollbar(root)
BarreGlissement.place(x=477, y=230, height=193, width=20)


#Labels
titrelabel = Label(root,text="YouTube Downloader by Miken & Sriram",width=36,relief="ridge" ,bd=4, font=("chiller",23,"italic bold"),fg="red")
titrelabel.place(x=10,y=20)

listbox = Listbox(root,yscrollcommand=BarreGlissement.set,width=50,height=10,font=("arial",12,"italic bold"),relief="ridge",bd=2,highlightcolor="blue",highlightbackground="orange",highlightthickness=2)
listbox.place(x=20,y=230)
listbox.bind("<<ListboxSelect>>", SelectionDuCurseur)



TéléchargementTailleLabel = Label(root,text="Taille totale : ",font=("arial",15,"italic bold"),bg="grey")
TéléchargementTailleLabel.place(x=500,y=240)

TéléchargementLabel = Label(root,text="Taille reçevevant : ",font=("arial",15,"italic bold"),bg="grey")
TéléchargementLabel.place(x=500,y=290)

TéléchargementTempsRestants = Label(root,text="Temps restants : ",font=("arial",15,"italic bold"),bg="grey")
TéléchargementTempsRestants.place(x=500,y=340)

TéléchargementTailleLabelRésultat = Label(root,text="",font=("arial",15,"italic bold"),bg="grey")
TéléchargementTailleLabelRésultat.place(x=650,y=240)

TéléchargementLabelRésultat = Label(root,text="",font=("arial",15,"italic bold"),bg="grey")
TéléchargementLabelRésultat.place(x=650,y=290)

TéléchargementLabelTempsRestants = Label(root,text="",font=("arial",15,"italic bold"),bg="grey")
TéléchargementTempsRestants.place(x=500,y=340)

TéléchargementBarreTexteLabel = Label(root,text="Barre de téléchargement",font=("arial",15,"italic bold"),bg="grey")
TéléchargementBarreTexteLabel.place(x=500,y=445)

TéléchargementBarre = Label(root,text="",font=("arial",15,"italic bold"),bg="grey",relief="raised")
TéléchargementBarre.place(x=20,y=445)



#Bouttons
BouttonClique = Button(root,text="Entrer le lien et cliquer", font=("Arial",10,"italic bold"),bg="green",fg="red",activebackground="white",width=23, bd=8, command=VideoUrl)
BouttonClique.place(x=530, y=145)

BouttonTélécharger = Button(root, text="Télécharger", font=("Arial",10,"italic bold"), bg="red", fg="white", activebackground="white",width=23, bd=8, command=TéléchargerVideo)
BouttonTélécharger.place(x=530, y=380)

#Entrée
TexteURL = StringVar()
EntréeURL = Entry(root, textvariable=TexteURL, font=("arial",20,"italic bold"),width=31)
EntréeURL.place(x=20, y=150)

#Barre de progression du téléchargement
TéléchargementProgressionBarre = Progressbar(TéléchargementBarre, orient=HORIZONTAL, value=0, length=100, maximum= total12)
TéléchargementProgressionBarre.grid(row=0, column=0, ipadx=185, ipady=3)



root.mainloop()