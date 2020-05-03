# Expert-System Chat Bot
Trivial expert system to diagnose computer related problems.
                                                                  
The program is designed to work as an expert system chat bot. The program was designed not using an expert system shell for a class project. There are more efficient ways to solve this problem

The knowledge base is an XML file in the "bin" folder. In theory any knowedge base that follows this format can be used.

-------------------------------------------------------------------------------------------

The following are "issues" that the program can "solve" (Goal)

When the program asks for an issue or "how can i help you?" input one of these.
Exact wording is not necessary however it is recommended to use atleast the words below
	
	-computer wont turn on (For example: my computer does not want to turn on)
	Operating system wont load (For example: my operating system refuses to load)
	Computer has no display ...
	Computer does not POST ...
	Computer is slow ...
	
	user input: my computer wont turn on  -> becomes ['my','computer','wont','turn','on']
    Goals ..                        example Goal0  ->['my','operating','system','wont','load',]
                                    example Goal1  ->['my','computer','wont','turn','on']
	
The program tries to match the most number of words from the input to the goal
Any other types of input may crash the program


The program will then ask a series of questions to find a solution
The system expects yes/no. If it does not find this it should keep asking

This type of input should work.
	yes my computer is plugged in

	The system tries to find one occurence of yes or no in the users input.
	
It is recommneded to avoid capitals and any types of punctuation or special characters eg(! , ? - ] { * &)
Input is cleansed but it may still cause problems as there are no checks for these specifically

I have tested multiple routes through the knowledge base, I am able to achieve more than 5 goals.
However for some unknown reason the program will sometimes return as "Unable to find solution"
when there is indeed a solution. 

*If the program crashes or fails to respond, close the program and restart.

Everything that I normally "print" will show up in console that opens up.
This is dual purpose for debugging and to see the system logic in real time.
