#!/usr/bin/env python3.7

class MusicBox:
    def __init__(self, id):
        self.dbID = id
        self.object_dict = {}
        self.undo_stack = []
        self.redo_stack = []

    def get_columns(self):
        return tuple(self.object_dict.keys())

    def get_id(self):
        return self.dbID

    def get_table(self):
        return self.table

    def get_value(self, keys):
        if not(isinstance(keys, str)):
            value = []
            for key in keys:
                value.append(self.object_dict[key])
            value = tuple(value)
        else:
            value = self.object_dict[keys]
        return value

    def get_object_dict(self):
        return self.object_dict

    def set_object_dict(self, write_dict):
        self.object_dict.update(write_dict)

    def set_object_dict_undo(self, keys):
        if not(keys == []):
            self.undo_stack.append(self.object_dict)
        return

    def object_dict_undo(self):
        self.redo_stack.append(self.object_dict)
        self.object_dict = self.undo_stack.pop()
        return

    def object_dict_redo(self):
        self.undo_stack.append(self.object_dict)
        self.object_dict = self.redo_stack.pop()
        return


class Song(MusicBox):
    def __init__(self, id, title, album, artist, composer,
            key, chords , lyrics,  year
        ):
        super().__init__(id)
        self.object_dict = {
            'Title': title, 'Album': album, 'Artist': artist,
            'Composer': composer, 'Key': key, 'Chords': chords,
            'Lyrics': lyrics, 'Year': year
        }
        self.table = 'Songs'

    def __str__(self):
        return f"SongObj{self.object_dict['Title']}"

    def __repr__(self):
        return f"Song Object: {self.object_dict['Title']}"

    def show_full_entry(self):
        print(f'Title:{self.object_dict["Title"]} | Album:{self.object_dict["Album"]} | '
              f'Artist:{self.object_dict["Artist"]} | Composer:{self.object_dict["Composer"]} '
              f'| Year:{self.object_dict["Year"]}'
        )
        print(f'Key:{self.object_dict["Key"]} | Chords:{self.object_dict["Chords"]}')
        print(f'Lyrics:{self.object_dict["Lyrics"]}')
        return

    def get_full_details(self):
        full_details = (
            f'Title: {self.object_dict["Title"]}\n'
            f'Album: {self.object_dict["Album"]}\n'
            f'Artist: {self.object_dict["Artist"]}\n'
            f'Composer: {self.object_dict["Composer"]}'
            f' | Year: {self.object_dict["Year"]}'
        )
        return full_details

class SetList(MusicBox):
    def __init__(self, id, band, date, venue, songs):
        super().__init__(id)
        self.object_dict = {
            'Band': band, 'Date': date, 'Venue': venue, 'Songs': songs
        }
        self.table = 'SetLists'

    def __str__(self):
        return f'{self.object_dict["Band"]} - {self.object_dict["Date"]}'

    def __repr__(self):
        return f'SetList Object:{self.object_dict["Band"]} - {self.object_dict["Date"]}'

    def show_full_entry(self):
        print(f'{self.object_dict["Band"]} - {self.object_dict["Date"]} @ {self.object_dict["Venue"]}')
        return

    def get_full_details(self):
        full_details = (
            f'Band: {self.object_dict["Band"]}\n'
            f'Date: {self.object_dict["Date"]}\n'
            f'Venue: {self.object_dict["Venue"]}\n'
            f'Songs: {self.object_dict["Songs"]}'
        )
        return full_details
