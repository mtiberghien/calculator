from math import floor
from tkinter import Tk, Button, Label
from functools import partial

available_operators = ['+', '-', '*', '/']
numbers = ['']
current_number = 0
operators = []


def update_display(last_index=-1):
    global current_number
    text = '\n'.join(display.cget('text').splitlines(False)[:last_index])
    s = '\n' if current_number > 0 else ''
    display.config(text=f'{text}{s}{numbers[current_number]}')


def add_digit(button: Button):
    global current_number
    last_index = None if numbers[current_number] == '' else -1
    numbers[current_number] += button.cget('text')
    update_display(last_index)


def add_operator(button: Button):
    global current_number
    if len(numbers[current_number]) > 0:
        operators.append(button.cget('text'))
        numbers.append('')
        current_number += 1

        display.config(text=display.cget('text') + f'\n{button.cget("text")}\n{numbers[current_number]}')


def calculate():
    value = 0
    global numbers
    global operators
    for i in range(len(numbers)):
        if numbers[i] == '':
            break
        operand = float(numbers[i])
        if i == 0:
            value = operand
        else:
            operator = operators[i-1]
            if operator == '+':
                value += operand
            elif operator == '-':
                value -= operand
            elif operator == '*':
                value *= operand
            elif operator == '/':
                value /= operand
    if value.is_integer():
        value = int(value)
    numbers = [str(value)]
    global current_number
    current_number = 0
    operators = []
    display.config(text=str(value))


def clear_line():
    global current_number
    numbers[current_number]= ''
    update_display()


def clear_all():
    global current_number, numbers, operators
    numbers = ['']
    current_number = 0
    operators = []
    display.config(text='')


def delete():
    global current_number
    numbers[current_number] = ''.join(numbers[current_number][:-1])
    update_display()


def add_dot():
    global numbers, current_number
    text = numbers[current_number]
    if '.' not in text:
        if text == '':
            numbers[current_number] = '0.'
        else:
            numbers[current_number] += '.'
        update_display()


root = Tk()
root.title('Calculator')
root.resizable(False, False)
display = Label(root, text='')
display.grid()

for i in range(0, 10):
    btn: Button = Button(root, text=str(i), width=1, height=1)
    btn.config(command=partial(add_digit, btn))
    if i == 0:
        btn.grid(column=0, row=5)
    else:
        btn.grid(column=(i - 1) % 3, row=floor((i - 1) / 3) + 2)

for o in available_operators:
    btn: Button = Button(root, text=o, width=1, height=1)
    btn.config(command=partial(add_operator, btn))
    btn.grid(column=3, row= 2 + available_operators.index(o))

Button(root, text='=', command=calculate, width=1, height=1).grid(column=2, row=5)
Button(root, text='.', command=add_dot, width=1, height=1).grid(column=1, row=5)
Button(root, text='C', command=clear_line, width=1, height=1).grid(column=0, row=1)
Button(root, text='CA', command=clear_all, width=1, height=1).grid(column=1, row=1)
Button(root, text='<-', command=delete, width=1, height=1).grid(column=2, row=1)

root.mainloop()
