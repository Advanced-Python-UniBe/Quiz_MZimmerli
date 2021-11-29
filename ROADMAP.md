# Advanced python course - quiz project

## Goal of the project
As outlied in the [README](https://github.com/MadpenguinCH/Advanced_python_course_quiz_project/blob/main/README.md) file, 
the goal of this project is basically artificially dictated by it being an exercise for a university course. 
Thus, it is not expected that anyone will actually ever use the final product. 
So with no clear utility in mind, the ACTUAL goal of this project is therefore simply to satisfy the requirements specified in the exercise description:
![image](https://user-images.githubusercontent.com/84137357/142775417-8c9e5805-2233-4444-9a76-60b1fa49cea6.png)

The intended timeline from the start of the project on the 08.11.2021 until the end of the project on 20.12.2021 is given below

## Timeline & milestones
### November 8th - Start of the project
Familiarized myself with the problem but otherwise not much to be done at this point.

### November 15th
Deadline for handing in a first version of the code which fulfills Task 1 of the project description.
I.e. at this point there should exist a framework for a database of multiple choice questions, possible choices & answers 
(an indicator for each possible answer which can be chosen whether it is correct or incorrect).
Directly required by the project description at this point is the ability to input new questions into the database.
The 'database' used in this case was chosen as a simple CSV file.
Functions were added which should allow for 
1. Reading the current state of the CSV file (questions already in the database) 
2. Adding own questions to the database
3. Writing the modified data back into the CSV file to save the changes
Additionally, a function was added which displays the currently saved questions (loaded from csv and added by user in this session)
in a more easily human readable format.
Also implemented a minimalistic text-interface which allows a user to easily access these functions
via terminal without having to specificy any input arguments in advance.

### November 21st
Creation of this git-hub repository.
Also the point at which this roadmap (and the README) was written, 
which is why the previous two entries are written in past tense and not a description of taks to be done.

### November 22nd
Deadline for handing in the auxilliary ROADMAP, README & CONTRIBUTING files which should make the project more accessible.
The 'CONTRIBUTING' file was postponed until the 29th since without setting up the repository for pull requests, there is no practical way to contribute to the project yet anyways.

### November 29th
At this point, it should be possible to generate short 'quizzes' from the questions in the database, consisting of 5 questions.
A user should then be able to answer the questions in a quiz and receive feedback on whether the answers they chose were correct or not.
To this end, it will be necessary to implement code for
1. Random selection of 5 (or potentially variable size) questions from the database
2. Displaying the questions of the quiz to the user (function already implemented - see November 15th) and accepting a user input to select which answers they think are correct.
3. Checking the input answers against the database to evaluate whether the selected options were correct
4. Output a feedback on the correctness of the guess to the user

### December 6th
Specific deliverable yet to be defined.
Deliverable aside, use the time until this date to clean up the code, create classes & refactor the code as necessary to make the code more easy to understand and use.

### December 13th
According to the courses project description, a 'unit test' has to be implemented until this point.
Since the quiz interface will not correspond to a classic input-output problem (and includes RANDOM question selection), it's a bit hard to define what an appropriate test would be.
However, might be feasible for specific functions (e.g. checking if a question has been added i.a.).

### December 20th 
End of the project & presentation of project in class.
This of course also requires implementation of the third feature required by the project description:
The ability to keep track of user responses & scores and handling of mutliple different users.
Also required is a way for each user to retreive their own score and/or plot the score of ALL users.



