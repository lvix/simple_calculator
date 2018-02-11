#!/usr/bin/env python3

"""
@version: 0.0.1
@author: Lvix
@project: SimpleCal
@file: tk_test.py
@time: 18/2/10 1:46
"""

from tkinter import *
from calculation import FNode


# from tkinter.ttk import *

class Screen(object):
    is_init_status = True

    def __init__(self, parent):
        # ============== Screen ==============
        self.screen_frame = Frame(parent, width=480, height=240, bg='#e1e7e7')
        # fixed size for children widgets
        self.screen_frame.grid_propagate(False)
        self.screen_frame.pack()

        # Frame1

        self.screen_child1 = Frame(self.screen_frame, width=480, height=60, bg='#e1e7e7')
        # fixed size
        self.screen_child1.pack_propagate(False)
        self.screen_child1.pack()
        # Frame2

        self.screen_child2 = Frame(self.screen_frame, width=480, height=60, bg='#e1e7e7')
        self.screen_child2.pack_propagate(False)
        self.screen_child2.pack()
        # Frame3

        self.screen_child3 = Frame(self.screen_frame, width=480, height=120, bg='#e1e7e7')
        self.screen_child3.pack_propagate(False)
        self.screen_child3.pack()

        # content
        self.main_content = StringVar()
        self.main_content.set('0')
        self.history_content_middle = StringVar()
        self.history_content_middle.set('')
        self.history_content_above = StringVar()
        self.history_content_above.set('')

        self.is_init_status = True

        # max_len = 10
        self.history_label_above = Label(self.screen_child1, text='12345678901234\n567890',
                                         textvariable=self.history_content_above,
                                         font=('Roboto Light', 32), foreground='#5b5b5b',
                                         bg='#e1e7e7', anchor=SE, justify='right', padx=15)

        # max_len = 18
        self.history_label_middle = Label(self.screen_child2, text='12345678901234\n567890',
                                          textvariable=self.history_content_middle,
                                          font=('Roboto Light', 32), foreground='#5b5b5b',
                                          bg='#e1e7e7', anchor=SE,
                                          justify='right', padx=15)
        # max_len = 9
        self.main_label = Label(self.screen_child3, text='1234567890123', textvariable=self.main_content,
                                font=('Roboto Light', 64), foreground='#5b5b5b',
                                bg='#e1e7e7', anchor=SE,
                                justify='right', padx=15)

        self.history_label_above.pack(side=RIGHT)
        self.history_label_middle.pack(side=RIGHT)
        self.main_label.pack(side=RIGHT)

    def clear(self):
        self.main_content.set('0')
        self.history_content_middle.set('')
        self.history_content_above.set('')
        self.check_len()
        self.is_init_status = True

    def cal(self):
        # 导入模块进行运算
        content = self.main_content.get()
        content = content.replace('×', '*')
        content = content.replace('÷', '/')
        content = content.replace('−', '-')

        try:
            result = str(FNode(content).cal())[:18]

            if '.' in result:
                left_part, right_part = result.split('.')
                if len(left_part) > 18:
                    # 以后可能使用科学计数法
                    result = 'Out of Range'
                    self.is_init_status = True
                else:
                    result = result[:18]
            else:
                if len(result) > 18:
                    result = 'Out of Range'
                    self.is_init_status = True

            self.history_content_above.set(self.history_content_middle.get())
            self.history_content_middle.set(self.main_content.get())
            self.main_content.set(result)
            self.check_len()
        except Exception as e:
            # print(e)
            self.main_content.set('Error')
        # 重置到初始状态
        self.is_init_status = True

    def backspace(self):
        if self.is_init_status:
            self.clear()
        else:
            content = self.main_content.get()
            self.main_content.set(content[:-1])
            if self.main_content.get() == '':
                self.clear()

    def btn_input(self, btn_char):
        content = self.main_content.get()
        is_cal = False
        if self.is_init_status:
            if content == 'Out of Range' or content == 'Error':
                content = '0'
                self.main_content.set(content)
                self.check_len()
                return

            if content == '0':
                # 如果是 0 状态
                # 输入 数字，content = input
                # 输入 '.'， content = '0.'
                # 输入 '+−×÷', content = content + input
                # 输入 左括号，content = input
                # 输入 右括号，clear()
                # 输入 等号， clear()
                if btn_char in '0123456789':
                    content = btn_char
                    if btn_char == '0':
                        self.clear()
                        return
                elif btn_char == '.':
                    content += btn_char
                elif btn_char in '+−×÷':
                    if btn_char == '−':
                        content = '−'
                    else:
                        content += ' ' + btn_char + ' '
                elif btn_char == '(':
                    content = '('
                elif btn_char == ')' or btn_char == '=':
                    self.clear()
                    return
            else:
                # 计算得出结果后，
                # 输入数字, content = btn_char
                # 输入.， content = '0.'
                # 输入加减乘除，content += ' ' + btn_char + ' '
                # 输入左括号，content = btn_char
                # 输入右括号, clear()
                # 输入等号, return()
                if btn_char in '0123456789':
                    content = btn_char
                elif btn_char == '.':
                    content = '0.'
                elif btn_char in '+−×÷':
                    content += ' ' + btn_char + ' '
                elif btn_char == '(':
                    content = '('
                elif btn_char == ')':
                    self.clear()
                    return
                else:
                    return
            self.is_init_status = False

        elif content.strip()[-1] == '.':
            # 如果结尾是 '.'，
            # 输入 数字， content + input
            # 输入 '.'，content + ''
            # 输入 '+−×÷'， content[:-1] + input
            # 输入 左括号， content[:-1] + input
            # 输入 右括号, content[:-1] + input
            # 输入 等号，content = content[:-1] , cal()
            if btn_char in '0123456789':
                content += btn_char
            elif btn_char == '.':
                content += ''
            elif btn_char in '+−×÷':
                content += btn_char
            elif btn_char == '(':
                content = content[:-1] + ' * ' + btn_char
            elif btn_char == ')':
                content = content[:-1] + btn_char
            elif btn_char == '=':
                content = content[:-1]
                # self.main_content.set(content)
                # 需要计算
                is_cal = True

        elif content.strip()[-1] in '0123456789':
            # 如果结尾是数字
            # 输入数字，content + 数字
            # 输入. ，如果到前一个标点符号之前，不存在一个非零整数，content + ''
            # 否则 content + ''
            # 输入 '+−×÷'， content + 数字
            # 输入 左括号， content + ' * ('
            # 输入 右括号, content + ')'
            # 输入 等号 cal()
            if btn_char in '0123456789':
                content += btn_char
            elif btn_char == '.':
                for i in range(len(content) - 1, -1, -1):
                    if content[i] in '+−×÷':
                        break
                chk_num = content[i+1:].strip()
                if '.' in chk_num or chk_num == '':
                    return
                else:
                    content += btn_char
                    # try:
                    #     chk_num = int(chk_num)
                    #     content += btn_char
                    # except Exception as e:
                    #     return

            elif btn_char in '+−×÷':
                content += ' ' + btn_char + ' '
            elif btn_char == '(':
                content += ' * ' + btn_char
            elif btn_char == ')':
                content += btn_char
            elif btn_char == '=':
                is_cal = True

        elif content.strip()[-1] == '(':
            # 如果结尾是左括号
            # 输入数字，content + 数字
            # 输入.， content + ''
            # 输入 '+−×÷', content +
            # 输入左括号, content + 括号
            # 输入右括号, content + 括号
            # 输入等号， err

            if btn_char in '0123456789':
                content += btn_char
            elif btn_char == '.':
                content += ''
            elif btn_char in '+−×÷':
                content += btn_char
            elif btn_char == '(':
                content += btn_char
            elif btn_char == ')':
                content += ''
            elif btn_char == '=':
                content += ''

        elif content.strip()[-1] == ')':
            # 如果结尾是右括号
            # 输入数字, content + ' * ' + btn_char
            # 输入., content+''
            # 输入 '+−×÷' ， content + 符号
            # 输入左括号，content + ' * ('
            # 输入右括号, content + 右括号
            # 输入等号，cal()

            if btn_char in '0123456789':
                content += ' * ' + btn_char
            elif btn_char == '.':
                content += ''
            elif btn_char in '+−×÷':
                content += ' ' + btn_char + ' '
            elif btn_char == '(':
                content += ' * ' + btn_char
            elif btn_char == ')':
                content += btn_char
            elif btn_char == '=':
                is_cal = True

        elif content.strip()[-1] in '+−×÷':
            # 如果结尾是加减乘除
            # 输入数字, content + input
            # 输入.， content + ''
            # 输入加减乘除，content[-2] = input
            # 输入左括号，content + ''
            # 输入右括号, content + ''
            # 输入等号, content = content[:-3] , cal()
            if btn_char in '0123456789':
                content += btn_char
            elif btn_char == '.':
                content += ''
            elif btn_char in '+−×÷':
                content = content[:-2] + btn_char + ' '
            elif btn_char == '(':
                content += btn_char
            elif btn_char == ')':
                content += ''
            elif btn_char == '=':
                content = content.strip()[:-2]
                is_cal = True

        self.main_content.set(content)
        self.check_len()
        if is_cal:
            self.cal()

    def check_len(self):
        content = self.main_content.get()
        if len(content) > 9:
            # 改变 main_label 的字体大小
            # 处理过长数字
            # if '.' in content:
            #     left_part, right_part = content.split('.')
            #     if len(left_part) > 18:
            #         # 以后可能使用科学计数法
            #         content = 'Out of Range'
            #         self.is_init_status = True
            #     else:
            #         content = content[:18]
            # else:
            #     if len(content) > 18:
            #         content = 'Out of Range'
            #         self.is_init_status = True
            content = content[:18]
            self.main_content.set(content)
            self.main_label.config(font=('Roboto', 32))
        else:
            self.main_label.config(font=('Roboto', 64))


class PanelButton(object):
    button = None
    button_obj = None

    def __init__(self, parent, dsp_screen, text, coordx, coordy, text_color, bg_color, wd=120, ht=120):
        self.coordx = coordx
        self.coordy = coordy
        self.button = Frame(parent, width=wd, height=ht)
        # The normal behavior (propagate is True) causes the frame to request a
        # size that reflects what the children request.  When propagate is false,
        # the frame uses its width= and height= as the requested size.
        self.button.pack_propagate(0)
        # 绑定到屏幕
        self.screen = dsp_screen
        self.cmd_char = text
        self.button_obj = Button(self.button,
                                 text=text,
                                 relief='flat',
                                 bd=0,
                                 font=('Roboto', 32),
                                 bg=bg_color,
                                 foreground=text_color,
                                 activebackground=bg_color,
                                 activeforeground=text_color,
                                 highlightcolor='#ffffff',
                                 command=self.trigger
                                 )

    def draw(self):
        # 跟随着父元素一起重新调整尺寸
        self.button_obj.pack(fill=BOTH, expand=1)
        # self.button.grid_propagate(0)
        self.button.grid(column=self.coordx, row=self.coordy, sticky=NW)

    def trigger(self):
        if self.cmd_char == 'C':
            self.screen.clear()
        elif self.cmd_char == 'D':
            self.screen.backspace()
        else:
            self.screen.btn_input(self.cmd_char)


# ============== Main Window ==============
window = Tk()
window.geometry('480x840+400+100')
window.title('Simple Calculator')
window.resizable(False, False)
# 去掉边框
# window.overrideredirect(True)
window.iconbitmap('icon.ico')
# 最小化
# window.iconify()

root_frame = Frame(window, width=480, height=840, bg='#ffffff')
root_frame.pack()
# Screen
screen = Screen(root_frame)
# ============== Keyboard Panel ==============
panel_frame = Frame(root_frame, width=480, height=600, bg='#ffffff')
panel_frame.pack()
panel_frame.grid_propagate(False)

button_chars = ['C', '(', ')', 'D',
                '7', '8', '9', '÷',
                '4', '5', '6', '×',
                '1', '2', '3', '−',
                '0', '.', '=', '+']
btn_list = []
index = 0
for char in button_chars:
    cx = int(index % 4)
    cy = int(index / 4)
    if char == 'C' or char == '=':
        btn = PanelButton(panel_frame, screen, char, cx, cy, '#ff7d00', '#ffffff')
    else:
        if cx == 3:
            btn = PanelButton(panel_frame, screen, char, cx, cy, '#ffffff', '#feaa5a')
        else:
            btn = PanelButton(panel_frame, screen, char, cx, cy, '#5b5b5b', '#ffffff')
    btn.draw()
    btn_list.append(btn)
    index += 1

window.mainloop()
