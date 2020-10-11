import tkinter,os,pygame,random,time,threading
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.font import Font
from mutagen.mp3 import MP3
class musicplayer:

    def __init__(self):
        self.window=tkinter.Tk()
        self.window.config(bg="White")
        self.window.title("Octave")
        self.ws = self.window.winfo_screenwidth()
        self.hs = self.window.winfo_screenheight()
        # calculate position x, y
        w,h=500,625
        x = (self.ws/2) - (w/2)    
        y = (self.hs/2.2) - (h/2)
        self.window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.window.resizable(0,0)
        pygame.init()
        pygame.mixer.init()
        self.file="music_files.txt"
        self.songtracks=list()
        self.playing=-1
        self.no=0
        self.songlist=list()
        self.vol=0.5
        self.l=0
        self.dark=1
        self.var=DoubleVar()
        self.var=50.0
        self.var2=StringVar()
        self.running=True
        self.color=["#5B2C6F"]
        self.queue=list()
        
        # icon
        self.window.iconbitmap("illu.ico")
        # scrollbar and listbox
        self.scrollbar = Scrollbar(self.window,bd=0)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox = Listbox(self.window,font="Calibri 12 italic",height=26,width=55,selectmode=SINGLE,relief=FLAT,
                        highlightthickness=0,bg="White",fg="#1B2631",selectbackground="#c2bebe",selectforeground="#1B2631",activestyle=NONE)
        self.listbox.pack(anchor=CENTER,pady=10) 
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        # self.l3.image=photo
        self.var=self.vol*100
        pygame.mixer.music.set_volume(self.vol)
        
        # song label
        myFont = Font(family='Comic Sans MS',size=10,slant='italic')
        self.l4=Label(self.window,bd=0,bg="White",fg="#1B2631",font=myFont,textvariable=self.var2)
        self.l4.pack(anchor=CENTER)
        self.var2.set("Select a song to start playing")
        self.l4.config(fg=random.choice(self.color))
        
        # buttons
        self.prev=Button(self.window,text="<<",font="Calibri 12 bold",bg="White",fg="#1B2631",activebackground="White",bd=0,command=self.previous)
        self.prev.place(x=165,y=575)
        self.play=Button(self.window,text=" Play/Pause",font="Calibri 12 bold",bg="White",fg="#1B2631",activebackground="White",bd=0,command=self.play_pause)
        self.play.pack(anchor=CENTER,pady=10)
        self.next=Button(self.window,text=">>",font="Calibri 12 bold",bg="White",fg="#1B2631",activebackground="White",bd=0,command=self.next_song)
        self.next.place(x=298,y=575)
        #self.queue_btn=Button(self.window,text="Queue",font="Calibri 12 bold",bg="White",fg="#1B2631",bd=0,command=self.queue_song)
        #self.queue_btn.place(x=420,y=575)

        
        # key bindings
        self.listbox.bind("<Double-1>",self.selected_song)
        self.window.bind("<Control-q>",self.exitfile)
        self.window.bind("<Control-f>",self.adddirectory)
        self.window.bind("<space>",self.play_pause)
        self.window.bind("<Right>",self.next_song)
        self.window.bind("<n>",self.next_song)
        self.window.bind("<Left>",self.previous)
        self.window.bind("<b>",self.previous)
        self.window.bind("<Up>",self.increase_vol)
        self.window.bind("<Down>",self.decrease_vol)
        self.window.bind("<q>",self.queue_song)
        self.window.bind("<r>",self.scan_newsongs)
        self.window.bind("<h>",lambda e: self.go_up_down(1))
        self.window.bind("<j>",lambda e: self.go_up_down(-1))
        self.window.bind("<Return>",self.selected_song)
        self.window.bind("<f>",self.selected_song)

        #self.toggle_dark()  #calling to change the default mode to light 
        self.start_set()
        self.window.protocol("WM_DELETE_WINDOW",self.exitfile)   # goes to self.exitdile() when close button is pressed
        self.window.mainloop()

    def adddirectory(self,Event=None):
        directory=filedialog.askdirectory()
        if(directory==None or directory==""):
            pass
        else:
            with open(self.file,"w") as file:
                file.write(directory)
            self.listbox.delete(0,END)
            self.stop_play()
            self.start_set()

    def start_set(self):
        try:
            file=open(self.file,"r+")
            d=file.readline()
            if(len(d)>1):
                self.cdir=d
                os.chdir(self.cdir)
                temp= os.listdir()
                self.songtracks.clear()
                self.songlist.clear()
                self.no=0
                for i in temp:
                    if(i[len(i)-4:]==".mp3"):       #endswith(".mp3") can also be used 
                        self.songtracks.insert(0,i)
                self.songtracks.sort()
                for i in self.songtracks:
                    self.listbox.insert(END,i[:-4])
        except:
            tkinter.messagebox.showinfo("Message","select the song directory by going to file -> Select/Change Directory  ")

    def scan_newsongs(self,Event=None):
            self.listbox.delete(0,END)
            self.songtracks.clear()
            for song in os.listdir():
                if(song.endswith(".mp3")):       #endswith(".mp3") can also be used 
                    self.songtracks.insert(0,song)
            self.songtracks.sort()
            for song in self.songtracks:
                self.listbox.insert(END,song[:-4])   

    def play_pause(self,Event=None):
            if(self.playing==-1):
                self.songlist.insert(self.no,random.choice(self.songtracks)) 
                pygame.mixer.music.load(self.songlist[self.no])
                pygame.mixer.music.set_endevent( pygame.USEREVENT )
                self.running=True
                self.playing=1
                pygame.mixer.music.play()
                self.var2.set(str(self.songlist[self.no])[:-4])
                self.t1 =threading.Thread(target=self.loop)
                self.t1.start()
            elif(self.playing==0):                              #resume
                pygame.mixer.music.unpause()
                self.playing=1
            elif(self.playing==1):                              #pause
                pygame.mixer.music.pause()
                self.playing=0
        
    def loop(self,Event=None):              #calls self.next() to play next song once the current song gets over
        while self.running:
            for event in pygame.event.get():   #gets all the event made by pygame
                if( event.type == pygame.USEREVENT):        
                   self.next_song()
               
    def queue_song(self,Event=None):
        self.temp_no=self.no
        sel_song=self.listbox.get(ACTIVE)+".mp3"
        self.queue.append(sel_song)
        self.var2.set(f'"{self.queue[len(self.queue)-1][0:-4]}" added to queue')
        
        

    def next_song(self,Event=None): 
        if(self.playing==-1):
            self.play_pause()
        else:
            if(self.playing==0):
                self.playing=1
            elif len(self.queue)!=0:
                self.no=self.no+1
                self.songlist.insert(self.no,self.queue[0])
                del self.queue[0]    #   self.queue.remove(0)
            else:
                self.no=self.no+1
                self.songlist.insert(self.no,random.choice(self.songtracks))
            pygame.mixer.music.load(self.songlist[self.no])
            self.var2.set(str(self.songlist[self.no])[:-4])
            pygame.mixer.music.play()
            
            
    def previous(self,Event=None):
        if(self.no>0):
            if(self.playing==0):
                self.playing=1
            self.no=self.no-1
            pygame.mixer.music.load(self.songlist[self.no])
            pygame.mixer.music.play()
            self.var2.set(str(self.songlist[self.no])[:-4])
        
    
    def selected_song(self,Event=None):
        if(self.playing==-1 ):
            self.songlist.insert(self.no,self.listbox.get(ACTIVE)+".mp3")
            pygame.mixer.music.set_endevent( pygame.USEREVENT )
            pygame.mixer.music.load(self.songlist[self.no])
            self.running=True
            self.playing=1
            self.t1 =threading.Thread(target=self.loop)
            self.t1.start()
        else: 
            self.no=self.no+1
            self.songlist.insert(self.no,self.listbox.get(ACTIVE)+".mp3")
            pygame.mixer.music.load(self.songlist[self.no])
        pygame.mixer.music.play()
        self.var2.set(str(self.songlist[self.no])[:-4])
        self.playing=1

    def runnging_selection(self,curr,num):
            next=curr + num
            self.listbox.select_clear(0, "end")
            self.listbox.selection_set(next)
            self.listbox.see(next)
            self.listbox.activate(next)
            self.listbox.selection_anchor(next)

    def go_up_down(self,num,event=None):
        curr=self.listbox.curselection()
        #print("size: ",self.listbox.size())
        if len(curr)==0:
            self.runnging_selection(0,0) 
        elif curr[0]==self.listbox.size()-1:
            if num==-1:
                self.runnging_selection(curr[0],num)
            else:
                pass
        elif curr[0]>0:
            self.runnging_selection(curr[0],num)
        else:                   # cur is zero
            if num==1:
                self.runnging_selection(curr[0],num)  
            else:
                self.runnging_selection(0,0)  

    def volume(self,Event=None):
        self.vol=self.var/100.0
        pygame.mixer.music.set_volume(self.vol)

    def increase_vol(self,Event):
        if(self.vol<=0.9):
            self.vol=self.vol + 0.1
            self.var=self.var+10.0
            pygame.mixer.music.set_volume(self.vol)
        elif(self.vol>0.9):
            self.vol=1.0
            self.var=100.0
            pygame.mixer.music.set_volume(self.vol)
    
    def decrease_vol(self,Event):
        if(self.vol<0.1):
            self.vol=0.0
            self.var=0.0
            pygame.mixer.music.set_volume(self.vol)
        elif(self.vol<=1.0):
            self.vol=self.vol - 0.1
            self.var=self.var-10.0
            pygame.mixer.music.set_volume(self.vol)

    def stop_play(self):
        self.playing=-1  
        self.running=False
        pygame.mixer.music.set_endevent()   #clears the end event
        pygame.mixer.music.stop()
        self.songlist.clear()
        self.queue.clear()
        self.var2.set("Select a song to start playing")
        self.no=0
        # to stop the loop() iteration
   
    def exitfile(self,Event=None):
        self.stop_play()                      
        self.window.quit()              # to close everything
        self.window=None

if(__name__=="__main__"):
    ms=musicplayer()

#  to build an exe file install pyinstaller and run the command below
#  pyinstaller Octave.py --onefile --windowed --icon="image/illu.ico"