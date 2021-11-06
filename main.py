"""
https://wiki.tcl-lang.org/page/tkinter.Label

"""
from tkinter import *
import sqlite3

ROOT_GEOMETRY = "500x500"
ROOT_TITLE = "Registration Form"


class RegistrationForm:
    __LABELS = ('FirstName', 'LastName', 'Email', 'Gender', 'Country', 'Language')

    def __init__(self):
        """

        """
        self._entries = {}
        self._form = Tk()
        self.__configure_form()
        self.__conn = sqlite3.connect('example.db')

    def __signup_user(self):
        data = {}
        is_valid = True
        for key, value in self._entries.items():
            if not value:
                value.set("This field is required!")
                is_valid = False
            else:
                data.update({key.lower(): value.get()})

        if is_valid:
            # check user existance
            cursor = self.__conn.cursor()
            cursor.execute(f"SELECT * FROM `users` WHERE `username` = {data.get('username')}")
            if cursor.fetchone() is not None:
                print("Username has been already taken.")
            else:
                cursor.execute(
                    f"INSERT INTO `user` (firstname, lastname, username, password, gender, country, language) VALUES({data.get('firstname')}, {data.get('lastname')}, {data.get('username')}, {data.get('password')}, {data.get('gender')}, {data.get('country')}, {data.get('language')})")
                self.__conn.commit()

                for value in self._entries.values():
                    value.set("")

                cursor.close()
                self.__conn.close()

    def __pack_labels(self):
        """

        :return:
        """
        # labels
        for label_name in self.__LABELS:
            # create a frame at first
            frame_widget = Frame(self._form)
            # create label
            label_widget = Label(frame_widget, width=22, text=f"{label_name}: ", anchor='w')

            # create entry to get input from user
            entry_widget = Entry(frame_widget)
            entry_widget.insert(0, label_name.title())

            frame_widget.pack(side=TOP, fill=X, padx=5, pady=5)
            label_widget.pack(side=LEFT)
            entry_widget.pack(side=RIGHT, expand=YES, fill=X)

            self._entries[label_name] = entry_widget

    def __pack_buttons(self):
        button = Button(self._form, text="Registration", command=(lambda: self.__signup_user()))
        button.pack(side=BOTTOM, padx=5, pady=5)

    def __configure_form(self):
        """

        :return:
        """

        self._form.geometry(ROOT_GEOMETRY)
        self._form.title(ROOT_TITLE)
        self.__pack_labels()
        self.__pack_buttons()

    def run(self):
        self._form.mainloop()


if __name__ == '__main__':
    RegistrationForm().run()
