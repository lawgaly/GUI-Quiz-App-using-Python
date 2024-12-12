# import os
# os.system('pip install pandas')
import tkinter as tk
import pandas as pd
from tkinter import ttk 
from tkinter import messagebox
import random
current_question_index = 0
score = 0
def get_test_questions(Category,difficulty_level,quiz_time_in_sec):
    questions = pd.read_csv('quiz_questions.csv')
    df = pd.DataFrame(questions)
    if Category!="Any" and difficulty_level !="Any":
        filtered_questions = df.query('difficulty ==  @difficulty_level and category ==  @Category')
    elif Category!="Any" and difficulty_level =="Any":
        filtered_questions = df.query('category ==  @Category')
    elif Category=="Any" and difficulty_level !="Any":
        filtered_questions = df.query('difficulty ==  @difficulty_level')
    else:
        filtered_questions = questions
    numberofquestions=len(filtered_questions)
    # To Set up the GUI for questions ,answer, timer , and score.
    number_of_questions_label=tk.Label(exam_window,text=f"You have {quiz_time_in_sec} seconds to answer {numberofquestions} questions.",font=("Arail",13,"italic"))
    number_of_questions_label.grid(row=1, column=0, columnspan=2, padx=10,pady=10)
    questions_label=tk.Label(exam_window,text="",font=("Arail",13,"italic"),wraplength=400, justify="center")
    questions_label.grid(row=2, column=0, columnspan=2, padx=10,pady=10)
    load_question(filtered_questions,questions_label,current_question_index,numberofquestions)
    your_Answer_label=tk.Label(exam_window,text="Your Answer is : ",font=("Arail",13,"italic"),wraplength=400, justify="center")
    your_Answer_label.grid(row=3, column=0, padx=10,pady=10)
    button_ture_answer=tk.Button(exam_window,text="True",width=10, height=1, font=("Arail",13,"italic bold"),bg="#4caf50", fg="white",command=lambda: func_checking_answer(True,current_question_index,filtered_questions,feedback_question_label,your_score_label))
    button_ture_answer.grid(row=4,column=0,columnspan=2)
    feedback_question_label=tk.Label(exam_window,text="",font=("Arail",13,"italic"),wraplength=400, justify="center")
    feedback_question_label.grid(row=5, column=0, columnspan=2)
    button_false_answer=tk.Button(exam_window,text="False",width=10, height=1, font=("Arail",13,"italic bold"),bg="#c2574f", fg="white",command=lambda: func_checking_answer(False,current_question_index,filtered_questions,feedback_question_label,your_score_label))
    button_false_answer.grid(row=6,column=0,columnspan=2,padx=10,pady=10)
    button_next_question=tk.Button(exam_window,text="Next Question",width=15, height=1, font=("Arail",10,"italic bold"),bg="#7297ed",command=lambda: next_question(filtered_questions,questions_label,numberofquestions,feedback_question_label))
    button_next_question.grid(row=7,column=1,pady=10)
    your_score_label=tk.Label(exam_window,text=f"Your Score is : {score}", font=("Arail",12,"italic bold"))
    your_score_label.grid(row=8, column=0,pady=0,padx=0)
    timer_label=tk.Label(exam_window,text=f"Timer :{quiz_time_in_sec} seconds", font=("Arail",12,"italic bold"))
    timer_label.grid(row=8, column=1, columnspan=2, padx=10, pady=10)
    quiz_time = {"time_left": int(quiz_time_in_sec)}
    timer_down(quiz_time,timer_label)

def func_checking_answer(user_answer,current_question_index,questions,feedback_question_label,score_label):
    global score
    current_question=questions.iloc[current_question_index]
    if user_answer == current_question['correct_answer']:
        feedback_question_label.config(fg="green", text="Correct!", )
        score+=1
        score_label.config(text=f"Your Score is: {score}")
        exam_window.update_idletasks()
    else:
        feedback_question_label.config(fg="red",text=f"Wrong! The correct answer is {current_question['correct_answer']}")
        
def load_question(questions,questions_label,current_question_index,num_of_questions):   
    if current_question_index < num_of_questions:       
        current_Question = questions.iloc[current_question_index]
        questions_label.config(text=f"Q{current_question_index + 1}): {current_Question['question']}")
    else:
        questions_label.config(text="Quiz Completed!")
def next_question(filtered_questions,questions_label,numberofquestions,feedback_question_label):
    global current_question_index
    if current_question_index + 1 < numberofquestions:
        current_question_index += 1
        feedback_question_label.config(text="")
        load_question(filtered_questions, questions_label, current_question_index, numberofquestions)
    else:
        messagebox.showinfo("Quiz Completed", f"Your final score is: {score}")
        exam_window.destroy()

def show_exam_window():
    user_full_name= full_name.get()
    quiz_time_in_sec=time_in_sec.get()
    Category=Category_combobox.get()
    difficulty_level=difficulty_combobox.get()
    if not user_full_name or not quiz_time_in_sec:
        error_Text.config(text="Please fill in all the fields!", fg="red")
        return
    global exam_window
    exam_window = tk.Toplevel(root)
    exam_window.title("Quiz page.")
    exam_window.geometry("450x450")
    hello_label=tk.Label(exam_window,text=f"Hello, {user_full_name} ! , ",fg="red",font=("Arail",13,"bold italic"),justify="center")
    hello_label.grid(row=0, column=0, columnspan=2,padx=10,pady=10)
    get_test_questions(Category,difficulty_level,quiz_time_in_sec)

def timer_down(quiz_time, timer_label):
    if quiz_time["time_left"] > 0:
        quiz_time["time_left"] -= 1
        timer_label.config(text=f"Time Left: {quiz_time['time_left']} seconds")
        exam_window.after(1000, lambda: timer_down(quiz_time, timer_label))
    else:
        timer_label.config(text="Time's up!")    
        messagebox.showinfo("Quiz Completed", f"Your final score is: {score}")
        exam_window.destroy()
# main 
root = tk.Tk()
root.title("Quiz Application.")
root.geometry("450x450")
label_window = tk.Label(root, text="Test your knowledge", font=("Arial", 16))
label_window.grid(row=0, column=0, columnspan=2, pady=10)
full_name_label = tk.Label(root, text="Enter your Full Name:", font=("Arial", 10))
full_name_label.grid(row=1, column=0, pady=30)
full_name = tk.Entry(root, font=("Arial", 12))
full_name.grid(row=1, column=1, pady=30)
time_in_sec_label = tk.Label(root, text="Enter the required time in seconds:", font=("Arial", 10))
time_in_sec_label.grid(row=2, column=0, pady=5)
time_in_sec = tk.Entry(root, font=("Arial", 12))
time_in_sec.grid(row=2, column=1, pady=5)
Category_label = tk.Label(root, text="Choose the Category questions:", font=("Arial", 10))
Category_label.grid(row=3, column=0, pady=15)
Category_combobox = ttk.Combobox(root, width=27,values=["Any","General Knowledge", "Entertainment: Books", "Entertainment: Film", "Entertainment: Music", "Entertainment: Video Games", "Science &amp; Nature", "Science: Computers","Geography","History"])
Category_combobox.set("Any")
Category_combobox.grid(row=3, column=1, pady=15)
difficulty_label = tk.Label(root, text="Choose the difficulty Level:", font=("Arial", 10))
difficulty_label.grid(row=4, column=0, pady=15)
difficulty_combobox = ttk.Combobox(root, width=27,values=["Any","easy", "medium", "hard"])
difficulty_combobox.set("Any") 
difficulty_combobox.grid(row=4, column=1, pady=15)
error_Text = tk.Label(root, text="", font=("Arial", 12))
error_Text.grid(row=5, column=0, pady=5)
show_Exam_button = tk.Button(root, text="Start Your Exam",font=("Arial ", 10),bg="#4caf50", fg="white", width=20,command=show_exam_window)
show_Exam_button.grid(row=6, column=0, columnspan=2, pady=20)  # Center the button
root.mainloop()