#!/usr/bin/env python3.7

import mods.menus
import mods.music_box
import tkinter as tk

class EditObject:
    '''EditObject is a super class.  Not meant to be instnatiated'''
    def __init__(self, db_bot, master_frame):
        self.name = 'edit'
        self.master_frame = master_frame
        self.entry = None

    def __str__(self):
        return 'Edit Object'

    def set_helpers(self, objects):
        self.db_bot = objects[0]
        self.default_menu_list = objects[1]
        self.query_bot = objects[2]
        self.gui_root = objects[3]
        self.main_frame = self.query_bot.main_frame
        return

    def show_edit_screen(self, entry=None):
        '''entry is a music_box object'''
        self.entry = entry
        self.destroy_packed_widgets(self.main_frame)
        self.set_edit_gui()
        return

    def write_db(self):
        self.entry.set_object_dict_undo(list(self.new_values.keys()))
        self.entry.set_object_dict(self.new_values)
        self.db_bot.write_db(self.entry)
        self.back_to_main_menu()
        return

    def delete_entry(self):
        self.db_bot.delete_entry(self.entry)
        self.back_to_main_menu()
        return

    def write_new_entry(self):
        self.new_object_dict = {'row_id': None}
        self.clear_packed_widgets(self.master_frame)
        self.set_edit_gui()
        return

    def set_edit_gui(self):
        print('not implemented')

    def write_entry(self):
        self.new_object_dict.update(
            self.new_values
        )
        self.create_new_music_object(self.new_object_dict)
        confirmation_window = tk.Toplevel(
            self.main_frame, background='#555555'
        )
        confirmation_window.minsize(300,100)
        confirmation_window.geometry('+500+100')
        confirmation_message = tk.Message(
            confirmation_window, width=500,
            text='Confirm database writing'
        )
        confirmation_buttons_frame = tk.Frame(confirmation_window)
        confirmation_yes = tk.Button(
            confirmation_buttons_frame, text='Yes', foreground='red',
            command=lambda: self.write_db_confirmed(confirmation_window)
        )
        confirmation_no = tk.Button(
            confirmation_buttons_frame, text='No', foreground='red',
            command=confirmation_window.destroy
        )
        confirmation_no.pack(side='left')
        confirmation_yes.pack(side='left')
        confirmation_message.pack()
        confirmation_buttons_frame.pack(side='bottom')
        return

    def write_db_confirmed(self, window):
        window.destroy()
        return self.write_db()

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

    def return_to_edit(self):
        return self.show_edit_screen(self.entry)

    def prep_db_write(self):
        print('not implemented')

    def show_restrictions(self):
        print('not implemented')
        return

    def back_to_main_menu(self):
        self.entry = None
        self.clear_entry_fields()
        return self.query_bot.back_to_main_with_destroy()

    def back_to_results(self):
        self.entry = None
        self.clear_entry_fields()
        self.destroy_packed_widgets(self.main_frame)
        self.query_bot.show_db_results()
        return

    def delete_entry_confirmation(self):
        confirmation_window = tk.Toplevel(
            self.main_frame, background='#555555'
        )
        confirmation_window.minsize(300,100)
        confirmation_window.geometry('+500+100')
        confirmation_message = tk.Message(
            confirmation_window, width=500,
            text='Are you sure you want to delete this entry?'
        )
        confirmation_buttons_frame = tk.Frame(confirmation_window)
        confirmation_yes = tk.Button(
            confirmation_buttons_frame, text='Yes', foreground='red',
            command=lambda: self.delete_entry_confirmed(confirmation_window)
        )
        confirmation_no = tk.Button(
            confirmation_buttons_frame, text='No', foreground='red',
            command=confirmation_window.destroy
        )
        confirmation_no.pack(side='left')
        confirmation_yes.pack(side='left')
        confirmation_message.pack()
        confirmation_buttons_frame.pack(side='bottom')
        return

    def delete_entry_confirmed(self, window):
        window.destroy()
        return self.delete_entry()

class SongEditObject(EditObject):
    def __init__(self, db_bot, master_frame):
        super().__init__(db_bot, master_frame)
        self.table = 'Songs'
        self.columns = (
            'Title', 'Album', 'Artist', 'Composer',
            'Key', 'Chords', 'Lyrics', 'Year'
        )
        self.title_var = tk.StringVar()
        self.album_var = tk.StringVar()
        self.artist_var = tk.StringVar()
        self.composer_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.key_var = tk.StringVar()
        self.edit_var_list = [
            self.title_var, self.album_var, self.artist_var,
            self.composer_var, self.year_var, self.key_var
        ]

    def set_edit_gui(self):
        self.edit_frame = tk.Frame(self.main_frame)
        self.edit_message = tk.Message(
            self.main_frame, width=500,
            text='New Entry'
        )
        edit_frame_1 = tk.Frame(self.edit_frame)
        title_entry = tk.Entry(
            edit_frame_1, textvariable=self.title_var
        )
        title_entry_label = tk.Label(
            edit_frame_1, text='Title'
        )
        title_entry_label.pack(side='left')
        title_entry.pack(side='left')
        album_entry = tk.Entry(
            edit_frame_1, textvariable=self.album_var
        )
        album_entry_label = tk.Label(
            edit_frame_1, text='Album'
        )
        album_entry_label.pack(side='left')
        album_entry.pack(side='left')
        edit_frame_2 = tk.Frame(self.edit_frame)
        artist_entry = tk.Entry(
            edit_frame_2, textvariable=self.artist_var
        )
        artist_entry_label = tk.Label(
            edit_frame_2, text='Artist'
        )
        artist_entry_label.pack(side='left')
        artist_entry.pack(side='left')
        composer_entry = tk.Entry(
            edit_frame_2, textvariable=self.composer_var
        )
        composer_entry_label = tk.Label(
            edit_frame_2, text='Composer'
        )
        composer_entry_label.pack(side='left')
        composer_entry.pack(side='left')
        edit_frame_3 = tk.Frame(self.edit_frame)
        year_entry = tk.Entry(
            edit_frame_3, textvariable=self.year_var
        )
        year_entry_label = tk.Label(
            edit_frame_3, text='Year'
        )
        year_entry_label.pack(side='left')
        year_entry.pack(side='left')
        key_entry = tk.Entry(
            edit_frame_3, textvariable=self.key_var
        )
        key_entry_label = tk.Label(
            edit_frame_3, text='Key'
        )
        key_entry_label.pack(side='left')
        key_entry.pack(side='left')
        edit_frame_4 = tk.Frame(
            self.edit_frame, borderwidth=2,
            background='black'
        )
        self.chords_entry = tk.Text(edit_frame_4, width=100, height=10)
        chords_entry_label = tk.Label(
            edit_frame_4, text='Chords'
        )
        chords_entry_label.pack(side='left')
        self.chords_entry.pack(side='left')
        edit_frame_5 = tk.Frame(
            self.edit_frame, borderwidth=2,
            background='black'
        )
        self.lyrics_entry = tk.Text(edit_frame_5, width=100)
        lyrics_scrollbar = tk.Scrollbar(
            edit_frame_5, command=self.lyrics_entry.yview
        )
        lyrics_scrollbar.pack(side='right')
        self.lyrics_entry['yscrollcommand'] = lyrics_scrollbar.set
        lyrics_entry_label = tk.Label(
            edit_frame_5, text='Lyrics  '
        )
        lyrics_entry_label.pack(side='left')
        self.lyrics_entry.pack(side='left')


        edit_control_frame = tk.Frame(self.main_frame)
        edit_submit_button = tk.Button(
            edit_control_frame, text='Submit Changes', foreground='red',
            command=self.prep_db_write
        )
        back_to_results_button = tk.Button(
            edit_control_frame, text='Back To Results', foreground='red',
            command=self.back_to_results
        )
        back_to_main_button = tk.Button(
            edit_control_frame, text='Back To Main Menu',
            foreground='red',
            command=self.back_to_main_menu
        )
        exit_button = tk.Button(
            edit_control_frame, text='Exit', foreground='red',
            command=self.gui_root.quit
        )
        delete_entry_button = tk.Button(
            edit_control_frame, text='Delete Entry', foreground='red',
            command=self.delete_entry_confirmation
        )
        exit_button.pack(side='right', expand=True, fill='both')
        back_to_main_button.pack(side='right', expand=True, fill='both')
        if self.entry != None:
            back_to_results_button.pack(side='right', expand=True, fill='both')
        edit_submit_button.pack(side='right', expand=True, fill='both')


        if self.entry != None:
            delete_entry_button.pack(side='right')
            self.new_object_dict = {'row_id':self.entry.get_id()}
            self.title_var.set(self.entry.get_value('Title'))
            self.album_var.set(self.entry.get_value('Album'))
            self.artist_var.set(self.entry.get_value('Artist'))
            self.composer_var.set(self.entry.get_value('Composer'))
            self.key_var.set(self.entry.get_value('Key'))
            self.chords_entry.insert(1.0, self.entry.get_value('Chords'))
            self.lyrics_entry.insert(1.0, self.entry.get_value('Lyrics'))
            self.year_var.set(self.entry.get_value('Year'))
            self.edit_message.destroy()
        else:
            self.edit_message.pack()

        self.main_frame.pack()
        self.edit_frame.pack()
        edit_frame_1.pack()
        edit_frame_2.pack()
        edit_frame_3.pack()
        edit_frame_4.pack(fill='both')
        edit_frame_5.pack(fill='both')
        edit_control_frame.pack(expand=True, fill='both')

        self.master_frame.update()
        return

    def prep_db_write(self):
        self.new_values = {
            'Title':self.title_var.get(), 'Album':self.album_var.get(),
            'Artist':self.artist_var.get(), 'Composer':self.composer_var.get(),
            'Key':self.key_var.get(),
            'Chords':self.chords_entry.get(1.0, 'end'),
            'Lyrics':self.lyrics_entry.get(1.0, 'end'),
            'Year':self.year_var.get()
        }
        return self.write_entry()

    def clear_entry_fields(self):
        for field in self.edit_var_list:
            field.set('')
        self.chords_entry.delete(1.0, 'end')
        self.lyrics_entry.delete(1.0, 'end')
        return

    def create_new_music_object(self, new_object_dict):
        self.entry = mods.music_box.Song(
            *new_object_dict.values()
        )
        return

class SetListEditObject(EditObject):
    def __init__(self, db_bot, master_frame):
        super().__init__(db_bot, master_frame)
        self.table = 'SetLists'
        self.columns = (
            'Band', 'Date', 'Venue', 'Songs'
        )
        self.band_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.venue_var = tk.StringVar()
        self.edit_var_list = [
            self.band_var, self.date_var, self.venue_var
        ]

    def set_edit_gui(self):
        self.edit_frame = tk.Frame(self.main_frame)
        self.edit_message = tk.Message(
            self.main_frame, width=500,
            text='New Entry'
        )
        edit_frame_1 = tk.Frame(self.edit_frame)
        band_entry = tk.Entry(
            edit_frame_1, textvariable=self.band_var
        )
        band_entry_label = tk.Label(
            edit_frame_1, text='Band'
        )
        band_entry_label.pack(side='left')
        band_entry.pack(side='left')
        date_entry = tk.Entry(
            edit_frame_1, textvariable=self.date_var
        )
        date_entry_label = tk.Label(
            edit_frame_1, text='Date'
        )
        date_entry_label.pack(side='left')
        date_entry.pack(side='left')
        venue_entry = tk.Entry(
            edit_frame_1, textvariable=self.venue_var
        )
        venue_entry_label = tk.Label(
            edit_frame_1, text='Venue'
        )
        venue_entry_label.pack(side='left')
        venue_entry.pack(side='left')
        edit_frame_2 = tk.Frame(
            self.edit_frame, borderwidth=2,
            background='black'
        )
        self.songs_entry = tk.Text(edit_frame_2, width=100)
        songs_entry_label = tk.Label(
            edit_frame_2, text='Songs'
        )
        songs_entry_label.pack(side='left')
        self.songs_entry.pack(side='left')


        edit_control_frame = tk.Frame(self.main_frame)
        edit_submit_button = tk.Button(
            edit_control_frame, text='Submit Changes', foreground='red',
            command=self.prep_db_write
        )
        back_to_results_button = tk.Button(
            edit_control_frame, text='Back To Results', foreground='red',
            command=self.back_to_results
        )
        back_to_main_button = tk.Button(
            edit_control_frame, text='Back To Main Menu',
            foreground='red',
            command=self.back_to_main_menu
        )
        exit_button = tk.Button(
            edit_control_frame, text='Exit', foreground='red',
            command=self.gui_root.quit
        )
        delete_entry_button = tk.Button(
            edit_control_frame, text='Delete Entry', foreground='red',
            command=self.delete_entry_confirmation
        )
        exit_button.pack(side='right')
        back_to_main_button.pack(side='right')
        if self.entry != None:
            back_to_results_button.pack(side='right')
        edit_submit_button.pack(side='right')


        if self.entry != None:
            delete_entry_button.pack(side='right')
            self.new_object_dict = {'row_id':self.entry.get_id()}
            self.band_var.set(self.entry.get_value('Band'))
            self.date_var.set(self.entry.get_value('Date'))
            self.venue_var.set(self.entry.get_value('Venue'))
            self.songs_entry.insert(1.0, self.entry.get_value('Songs'))
            self.edit_message.destroy()
        else:
            self.edit_message.pack()

        self.main_frame.pack()
        self.edit_frame.pack()
        edit_frame_1.pack()
        edit_frame_2.pack(fill='both')
        edit_control_frame.pack()

        self.master_frame.update()
        return

    def prep_db_write(self):
        self.new_values = {
            'Band':self.band_var.get(), 'Date':self.date_var.get(),
            'Venue':self.venue_var.get(),
            'Songs':self.songs_entry.get(1.0, 'end')
        }
        return self.write_entry()

    def clear_entry_fields(self):
        for fields in self.edit_var_list:
            fields.set('')
        self.songs_entry.delete(1.0, 'end')
        return


    def create_new_music_object(self, new_object_dict):
        self.entry = mods.music_box.SetList(
            *new_object_dict.values()
        )
        return
