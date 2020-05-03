import xml.etree.ElementTree as ET
import random

'''
Chat Bot Class
Handles most of the logic behind parsing the knowledge base
Finds the goals, questions, and applies them to the rules to find a solution
'''
class ChatBot:

    '''
    Bot INIT
    Many instance variables
    Not all of them needed to be instance variables
    Manry were set during programming to debug and now im to scared to change them back
    '''
    def __init__(self):
        print("ChatBot")
        self.botName = "Charles"
        self.tree = ET.parse('bin/fnr.xml') #Gets XML file from bin folder
        self.root = self.tree.getroot() #Gets all elements in xml file
        self.xpath = self.root.findall("./goals/goal") #Gets all goals
        self.rules = self.root.findall("./rule") #Get all rules
        self.inputSplit = [] #Sotrage for splitting the input to isolate yes/no for questions
        self.interMatch = [] #used for sotrage to check each word of user input
        self.questions = [] #List of questions from goal
        self.goal = None #current goal
        self.currentQ = None #current question
        self.QAkp =  {} #Question Answer disctionary eg {'plugged':'yes'}
        self.Q_Sequence = False #question sequence False by default
        self.valueList = [] #Has values from knwoledge base
        self.solution = [] #A list of possible solutions
        self.RuleID = None #RuleID. used to find a solution from a rule
        self.solutions = [] #Another list of solutions for some reason
        self.maxIndex = None #Index with the max value see getGoal()
        self.maxValue = None #Max value see getGoal()
        self.mostMatches = 0 #temp variable to store the most number of rule matches
        self.MM_ID=None #Replacement rule id


    #parse user input and send a response
    '''
    Get Goal
    This method is used to get a goal based on the user input. It takes the users input, splits the words
    and checks against the goals. The goal with the most intersections becomes the current goal
    eg.
    user input: my computer wont turn on  -> becomes ['my','computer','wont','turn','on']
    Goals ..                                Goal0  ->['my','operating','system','wont','load',]
                                            Goal1  ->['my','computer','wont','turn','on']

    Since the user input intersects more often with Goal1. Goal1 is elected to be the curent goal.
    
    '''
    def getGoal(self, input1):

        #words = ['computer', 'wont', 'turn', 'on'] #Temporary testing input
        input1 = input1.lower() #All input is changed to lower case
        resp = input1.split() #Splits input
        for i in range(len(self.xpath)): #for loop will loop depending on the number of goals
            self.inputSplit.append(self.xpath[i].text.lower().split()) #Splits the goals
        for i in self.inputSplit: #Checks for intersections
            intersection = list(set(i).intersection(set(resp)))
            self.interMatch.append(len(intersection))
            #Max index
            
        self.maxIndex = self.interMatch.index(max(self.interMatch))
        self.maxValue = max(self.interMatch) #The goal with the most matches. Eg if MaxValue = 0 then that means Goal0

        
        if self.maxValue == 0: #Did not find a goal. returns empty string to enter command
            return " "

        '''
        Store the number of matches into an array, then find the largest value
        and take the corresponding index  to use with self.goal to get the
        problem from the user. if there are no matches for anything go to the
        last index to say "I dont know what the problem is, sorry!" this
        index will be called maxIndex
        '''
        
        if self.maxValue >= 1:
            #uses the max index to get questions pertaining to goal
            #see maxIndex comments above
            q = "[@goal=\'"+str(self.maxIndex)+"\']"

            self.goal = self.root.findall("./goals/goal"+q) #Gets goals from knowledge base
            
            xpath = self.root.findall("./question//goal"+q+"../description")#Gets the goal descriptions

            '''
            This doule for loop gets the questions that are realted
            to a specific goal
            '''
            for i in xpath:
                self.questions.append(i.text)

                desc = "[description=\'"+str(i.text)+"\']"

                xpath = self.root.findall("./question/"+desc+"./option/then/fact")
                for p in xpath: #gets all attribute names for questions for goal
                    if p.attrib['name'] not in self.valueList:
                        self.valueList.append(p.attrib['name'])
                            #example output ['plugged', 'outlet', 'voltage'...ect]
                            #this is stored in newList
        print(self.questions) #For debug
        print(self.valueList) #for debug
        return "I am analyzing this issue, please give me a few moments" #Tells the user to wait.
            
    '''
    askQuestions
    Loops through the questions, asking the user and storing the input in self.QAkp
    Once a question is asked it is removed from the array
    '''
    def askQuestion(self):
        anwser = " "
        #No more questions
        if len(self.questions) == 0:
            self.Q_Sequence = False
            self.solution = self.FindSol(self.QAkp)
            #return "This should be the solution"
            return self.solution[0]
        #1 or more questions   
        if len(self.questions) >= 1:
            print(" CQ: " + str(self.currentQ))#debug
            self.currentQ = str(self.questions[0]) #sets current question
            print(" CQ: " + str(self.currentQ))#debug
            self.questions.remove(self.currentQ)#Removes question from array
        return str(self.currentQ)
        
        #return str(self.questions[0])
        
    '''
    FindSol
    This Method finds a solution, effectively it is the "Inference Engine"
    3 nested for loops = Cluseter Fuck
    
    '''

    def FindSol(self, keypair):
        #keypair = {'plugged':'yes', 'beeps':'no', 'fans':'no', 'outlet':'yes', 'voltage':'no'} #temp for testing
        print(str(self.goal))
        g = "[@goal=\'"+str(self.maxIndex)+"\']"#This is used to parse the xml and get the goal
        print g
        for m in self.rules: #effectively says FOR ALL THE RULES
            
            var = "[@id=\'"+m.attrib['id']+"\']" #parsing
            ruleFacts = self.root.findall(".//rule/"+var+"/goal/"+g+"../if//fact") #More parsing
            matches = 0
            print("RuleID: " + m.attrib['id']) #debug
            
            for i in ruleFacts:#For all the Facts that make up the rules
                print i.attrib['name'] + " : " + i.text#debug

                
                for j in keypair:#Finds matches between user responses and the facts for the rules
                    
                    if i.attrib['name'] == j and i.text == keypair[j]: #IF they match
                        print "-"+j + " : " + keypair[j]
                        matches = matches + 1 #increase match count
                         #print "Rule: " + i.attrib['name'] + " " + i.text
                         #print "Fact: " + j + " " + keypair[j]
                        self.RuleID = m.attrib['id']
                        if matches == len(ruleFacts): #If the number of matches, matches the number of facts for that rule exit early
                            print("found way out early")
                            self.mostMatches = matches
                            self.MM_ID =  m.attrib['id']#Sets RuleID
                            var = "[@id=\'"+self.MM_ID+"\']"
                            xpath = self.root.findall(".//rule/"+var+"/then/fact")
                            for i in xpath: #To parse solutions
                                self.solutions.append(i.text)
                            return self.solutions #soltuion
            print "Matches: " + str(matches)     
            #print(self.RuleID)
            #print("-----\n")
            if matches > self.mostMatches: #if the next rule has more matches than the previous it is the new candidate 
                self.mostMatches = matches
                self.MM_ID =  m.attrib['id']
            print ("----END Rule-----")
        if self.mostMatches != len(ruleFacts): #not all the facts of a rule were matched
            self.mostMatches = 0
            return self.solutions
        if self.mostMatches == 0: #There were no matches == no solutions available in knowledge base
            print("Sorry I dont know how to help!")
            self.solutions.append("Sorry I dont know how to help!")
            return self.solutions
        print("The Rule with the most Matches: " + self.MM_ID)

        #I dont think this does anothing anymore, the previous if statements should catch before
        if self.MM_ID != None:
            var = "[@id=\'"+self.MM_ID+"\']"
            xpath = self.root.findall(".//rule/"+var+"/then/fact")
            for i in xpath:
                self.solutions.append(i.text)
                self.RuleID = None
                print("##########################")
                print(self.solutions)
                return self.solutions


        '''
        Standard greetings that were used in early version.
        Would respond to any "greetings" with any greetResponse
        Was trying to make the bot seem more "real". It caused
        problems and was removed.
        
        greetings = ['hello', 'hi', 'hey', 'bonjour']
        greetResponse = ['Hello!', 'hey', 'oui allo', 'ci']
        input = input.strip()
        if input in greetings:
            return greetResponse[random.randint(0,3)]
        if input == "":
           return "Are you there?"
        else:
            return "Sorry I dont understand!"
        '''
        
