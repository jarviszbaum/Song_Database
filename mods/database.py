#!/usr/bin/env python3.7

import sqlite3

class DatabaseObject:
    def __init__(self, db):
        self.db_connection = sqlite3.connect(f'{db}')
        self.db_cursor = self.db_connection.cursor()
        self.db_table_dict = self.set_db_table_dict()

    def set_db_table_dict(self):
        db_table_dict = {}
        for table in self.get_db_table_list():
            db_table_dict.update(
                {f'{table}':self.get_db_table_columns(table)}
            )
        return db_table_dict

    def get_db_table_list(self):
        db_table_list = []
        for table in self.db_cursor.execute(
            "SELECT name FROM sqlite_master where type = 'table'"
        ):
            db_table_list.append(table[0])
        return db_table_list

    def get_db_table_columns(self, table):
        table_columns = []
        for columns in self.db_cursor.execute(
            f"PRAGMA table_info('{table}')"
        ):
            table_columns.append(f'{columns[1]}')
        return table_columns

    def search_db(self, queryObj):
        db_return = self.db_cursor.execute(
            f'SELECT ROWID, * FROM {queryObj.table} '
            f'WHERE {queryObj.user_column_restrictions} LIKE ?;',
            queryObj.user_search_term
        )
        return db_return

    def list_db(self, queryObj):
        db_return = self.db_cursor.execute(
            f'SELECT ROWID, * FROM {queryObj.table} '
            f'ORDER BY {queryObj.user_column_restrictions};'
        )
        return db_return

    def write_db(self, entry):
        '''entry is a music_box object'''
        self.row_id = entry.get_id()
        self.write_table = entry.get_table()
        self.prep_write_package(entry.get_object_dict())
        entry.set_object_dict_undo(self.write_columns)
        self.update_db(entry)
        return

    def delete_entry(self, entry):
        '''entry is a music_box object'''
        self.db_cursor.execute(
            f'DELETE FROM {entry.get_table()} '
            f'WHERE ROWID={entry.get_id()};'
        )
        self.db_connection.commit()
        return

    def update_db(self, entry):
        try:
            self.db_cursor.execute(
                self.determine_db_write_command(),
                self.write_values
            )
            self.db_connection.commit()
            entry.dbID = self.db_cursor.lastrowid
        except Exception as exc:
            print('error writing to db')
            print(f'**!{type(exc)}!** @-> {str(exc)}')
        return

    def prep_write_package(self, value_pack):
        if len(value_pack) == 1:
            col = tuple(value_pack.keys())
            self.write_columns = col[0]
            self.question_mark_set = '?'
        else:
            self.write_columns = tuple(value_pack.keys())
            self.question_mark_set = (
                ("(") + "?, " * (len(self.write_columns) - 1) + ("?)")
            )
        self.write_values = tuple(value_pack.values())
        return

    def determine_db_write_command(self):
        if self.row_id == None:
            command = (f'INSERT into {self.write_table} '
                       f'VALUES{self.question_mark_set};'
            )
        else:
            command = (
                f'UPDATE {self.write_table} SET {self.write_columns} = '
                f'{self.question_mark_set}'
                f'WHERE ROWID={self.row_id};'
            )
        return command

    def close_db(self):
        self.db_connection.close()
        return
