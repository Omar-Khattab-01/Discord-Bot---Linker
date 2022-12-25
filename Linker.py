#My first bot

import os
import urllib
import json
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import has_permissions
from discord.ext.tasks import loop
from win10toast_click import ToastNotifier
import random
import urllib.request
from datetime import datetime
from win10toast_click import ToastNotifier
import tkinter as tk
from tkinter import *
from decimal import Decimal
import webbrowser

noti = ToastNotifier()

top = 0
label = 0
canvas = 0
img = ""

def makeWindow():
    global top, label, canvas, img
    top = tk.Tk()
    top.geometry('50x50')
    top.title('shop')
    canvas = Canvas(top, bg="blue", height=250, width=300)
    img = PhotoImage(file="sched.png")
    label = Label(top, image=img)
    label.place(x=0, y=0, relwidth=1, relheight=1)
    label.place(x=0, y=0)


def notify():
    global noti, top
    noti.show_toast('Random', 'Hello World', threaded=True, callback_on_click=open_link)
    top.destroy()
    

class AppURLopener(urllib.request.URLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
dic = {}
keyWords = {}
fileName = "links.txt"
link = ""

##client2 = binance.Client("OGrXiM0h6J51ulhAuc9wpGgwccXeGcNvHGQp5o5hhK8zUoTZ2KBq9vnSorqBC5yU", "BdgNPIderDvov5gm9677dZj1rCpGkEt8VWK8IGgRjcwL5NY4sgZEYYk3vaYgXEIk")
def open_link():
    global link
    webbrowser.open(link)


@tasks.loop(seconds=60.0)
async def printer():
    global link, noti
    now = datetime.now()
    current_time = str(datetime.today().weekday()) + now.strftime("%H:%M")
    # print(current_time)
    if current_time in keyWords:
        link = dic[keyWords[current_time].lower()]
        makeWindow()
        noti = ToastNotifier()
        btn = Button(top, text="Enter", command=notify)
        btn.pack()

        top.mainloop()


def aquire_loop_status(fileName):
    links = open(fileName).read().split()
    if links[0] == "***True":
        printer.start()


aquire_loop_status(fileName)


def aquire_Json(url):
    response = opener.open(url)
    data = json.loads(response.read())
    return data


def populate():
    x = 0
    links = open(fileName).read().split("\n")
    for line in links:
        line = line.split()
        if len(line) != 1 and len(line) != 0:
            # print(line)
            dic.update({line[0]: line[1]})
            keyWords.update({line[2]: line[0]})

def add(key, link, time):
    dic.update({key.lower(): link})
    keyWords.update({time: key.lower()})
    file = open(fileName).read().split("\n")
    write = open(fileName, "w")
    write.write("\n"+key + " " + link + " " + time + "\n")
    
           
def cryptofetch():
    data=aquireJson('https://api.binance.com/api/v3/klines?symbol=DOGEBUSD&limit=1&interval=1m')
    return float(data[0][4])


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

client.counter = 1
client.flag = True





bot = commands.Bot(command_prefix='>')



@bot.command(name='doge', help = 'Returns the price of doge')
async def doge(ctx):
    
    dogePrice = cryptofetch()
    await ctx.send(dogePrice)

@bot.command(name='stopbelow', help = 'stop below ')
async def doge(ctx):
    
    client.flag = False


@bot.command(name='below', help = 'Returns if price go below a price')
async def below(ctx , price, tag1, tag2):
    flag = True
    while flag:
        dogePrice = cryptofetch()
        if dogePrice < float(price):
            flag = False
            await ctx.send("Doge price went below "+price+" Doge - >"+str(dogePrice)+" "+tag1+" "+tag2)

@bot.command(name='add', help='adds link to the dic')
async def addLink(ctx, key, time, link):
    if key in dic:
        await ctx.send("keyword: (" + key + ") was used before. Please use a different keyword.")
    else:
        add(key, link, time)


@bot.command(name='>', help='opens lectures zoom link')
async def show(ctx, t):
    try:
        # print(dic)
        webbrowser.open(dic[t.lower()])

    except:
        await ctx.send(t + " not found")


@bot.command(name='?', help='lists all keywords and links saved in database')
async def list(ctx):
    file = open(fileName).read()
    file2 = "keywords -> link\n\n" + file
    await ctx.send(file2)


@bot.command(name="clr")
async def clear(ctx):
    file = open(fileName, "w")
    file.write("")


@bot.command(name="enableauto")
async def enable(ctx):
    try:
        printer.start()
        with open('links.txt', 'r') as file:
            filedata = file.read()
        # Replace the target string
        filedata = filedata.replace('**False', '**True')

        # Write the file out again
        with open('links.txt', 'w') as file:
            file.write(filedata)
        print("Auto on")
    except:
        print("Already on")

@bot.command(name="disableauto")
async def disable(ctx):
    printer.cancel()
    with open('links.txt', 'r') as file:
        filedata = file.read()
    # Replace the target string
    filedata = filedata.replace('**True', '**False')

    # Write the file out again
    with open('links.txt', 'w') as file:
        file.write(filedata)
    printer.stop()
    print("Auto off")

def populateAll():
    populate()

populateAll()
bot.run(TOKEN)
on_ready()
            
        
##    await ctx.send("Doge price went below "+price+" Doge - >"+str(dogePrice)+" "+tag)
##    await ctx.send("#below "+price+" "+tag)

##@bot.command(name='above', help = 'Returns if price go above a price')
##async def above(ctx , price, tag):
##    dogePrice = cryptofetch()
##    while client.flag:
##        if dogePrice > float(price):
##            await ctx.send("Doge price went above "+price+" Doge - >"+str(dogePrice)+" "+tag)
##            price = str(dogePrice)
##            dogePrice = cryptofetch()
##        else:
##            dogePrice = cryptofetch()    



    


