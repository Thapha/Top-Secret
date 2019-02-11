import pyautogui as gui
import constant as c
import time

w=c.WIDTH
h=c.HEIGHT

dragon_x = w*22/100
dragon_y = h*58.5/100

tiger_x = w*33/100
tiger_y = h*58.5/100

money_x = w*31/100
money_y = h*85/100

confirm_x = w*23/100
confirm_y = h*85/100

def moveMouseToTiger():
    gui.moveTo(tiger_x, tiger_y)

def moveMouseToDragon():
    gui.moveTo(dragon_x,dragon_y)

def moveMouseToMoney():
    gui.moveTo(money_x,money_y)

def moveMouseToConfirm():
    gui.moveTo(confirm_x,confirm_y)

def clickToTiger():
    gui.click(tiger_x,tiger_y)

def clickToDragon():
    gui.click(dragon_x,dragon_y)

def clickToMoney():
    gui.click(money_x,money_y)

def clickToConfirm():
    gui.click(confirm_x,confirm_y)

def setMoney(number):
    n = str(number)
    for i in n:
        time.sleep(.4)
        gui.keyDown(key=str(i))

def clearMoneyBox():
    for i in range(0,5):
        gui.press('delete')
        time.sleep(.1)

def betMode1(money):
    clickToMoney()
    time.sleep(.3)
    clearMoneyBox()
    time.sleep(.3)
    setMoney(money)
    time.sleep(.3)
    clickToDragon()
    time.sleep(.3)
    clickToConfirm()

def betMode2(money):
    clickToMoney()
    time.sleep(.3)
    clearMoneyBox()
    time.sleep(.3)
    setMoney(money)
    time.sleep(.3)
    clickToTiger()
    time.sleep(.3)
    clickToConfirm()
