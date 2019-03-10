#!/usr/bin/env python3.7

import mods.menus as menus
import mods.music_box as music_box
import tkinter as tk


class QueryObject:
    def __init__(self, db_bot, master_frame):
        self.name = 'query'
        self.master_frame = master_frame
        self.main_frame = tk.Frame(master_frame)
        self.search_entry_var = tk.StringVar()


    def set_helpers(self, objects):
        self.db_bot = objects[0]
        self.default_menu_list = objects[1]
        self.edit_bot = objects[2]
        self.gui_root = objects[3]
        return


    def list_db(self, column_restrictions):
        self.user_column_restrictions = column_restrictions
        self.get_list_db_results()
        self.show_db_results()
        return

    def get_user_search_entry(self):
        self.clear_packed_widgets(self.master_frame)
        # self.main_frame = tk.Frame(self.master_frame)
        self.set_restriction_checkbuttons()
        self.main_frame.pack(fill='both')
        self.set_user_entry_gui()
        return

    def set_user_entry_gui(self):
        self.search_frame = tk.Frame(self.main_frame)
        self.search_entry = tk.Entry(
            self.search_frame,
            textvariable=self.search_entry_var
        )
        self.search_submit_button = tk.Button(
            self.search_frame, text='Submit',
            foreground='red',
            command=self.process_user_search_entry
        )
        self.search_entry.bind(
            '<Return>', self.process_user_search_entry
        )
        self.search_entry.pack(side='left', fill='both')
        self.search_submit_button.pack(side='left', fill='both')
        self.restriction_message = tk.Message(
            self.main_frame, width=500,
            text='Choose column restrictions'
            '(leave blank for no restrictions):'
        )

        self.restriction_message.pack(side='top')
        for checkbutton in self.checkbutton_list:
            checkbutton.pack(side='left')
        self.checkbutton_frame.pack(side='top')
        self.search_frame.pack(side='top')
        self.master_frame.update()
        return

    def clear_packed_widgets(self, frame):
        pack_list = [a for a in frame.winfo_children()]
        if pack_list != []:
            for slot in pack_list:
                if slot.winfo_manager() == 'pack':
                    slot.pack_forget()
        self.master_frame.update()
        return

    def destroy_packed_widgets(self, frame):
        pack_list = [a for a in frame.winfo_children()]
        if pack_list != []:
            for slot in pack_list:
                if slot.winfo_manager() == 'pack':
                    slot.destroy()
        return

    def search_db(self):
        self.get_search_db_results()
        return

    def show_db_results(self):
        result_menu = self.set_result_menu()
        return result_menu.load_menu()

    def set_result_menu(self):
        result_menu = menus.Result_Menu(
            'Results', self.master_frame
        )
        result_menu.set_menu(self.set_result_menu_list())
        return result_menu

    def pick_entry(self, entry):
        self.destroy_packed_widgets(self.main_frame)
        self.clear_packed_widgets(self.master_frame)
        self.edit_bot.show_edit_screen(entry)
        return

    # def show_entry_pick_menu(self, data):
    #     self.entry_pick = data
    #     self.set_entry_pick_menu()
    #     return
    #
    # def set_entry_pick_menu(self):
    #     self.destroy_packed_widgets(self.main_frame)
    #     self.clear_packed_widgets(self.master_frame)
    #     self.entry_details_message = tk.Message(
    #         self.main_frame, width=500,
    #         text=self.entry_pick.get_full_details()
    #     )
    #     choice_frame = tk.Frame(self.main_frame)
    #     edit_button = tk.Button(
    #         choice_frame, text='Edit Entry', foreground='red',
    #         command=lambda: self.edit_bot.show_edit_screen(self.entry_pick)
    #     )
    #     # add_to_setlist_button = tk.Button(
    #     #     choice_frame, text='Add To Set List', foreground='red',
    #     #     command=lambda: self.edit_bot.add_to_set_list(self.entry_pick)
    #     # )
    #     back_to_results_button = tk.Button(
    #         choice_frame, text='Back To Results', foreground='red',
    #         command=self.show_db_results
    #     )
    #     back_to_main_button = tk.Button(
    #         choice_frame, text='Back To Main Menu', foreground='red',
    #         command=self.back_to_main_with_destroy
    #     )
    #     exit_button = tk.Button(
    #         choice_frame, text='Exit', foreground='red',
    #         command=self.gui_root.quit
    #     )
    #     self.main_frame.pack(fill='both')
    #     self.entry_details_message.pack(fill='both')
    #     edit_button.pack(side='left', fill='both')
    #     # add_to_setlist_button.pack(side='left', fill='both')
    #     back_to_results_button.pack(side='left', fill='both')
    #     back_to_main_button.pack(side='left', fill='both')
    #     exit_button.pack(side='left', fill='both')
    #     choice_frame.pack(side='top', fill='both')
    #     self.master_frame.update()
    #     return

    def back_to_main_with_destroy(self):
        self.destroy_packed_widgets(self.main_frame)
        self.default_menu_list[0].load_menu()

    def get_list_db_results(self):
        results = self.db_bot.list_db(self)
        self.db_results = self.package_db_results(results)
        return

    def get_search_db_results(self):
        results = [entry for entry in self.db_bot.search_db(self)]
        if results == []:
            self.raise_search_failure()
        else:
            self.db_results = self.package_db_results(results)
            self.show_db_results()
        return

    def process_user_search_entry(self, event=None):
        restriction_list = []
        for var, restriction in zip(
            self.checkbutton_var_list,
            self.default_column_restrictions_list
        ):
            if var.get() == 1:
                restriction_list.append(
                    restriction
                )
        if restriction_list == []:
            self.user_column_restrictions = self.default_column_restrictions
        elif len(restriction_list) == 1:
            self.user_column_restrictions = restriction_list[0]
        else:
            self.user_column_restrictions = ' ' + ' || '.join(
                restriction_list
            ) + ' '
        self.set_user_search_term(self.search_entry_var.get())
        self.clear_checkbuttons()
        # self.search_entry.delete(0, 'end')
        self.search_entry_var.set('')
        self.destroy_packed_widgets(self.main_frame)
        self.search_db()
        return

    def set_user_search_term(self, search_entry):
        self.user_search_term = (
            "".join([f'%', search_entry.strip(), f'%']),
        )
        return

    def raise_search_failure(self):
        self.clear_packed_widgets(self.main_frame)
        search_fail_message = tk.Message(
            self.main_frame, width=500,
            text='Sorry, we found no matches for your query.\n'
                 'Search again?'
        )
        choice_frame = tk.Frame(self.main_frame)
        yes_button = tk.Button(
            choice_frame, text='Yes', foreground='red',
            command=self.reget_user_search_entry
        )
        no_button = tk.Button(
            choice_frame, text='No', foreground='red',
            command=self.show_return_menu
        )
        self.main_frame.pack(fill='both')
        search_fail_message.pack(expand=True, fill='both')
        choice_frame.pack(fill='both')
        yes_button.pack(expand=True, side='right', fill='both')
        no_button.pack(expand=True, side='right', fill='both')
        self.master_frame.update()
        return

    def reget_user_search_entry(self):
        self.destroy_packed_widgets(self.main_frame)
        return self.get_user_search_entry()

    def show_return_menu(self):
        self.destroy_packed_widgets(self.main_frame)
        self.return_menu = menus.Radiobutton_Menu(
            'Return Menu', self.master_frame
        )
        self.return_menu.set_menu(
            {'Back To Main Menu':('load_menu', self.default_menu_list[0]),
            'Exit':('quit', self.gui_root)}
        )
        self.return_menu.load_menu()
        return

    def clear_checkbuttons(self):
        for checkbutton in self.checkbutton_var_list:
            checkbutton.set(0)
        return

    def package_db_results(self, results):
        print('not implemented')
        return
    def get_entry_pick_menu(self):
        print('not implemented')
        return

class SongQueryObject(QueryObject):
    def __init__(self, db_bot, master_frame):
        super().__init__(db_bot, master_frame)
        self.table = 'Songs'
        self.default_column_restrictions_list = [
            'Title', 'Album', 'Artist', 'Composer',
            'Lyrics', 'Year'
        ]
        self.default_column_restrictions = ' ' + ' || '.join(
            self.default_column_restrictions_list
        ) + ' '
        self.title_var = tk.IntVar()
        self.album_var = tk.IntVar()
        self.artist_var = tk.IntVar()
        self.composer_var = tk.IntVar()
        self.lyrics_var = tk.IntVar()
        self.year_var = tk.IntVar()
        self.checkbutton_var_list = [
            self.title_var, self.album_var, self.artist_var,
            self.composer_var, self.lyrics_var, self.year_var,
        ]

    def set_restriction_checkbuttons(self):
        self.checkbutton_list = []
        self.checkbutton_frame = tk.Frame(self.main_frame)
        for var, restriction in zip(
            self.checkbutton_var_list,
            self.default_column_restrictions_list
        ):
            self.checkbutton_list.append(
                tk.Checkbutton(
                    self.checkbutton_frame, text = restriction,
                    variable = var
                )
            )
        return

    def __str__(self):
        return 'Song Query'

    def package_db_results(self, results):
        result_list = [
            music_box.Song(*hits) for hits in results
        ]
        return result_list

    def set_result_menu_list(self):
        result_menu_list = []
        for song in self.db_results:
            result_menu_list.append(
                (f'{song.object_dict["Title"]} - '
                 f'{song.object_dict["Artist"]}',
                 'pick_entry', self, song)
            )
        result_menu_list += [
            ('Back To Main Menu', 'load_menu', self.default_menu_list[0]),
            ('Exit', 'quit', self.gui_root)
        ]
        return result_menu_list

class SetListQueryObject(QueryObject):
    def __init__(self, db_bot, master_frame):
        super().__init__(db_bot, master_frame)
        self.table = 'SetLists'
        self.default_column_restrictions_list = [
            'Band', 'Date', 'Venue', 'Songs'
        ]
        self.default_column_restrictions = ' ' + ' || '.join(
            self.default_column_restrictions_list
        ) + ' '
        self.band_var = tk.IntVar()
        self.date_var = tk.IntVar()
        self.venue_var = tk.IntVar()
        self.songs_var = tk.IntVar()
        self.checkbutton_var_list = [
            self.band_var, self.date_var,
            self.venue_var, self.songs_var
        ]

    def set_restriction_checkbuttons(self):
        self.checkbutton_list = []
        self.checkbutton_frame = tk.Frame(self.main_frame)
        for var, restriction in zip(
            self.checkbutton_var_list,
            self.default_column_restrictions_list
        ):
            self.checkbutton_list.append(
                tk.Checkbutton(
                    self.checkbutton_frame, text = restriction,
                    variable = var
                )
            )
        return

    def __str__(self):
        return 'Set List Query'

    def package_db_results(self, results):
        result_list = [
            music_box.SetList(*hits) for hits in results
        ]
        return result_list

    def set_result_menu_list(self):
        result_menu_list = []
        for set_list in self.db_results:
            result_menu_list.append(
                (set_list.object_dict['Band'], 'pick_entry',
                 self, set_list)
            )
        result_menu_list += [
            ('Back To Main Menu', 'load_menu', self.default_menu_list[0]),
            ('Exit', 'quit', self.gui_root)
        ]
        return result_menu_list
