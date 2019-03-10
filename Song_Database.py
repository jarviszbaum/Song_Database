
import mods.database as database
import mods.menus as menus
import mods.query_ui as query_ui
import mods.edit_ui as edit_ui
import mods.exit as exit
import tkinter as tk
import os

script_dir = os.path.dirname(__file__)
relative_path = r'database/Songs.db'
full_db_path = os.path.join(script_dir, relative_path)

def set_default_menus():
    main_menu.set_menu(
        {'Search':('get_user_search_entry', song_query),
         'List':('load_menu', list_menu),
         'New Entry':('write_new_entry', song_edit),
         'Set List':('load_menu', setlist_menu),
         'Exit':('quit', root)}
    )
    list_menu.set_menu(
        {'Title':('list_db', song_query),
         'Album':('list_db', song_query),
         'Artist':('list_db', song_query),
         'Composer':('list_db', song_query),
         'Year':('list_db', song_query),
         'Back To Main Menu':('load_menu', main_menu),
         'Exit':('quit', root)}
    )
    setlist_menu.set_menu(
        {'Search Set Lists':('get_user_search_entry', setlist_query),
         'Write New Set List':('write_new_entry', setlist_edit),
         'Back To Main Menu':('load_menu', main_menu),
         'Exit':('quit', root)}
    )

def configure_query_and_edit_helpers():
    song_query.set_helpers(
        (db_bot,
         [main_menu, list_menu, setlist_menu],
         song_edit, root)
    )
    setlist_query.set_helpers(
        (db_bot,
         [main_menu, list_menu, setlist_menu],
         setlist_edit, root)
    )
    song_edit.set_helpers(
        (db_bot,
         [main_menu, list_menu, setlist_menu],
         song_query, root)
    )
    setlist_edit.set_helpers(
        (db_bot,
         [main_menu, list_menu, setlist_menu],
         setlist_query, root)
    )

db_bot = database.DatabaseObject(full_db_path)

root = tk.Tk()
root.minsize(500,600)
root.geometry('+300+0')
root.title('Song Database')
master_frame = tk.Frame(root)
master_frame.pack(fill='both', expand=True)
main_menu = menus.Radiobutton_Menu(
    'Main Menu', master_frame
)
list_menu = menus.Radiobutton_Menu(
    'List Menu', master_frame
)
setlist_menu = menus.Radiobutton_Menu(
    'Set List Menu', master_frame
)
song_edit = edit_ui.SongEditObject(db_bot, master_frame)
setlist_edit = edit_ui.SetListEditObject(db_bot, master_frame)
song_query = query_ui.SongQueryObject(db_bot, master_frame)
setlist_query = query_ui.SetListQueryObject(db_bot, master_frame)
set_default_menus()
configure_query_and_edit_helpers()

main_menu.load_menu()

root.mainloop()

db_bot.close_db()
