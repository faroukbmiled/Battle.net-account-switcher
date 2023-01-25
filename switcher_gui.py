import os
import json
import psutil
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore
import time
import sys


class BattleNetSwitcher(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ryuk's Battle.net Account Switcher")
        self.setWindowIcon(QtGui.QIcon('ryuk.ico'))
        font = QtGui.QFont("Arial", 10)
        app.setFont(font)
        self.name_label = QtWidgets.QLabel(
            "\nRyuk's Switcher\n")
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.setGeometry(100, 100, 250, 250)
        font = self.name_label.font()
        font.setPointSize(15)
        self.name_label.setFont(font)

        os.chdir(os.path.expandvars(r"%APPDATA%\Battle.net"))
        with open("Battle.net.config", "r") as f:
            self.config = json.load(f)
        self.accounts = self.config["Client"]["SavedAccountNames"].split(",")

        self.account_button_group = QtWidgets.QButtonGroup()
        self.account_button_group.setExclusive(True)
        self.account_buttons = []
        for i, account in enumerate(self.accounts):
            button = QtWidgets.QRadioButton(account)
            button.setStyleSheet(
                "QRadioButton { background-color: #1d1f23; color: white; font-weight: bold; padding: 10px; border-radius: 5px; } QRadioButton:hover { background-color: #6f7080; } QRadioButton:pressed { background-color: green;}")
            self.account_button_group.addButton(button)
            self.account_buttons.append(button)
            if i == 0:
                button.setChecked(True)

        self.switch_button = QtWidgets.QPushButton("Switch", self)
        self.switch_button.setStyleSheet(
            "QPushButton { background-color: #1d1f23; color: white; font-weight: bold; padding: 10px; border-radius: 5px; } QPushButton:hover { background-color: #6f7080; } QPushButton:pressed { background-color: green;}")
        self.add_button = QtWidgets.QPushButton("Add", self)
        self.add_button.setStyleSheet(
            "QPushButton { background-color: #1d1f23; color: white; font-weight: bold; padding: 10px; border-radius: 5px; } QPushButton:hover { background-color: #6f7080; } QPushButton:pressed { background-color: green;}")
        self.remove_button = QtWidgets.QPushButton("Remove", self)
        self.remove_button.setStyleSheet(
            "QPushButton { background-color: #1d1f23; color: white; font-weight: bold; padding: 10px; border-radius: 5px; } QPushButton:hover { background-color: #6f7080; } QPushButton:pressed { background-color: green;}")

        self.add_button.clicked.connect(self.add_account)
        self.remove_button.clicked.connect(self.remove_account)
        self.switch_button.clicked.connect(self.switch_account)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.name_label)
        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)
        for button in self.account_buttons:
            layout.addWidget(button)
        layout.addWidget(self.switch_button)
        self.setStyleSheet('''
        QWidget {
            background-color: #2f303b;
            color: white;
        }
        QPushButton {
            background-color: white;
            color: black;
        }
        ''')

    def switch_account(self):
        selected_button = self.account_button_group.checkedButton()
        selected_account = selected_button.text()

        new_accounts = [selected_account]
        for account in self.accounts:
            if account != selected_account:
                new_accounts.append(account)
        self.config["Client"]["SavedAccountNames"] = ",".join(new_accounts)

        if "Battle.net.exe" not in (p.name() for p in psutil.process_iter()):
            print("Battle.net is not running.")
        else:
            print("Stopping Battle.net...")
            os.system("taskkill /IM Battle.net.exe /F")

        os.system(f"copy Battle.net.config Battle.net.config.switcher-backup")
        with open("Battle.net.config", "w") as f:
            json.dump(self.config, f)

        print("Launching Battle.net...")
        subprocess.run([BATTLE_NET])

    def add_account(self):
        email, ok = QtWidgets.QInputDialog.getText(self, "New Account", "Email:", QtWidgets.QLineEdit.Normal, "")
        if ok and email!="":
            reply = QtWidgets.QMessageBox.question(self, 'Confirm',
                                                   f'Do you want to add {email} as a new account?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                button = QtWidgets.QRadioButton(email)
                button.setStyleSheet("QRadioButton { background-color: #1d1f23; color: white; font-weight: bold; padding: 10px; border-radius: 5px; } QRadioButton:hover { background-color: #6f7080; } QRadioButton:pressed { background-color: green;}")
                self.account_button_group.addButton(button)
                self.account_buttons.append(button)
                self.layout().insertWidget(len(self.accounts), button)
                button.setChecked(True)
                self.accounts.append(email)
                self.config["Client"]["SavedAccountNames"] = ",".join(self.accounts)
                with open("Battle.net.config", "w") as f:
                    json.dump(self.config, f)
                self.switch_account()

    def remove_account(self):
        selected_button = self.account_button_group.checkedButton()
        selected_account = selected_button.text()
        new_accounts = [account for account in self.accounts if account != selected_account]
        self.config["Client"]["SavedAccountNames"] = ",".join(new_accounts)
        with open("Battle.net.config", "w") as f:
            json.dump(self.config, f)
        self.accounts = new_accounts
        self.account_buttons = []
        layout = self.layout()
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

        layout.addWidget(self.name_label)
        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)
        for i, account in enumerate(self.accounts):
            button = QtWidgets.QRadioButton(account)
            button.setStyleSheet(
                "QRadioButton { background-color: #1d1f23; color: white; font-weight: bold; padding: 10px; border-radius: 5px; } QRadioButton:hover { background-color: #6f7080; } QRadioButton:pressed { background-color: green;}")
            self.account_button_group.addButton(button)
            self.account_buttons.append(button)
            layout.addWidget(button)
        layout.addWidget(self.switch_button)



if __name__ == "__main__":
    BATTLE_NET = "C:\\Program Files (x86)\\Battle.net\\Battle.net Launcher.exe"
    app = QtWidgets.QApplication([])
    window = BattleNetSwitcher()
    window.show()
    app.exec_()
