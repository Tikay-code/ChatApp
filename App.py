import socket
import tkinter as tk
from tkinter import messagebox
import sys
import threading
import random

App = tk.Tk()
App.geometry("1200x700")
App.title("Chat App")
App.resizable(width=False, height=False)
App.iconbitmap("Images/Chat App Icon.ico")

# Fonts To Use: Gabriola, Impact, Courier New, Corbel Light, Consolas, Comic Sans MS, Candara Light, Arial Black


### Variables ###
Name = ""
output = ""
Smiles = '''
:happy - \U0001F604                             
:sad - \U0001F61E                             
:raised_eyebrow - \U0001F928                             
:heart_eyes - \U0001F60D                             
:kissing_face - \U0001F617                             
:zany - \U0001F92A                             
:money_mouth - \U0001F911                             
:smiling - \U0001F642                             
:winking - \U0001F609                             
:laughs - \U0001F602                             
:embarrassed - \U0001F605                             
'''


def TextConvert(WhatToConvert):
    global output
    words = WhatToConvert.split(" ")
    emojisAndCurses = {
        # emojis:
        ":happy": "\U0001F604",
        ":sad": "\U0001F61E",
        ":raised_eyebrow": "\U0001F928",
        ":heart_eyes": "\U0001F60D",
        ":kissing_face": "\U0001F617",
        ":zany": "\U0001F92A",
        ":money_mouth": "\U0001F911",
        ":smiling": "\U0001F642",
        ":winking": "\U0001F609",
        ":laughs": "\U0001F602",
        ":embarrassed": "\U0001F605",
        # Censorship of curses
        "Fuck": "F***",
        "Fuk": "F**",
        "Bitch": "Bi***"
    }

    output = ""
    for word in words:
        output += emojisAndCurses.get(word, word) + " "


def Home():
    WelcomeFrame.destroy()
    DetailsFrame.destroy()

    HomeFrame = tk.Frame(App, bg="#ccc")
    HomeFrame.pack(side="bottom", fill="both", expand=True)

    StatusFrame = tk.Frame(HomeFrame, bg="#ccc", width=220)
    StatusFrame.pack(fill="y", side="left", anchor="center")

    SmilesFrame = tk.Frame(HomeFrame, bg="#ccc", width=300)
    SmilesFrame.pack(fill="y", side="right")

    SmileLabel = tk.Label(SmilesFrame, text="\n" + Smiles, font=("Candara Light", 13), bg="#ccc", anchor="center")
    SmileLabel.pack(side="top")

    UserName = tk.Label(StatusFrame, text="Name: " + Name + "\n\nOnline Users:", bg="#ccc", font=("Candara Light", 15), fg="black", anchor="center")
    UserName.pack(side="top")

    App.title("Chat App - Home")

    Chat = tk.Frame(HomeFrame, width=500)

    ChatFrame = tk.Canvas(Chat, height=650, width=500)
    scroll_bar = tk.Scrollbar(Chat, command=ChatFrame.yview)

    scroll_bar.config(command=ChatFrame.yview)
    scroll_bar.pack(side="right", fill="y")
    scrollable_frame = tk.Frame(ChatFrame)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: ChatFrame.configure(
            scrollregion=ChatFrame.bbox("all")
        )
    )

    ChatFrame.create_window((0, 0), window=scrollable_frame, anchor="nw")
    ChatFrame.configure(yscrollcommand=scroll_bar.set)

    Chat.pack(fill="y", expand=True)
    ChatFrame.pack()
    scroll_bar.pack()

    ### Login To The Server ###
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        HOST = "192.168.14.66"
        PORT = 7500

        client.connect((HOST, PORT))

        client.send(Name.encode("utf-8"))

        ClientsUsernames = client.recv(1024).decode("utf-8")
        ClientsUsernamesList = []
        for user in ClientsUsernames.split("\n"):
            ClientsUsernamesList.append(user)

        ClientsUsernamesLabel = tk.Label(StatusFrame, text="", bg="#ccc", font=("Candara Light", 15), fg="black", anchor="center")
        ClientsUsernamesLabel.pack(side="top")

        def OnlineUsers():
            #for username in ClientsUsernamesList:
            ClientsUsernamesLabel.config(text="\n".join(ClientsUsernamesList))

        OnlineUsers()
        UserChatFrame = tk.Frame(Chat)
        UserChatFrame.pack(side="bottom")

        MassageEntry = tk.Entry(UserChatFrame, borderwidth=0, width=50, font=("Candara Light", 12))
        MassageEntry.grid(row=0, column=0)

        def SendMassage():
            if len(MassageEntry.get()) != 0:
                clientName = Name
                clientMassage = MassageEntry.get()

                # Add a feature that converts Kaomoji to Emoji

                TextConvert(clientMassage)

                client.send(clientName.encode("utf-8"))

                Massages = tk.Label(scrollable_frame, text="You: " + output, font=("Comic Sans MS", 11))
                Massages.pack(side="top", anchor="nw")
                client.send(clientMassage.encode("utf-8"))

                MassageEntry.delete(0, tk.END)

        ButtonSendMassage = tk.Button(UserChatFrame, bd=0, width=10, bg="#d9d9d9", text="Send", font=("Consolas", 10), command=SendMassage)
        ButtonSendMassage.grid(row=0, column=1)

        MassageEntry.bind("<Return>", lambda Event: SendMassage())

        def ReceivedMassage():
            while True:
                serverMassage = client.recv(1024).decode("utf-8")

                if serverMassage.find("Join To The Server") == -1:
                    pass
                else:
                    NewUser = serverMassage.replace(" Join To The Server", "")
                    ClientsUsernamesList.append(NewUser)
                    OnlineUsers()

                if serverMassage.find("disconnect") == -1:
                    pass
                else:
                    DisconnectUser = serverMassage.replace(" disconnect", "")
                    ClientsUsernamesList.remove(DisconnectUser)
                    OnlineUsers()

                TextConvert(serverMassage)

                Massages = tk.Label(scrollable_frame, text="" + output, font=("Comic Sans MS", 11))
                Massages.pack(side="top", anchor="nw")

        recvThread = threading.Thread(target=ReceivedMassage)
        recvThread.daemon = True
        recvThread.start()

    except ConnectionResetError:
        sys.exit()

    except ConnectionRefusedError:
        sys.exit()

    except ConnectionAbortedError:
        sys.exit()


def init():
    def Welcome():
        global WelcomeFrame, DetailsFrame

        WelcomeFrame = tk.Frame(App, width=200)
        WelcomeFrame.pack(side="bottom", fill="both", expand=True)

        WelcomeLabel = tk.Label(WelcomeFrame, text="Welcome To Chat App :)\n\nPlease Pick A Name To Continue\n",
                                font=("Candara Light", 15))
        WelcomeLabel.pack()

        DetailsFrame = tk.Frame(WelcomeFrame)
        DetailsFrame.pack()

        # Fill The Name
        NameLabel = tk.Label(DetailsFrame, text="Name:", font=("Comic Sans MS", 12))
        NameInput = tk.Entry(DetailsFrame, width=30, borderwidth=0, font=("Consolas", 10))
        NameLabel.grid(row=0, column=0)
        NameInput.grid(row=0, column=1)

        EntryText = tk.Label(DetailsFrame, text="  ")
        EntryText.grid(row=0, column=2)

        def RandomName():
            Names = ["Jonatan", "Rick", "Yarin", "Mike", "Jack", "Noah", "Daniel", "Conor", "James", "Finn", "Alex",
                     "Ryan", "Oliver", "Harry", "Michael", "Adam", "Liam", "Leo", "Lagon", "Mia", "Ella", "Olivia", "Oscar", "Arthur"]
            UserName = random.choice(Names)
            NameInput.delete(0, tk.END)
            NameInput.insert(0, UserName)

        RandomNameBtn = tk.Button(DetailsFrame, text="Random", bd=0, font=("Corbel Light", 10), command=RandomName)
        RandomNameBtn.grid(row=0, column=3)

        def CheckName():
            global Name
            if len(NameInput.get()) == 0:
                tk.messagebox.showerror("Valid Length", "Name length can't be 0")
            else:
                Name = NameInput.get()
                Home()

        ContinueImage = tk.PhotoImage(file="Images/Continue Button Image.png")
        ContinueButton = tk.Button(WelcomeFrame, image=ContinueImage, bd=0, command=CheckName)
        ContinueButton.image = ContinueImage
        ContinueButton.pack()

        NameInput.bind("<Return>", lambda Event: CheckName())

    Welcome()


init()
App.mainloop()

# Finally with 322 lines of code