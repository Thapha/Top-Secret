import numpy.core.multiarray
from tkinter import *
import image as im
import constant as c
from threading import Thread
import control as ctr

#<Version 1.0.0.2> ADD
import recognize as re
#</Version 1.0.0.2> ADD

#-----V1.0.0.0: Basic form for the application
#-----V1.0.0.1: Run application now will get the game's box
#-----V1.0.0.2: Added game info - timer counter in game
#-----V1.0.0.3: Added Money place box and updated game info
#-----V1.0.0.4: Updated game info GUI - now App can recognize current money
#-----V1.0.1.0: Complete version 1

#<Version 1.0.0.0> ADD
CONST_WIDTH = 300
CONST_HEIGHT = 500

ISRUN = False                       #Check if the application is running
w = c.WIDTH                         #Get Width of monitor
h = c.HEIGHT                        #Get Height of monitor

timeCount = '00:00:00'              #Initialize the time counter

#<Version 1.0.0.2> ADD
timeInGame = '0'                    #Time counter in game
getTimeSuccess = False               #Get timer in game successfuly
#</Version 1.0.0.2> ADD

#<Version 1.0.0.4> ADD
moneyInGame = 0                     #current money in game
getMoneySuccess = False             #Get timer in game successfuly
#</Version 1.0.0.4> ADD

#<Version 1.0.1.0> ADD
isBet = False
moneyPrvGame = moneyInGame
isLosingStreak=False
moneyBetting=0
changeMode = True       #for mode 3
duplicateMode = False   #for mode 4
#</Version 1.0.1.0> ADD

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Master Form")
        master.resizable(0,0)
        frame = Frame(master=master, width=CONST_WIDTH, height=CONST_HEIGHT)
        frame.pack()

        #<Run Button>
        btn_run_width = 120
        btn_run_height = 30
        btn_run_padding = (0,30,10,0) #Top Right Bot Left
        btn_run_x = (CONST_WIDTH-btn_run_width)-(btn_run_padding[1] - btn_run_padding[0]) - 120
        btn_run_y = (CONST_HEIGHT-btn_run_height)-(btn_run_padding[2]-btn_run_padding[3])
        master.bind('<Return>', self.Run)#binding enter key for Running Button
        self.btn_run = Button(frame, text="Run")
        self.btn_run.bind("<Button-1>", self.Run)
        self.btn_run.place(height=btn_run_height,width=btn_run_width,x=btn_run_x,y=btn_run_y)
        #</Run Button>

        #<Close Button>
        btn_close_width = 120
        btn_close_height = 30
        btn_close_padding = (0,20,10,0) #Top Right Bot Left
        btn_close_x = (CONST_WIDTH-btn_close_width)-(btn_close_padding[1] - btn_close_padding[0])
        btn_close_y = (CONST_HEIGHT-btn_close_height)-(btn_close_padding[2]-btn_close_padding[3])
        btn_close = Button(frame, text="Close", command=master.quit)
        btn_close.place(height=btn_close_height,width=btn_close_width,x=btn_close_x,y=btn_close_y)
        #</close Button>

        #<Group 1>
        #<Label 1>
        lbl_type_x = 15
        lbl_type_y = 15
        lbl_type = Label(frame,text="Loại: ")
        lbl_type.place(x=lbl_type_x,y=lbl_type_y)
        #</Label 1>

        #<RadioButton 1>
        MODES = [
            ('Chỉ Chọn A',0),
            ('Chỉ Chọn B',1),
            ('Chọn A và B xen kẽ',2),
            ('AA - BB',3),
            ('AA - B',4),
            ('BB - A',5)
            ]
        self.rdbType = dict()
        self.var = IntVar(None,0)
        rdb_y = 15
        for text,index in MODES:
            rdb_x = 50
            self.rdbType[index] = Radiobutton(frame,text=text,variable=self.var,value=index)
            self.rdbType[index].place(x=rdb_x,y=rdb_y)
            rdb_y += 22
        #</RadioButton 1>
        #</Group 1>

        #<Group 2>
        #<Label 2>
        lbl_time_x = 15
        lbl_time_y = 150
        lbl_time = Label(frame,text="Thời gian tắt chương trình (Phút): ")
        lbl_time.place(x=lbl_time_x,y=lbl_time_y)
        #</Label 2>
        #<Textbox 1>
        txt_time_x = 15
        txt_time_y = 175
        txt_time_width = 220
        txt_time_height = 25
        self.v = StringVar(frame)
        vcmd = (master.register(self.validate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.txt_time = Entry(frame,textvariable=self.v,validate = 'key',validatecommand = vcmd)
        self.txt_time.place(width=txt_time_width,height=txt_time_height, x=txt_time_x,y=txt_time_y)
        self.txt_time.focus()
        #</Textbox 1>
        #</Group 2>

#<Version 1.0.0.3> ADD
        #<Group 5>
        #<Label 6>
        lbl_moneyPlaceStop_x = 15
        lbl_moneyPlaceStop_y = 210
        lbl_moneyPlaceStop = Label(frame,text="Số tiền muốn dừng: ")
        lbl_moneyPlaceStop.place(x=lbl_moneyPlaceStop_x,y=lbl_moneyPlaceStop_y)
        #</Label 6>
        #<Textbox 2>
        txt_moneyPlaceStop_x = 15
        txt_moneyPlaceStop_y = 230
        txt_moneyPlaceStop_width = 220
        txt_moneyPlaceStop_height = 25
        self.vms = StringVar(frame)
        self.txt_moneyPlaceStop = Entry(frame,textvariable=self.vms,validate = 'key',validatecommand = vcmd)
        self.txt_moneyPlaceStop.place(width=txt_moneyPlaceStop_width,height=txt_moneyPlaceStop_height, x=txt_moneyPlaceStop_x,y=txt_moneyPlaceStop_y)
        #</Textbox 2>

        #<Label 7>
        lbl_moneyPlace_x = 15
        lbl_moneyPlace_y = 255
        lbl_moneyPlace = Label(frame,text="Số tiền khởi điểm: ")
        lbl_moneyPlace.place(x=lbl_moneyPlace_x,y=lbl_moneyPlace_y)
        #</Label 7>
        #<Textbox 3>
        txt_moneyPlace_x = 15
        txt_moneyPlace_y = 275
        txt_moneyPlace_width = 220
        txt_moneyPlace_height = 25
        self.vm = StringVar(frame)
        self.txt_moneyPlace = Entry(frame,textvariable=self.vm,validate = 'key',validatecommand = vcmd)
        self.txt_moneyPlace.place(width=txt_moneyPlace_width,height=txt_moneyPlace_height, x=txt_moneyPlace_x,y=txt_moneyPlace_y)
        #</Textbox 3>

        #</Group 5>
#</Version 1.0.0.3> ADD

        #<Group 3>
        #<Label 3>
        lbl_timeCount_x = 15
        lbl_timeCount_y = 320
        self.lbl_timeCount = Label(frame,text="Bộ đếm ngược: "+timeCount)
        self.lbl_timeCount.place(x=lbl_timeCount_x,y=lbl_timeCount_y)
        #</Label 3>
        #</Group 3>

#<Version 1.0.0.2> ADD
        #<Group 4>
        #<Label 4>
        lbl_gameInfo_x = 15
        lbl_gameInfo_y = 350
        lbl_gameInfo = Label(frame,text="Thông tin game: ")
        lbl_gameInfo.place(x=lbl_gameInfo_x,y=lbl_gameInfo_y)
        #</Label 4>

        #<Label 5>
        lbl_gameTime_x = 15
        lbl_gameTime_y = 370
        self.lbl_gameTime = Label(frame,text="Thời gian trong game: "+timeInGame)
        self.lbl_gameTime.place(x=lbl_gameTime_x,y=lbl_gameTime_y)
        #</Label 5>

        #<Label 6>
        lbl_gameMoney_x = 15
        lbl_gameMoney_y = 390
        self.lbl_gameMoney = Label(frame,text="Số tiền hiện có: "+str(moneyInGame))
        self.lbl_gameMoney.place(x=lbl_gameMoney_x,y=lbl_gameMoney_y)
        #</Label 6>
        #</Group 4>
#</Version 1.0.0.2> ADD
    #Form methods
    def Run(self,event):
        global ISRUN
        global moneyBetting
        ISRUN = not ISRUN
        if ISRUN == True:
            flatTime = int(self.v.get())*60
            moneyBetting = self.vm.get()
            self.countdown(flatTime)
            self.countdown_newThread(flatTime)
            self.countdown_action(flatTime)
#<Version 1.0.0.1> ADD
            #im.getFrame()
            #im.getMoney()
            #im.getTime()
#</Version 1.0.0.1> ADD
            self.disableForm()
        else:
            self.enableForm()

    def disableForm(self):
        self.txt_time['state']='disable'
        self.txt_moneyPlaceStop['state']='disable'
        self.txt_moneyPlace['state'] = 'disable'
        self.btn_run['text']='Stop'
        #for i in range(0,len(self.rdbType)):
        #    self.rdbType[i]['state']='disable'

    def enableForm(self):
        self.btn_run['text']='Run'
        self.txt_time['state']='normal'
        self.txt_moneyPlaceStop['state']='normal'
        self.txt_moneyPlace['state'] = 'normal'
        #for i in range(0,len(self.rdbType)):
        #    self.rdbType[i]['state']='normal'
        timeCount = '00:00:00'

    def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789':
            try:
                int(text)
                return True
            except ValueError:
                return False
        else:
            return False

    def countdown(self,count): #Get time in game
        hours = count//3600
        minutes = ((count//60) - (hours*60))
        seconds = count - (hours*3600 + minutes*60)
        timeCount = (f"{hours:02d}")+":"+(f"{minutes:02d}")+":"+(f"{seconds:02d}")
        self.lbl_timeCount['text'] = "Bộ đếm ngược: "+  timeCount
#<Version 1.0.0.2> ADD
        global timeInGame
        global getTimeSuccess
        global isBet
#<Version 1.0.0.4> ADD
        #global moneyInGame
        #global getMoneySuccess
#</Version 1.0.0.4> ADD
        strTime=""
        digits=[]
        getDetails = im.getDetails()
        if getTimeSuccess == False:
            try:
                digits = re.getTime(getDetails[0])
                getTimeSuccess = True
            except:
                digits = []
                getTimeSuccess = False

            if len(digits)>0:
                for digit in digits:
                    strTime = strTime + str(digit)
                    timeInGame = strTime
        else:
            timeInGame = int(timeInGame)
            timeInGame = timeInGame - 1
#<Version 1.0.1.0> ADD
        if int(timeInGame) == 8:
            isBet = True
#</Version 1.0.1.0> ADD

        if int(timeInGame) == 0:
            getTimeSuccess = False
#<Version 1.0.0.4> ADD
            getMoneySuccess==False
        #if int(timeInGame) >= 14 and getMoneySuccess==False:
        #    moneyInGame = re.getMoney(getDetails[1])
        #    getMoneySuccess = True

#        self.lbl_gameMoney['text'] = "Số tiền hiện có: "+ str(moneyInGame)
#</Version 1.0.0.4> ADD
        self.lbl_gameTime['text'] = "Thời gian trong game: "+ str(timeInGame)
        #print(str(getTimeSuccess) + ":" + strTime)
#</Version 1.0.0.2> ADD
        if count > 0 and int(self.vms.get()) > moneyInGame:
            if ISRUN == True:
                root.after(1000, self.countdown, count-1)
            else:
                timeCount = '00:00:00'
                self.countdown(0)
        else:
            self.enableForm()
            self.ISRUN = False

#<Version 1.0.1.0> ADD
    def countdown_newThread(self,count): #Get money in game
        global moneyInGame
        global moneyPrvGame
        global getMoneySuccess
        global moneyBetting
        if int(timeInGame) >= 14 and getMoneySuccess==False:
            try:
                moneyInGame = re.getMoney(im.getDetails()[1])
                getMoneySuccess = True
                if(moneyPrvGame != 0 and moneyPrvGame>moneyInGame):
                    isLosingStreak=True
                else:
                    isLosingStreak = False

                if isLosingStreak == True:
                    moneyBetting = moneyBetting*2
                else:
                    moneyBetting = self.vm.get()


                moneyPrvGame = moneyInGame
            except:
                getMoneySuccess = False

        self.lbl_gameMoney['text'] = "Số tiền hiện có: "+ str(moneyInGame)
        if count > 0 and int(self.vms.get()) > moneyInGame:
            if ISRUN == True:
                root.after(1000, self.countdown_newThread, count-1)
            else:
                self.countdown_newThread(0)
        else:
            self.enableForm()
            self.ISRUN = False

    def action_Mode1(self):
        if(self.var.get() == 0):
            global isBet
            global moneyBetting
            #print(str(isBet) +":"+str(timeInGame))
            if isBet == True:
                #print(int(self.txt_moneyPlace['text']))
                ctr.betMode1(moneyBetting)
                isBet = False

    def action_Mode2(self):
        if(self.var.get() == 1):
            global isBet
            global moneyBetting
            if isBet == True:
                #print(int(self.txt_moneyPlace['text']))
                ctr.betMode2(moneyBetting)
                isBet = False

    def action_Mode3(self):
        if(self.var.get() == 2):
            global isBet
            global moneyBetting
            global changeMode
            if isBet == True:
                if changeMode == True:
                    ctr.betMode2(moneyBetting)
                else:
                    ctr.betMode1(moneyBetting)
                changeMode = not changeMode
                isBet = False

    def action_Mode4(self):
        if(self.var.get() == 3):
            global isBet
            global moneyBetting
            global changeMode
            global duplicateMode
            if isBet == True:
                if changeMode == True:
                    ctr.betMode2(moneyBetting)
                else:
                    ctr.betMode1(moneyBetting)
                if duplicateMode == True:
                    changeMode = not changeMode
                isBet = False
                duplicateMode = not duplicateMode


    def action_Mode5(self):
        if(self.var.get() == 4):
            global isBet
            global moneyBetting
            global changeMode
            global duplicateMode
            if isBet == True:
                if changeMode == True:
                    ctr.betMode2(moneyBetting)
                else:
                    ctr.betMode1(moneyBetting)
                    if duplicateMode == True:
                        changeMode = not changeMode
                duplicateMode = not duplicateMode
                changeMode = not changeMode
                isBet = False

    def action_Mode6(self):
        if(self.var.get() == 5):
            global isBet
            global moneyBetting
            global changeMode
            global duplicateMode
            if isBet == True:
                if changeMode == True:
                    ctr.betMode2(moneyBetting)
                    if duplicateMode == False:
                        changeMode = not changeMode
                else:
                    ctr.betMode1(moneyBetting)
                duplicateMode = not duplicateMode
                changeMode = not changeMode
                isBet = False

    def switcher(self,x):
        return {
            0:self.action_Mode1(),
            1:self.action_Mode2(),
            2:self.action_Mode3(),
            3:self.action_Mode4(),
            4:self.action_Mode5(),
            5:self.action_Mode6()
        }.get(x,0)

    def countdown_action(self,count): #New thread for action in game
        self.switcher(self.var.get())
        #print(self.var.get())
        if count > 0 and int(self.vms.get()) > moneyInGame:
            if ISRUN == True:
                root.after(1000, self.countdown_action, count-1)
            else:
                self.countdown_action(0)
        else:
            self.enableForm()
            self.ISRUN = False
#</Version 1.0.1.0> ADD

root = Tk()
my_gui = GUI(root)
root.geometry('%dx%d+%d+%d' % (CONST_WIDTH, CONST_HEIGHT, w-CONST_WIDTH, 0))
root.mainloop()
#</Version 1.0.0.0> ADD
