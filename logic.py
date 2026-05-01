import csv
from PyQt6.QtWidgets import *
from gui import *

#To run after QT updates (terminal): pyuic6 -x gui.ui -o gui.py

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        """
        Starts up the GUI window and allows for submit button use with mouse or enter key
        :return: None
        """

        super().__init__()
        self.setupUi(self)
        self.submit_button.clicked.connect(lambda: self.__submit_vote())
        self.id_input.returnPressed.connect(self.__submit_vote)  # Google helped for enter button submitting


    def __submit_vote(self) -> None:
        """
        Will check if voter_id is int, is a length of 8, and is not already in data.csv
        :return: None
        """

        voter_id = self.id_input.text().strip()

        if self.vote_buttonsG.checkedButton() is None:
            self.__fail("no candidate")
            return

        try:
            try:
                int(voter_id)
            except ValueError:
                raise TypeError

            if (len(voter_id)) != 8:
                raise ValueError

        except ValueError:
            self.__fail("only 8 nums")
            return
        except TypeError:
            self.__fail("no non nums")
            return


        with open('data.csv', 'a+', newline='') as csvfile:
            csvfile.seek(0)  # AI helped slightly in logic for searching in the csv to compare
            reader = csv.reader(csvfile)
            existing_ids = []

            for row in reader:
                existing_ids.append(row)

            for value in existing_ids:
                if voter_id == value[1]:
                    self.__fail("already voted")
                    return

            writer = csv.writer(csvfile)
            writer.writerow(["Voter ID: ",voter_id])

        self.id_input.clear()
        self.need_8_label.clear()
        self.repeat_label.clear()
        self.id_input.setFocus() # Google helped for returning the focus to entry box


    def __fail(self, error_type) -> None:
        """
        Will process each parameter given from a failure to enter the ID

        :param error_type: the error/problem raised from submit_vote checking,will be from either non-int
                            characters, too many/few ints, or the voter id already being in the csv
        :return: None
        """
        if error_type == "no candidate":
            self.need_8_label.setText("Need to select a candidate")
            self.id_input.setFocus()
        if error_type == "only 8 nums":
            self.id_input.clear()
            self.repeat_label.clear()
            self.need_8_label.setText("Only 8 numbers are allowed")
            self.id_input.setFocus()
        if error_type == "no non nums":
            self.id_input.clear()
            self.repeat_label.clear()
            self.need_8_label.setText("Please only enter numbers")
            self.id_input.setFocus()
        if error_type == "already voted":
            self.id_input.clear()
            self.need_8_label.clear()
            self.repeat_label.setText("Already Voted")
            self.id_input.setFocus()