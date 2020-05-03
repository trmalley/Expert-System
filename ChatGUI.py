from Tkinter import *
import ttk
import tkMessageBox
import ScrolledText
import time
from PIL import Image, ImageTk

'''
GUI Class
Runs the GUI including input box, chat box, button and pictures
'''
class ChatGUI:
    
    '''
    GUI init
    The bot is passed to the gui so that the gui can access bot methods
    The root frame is binded to the master class
    The window title and size are set
    '''
    
    def __init__(self, rootFrame, bot):#BOT passsed bot instance to this class so it should be able to access bot functions
        self.bot = bot                  
        self.rootFrame = rootFrame #Binds master class to ChatGui class
        self.rootFrame.wm_title("ChatBot") #Window title
        self.rootFrame.geometry("730x610") #Main Window Size
        self.rootFrame.resizable(False,False) #cant resize window
        self.start() #runs start() method
        
    '''
    Start Method
    Systematically starts gui components 
    '''
    def start(self):
        self.containers() #init the containers for the GUI
        self.scrollWidgets() #Init the scroll widgets for the GUI
        self.buttons() #Init buttons for the GUI
        self.count = 0
        self.solution = []
    '''
    Containers
    This method creates all the containers in the gui

        Label Frames were used for testing/dev purposes but now changing
        them to normal frames breaks
    '''   
    def containers(self):
        #Chat box frame that holds the chat window
        self.chatBoxFrame = ttk.LabelFrame(self.rootFrame,width=550, height=450, text="Chat Box")
        self.chatBoxFrame.grid(column=1, row=1, padx=10, pady=0, ipadx=0, ipady=0, sticky=W)

        #input Box frame that holds the user input entry widget
        self.inputBox = ttk.LabelFrame(self.rootFrame,width=550, height=150, text="Input Box")
        self.inputBox.grid(column=1, row=2, padx=10, pady=0, ipadx=0, ipady=0)

        #Agent box to hold picture of the Agent
        self.agentBox = ttk.LabelFrame(self.rootFrame,width=100, height=100, text="Agent")
        self.agentBox.grid(column=2, row=1, padx=10, pady=0, sticky=N)
        
        #User button box to hold an enter button for the user
        self.userButBox = ttk.LabelFrame(self.rootFrame,width=100, height=100, text="")
        self.userButBox.grid(column=2, row=2, padx=10, pady=0, sticky=N)
    '''
    Widgets
    This method creates the ChatBox and InputBox for the user
    '''
    def scrollWidgets(self):
        self.chatScroll = ScrolledText.ScrolledText(self.chatBoxFrame, width=65)
        self.chatScroll.grid(column=0)
        self.chatScroll.config(state=DISABLED)
        self.userInput = Entry(self.inputBox, width=85)
        self.userInput.pack(side=LEFT, ipady=50)

    '''
    This command takes the user input from the input box, displays it in the chat box and deletes it.
    It also does some preliminary parsing and logic/talks with the bot.
    '''
    def enter_command(self):
        input1 = self.userInput.get()#takes user input 
        input1.strip()#Removes and extras
        self.updateChatUser(str(input1)) #displays it in chat  
        self.userInput.delete(0, 'end') #deletes input from entry widget
        print(" ##: " + str(self.bot.QAkp))#Prints bots Question/Anwser keypair for debug only
        print(self.bot.valueList) #Prints bot value list, for debug only

        #Self.bot.Q_Sequence is False until a goal is obtained
        if self.bot.Q_Sequence: #if the bot is expecting questions answer has to be yes or no
            if 'yes' in input1:
                self.bot.QAkp.update({str(self.bot.valueList[self.count]):'yes'})                    
            elif 'no' in input1:
                self.bot.QAkp.update({str(self.bot.valueList[self.count]):'no'})
            else:#This loops back to the beginning of this method (user didint enter yes or no, ask again)
                return self.updateChatBot("Sorry I don't understand.\n"+str(self.bot.currentQ)) 
           
            self.count = self.count + 1  #increments counter to know how many questions have been asked.
            
            print(self.bot.QAkp) #Again for debud
            
            self.solution = self.bot.FindSol(self.bot.QAkp)  #Tries to find a solution given the current anwsers

            if len(self.solution) == 0: #If there is no solution
                print("No solution found yet") #print this message (For Debug)
                talk = self.bot.askQuestion() #Ask another question
            if len(self.solution) == 0 and len(self.bot.questions) == 0:#If there is no solution and no more questions
                print("There is no solution")
                #The knowledge base does not have a solution, reset bot and ask again
                return self.resetBotInstance("It seems I do not have a solution!")

            if len(self.solution) > 0: #There is atleast one solution. display solution and reset
                self.resetBotInstance(self.solution[0])
            self.updateChatBot(talk)
 
        
        if self.bot.goal == None: #Bot has no goal
            talk = self.bot.getGoal(input1)  #<- FOR BOT SEE IT WORKS!!!
            if talk == " ":
                self.bot.goal = None
                return self.updateChatBot("Sorry I don't understand.\n Can you repeat the question?")#user asked something not in knowledge base
            #There is a goal, get questions and being Question Sequence
            talk = str(talk)
            self.updateChatBot(talk)
            self.bot.Q_Sequence = True
            talk = self.bot.askQuestion()
            self.updateChatBot(talk)

    '''
    This resets the bot instance. Resets bot instance variables
    Should make bot act like first loop when program is first loaded
    '''
    def resetBotInstance(self, talk):
        self.updateChatBot(talk)
        self.solution = []
        print(self.solution) #For debugging
        self.count = 0
        self.bot.__init__() #This is actually what resets the bot
        return self.updateChatBot("Please type any issues that may be occuring.")#Sends message to the user asking for another goal

    '''
    buttons
    Inits buttons ans well as the stock photo of the chat bot
    '''
    #Inits buttons for use by user
    def buttons(self):
        self.enterButton = Button(self.userButBox, text="Send", command = self.enter_command, height = 2, width = 10)
        self.enterButton.grid(column=0, row=0)

        size = 130, 130
        self.imgFile = 'bin/agent.png' #gets image from bin
        self.img = Image.open(self.imgFile)#Opens file
        self.img = self.img.resize(size, Image.ANTIALIAS) #no idea but dosent work without it
        self.ph = ImageTk.PhotoImage(self.img) #sets image
        self.image = Label(self.agentBox, image = self.ph)
        self.image.pack()#Place on frame

    '''
    Update Chat User - Update Chat Bot - Update Chat

    These threee methods are the same, it is to prefix the Chat Box with the appropriate title
    This could be made into one method with a userType passed in. However this seemed easier to program
    and for readability to be able to differentiate who was sending the message.
    '''
    #Input text to chat window with "User: " prefix - For User
    def updateChatUser(self, text):
        userType = "User: "
        self.chatScroll.config(state=NORMAL)
        self.chatScroll.insert('end', userType + text + "\n \n")
        self.chatScroll.see("end")
        self.chatScroll.config(state=DISABLED)
   #Input text to chat window with "Agent: " prefix - For BOT
    def updateChatBot(self, text):
        userType = "Agent: "
        self.chatScroll.config(state=NORMAL)
        self.chatScroll.insert('end', userType + text + "\n \n")
        self.chatScroll.see("end")
        self.chatScroll.config(state=DISABLED)
   #Input text to chat window Backup with "System: " prefix - For system messages
    def updateChat(self, text):
        userType = "System: "
        self.chatScroll.config(state=NORMAL)
        self.chatScroll.insert('end', userType + text + "\n \n")
        self.chatScroll.see("end")
        self.chatScroll.config(state=DISABLED)
