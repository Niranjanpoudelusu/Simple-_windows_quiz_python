# import packages

from tkinter import *
from tkinter import messagebox as mb
import json


def display_title():
    title = Label(gui, text="Simple Quiz Example",
                  width=70, bg='green', fg='white',
                  font=('ariel', 20, 'bold'))

    # place of the title
    title.place(x=0, y=2)


def name_error():
    error = Label(gui, text='Did you forget your name?', fg='red')
    error.place(x=300, y=270)


def remove_widgets():
    for widget in gui.winfo_children():
        widget.destroy()


def correct_message():
    msg = "Correct Answer"
    message = Label(gui, text=msg, fg='blue')
    message.place(x=10, y=600)


def incorrect_message():
    msg = "Incorrect Answer"
    inMessage = Label(gui, text=msg, fg='red')
    inMessage.place(x=10, y=600)


class Quiz:
    def __init__(self):
        # call the function to display title
        self.opts = None
        display_title()
        self.question_no = 0
        self.opt_selected = IntVar()
        self.name = 'aa'
        self.name_entry()
        self.data_size = len(question_data)
        self.correct = 0

    # create a function to display the questions
    def display_question(self):
        remove_widgets()
        # set the question properties
        q_no = Label(gui, text=question_data[self.question_no]['question'],
                     font=('ariel', 10, 'bold'), anchor='w')

        # place the question
        q_no.place(x=70, y=50)

    def display_options(self):
        val = 0

        # deselecting the options
        self.opt_selected.set(0)

        for option in question_data[self.question_no]['options']:
            self.opts[val]['text'] = option
            val += 1

    def radio_buttons(self):

        # initialize the empty list
        q_list = []

        # position for first option
        y_pos = 150

        # adding the options to teh list
        while len(q_list) < 4:
            # setting the radio button properties
            radio_btn = Radiobutton(gui, text='', variable=self.opt_selected,
                                    value=len(q_list) + 1, font=('ariel', 10))

            q_list.append(radio_btn)

            # place the button
            radio_btn.place(x=120, y=y_pos)

            y_pos += 40

        return q_list

    # create the logic for submit
    def submit(self):
        if self.opt_selected.get() == question_data[self.question_no]['correct_answer']:
            correct_message()
        else:
            incorrect_message()

        submit1.place_forget()

        # create a next button as well
        next_button = Button(gui, text="Next Question", command=self.next_logic,
                             width=15, bg='red', fg='white', font=('ariel', 16, 'bold'))
        next_button.place(x=500, y=450)

    def next_logic(self):

        # check if the answer was correct
        if self.check_ans(self.question_no):
            question_data[self.question_no]["correct"] = 1
            self.correct += 1

        self.question_no += 1

        if self.question_no == self.data_size:
            self.display_result()

            gui.destroy()
        else:
            self.display_question()
            self.opts = self.radio_buttons()
            self.display_options()
            self.buttons()

    def display_result(self):

        wrong_count = self.data_size - self.correct
        correct = f"Correct: {self.correct}"
        wrong = f"Wrong: {wrong_count}"

        mb.showinfo("Result", f"{correct}\n{wrong}")

    # logic to check answer

    def check_ans(self, question_no):

        if self.opt_selected.get() == question_data[self.question_no]['correct_answer']:
            return True

    def buttons(self):
        global submit1
        submit1 = Button(gui, text="Submit", command=self.submit,
                         width=10, bg='blue', fg='white', font=('ariel', 16, 'bold'))

        submit1.place(x=100, y=450)

        # This is the second button which is used to Quit the GUI
        quit_button = Button(gui, text="Quit", command=gui.destroy,
                             width=5, bg="black", fg="white", font=("ariel", 16, " bold"))

        # placing the Quit button on the screen
        quit_button.place(x=900, y=50)

    def name_check(self):
        if self.name == "admin":
            self.display_question()
            self.opts = self.radio_buttons()
            self.display_options()
            self.buttons()
        else:
            name_error()

    def submit_name(self, entry_widget):
        self.name = entry_widget.get().lower()
        self.name_check()

    def name_entry(self):
        name = Label(gui, text='What is your name?')
        name.place(x=300, y=160)
        entry = Entry(gui)
        entry.place(x=300, y=200)

        # also display the button
        button_name = Button(gui, text="Submit my name", command=lambda: self.submit_name(entry))
        button_name.place(x=310, y=230)


gui = Tk()

# set the size of gui
gui.geometry("1000x700")

# set the title of the window
gui.title("Simple app with python")

# import the question_data
with open('Question.json') as f:
    question_data = json.load(f)

question_data = [i for i in question_data if i.get("correct") == 0]

# create class object
quiz = Quiz()

# Start the gui
gui.mainloop()

correct_data = [i for i in question_data if i.get("correct") == 1]

# save question data and correct data
with open("Question.json", 'w') as f:
    json.dump(question_data, f, indent=4)

with open("correct.json", 'r') as f:
    existing_data = json.load(f)

# Append the new data to the existing data
existing_data.extend(correct_data)

# Write the combined data back to the JSON file
with open("correct.json", 'w') as f:
    json.dump(existing_data, f, indent=4)
