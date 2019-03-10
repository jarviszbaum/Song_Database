#!/usr/bin/env python3.7

class Exit:
    def __init__(self, tk_obj):
        self.name = 'exit'
        self.tk_obj = tk_obj

    def __str__(self):
        return 'Exit Object'

    def exit_prog(self):
        # print('Goodbye')
        self.tk_obj.quit()
