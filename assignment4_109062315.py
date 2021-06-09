import sys
import tkinter as tk
from tkinter import ttk
from pyrecord import Records
from pycategory import Categories


categories = Categories()
records = Records()


def reset():
    input_str.set('')


def add():
    import re
    category = re.split(r'\s*-', category_str.get())
    print(category[1])
    record = input_date.get()+' '+category[1]+' '+input_description.get()+' '+input_money.get()
    records.add(record, categories)
    input_date.set('')
    category_str.set('')
    input_description.get()
    input_money.get()
    for idx, rec in enumerate(records.records):
        record = f'{rec.date} {rec.category} {rec.description} {rec.amount}'
        result_box.insert(idx, record)


def find():
    if len(input_str.get()) != 0:
        target_categories = categories.find_subcategories(input_str.get())
        records.find(target_categories)
        cat = list(filter(lambda rec: rec.category in target_categories, records.records))
        result_box.delete(0, tk.END)
        money = 0
        for idx, rec in enumerate(cat):
            record = f'{rec.date} {rec.category} {rec.description} {rec.amount}'
            result_box.insert(idx, record)
            money+=rec.amount
        total_money.set(f'The total money above is {money}')


def delete():
    for idx in result_box.curselection():
        print(result_box.get(idx))
        print(type(result_box.get(idx)))
        records.delete(result_box.get(idx))
        result_box.delete(idx)


def update():
    #print(input_initial_money.get())
    records._total_money+=int(input_initial_money.get())


root = tk.Tk()
frame = tk.Frame(root, width=960, height=500, borderwidth=5)
frame.grid(row=0, column=0)
tk.Label(frame, text='Find record').grid(row=0, column=0)
input_str = tk.StringVar()
tk.Entry(frame, textvariable=input_str).grid(row=0, column=1)
tk.Button(frame, text='Find', command=find).grid(row=0, column=2)
tk.Button(frame, text='Reset', command=reset).grid(row=0, column=3)
tk.Label(frame, text='Initial money').grid(row=0, column=4, columnspan=2)
result_box = tk.Listbox(frame)
result_box.grid(row=1, column=0, rowspan=6, columnspan=4)
input_initial_money = tk.StringVar()
tk.Entry(frame, textvariable=input_initial_money).grid(row=1, column=4)
tk.Button(frame, text='Update', command=update).grid(row=1, column=5)
tk.Label(frame, text='View Graph').grid(row=2, column=4)
graph_str = tk.StringVar()
view_graph_select = ttk.Combobox(frame, width=10, textvariable=graph_str)
view_graph_select['values'] = ('bar graph', 'pie graph')
view_graph_select.grid(row=2, column=5)
tk.Label(frame, text='Date').grid(row=3, column=4)
input_date = tk.StringVar()
tk.Entry(frame, textvariable=input_date).grid(row=3, column=5)
tk.Label(frame, text='Category').grid(row=4, column=4)
category_str = tk.StringVar()
category_select = ttk.Combobox(frame, width=10, textvariable=category_str)
category_select['values'] = categories.view()
category_select.grid(row=4, column=5)
tk.Label(frame, text='Description').grid(row=5, column=4)
input_description = tk.StringVar()
tk.Entry(frame, textvariable=input_description).grid(row=5, column=5)
tk.Label(frame, text='Amount').grid(row=6, column=4)
input_money = tk.StringVar()
tk.Entry(frame, textvariable=input_money).grid(row=6, column=5)
total_money = tk.StringVar()
tk.Label(frame, textvariable=total_money).grid(row=7, column=0, columnspan=4)
tk.Button(frame, text='Delete', command=delete).grid(row=7, column=3)
tk.Button(frame, text='Add a record', command=add).grid(row=7, column=4)
tk.mainloop()
records.save()
"""
while True:
    command = input('\nWhat do you want to do ( add / view / delete / view categories / find / exit / view graph )? ')
    if command == 'add':
        record = input('Add an expense or income record with date(optional), category, description, and amount \
(separate by spaces)\n')
        records.add(record, categories)
    elif command == 'view':
        records.view(0)
    elif command == 'delete':
        delete_record = input("Which record do you want to delete? (Description cost) ")
        records.delete(delete_record)
    elif command == 'view categories':
        categories.view()
    elif command == 'find':
        category = input('Which category do you want to find? ')
        target_categories = categories.find_subcategories(category)
        records.find(target_categories)
    elif command == 'exit':
        records.save()
        break
    elif command == 'view graph':
        graph = input('What graph do you want to view? (bar graph / pie graph) ')
        records.view_graph(categories, graph)
    else:
        sys.stderr.write('Invalid command. Try again.\n')"""
