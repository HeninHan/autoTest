"""
This module creates a graphical user interface (GUI) for a test application.
The GUI includes a treeview to display test data, a text box to display test logs,
and buttons to load data, run tests, and clear the test log.
"""

import time
from tkinter import *
import tkinter as tk
from tkinter import ttk

# Define color constants for the treeview rows
ODD_DEFAULT = '#F0F0F0'
EVEN_DEFAULT = '#E0E0E0'
ODD_PASS = '#00FF00'
EVEN_PASS = '#00EE00'
ODD_FAIL = '#FF0000'
EVEN_FAIL = '#EE0000'

# Define a template string for the test log
test_str = """
**************************************************
Test Name:{0}
USL:1        LSL:1        
Result:PASS
Output:
TEST PASSED
TEST PASSED
TEST PASSED
TEST PASSED
TEST PASSED
TEST PASSED
TEST PASSED
**************************************************

"""

class TestUI:
    """
    The main class for the user interface.

    This class creates and manages all the widgets in the user interface.
    """

    def __init__(self, root: Tk):
        """
        Initialize the UI class.

        :param root: The root window.
        """
        self._root = root
        self._top_frame = ttk.Frame(self._root)
        self._top_frame.pack(fill='x', side='top')
        self._check_count = 0
        self._test_fail_item = []

        # Create buttons for loading data, running tests, and clearing the test log
        self._btn_load = ttk.Button(self._top_frame, text="Load", command=self.load_data)
        self._btn_load.grid(row=0, column=0, sticky='w')
        self._btn_test = ttk.Button(self._top_frame, text="Test", command=self.test)
        self._btn_test.grid(row=0, column=1, sticky='w')
        self._btn_clear = ttk.Button(self._top_frame, text="Clear", command=self.clear)
        self._btn_clear.grid(row=0, column=2, sticky='w')
        self._btn_clear = ttk.Button(self._top_frame, text="Check", command=self.check)
        self._btn_clear.grid(row=0, column=3, sticky='w')

        # Create a frame to hold the treeview and text box
        self._mid_frame = ttk.Frame(self._root, height=1000)
        self._mid_frame.pack()

        # Create a frame to hold the treeview
        self._left_frame = ttk.Frame(self._mid_frame)
        self._left_frame.pack(side='left', fill='y')
        self.create_treeview(self._left_frame)
        self._ret_label = tk.Label(self._left_frame, text="Test Failed Items: ")
        self._ret_label.grid(row=1, column=0, sticky='w')

        # Create a frame to hold the text box
        self._right_frame = ttk.Frame(self._mid_frame)
        self._right_frame.pack(side='right', fill='y')
        self._test_log = tk.Text(self._right_frame, width=50)
        self._test_log.grid(row=0, column=0)
        self._test_log_yscrollbar = tk.Scrollbar(self._right_frame, orient=tk.VERTICAL, command=self._test_log.yview)
        self._test_log_yscrollbar.grid(row=0, column=1, sticky='ns')
        self._test_log.configure(yscrollcommand=self._test_log_yscrollbar.set)

    def check(self):
        print(self._test_fail_item[self._check_count]['test_name'])
        check_index = self._test_fail_item[self._check_count]['index']
        self._tree.yview_moveto(check_index * (1 / 1047))
        self._check_count += 1
        if self._check_count >= len(self._test_fail_item):
            print("Finish")
            self._check_count = 0
    def clear(self):
        """
        Clear the test log.
        """
        self._test_log.delete('1.0', END)

    def test(self):
        """
        Run the tests and update the treeview and test log.
        """
        item_list = self._tree.get_children()
        item_count = len(item_list)
        item_per_page = 10
        step = 1 / item_count
        print(item_count)
        import random
        random.seed(int(time.time()))
        ret = random.sample(item_list, 10)
        print(ret)

        for idx, item in enumerate(item_list):
            if self._tree.item(item)['tags'][0] == 'even':
                if str(idx) in ret:
                    self._test_fail_item.append({'test_name': self._tree.item(item)['values'][0], 'index':idx})
                    self._tree.item(item, tags='even_fail')
                else:
                    self._tree.item(item, tags='even_pass')

            else:
                if str(idx) in ret:
                    self._test_fail_item.append({'test_name': self._tree.item(item)['values'][0], 'index':idx})
                    self._tree.item(item, tags='odd_fail')
                else:
                    self._tree.item(item, tags='odd_pass')
            if idx >= item_per_page:
                self._tree.yview_moveto(idx * step)
            self._test_log.insert(END, test_str.format('Test Name ' + str(idx)), ('Test Log' + str(idx),))
            self._test_log.see(END)
            self._root.update()
        test_fail_items = ''
        for k,i in enumerate(self._test_fail_item):
            separator = '\t'
            if (k+1) % 3 == 0:
                separator = '\n'
            test_fail_items += i['test_name'] + separator
        self._ret_label['text'] = 'Test Failed Items: ' + test_fail_items

    def load_data(self):
        """
        Load the data into the treeview.
        """
        # Set the headings of the columns.
        if self._tree.get_children():
            self._tree.delete(*self._tree.get_children())
            self._tree.yview_moveto(0)
        for idx in range(1047):
            if idx % 2 == 0:
                self._tree.insert(parent='',
                                  index='end',
                                  iid=idx,
                                  text='Row 1',
                                  values=('Test Name ' + str(idx), 'Value ' + str(idx + 1), 'Value ' + str(idx + 2)),
                                  tags='even')
            else:
                self._tree.insert(parent='',
                                  index='end',
                                  iid=idx,
                                  text='Row 1',
                                  values=('Test Name ' + str(idx), 'Value ' + str(idx + 1), 'Value ' + str(idx + 2)),
                                  tags='odd')

    def create_treeview(self, master=None):
        """
        Create the treeview widget.

        :param master: The parent widget.
        """
        # Create the ttk.Treeview widget.
        self._tree = ttk.Treeview(master)
        self._tree.grid(row=0, column=0, sticky='nsew')

        # Configure the columns in the ttk.Treeview.
        self._tree['columns'] = ('one', 'two', 'three', 'four')

        # The first column is the _tree column. We don't need it, so set its width to 0.
        self._tree.column("#0", width=0, stretch=tk.NO)

        # Set the widths of the columns.
        self._tree.column("one", anchor=tk.W, width=120)
        self._tree.column("two", anchor=tk.W, width=120)
        self._tree.column("three", anchor=tk.W, width=120)
        self._tree.column("four", anchor=tk.W, width=120)

        # Set the headings of the columns.
        self._tree.heading("#0", text="", anchor=tk.W)
        self._tree.heading("one", text="Test Name", anchor=tk.W)
        self._tree.heading("two", text="LSL", anchor=tk.W)
        self._tree.heading("three", text="USL", anchor=tk.W)
        self._tree.heading("four", text="Result", anchor=tk.W)

        # Set y-scrollbar.
        self._tree_yscrollbar = tk.Scrollbar(self._left_frame, orient=tk.VERTICAL, command=self._tree.yview)
        self._tree_yscrollbar.grid(row=0, column=1, sticky='ns')
        self._tree.configure(yscrollcommand=self._tree_yscrollbar.set)

        # Set the tags for the rows.
        self._tree.tag_configure('odd', background=ODD_DEFAULT)
        self._tree.tag_configure('even', background=EVEN_DEFAULT)
        self._tree.tag_configure('odd_pass', background=ODD_PASS)
        self._tree.tag_configure('even_pass', background=EVEN_PASS)
        self._tree.tag_configure('odd_fail', background=ODD_FAIL)
        self._tree.tag_configure('even_fail', background=EVEN_FAIL)

        # Bind the selection event in the treeview.
        self._tree.bind('<<TreeviewSelect>>', self._on_select)

    def _on_select(self, event):
        """
        Handle the selection event in the treeview.

        :param event: The event object.
        """
        if self._tree.selection():
            selected_index = self._tree.selection()[0]
            navigator_str = self._tree.item(selected_index)['values'][0]
            navigator_pos = self._test_log.search(navigator_str, '1.0', stopindex=END)
            if navigator_pos:
                self._test_log.see(navigator_pos)


if __name__ == "__main__":
    root = tk.Tk()
    ui = TestUI(root)
    root.mainloop()