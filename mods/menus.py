#!/usr/bin/env python3.7

import tkinter as tk

class Radiobutton_Menu(tk.Frame):
    def __init__(self, name, master):
        super().__init__(master)
        self.name = 'name'
        self.menu_dict = {}
        self.menu_var = tk.StringVar()
        self.master_frame = master


    def __str__(self):
        return self.name

    def set_menu(self, menu_dict):
        self.menu_dict = menu_dict
        menu_list = []
        count = 0
        for key in self.menu_dict.keys():
            menu_list.append(
                tk.Radiobutton(
                    self,
                    text=key, variable=self.menu_var,
                    value=key, indicatoron=0,
                    command=lambda: self.activate_method(self.menu_var.get())
                )
            )
        for radiobutton in menu_list:
            radiobutton.pack(fill='both')

    def activate_method(self, button_value):
        label = button_value
        method_name = self.menu_dict[button_value][0]
        object = self.menu_dict[button_value][1]
        method = getattr(object, method_name, f'error')
        try:
            data = self.menu_dict[button_value][2]
            return method(data)
        except:
            if method_name == 'list_db':
                return method(label)
            else:
                return method()

    def load_menu(self):
        self.menu_var.set('')
        self.clear_packed_widgets()
        self.pack(fill='both', expand=True)
        self.master_frame.update()
        return

    def clear_packed_widgets(self):
        pack_list = [a for a in self.master.winfo_children()]
        if pack_list != []:
            for slot in pack_list:
                if slot.winfo_manager() == 'pack':
                    slot.pack_forget()
        return

    def destroy_packed_widgets(self, frame):
        pack_list = [a for a in frame.winfo_children()]
        if pack_list != []:
            for slot in pack_list:
                if slot.winfo_manager() == 'pack':
                    slot.destroy()
        return

class Result_Menu(Radiobutton_Menu):
    def __init__(self, name, master):
        super().__init__(name, master)
        self.menu_var = tk.IntVar()
        self.listbox_frame = tk.Frame(self, bg='black', relief='ridge')
        self.listbox_frame.pack(expand=True, fill='both')
        self.listbox = tk.Listbox(self.listbox_frame)
        self.listbox.pack(
            side='left', expand=True, fill='both', padx=3, pady=4
        )
        self.listbox_scrollbar = tk.Scrollbar(
            self.listbox_frame, command=self.listbox.yview
        )
        self.listbox_scrollbar.pack(side='right', fill='y')
        self.listbox['yscrollcommand'] = self.listbox_scrollbar.set
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side='bottom', fill='both')
        self.select_button = tk.Button(
            self.button_frame, text='Select', foreground='red',
            command=self.get_selection
        )
        self.listbox.bind('<Double-Button-1>', self.get_selection)
        self.select_button.pack(side='right', expand=True, fill='both')


    def set_menu(self, menu_list):
        result_menu_list = menu_list
        self.nav_list = []
        for a in range(2):
            self.nav_list.append(result_menu_list.pop())
        back_to_main_method = self.nav_list[1][1]
        back_to_main_object = self.nav_list[1][2]
        back_to_main_button = tk.Button(
            self.button_frame, text='Back To Main Menu', foreground='red',
            command=lambda: self.activate_button_method(
                back_to_main_method, back_to_main_object
            )
        )
        exit_method = self.nav_list[0][1]
        exit_object = self.nav_list[0][2]
        exit_button = tk.Button(
            self.button_frame, text='Exit', foreground='red',
            command=lambda: self.activate_button_method(
                exit_method, exit_object
            )
        )
        exit_button.pack(side='right', expand=True, fill='both')
        back_to_main_button.pack(side='right', expand=True, fill='both')

        self.menu_list = result_menu_list
        for entry in self.menu_list:
            self.listbox.insert('end', entry[0])

    def get_selection(self, event=None):
        '''event is there so the double click binding works.
           it does't do anything '''
        selection = self.listbox.curselection()
        index = selection[0]
        self.activate_method(index)
        return

    def activate_button_method(self, method_name, object):
        method = getattr(object, method_name, f'error')
        return method()

    def activate_method(self, button_value):
        label = self.menu_list[button_value][0]
        method_name = self.menu_list[button_value][1]
        object = self.menu_list[button_value][2]
        method = getattr(object, method_name, f'error')
        try:
            data = self.menu_list[button_value][3]
            return method(data)
        except:
            if method_name == 'list_db':
                return method(label)
            else:
                return method()
