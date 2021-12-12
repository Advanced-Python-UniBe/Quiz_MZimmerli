import os
import pandas as pd
from random import sample
import numpy as np
user_actions = ['Add a new question to the database','Print questions & answers','Take a quiz','Exit']
questions_answers_dict = {}

#TODO try to remove the NaN from empty initialization (if csv has to be created from scratch)
try:
    question_df = pd.read_csv('Questions_answers.csv',index_col=[0,1])
except:
    print('No existing question database detected')
    question_df = pd.DataFrame(index=[['Question'],['Options']],columns=['Is correct?'])


import os
def quit():
    global question_df
    question_df.to_csv('Questions_answers.csv')
    exit()
    

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

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
    global question_df
    print(question_df)

def question_to_df(question,options,correct):
    index = pd.MultiIndex.from_product([[question],options],names=['Question','Options'])
    df = pd.DataFrame(data = [answer in correct for answer in range(1,len(options)+1)],index=index, columns=['Is correct?'])
    return df

def take_quiz():
    global question_df
    QUIZ_QUESTION_COUNT = 5
    possible_questions = list(set(question_df.reset_index(level=[1]).index[1:]))
    # Make sure that the quesiton database is not empty
    assert len(possible_questions) != 0
    true_quiz_length = min([QUIZ_QUESTION_COUNT,len(possible_questions)])
    # print(sample(possible_questions,2))
    questions_sample = sample(possible_questions,true_quiz_length)
    no_answers_df_copy = question_df.copy()
    no_answers_df_copy['Is correct?'] = ''
    clearConsole()
    for question_number in range(true_quiz_length):
        # clearConsole()
        print('\nQuestion ' + str(question_number+1) + ':')
        question = no_answers_df_copy.loc[questions_sample[question_number]].reset_index()
        question.index += 1
        question.columns = ['Answer options','']
        print(question)
        answer_option_count = len(no_answers_df_copy.loc[questions_sample[question_number]].index)
        # print(str(answer_option_count) + ' options')
        # Reused code from add_questions --> if possible, make a reusable function out of this later
        while True:
        
            correct_index_str = input('\nPlease list the indices of all answers which you think are correct (separated by commas if multiple answers are correct):\n')

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

        correct_indices = np.flatnonzero(question_df.loc[questions_sample[question_number]]) + 1
        guesses = set(guess_index_list)
        solution = set(correct_indices)
        status = 'correct' if guesses == solution else 'incorrect'
        print('You guessed the following answers as correct: {}. The correct solution is: {}. Your answer is therefore {}\n'.format(guesses, solution ,status))

def chooseAction(action_index):
    action_functions = [add_questions,print_questions,take_quiz,quit]
    # if not isinstance(action_index,int):
    if not isinstance(action_index,str):
        raise TypeError('The chooseAction function was called with a non-string input argument')
    if not action_index.isdigit():
        raise TypeError('Invalid input - please type in the positive INTEGER corresponding to your action of choice')
    action_index = int(action_index)
    if not action_index in range(len(action_functions)):
        raise IndexError('The chosen index lies outside of the valid range 0-{}'.format(len(action_functions)-1))
    action_functions[action_index]()

def main():

    clearConsole()
    
    while True:
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