import random

#Defie a "main" function that will start the quiz, print the score, and pint "Done"
def main():
    #Create a Quiz object
    quiz = Quiz()
    #Start the quiz
    quiz.start()
    #Print the user's score and the totl number of questions
    print(f"Your score is {quiz.score}/{quiz.TOTAL_QUESTIONS}")
    #Print "Done" to indicate that the program has finished running
    print("Done")

#Creat a Quiz class that will keep track of the user's score and the current question
class Quiz:
    #Define an __init__ method that wil initialize the class with the total number of questions,
    #the maximum number of wrong trials, the user's score, the current question number, and the number of wrong trials
    def __init__(self):
        self.TOTAL_QUESTIONS =10
        self.MAX_WRONG_TRIALS = 5
        self.score = 0
        self.current_question = 0
        self.wrong_trials = 0

    #Define a start method that will begin the quiz and coninue until the user has answered all the questions
    #or until they have excededed the maximum number of wrong trials
    def start(self):
        #Print a message to inform the user that they can press "q"  to quit the quiz
        print('Press "q" to quit quiz\n')
        #Primpt the user to enter "START" to begin the quiz
        quiz_prompt = input("Type START: ").strip().upper()
        #While the user has not answered all of the questions,
        #and they have not exceeded the maximum number of trials
        while self.current_question < self.TOTAL_QUESTIONS:
            #If the user entered "START"
            if quiz_prompt == "START":
                #Increase the current question number by 1
                self.current_question += 1
                #Print the question number
                print(f"Question No. {self.current_question}")
                #Call the "pick" method to get a random question and prompt the user to answer it
                result=self.pick()
                #If the answer is correct
                if result=="CORRECT":
                    #Increase the user's score by 1
                    self.score+=1
                    #Print "CORRECT"
                    print(result + "\n")
                #If the user answered incorrectly
                else:
                    #Print "INCORRECT" or "INVALID INPUT"
                    print(result + "\n")
            #If the user entered "Q"
            elif quiz_prompt == "Q":
                #Quit the quiz
                quit()
            #If the user entered an invalid input
            else:
                #Increase the number of wrong trials by 1
                self.wrong_trials += 1
                #Print "INVALID INPUT"
                print("INVALID INPUT")
                #Prompt the user to enter "START" again
                quiz_prompt = input("Type START: ").upper()
                #If the user has exceeded the maximum number of wrong trials,
                #Print "TRY AGAIN LATER" and quit the quiz
                if self.wrong_trials == self.MAX_WRONG_TRIALS:
                    print("TRY AGAIN LATER")
                    quit()


    #Define a "pick" method tht will randomly select a question and prompt the user to answer it 
    def pick(self):
        #Generate a random number between 0 and 29
        q=random.choice(range(0,30))
        #find the question associated with the random number
        pick_quest=QuestionAnswer.questions[q]
        #print the question
        print(pick_quest)
        #Get user input for an answer and store it in athe "ans" variable
        ans_list=["A","B","C","D","E","Q"]
        ans=input("Answer: ").strip().upper()
        #Check if answer is valid
        if ans not in ans_list:
            return "INVALID INPUT"
        #Check if answer is correct
        elif ans==str(QuestionAnswer.answers[q]):
            return "CORRECT"
        #Check if user has chosen to quit the quiz
        elif ans=="Q":
            print("\nThank you for participating in our quiz")
            return quit()
        #If the user's answer is incorrect, return "INCORRECT"
        else:
            return "INCORRECT"


class QuestionAnswer:
    #Defining a class attribute, "questions" as tuple that holds the questions and their respecive options
    questions= ("""\n1. Who developed Python Programming Language?
    a) Wick van Rossum
    b) Rasmus Lerdorf 
    c) Guido van Rossum
    d) Niene Stom""", """\n2. Which type of Programming does Python support?
    a) object-oriented programming
    b) structured programming
    c) functional programming
    d) all of the mentioned""", """\n3. Is Python case sensitive when dealing with identifiers?
    a) no
    b) yes
    c) machine dependent
    d) none of the mentioned""", """\n4. Which of the following is the correct extension of the Python file?
    a) .python
    b) .pl
    c) .py
    d) .p""", """\n5. Is Python code compiled or interpreted?
    a) Python code is both compiled and interpreted
    b) Python code is neither compiled nor interpreted
    c) Python code is only compiled
    d) Python code is only interpreted""", """\n6. All keywords in Python are in _________
    a) Capitalized
    b) lower case
    c) UPPER CASE
    d) None of the mentioned""", """7. What will be the value of the following Python expression?
    4 + 3 % 5
    a) 7
    b) 2
    c) 4
    d) 1""", """8. Which of the following is used to define a block of code in Python language?
    a) Indentation
    b) Key
    c) Brackets
    d) All of the mentioned""",  """9. Which keyword is used for function in Python language?
    a) Function
    b) Def
    c) Fun
    d) Define""", """10. Which of the following character is used to give single-line comments in Python?
    a) //
    b) #
    c) !
    d) /*""", """11. Which of the following functions can help us to find the version of python that we are currently working on?
    a) sys.version(1)
    b) sys.version(0)
    c) sys.version()
    d) sys.version""", """12. Python supports the creation of anonymous functions at runtime, using a construct called __________
    a) pi
    b) anonymous
    c) lambda
    d) none of the mentioned""", """13. What is the order of precedence in python?
    a) Exponential, Parentheses, Multiplication, Division, Addition, Subtraction
    b) Exponential, Parentheses, Division, Multiplication, Addition, Subtraction
    c) Parentheses, Exponential, Multiplication, Division, Subtraction, Addition
    d) Parentheses, Exponential, Multiplication, Division, Addition, Subtraction""", """14. What does pip stand for python?
    a) unlimited length
    b) all private members must have leading and trailing underscores
    c) Preferred Installer Program
    d) none of the mentioned""", """15. Which of the following is true for variable names in Python?
    a) underscore and ampersand are the only two special characters allowed
    b) unlimited length
    c) all private members must have leading and trailing underscores
    d) none of the mentioned""", """16. Which of the following is the truncation division operator in Python?
    a) |
    b) //
    c) /
    d) %""", """17. Which of the following functions is a built-in function in python?
    a) factorial()
    b) print()
    c) seed()
    d) sqrt()""", """18. Which of the following is the use of id() function in python?
    a) Every object doesn’t have a unique id
    b) Id returns the identity of the object
    c) All of the mentioned
    d) None of the mentioned""", """19. What will be the output of the following Python function?
    min(max(False,-3,-4), 2,7)
    a) -4
    b) -3
    c) 2
    d) False""", """20. Which of the following is not a core data type in Python programming?
    a) Tuples
    b) Lists
    c) Class
    d) Dictionary""", """21. Which of these is the definition for packages in Python?
    a) A set of main modules
    b) A folder of python modules
    c) A number of files containing Python definitions and statements
    d) A set of programs making use of Python modules""", """22. What will be the output of the following Python function?
    len(["hello",2, 4, 6])
    a) Error
    b) 6
    c) 4
    d) 3""", """23. What is the order of namespaces in which Python looks for an identifier?
    a) Python first searches the built-in namespace, then the global namespace and finally the local namespace
    b) Python first searches the built-in namespace, then the local namespace and finally the global namespace
    c) Python first searches the local namespace, then the global namespace and finally the built-in namespace
    d) Python first searches the global namespace, then the local namespace and finally the built-in namespace""", """24. Which function is called when the following Python program is executed?
    f = foo()
    format(f)
    a) str()
    b) format()
    c) __str__()
    d) __format__()""", """25. Which one of the following is not a keyword in Python language?
    a) pass
    b) eval
    c) assert
    d) nonlocal""", """26. What arithmetic operators cannot be used with strings in Python?
    a) *
    b) –
    c) +
    d) All of the mentioned""", """27. Which of the following statements is used to create an empty set in Python?
    a) ( )
    b) [ ] 
    c) { }
    d) set()""", """28. To add a new element to a list we use which Python command?
    a) list1.addEnd(5)
    b) list1.addLast(5)
    c) list1.append(5)
    d) list1.add(5)""", """29. Which one of the following is the use of function in python?
    a) Functions don’t provide better modularity for your application
    b) you can’t also create your own functions
    c) Functions are reusable pieces of programs
    d) All of the mentioned""", """30. What is the maximum possible length of an identifier in Python?
    a) 79 characters
    b) 31 characters
    c) 63 characters
    d) none of the mentioned""")

    #Defining a list of answers as a class attribute
    answers=["C","D","A","C","B","D", "A", "A", "B", "B", "A", "C", "D", "C", "B", "B", "B", "B", "D", "C", "B", "C", "C", "C", "B", "B", "D", "C", "C", "D"]




if __name__ == "__main__":
    main()

