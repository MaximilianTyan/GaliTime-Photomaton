#!/bin/env python3
# encoding:utf-8
# coding:utf-8

"""
Module to handle the event options page
"""

import logging

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QDateEdit
from PyQt5.QtWidgets import QAbstractSpinBox

from PyQt5.QtCore import Qt, QDate

from ..managers.eventmanager import EventManager
from ..screenwindow import ScreenWindow

from .. import stylesheet
from ..constants import DATEFORMAT

logger = logging.getLogger(__name__)
logger.propagate = True


class OptionsPage:
    """
    StartPage : Handles option page functionnality
    """

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        self.tempEventInfo = {
            "saveFolder": None,
            "decorFile": None,
            "eventName": None,
            "eventDate": None,
        }

        self.EventInput = None
        self.EventDateInput = None
        self.saveFolderPathLabel = None
        self.DecorFileLabel = None
        self.errorLabel = None

        self.screenWindow = ScreenWindow.getScreen()

        self.eventOpened = False

    def load(self):
        """
        load : Loads the option page in a QWidget and returns it

        Returns:
            PyQt5.QtWidget: Option page loaded layout
        """
        logger.debug("Loading options page")
        # Main layout, vertical, contains Title, Button Layout
        MainContainer = QWidget(self.mainWindow)
        MainVLayout = QVBoxLayout()
        MainVLayout.setAlignment(Qt.AlignVCenter)
        MainContainer.setLayout(MainVLayout)

        # 1. Label "GaliTime Options"
        TitleLabel = QLabel("GaliTime - Options")
        TitleLabel.setStyleSheet("font-size: 50px")
        TitleLabel.setAlignment(Qt.AlignCenter)
        MainVLayout.addWidget(TitleLabel)

        # 2 Options GridLayout EventName
        OptionsGridLayout = QGridLayout()
        MainVLayout.addLayout(OptionsGridLayout)

        # 2.1 Line Edit
        self.EventInput = QLineEdit(EventManager.getEventName())
        self.EventInput.setPlaceholderText("Nom de l'??v??nement")
        self.EventInput.setAlignment(Qt.AlignCenter)
        OptionsGridLayout.addWidget(self.EventInput, 1, 1)

        # 2.2 Validate Button
        ValidateNameButton = QPushButton("Valider")
        ValidateNameButton.clicked.connect(self.changeEventName)
        ValidateNameButton.setStyleSheet(stylesheet.BigFlatButton)
        OptionsGridLayout.addWidget(ValidateNameButton, 1, 2)

        # 3.1 Date
        self.EventDateInput = QDateEdit(QDate.currentDate())
        self.EventDateInput.setDisplayFormat(DATEFORMAT)
        self.EventDateInput.setAlignment(Qt.AlignCenter)
        self.EventDateInput.setButtonSymbols(QAbstractSpinBox.NoButtons)
        OptionsGridLayout.addWidget(self.EventDateInput, 2, 1)

        # 3.2 Date
        ValidateDateButton = QPushButton("Valider")
        ValidateDateButton.clicked.connect(self.changeEventDate)
        ValidateDateButton.setStyleSheet(stylesheet.BigFlatButton)
        OptionsGridLayout.addWidget(ValidateDateButton, 2, 2)

        # 4.1 saveFolderPath label
        self.saveFolderPathLabel = QLabel(
            "Dossier d'enregistrement:\n" + EventManager.getEventFolder()
        )
        self.saveFolderPathLabel.setAlignment(Qt.AlignCenter)
        self.saveFolderPathLabel.setWordWrap(True)
        OptionsGridLayout.addWidget(self.saveFolderPathLabel, 3, 1)

        # 4.2 Browe button
        BrowseButton = QPushButton("Parcourir")
        BrowseButton.clicked.connect(self.chooseSaveFolderButtonCall)
        BrowseButton.setStyleSheet(stylesheet.BigFlatButton)
        OptionsGridLayout.addWidget(BrowseButton, 3, 2)

        # 5.1 Decorfile label
        self.DecorFileLabel = QLabel(
            "Image de D??coration:\n" + self.screenWindow.getDecorFile()
        )
        self.DecorFileLabel.setAlignment(Qt.AlignCenter)
        self.saveFolderPathLabel.setWordWrap(True)
        OptionsGridLayout.addWidget(self.DecorFileLabel, 4, 1)

        # 5.2 Browe button
        BrowseButton2 = QPushButton("Choisir")
        BrowseButton2.clicked.connect(self.chooseDecorFileButtonCall)
        BrowseButton2.setStyleSheet(stylesheet.BigFlatButton)
        OptionsGridLayout.addWidget(BrowseButton2, 4, 2)

        # 6 Error Label
        self.errorLabel = QLabel()
        self.errorLabel.setAlignment(Qt.AlignCenter)
        self.errorLabel.setStyleSheet("color: rgb(200,50,50)")
        MainVLayout.addWidget(self.errorLabel)

        # 7 Save & Cancel button
        ExitButtonsLayout = QHBoxLayout()
        MainVLayout.addLayout(ExitButtonsLayout)

        # 7.1 Save Button
        SaveButton = QPushButton("Enregistrer")
        SaveButton.setStyleSheet(stylesheet.BigButton)
        SaveButton.clicked.connect(self.controlPageCheck)
        ExitButtonsLayout.addWidget(SaveButton)

        # 7.1 Cancel Button
        CancelButton = QPushButton("Annuler")
        CancelButton.setStyleSheet(stylesheet.BigRedButton)
        CancelButton.clicked.connect(self.cancelOptions)
        ExitButtonsLayout.addWidget(CancelButton)

        TitleLabel.setFocus()

        logger.debug("Options page loaded")
        return MainContainer

    def chooseSaveFolderButtonCall(self) -> None:
        """
        choosesaveFolderPath : Prompts the user with a file dialog to choose
        the save folder where to save the event.
        """
        parentFolderPath = QFileDialog.getExistingDirectory(
            self.mainWindow, caption="Dossier d'enregistrement"
        )

        saveFolderPath = parentFolderPath + "/" + self.tempEventInfo["eventName"] + "/"

        self.tempEventInfo["saveFolder"] = saveFolderPath
        self.saveFolderPathLabel.setText("Dossier d'enregistrement:\n" + saveFolderPath)

    def chooseDecorFileButtonCall(self) -> None:
        """
        chooseDecorFile : Prompts the user with a file dialog to choose the
        save folder where to save the event.
        """
        selectedFilename = QFileDialog.getOpenFileName(
            self.mainWindow, caption="Image de d??cor"
        )[0]

        self.tempEventInfo["decorFile"] = selectedFilename
        self.DecorFileLabel.setText("Image de d??cor:\n" + selectedFilename)

    def changeEventName(self) -> None:
        """
        changeEventName : Retrieves the event name from the text input and
        saves it as event name
        """
        if self.EventInput.text().strip() != "":
            self.tempEventInfo["eventName"] = self.EventInput.text()

            self.EventInput.setStyleSheet("background-color: rgb(100, 200, 100)")
        else:
            self.EventInput.setStyleSheet("background-color: rgb(200, 100, 100)")

    def changeEventDate(self) -> None:
        """
        changeEventDate : Retrieves the event name from the text input and
        saves it as event name
        """
        date = self.EventDateInput.date()
        if date.isValid():
            self.tempEventInfo["eventDate"] = date.toString(DATEFORMAT)

            self.EventDateInput.setStyleSheet("background-color: rgb(100, 200, 100)")
        else:
            self.EventDateInput.setStyleSheet("background-color: rgb(200, 100, 100)")

    # Page switch

    def controlPageCheck(self) -> None:
        """
        controlPageCheck : Checks if all required information for event loading was
        provided and displays an error message if any is missing
        """

        checkDict = {
            "eventName": "Le nom de l'??v??nement doit ??tre valid??e",
            "eventDate": "La date de l'??v??nement doit ??tre valid??e",
            "saveFolder": "Le dossier d'enregistrement doit ??tre valide",
            "decorFile": "Le fichier de d??coration doit ??tre valide",
        }
        for field, errorMsg in checkDict.items():
            if self.tempEventInfo[field] is None:
                self.errorLabel.setText(errorMsg)
                return

        EventManager.setEventName(self.tempEventInfo["eventName"])
        EventManager.setEventDate(self.tempEventInfo["eventDate"])
        EventManager.setEventFolder(self.tempEventInfo["saveFolder"])
        self.screenWindow.setDecorFile(self.tempEventInfo["decorFile"])

        EventManager.initSaveFolder(EventManager.getEventFolder())

        if not self.eventOpened:
            self.screenWindow.startPreview()
            self.eventOpened = True

        self.mainWindow.loadPage("control")

    def cancelOptions(self) -> None:
        """
        cancelOptions : Return function for the option page, returns either to the
        control page if an event is opened, to start page otherwise
        """
        if self.eventOpened:
            self.mainWindow.loadPage("control")
        else:
            self.mainWindow.loadPage("start")
