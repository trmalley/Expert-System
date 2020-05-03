from Tkinter import *
import ttk
import tkMessageBox
import ScrolledText
from ChatBot import *
from ChatGUI import *

'''
ChatController Class
Initializes the GUI and the ChatBot and connects them

This project can be compiled with
pyinstaller setup.spec ChatController.py
'''
class Chat:

    #init the master class
    def __init__(self, master):
        self.master = master
        self.new_window()

    #builds and initializes the gui and bot
    def new_window(self):

        #bot init see ChatBot
        self.bot = ChatBot()

        #Gui initi see ChatGUI
        self.gui = ChatGUI(self.master, self.bot)

        #binds the enter button for the user input to the enter() method
        #when enter is pressed the enter method is called 
        button = self.gui.enterButton
        self.master.bind('<Return>', (lambda event: self.enter()))        
        #welcome msg from the system
        self.gui.updateChat("Welcome to the chatbot 4000 \n")
        self.gui.updateChatBot("Hello there! My name is " + self.bot.botName + ". How can I help you today?") 
        
    '''
    Connects both ChatGui and ChatBot when the user inputs some text in the gui,
    it is sent to the bot via the GUI. This is so that the user can use both the
    enter button on the gui and the keyboard
    
    '''
    def enter(self):
        self.gui.enter_command()

#forgot why this is but DONT FUCK WITH IT
def main(): 
    root = Tk()
    app = Chat(root)
    root.mainloop()
#Same with this!!!!!!!!!!
if __name__ == '__main__':
    main()
