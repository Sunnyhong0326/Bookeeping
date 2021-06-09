import datetime
import sys
import matplotlib.pyplot as plt
from datetime import date
import tkinter as tk


class Record:
    def __init__(self, time=date.today(), category=' ', description=' ', amount=0):
        self._category = category
        self._description = description
        self._amount = amount
        # type datetime
        self._time = time

    @property
    def amount(self):
        return self._amount

    @property
    def category(self):
        return self._category

    @property
    def description(self):
        return self._description

    @property
    def date(self):
        return self._time


class Records:
    def __init__(self):
        self._records = []
        self._total_money = 0
        try:
            fh = open('records.txt', 'r')
        except OSError:
            try:
                self._total_money = int(input('How much money do you have?'))
            except ValueError:
                sys.stderr.write(f'Invalid value for money. Set to 0 by default.\n')
                self._total_money = 0
        else:
            print('Welcome back!')
            try:
                self._total_money = int(fh.readline())
            except ValueError:
                sys.stderr.write('The file is empty. Set your money to 0 by default.\n')
                self.total_money = 0
            else:
                for idx, i in enumerate(fh.readlines()):
                    rec = i.split()
                    self._records.append(Record(date.fromisoformat(rec[0]), rec[1], rec[2], int(rec[3])))
                fh.close()

    def add(self, rec, cate):
        try:
            print(rec)
            time = date.today()
            record = rec.split()
            if len(record) == 4:
                try:
                    input_time = record[0]
                    time = date.fromisoformat(input_time)
                    record.pop(0)
                except ValueError:
                    sys.stderr.write(f'The format of date should be YYYY-MM-DD.\nFail to add a record.\n')
            amount = int(record[2])
        except ValueError:
            sys.stderr.write(f'Invalid input for money\nFail to add a record\n')
        except IndexError:
            sys.stderr.write(f'The format of a record should be like this: meal breakfast -50.\n\
Fail to add a record.')
        else:
            if cate.is_category_valid(record[0]):
                if (amount > 0 and record[0] in cate.find_subcategories('income')) or amount < 0 and record[0] \
                        in cate.find_subcategories('expense'):
                    self._records.append(Record(time, record[0], record[1], amount))
                    self._total_money += amount
                elif amount < 0:
                    sys.stderr.write(f"{record[0]} can't be negative\n")
                elif amount > 0:
                    sys.stderr.write(f"{record[0]} can't be positive\n")
            else:
                sys.stderr.write(f'The specified category is not in the category list.\n\
You can check the category list by command "view categories".\n\
Fail to add a record.')

    def view(self, flag, sub_cat=[]):
        """view all the expense and income of the description and how much money"""
        if flag == -1:
            pass
        if flag == 0:
            print("Here's your expense and income records:")
        elif type(flag) == list:
            print('Please choose the one you want to delete')
        print(f"{'Date':^10} {'Categories':^15} {'Description':^20} Amount")
        print('='*10, '=' * 15, '=' * 20, '=' * 6)
        if flag == 0:
            for idx, rec in enumerate(self._records):
                rec_str = f'{rec.date} {rec.category:^15} {rec.description:^20} {rec.amount:^6}'
                print(rec_str)
        elif flag == -1:
            for idx, rec in enumerate(sub_cat):
                rec_str = f'{rec.date} {rec.category:^15} {rec.description:^20} {rec.amount:^6}'
                print(rec_str)
        else:
            num = 1
            for idx, rec in enumerate(self._records):
                if idx in flag:
                    print(f'{rec.date} {rec.category:^15} {rec.description:^20} {rec.amount:^6}', end=' ')
                    print('------', num)
                    num += 1
                else:
                    print(f'{rec.date} {rec.category:^15} {rec.description:^20} {rec.amount:^6}')
        print('='*10, '=' * 15, '=' * 20, '=' * 6)
        if flag == 0:
            print('Now you have', self._total_money, 'dollars.')

    def delete(self, del_rec):
        des = 0
        index = []
        try:
            delete_rec = del_rec.split()
            if len(delete_rec) == 4:
                amount = int(delete_rec[3])
            else:
                amount = int(delete_rec[1])
        except (ValueError, TypeError):
            sys.stderr.write(f'Invalid input for money (should be a number)\nFail to delete a record.\n')
        except IndexError:
            sys.stderr.write(f'The format of a record should be like this: breakfast -50.\nFail to delete a record.\n')
        else:
            if len(delete_rec) == 4:
                for idx, rec in enumerate(self._records):
                    if date.fromisoformat(delete_rec[0]) == rec.date and delete_rec[1] == rec.category \
                            and delete_rec[2] == rec.description and amount == rec.amount:
                        self._records.pop(idx)
                        self._total_money -= amount
                        break
            else:
                for idx, rec in enumerate(self._records):
                    if delete_rec[0] == rec.description and rec.amount == amount:
                        index.append(idx)
                        des += 1
                if des == 0:
                    sys.stderr.write(f'No such record!\nFail to delete a record!\n')
                elif des == 1:
                    self._total_money -= self._records[index[0]].amount
                    self._records.pop(index[0])
                elif des > 1:
                    print(f'You have {des} records the same, which one do you want to delete?')
                    self.view(index)
                    num = int(input('Please input the number you want to delete '))
                    while num <= 0 or des < num:
                        num = int(input(f'Please input valid numbers you want to delete (1~{des})'))
                    self._total_money -= self._records[index[num - 1]].amount
                    self._records.pop(index[num - 1])

    def find(self, target_cate):
        try:
            cat = list(filter(lambda rec: rec.category in target_cate, self._records))
        except (ValueError, TypeError):
            sys.stderr.write(f'Fail to find such category!\n')
        else:
            print(f"Here's your expense and income records under category \"{target_cate[0]}\"")
            self.view(-1, cat)
            money = sum(map(lambda rec: rec.amount, cat))
            print(f'The total amount above is {money}.')

    def save(self):
        with open('records.txt', 'w') as fh:
            mon = 0
            for money in self._records:
                mon += money.amount
            fh.write(str(mon) + '\n')
            st = ''
            for rec in self._records:
                st = st + date.isoformat(rec.date) + ' ' + rec.category + ' ' + rec.description + ' ' + str(rec.amount) + '\n'
            fh.writelines(st)

    def view_graph(self, category, graph):
        cat = category.flatten()
        lst = self._records.copy()
        mon = []
        in_mon = []
        out_mon = []
        for idx, child in enumerate(cat):
            temp = category.find_subcategories(child)
            total = list(filter(lambda rec: rec.category in temp, lst))
            amount = 0
            for rec in total:
                amount += rec.amount
            if amount >= 0 and idx >= 8:
                in_mon.append(amount)
            elif amount <= 0 and idx <= 7:
                amount = -amount
                out_mon.append(amount)
            mon.append(amount)
        while True:
            """if graph == 'line graph':
                plt.title('Line graph')
                plt.plot([1, 2, 3, 4, 5, 6, 7, 8],in_mon, color='green', markersize=12, linestyle='dashed', marker='o')
                plt.plot([9, 10, 11], out_mon, color='r', markersize=12, marker='star')
                plt.xticks(len(mon), cat)
                plt.legend(['income', 'expense'])
                plt.show()
                break"""
            if graph == 'bar graph':
                plt.title("Bar graph")
                plt.bar([1, 2, 3, 4, 5, 6, 7, 8], out_mon, label='expense', color='r')
                plt.bar([9, 10, 11], in_mon, label='income', color='g')
                plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], cat, fontsize='7')
                plt.xlabel('Records')
                plt.ylabel('Categories')
                plt.legend(title='Records')
                plt.show()
                break
            elif graph == 'pie graph':
                plt.title("Pie graph")
                e = [0, 0]
                if in_mon[0] > out_mon[0]:
                    e[1] = 0.1
                else:
                    e[0] = 0.1
                plt.pie([out_mon[0], in_mon[0]], labels=['expense', 'income'], explode=e, colors=['r', 'g'])
                plt.legend(['expense', 'income'], title='Records')
                plt.show()
                break
            else:
                sys.stderr.write('Please input scatter graph, bar graph or pie graph\n')
                graph = input()

    @property
    def records(self):
        return self._records

    @property
    def total_mon(self):
        return self._total_money
