import os
import pandas as pd
from random import sample
import numpy as np
import csv
import re
import getpass
import matplotlib.pyplot as plt

user_actions = ['Add a new question to the database','Print questions & answers','Take a quiz','Review answers so far', 'Plot user scores', 'Logout']
user_selection = ['Log into an existing account','Create a new account','Quit']
questions_answers_dict = {}
current_user = None
question_df = None
userDict = None

def initializeDbs():
    global question_df
    global userDict
    #Load information from csv files containing question & user databases
    #TODO try to remove the NaN from empty initialization (if csv has to be created from scratch)
    try:
        question_df = pd.read_csv('Questions_answers.csv',index_col=[0,1])
    except:
        print('No existing question database detected')
        question_df = pd.DataFrame(index=[['Question'],['Options']],columns=['Is correct?'])

    try:
        with open('Users.csv', mode='r',newline='') as infile:
            reader = csv.reader(infile, delimiter=';')
            next(reader)
            userDict = {rows[0]:[rows[1],rows[2],rows[3],rows[4]]for rows in reader}
    except:
        with open('Users.csv', mode = 'w', newline = '') as newfile:
            writer = csv.writer(newfile, delimiter = ';')
            writer.writerow(['Username','Password','Quiz Started','Answers given','Score'])
        userDict = {}

def quit():
    global question_df
    question_df.to_csv('Questions_answers.csv')
    exit()
    
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def listStringToStringList(string):
    #Converts a string of form [a,b,c] into the corresponding list
    newList = string.strip('][').split(', ')
    if newList == ['']:
        return list([])
    newList = [element.strip('\'') for element in newList]
    return newList

def add_questions():
    global question_df
    clearConsole()
    question = input('Type in your new question for the quiz:\n')

    while True:
        try:
            answer_option_count = int(input('How many possible answer options would you like to add?:\n'))
            break
        except ValueError as ex:
            print(ex,'\nInvalid amount of quesitons specified')

    possible_answers = [input('Enter Option {}:\n'.format(i+1)) for i in range(answer_option_count)]
    clearConsole()
    
    print('Question:\n'+question+'\n\nFrom the given options:\n')
    for i in range(len(possible_answers)):
        print(str(i+1)+': '+possible_answers[i])
    
    while True:
        
        correct_index_str = input('\nPlease list the indices of all answers which are considered correct (separated by commas if multiple answers are correct):\n')
        if correct_index_str == '':
            answer_option_count += 1
            correct_index_list = [answer_option_count]
            possible_answers.append('None of the above')
            break
        
        try:
            correct_index_list = [int(index) for index in correct_index_str.split(',')]
        except:
            print('Solution input not recognized - either input a single integer or a list of integers separated by a comma')
            continue
        
        faulty_entries = set(correct_index_list).difference(range(1,answer_option_count+1))

        if  len(faulty_entries) != 0:
            print('Error: The given indices {} are not among the possible indices of 1-{}\n'.format(faulty_entries,answer_option_count))
            continue
        break
    
    clearConsole()
    print('Confirming new entry:\n')
    print('Question:\n' \
        +question +'\n\n'\
            +'Options:\n')
    for index, answer in enumerate(possible_answers):
        print('{}:  {}'.format(index+1,answer))
    print('Correct answers:',correct_index_list)
    
    while True:
        confirmation = input('Is this entry correct? (Y/N)\n').upper()
        if confirmation == 'N':
            clearConsole()
            print('Entry discarded - returning to main menu')
            break
        elif confirmation !='Y' and confirmation != 'N':
            print('Invalid input - please type either Y for yes or N for no')
        else:
            name = 'Question {}'.format(len(questions_answers_dict.keys()))
            questions_answers_dict[name] = (question,possible_answers,correct_index_list)
            clearConsole()
            question_df = pd.concat([question_df,question_to_df(question,possible_answers,correct_index_list)])
            print('Entry added to the database - returning to main menu')

            break

def print_questions():
    clearConsole()
    global question_df
    print('',question_df.fillna(''))

def question_to_df(question,options,correct):
    index = pd.MultiIndex.from_product([[question],options],names=['Question','Options'])
    df = pd.DataFrame(data = [answer in correct for answer in range(1,len(options)+1)],index = index, columns=['Is correct?'])
    return df

def generate_quiz():
    print('generating new quiz')
    global question_df
    global userDict
    QUIZ_QUESTION_COUNT = 5
    possible_questions = list(set(question_df.reset_index(level=[1]).index[1:]))
    # Make sure that the quesiton database is not empty
    assert len(possible_questions) != 0
    true_quiz_length = min([QUIZ_QUESTION_COUNT,len(possible_questions)])
    questions_sample = sample(possible_questions,true_quiz_length)
    userDict[current_user][1] = questions_sample
    # Immediately commit changes to csv file
    commitUserChanges()
    
def take_quiz():
    clearConsole()
    no_answers_df_copy = question_df.copy()
    no_answers_df_copy['Is correct?'] = ''
    questions = listStringToStringList(userDict[current_user][1])
    if len(questions) == 0:
        generate_quiz()
    questions = listStringToStringList(userDict[current_user][1])
    answers = listStringToStringList(userDict[current_user][2])
    # print('Questions: ' + str(questions))
    # print('Answers: ' + str(answers))
    alreadyAnswered = 0
    for _ in answers:
        alreadyAnswered += 1

    if len(questions) == alreadyAnswered:
        print('Quiz already finished with score ' + userDict[current_user][3])
        return None
    if alreadyAnswered > 0:
        print('Already answered {} questions.\nContinuing with question {}:'.format(alreadyAnswered,alreadyAnswered + 1))
    for question_number in range(alreadyAnswered, len(questions)):
        print('\nQuestion ' + str(question_number+1) + ':')
        print(questions[question_number])
        question = no_answers_df_copy.loc[questions[question_number]].reset_index()
        question.index += 1
        question.columns = ['Answer options','']
        print(question)
        answer_option_count = len(no_answers_df_copy.loc[questions[question_number]].index)
        while True:
        
            correct_index_str = input('\nPlease list the indices of all answers which you think are correct (separated by a \',\' if multiple answers are correct, alternatively type in \'q\' to pause the quiz):\n')
            if correct_index_str == 'q':
                return None

            if correct_index_str == '':
                print('empty input not accepted (at least one option has to be true)')
                continue
            
            try:
                guess_index_list = [int(index) for index in correct_index_str.split(',')]
            except:
                print('Solution input not recognized - either input a single integer or a list of integers separated by a comma')
                continue
            
            faulty_entries = set(guess_index_list).difference(range(1,answer_option_count+1))

            if  len(faulty_entries) != 0:
                print('Error: The given indices {} are not among the possible indices of 1-{}\n'.format(faulty_entries,answer_option_count))
                continue
            break

        correct_indices = np.flatnonzero(question_df.loc[questions[question_number]]) + 1
        guesses = set(guess_index_list)
        solution = set(correct_indices)
        status = 'correct' if guesses == solution else 'incorrect'
        guess_index_list = [str(element) for element in guesses]
        # Update answer given and score
        # print(guesses)
        userDict[current_user][2] = listStringToStringList(userDict[current_user][2]) + ['&'.join(guess_index_list)]
        if status == 'correct':
            userDict[current_user][3] = int(userDict[current_user][3]) + 1
        commitUserChanges()
        print('You guessed the following answers as correct: {}. The correct solution is: {}. Your answer is therefore {}\n'.format(guesses, solution ,status))

def review_answers():
    clearConsole()
    no_answers_df_copy = question_df.copy()
    no_answers_df_copy['Is correct?'] = ''
    questions = listStringToStringList(userDict[current_user][1])
    answers = listStringToStringList(userDict[current_user][2])
    if len(questions) == 0 or len(answers) == 0:
        print('No quiz not started yet')
        return None
    alreadyAnswered = len(answers)
    for question_number in range(alreadyAnswered):
        print('\nQuestion ' + str(question_number+1) + ':')
        print(questions[question_number])
        question = no_answers_df_copy.loc[questions[question_number]].reset_index()
        question.index += 1
        question.columns = ['Answer options','User answer']
        # print(answers[question_number].split('&'))
        question['User answer'] = [str(i) in answers[question_number].split('&') for i in range(1,len(question.index)+1)]
        reference = question_df.loc[questions[question_number]]
        # print(reference['Is correct?'])
        # print(reference.columns)
        # print(reference.index)
        question['Solution'] = reference.values
        question['Guessed correctly'] = question['Solution'] == question['User answer']
        print(question)
    
    print('\nAnswered {} out of {} questions. Current score = {}'.format(alreadyAnswered, len(questions), userDict[current_user][3]))

def plot_scores():
    labels = []
    scoresAchieved = []
    scoresMax = []
    for user in userDict.keys():
        labels.append(user)
        scoresAchieved.append(int(userDict[user][3]))
        scoresMax.append(len(listStringToStringList(userDict[user][2])))
    width = 0.35       # the width of the bars: can also be len(x) sequence

    print(scoresAchieved,scoresMax)
    fig, ax = plt.subplots()

    ax.bar(labels, scoresAchieved, width, label='Score achieved')
    ax.bar(labels, [scoresMax[i] - scoresAchieved[i] for i in range(len(scoresMax))], width, bottom = scoresAchieved, label='Questions answered = Max. score possible')

    ax.set_ylabel('Scores')
    ax.set_title('Scores by user')
    ax.legend()

    plt.show()

def logIn():
    print('Logging into existing account:')
    
    #Get username input
    while True:
        name = input('Username: ')
        if len(name) == 0:
            print('Username can\'t be empty string')
            continue
        break
    
    #Check if a user under this name can be found in the database 
    try:
        if name not in userDict.keys():
            clearConsole()
            raise KeyError('No user with name ' + str(name) + ' found in the database')
        user_data = userDict[name]
        # If user was found check password
        savedPassword = user_data[0]
        inputPassword = getpass.getpass('Enter your password:')
        if inputPassword != savedPassword:
            clearConsole()
            raise ValueError('Wrong password')
        global current_user
        current_user = name
    except KeyError as ex:
        print(ex)
        print('\nKnown users: ')
        for user in userDict.keys():
            print(user)
        print('\n')

def logOut():
    global current_user
    current_user = None
    clearConsole()

def createNewUser():
    global userDict
    #Choose a username
    while True:
        name = input('Please input a username for your new account (english alphabet letters only): ')
        if len(name) == 0:
            clearConsole()
            print('Username can\'t be empty string')
            continue
        validPattern = re.compile(r'[a-zA-Z]*')
        validChars = validPattern.search(name).group(0)
        if validChars != name:
            clearConsole()
            print('Invalid characters - only letters from the english alphabet (A-Z upper or lower case) are allowed in the username\n \
            (Whitespaces are not allowed either - so concatenate if necessary)')
            continue
        if name in userDict.keys():
            clearConsole()
            print('Username already taken')
            continue
        break

    # Choose a password and type it in again to confirm it
    while True:
        print('Choose a password (Minimum five characters - only letters A-Z and digits 0-9 allowed)')
        password  = getpass.getpass('Enter a password for new user '+ name +': ')
        if len(password) < 5:
            print('Password is too short')
            continue
        validPattern = re.compile(r'[a-zA-Z0-9]*')
        validChars = validPattern.search(password).group(0)
        if validChars != password:
            print('Invalid characters - only letters A-Z and digits 0-9 allowed')
            continue
        if password == getpass.getpass('Type in your password again to confirm it:'):
            break
        else:
            print('The two passwords entered did not match - please try again')
    
    global current_user
    current_user = name
    userDict[name] = [password,[],[],0]
    commitUserChanges()

def chooseAction(action_index,action_functions = [add_questions,print_questions,take_quiz, review_answers, plot_scores, logOut]):
    # if not isinstance(action_index,int):
    if not isinstance(action_index,str):
        raise TypeError('The chooseAction function was called with a non-string input argument')
    if not action_index.isdigit():
        raise TypeError('Invalid input - please type in the positive INTEGER corresponding to your action of choice')
    action_index = int(action_index)
    if not action_index in range(len(action_functions)):
        raise IndexError('The chosen index lies outside of the valid range 0-{}'.format(len(action_functions)-1))
    action_functions[action_index]()

def commitUserChanges():
    global userDict
    # Write updated user information to Users.csv
    # Inefficient since it writes the entire dictionary from scratch to update a single entry
    with open('Users.csv', mode = 'w', newline = '') as newfile:
            writer = csv.writer(newfile, delimiter = ';')
            writer.writerow(['Username','Password','Quiz Started','Answers given','Score'])
            for user in userDict.keys():
                userData = userDict[user]
                writer.writerow([user,userData[0],userData[1],userData[2],userData[3]])
    with open('Users.csv', mode='r',newline='') as infile:
            reader = csv.reader(infile, delimiter=';')
            next(reader)
            userDict = {rows[0]:[rows[1],rows[2],rows[3],rows[4]]for rows in reader}

def main():
    initializeDbs()
    clearConsole()
    global current_user

    while True:
        
        #Log in or create new account
        if current_user == None:
            print('Would you like to...')
            for index,action in enumerate(user_selection):
                print(str(index)+': '+action)
            action = input('Please select your action: ')
            clearConsole()
            try:
                chooseAction(action,action_functions=[logIn,createNewUser,quit])
                continue
            except Exception as ex:
                print(ex)
                continue
 
        print('\nWelcome to the Quiz interface\n\nWhat would you like to do?')
        for index,action in enumerate(user_actions):
            print(str(index)+': '+action)

        action = input('Please select your action: ')
        try:
            chooseAction(action)
        except Exception as ex:
            print(ex)

if __name__ == '__main__':
    main()