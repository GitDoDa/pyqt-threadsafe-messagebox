from PyQt5.QtWidgets import (
    QApplication, QMessageBox, QDialog, QLabel, QVBoxLayout, QPushButton,
    QComboBox, QWidget, QStyleFactory
)

from PyQt5.QtCore import (
    QEventLoop, QTimer, pyqtSlot, QObject, pyqtSlot,
    QMetaObject, Q_ARG, Qt, QThread, Q_RETURN_ARG
    )

from PyQt5.QtGui import QPixmap
from typing import Optional, List
import sys

def QSleep(sec:float):
    """
    This function will sleep the thread for the specified time.

    :param sec: The time in seconds to sleep the thread.
    """
    loop = QEventLoop()
    QTimer.singleShot(int(sec * 1000), loop.quit)
    loop.exec_()

def get_active_window():
    """
    Get the active window in the application.
    """
    return QApplication.activeWindow()


class MessageBoxHandler(QObject):
    """
    Thread-safe message box handler
    """
    def __init__(self,
                 style: Optional[str] = "Fusion", 
                 bg_color: Optional[str] = "White",
                 parent: Optional[QWidget] = None) -> None:
        """
        :param style: The style to use for the message boxes. Default is "Fusion".
                      Based on the available styles in QStyleFactory.
        :param bg_color: The background color of the message boxes. Default is "White".
        :param parent: The parent widget for the message boxes <Optional>.
        """
        
        # If no QApplication exists, create one.
        if QApplication.instance() is None:
            # If no QApplication exists, create one.
            self._app = QApplication(sys.argv)
        else:
            self._app = None

        # If a parent was provided, pass it along; otherwise, use None.
        super().__init__(parent)
        self.style = QStyleFactory.create(style)
        self.bg_color = bg_color

    def yes_no_message(self, 
                       title="Title", 
                       content="Content",
                       button_yes="Yes", 
                       button_no="No",
                       block:bool = True) -> bool:
        """
        Show a message box with Yes and No buttons (Specified by the user).
        Returns True if the user clicks Yes, False if the user clicks No.

        :param title: The title of the message box.
        :param content: The content of the message box.
        :param button_yes: The text to display on the Yes button.
        :param button_no: The text to display on the No button.
        :param block: Whether to block the current thread until the message box is closed default is True.

        :return: True if the user clicks Yes, False if the user clicks No.
        """
        # Are we in the main thread already?
        instance = QApplication.instance()

        if instance and QThread.currentThread() == instance.thread():
            # We can call the slot directly
            return self._yes_no_message(title, content, button_yes, button_no)

        # We must invoke the slot in the main thread, blocking this thread
        res = QMetaObject.invokeMethod(
            self,
            self._yes_no_message.__name__,
            self._get_connection_type(block),
            Q_RETURN_ARG(bool),
            Q_ARG(str, title),
            Q_ARG(str, content),
            Q_ARG(str, button_yes),
            Q_ARG(str, button_no)
        )
        return res

    def yes_no_continue_message(self, 
                                title="Title", 
                                content="Content", 
                                button_yes="Yes", 
                                button_no="No", 
                                button_continue="Continue",
                                block:bool = True) -> str:
            """
            Show a message box with 3 buttons: Yes, No, and Continue (Specified by the user).

            :param title: The title of the message box.
            :param content: The content of the message box.
            :param button_yes: The text to display on the Yes button.
            :param button_no: The text to display on the No button.
            :param button_continue: The text to display on the Continue button.
            :param block: Whether to block the current thread until the message box is closed default is True.

            :return: The text of the button that was clicked.
            """
            # Are we in the main thread already?
            instance = QApplication.instance()

            if instance and QThread.currentThread() == instance.thread():
                # We can call the slot directly
                res = self._yes_no_continue_message(title, content, button_yes, button_no, button_continue) 
            else: 
                # We m`ust invoke the slot in the main thread, blocking this thread
                res = QMetaObject.invokeMethod(
                    self,
                    self._yes_no_continue_message.__name__,
                    self._get_connection_type(block),
                    Q_RETURN_ARG(int),
                    Q_ARG(str, title),
                    Q_ARG(str, content),
                    Q_ARG(str, button_yes),
                    Q_ARG(str, button_no),
                    Q_ARG(str, button_continue)
                )
            
            if res == 0: return button_yes
            elif res == 1: return button_no
            return button_continue

    def info_message(self, 
                     title="Information", 
                     content="Here is some information.", 
                     button_ok="OK",
                     block:bool = True) -> None:
        """
        Show `Information` message box with an OK button.

        :param title: The title of the message box.
        :param content: The content of the message box.
        :param button_ok: The text to display on the OK button.
        :param block: Whether to block the current thread until the message box is closed default is True.
        """
        instance = QApplication.instance()
        if instance and QThread.currentThread() == instance.thread():
            return self._info_message(title, content, button_ok)
        
        QMetaObject.invokeMethod(
            self,
            self._info_message.__name__,
            self._get_connection_type(block),
            Q_ARG(str, title),
            Q_ARG(str, content),
            Q_ARG(str, button_ok)
        )

    def warning_message(self,
                        title="Warning",
                        content="This is a warning.",
                        button_ok="OK",
                        block:bool = True) -> None:
        """
        Show a `Warning` message box with an OK button.

        :param title: The title of the message box.
        :param content: The content of the message box.
        :param button_ok: The text to display on the OK button.
        :param block: Whether to block the current thread until the message box is closed default is True.
        """
        instance = QApplication.instance()
        if instance and QThread.currentThread() == instance.thread():
            return self._warning_message(title, content, button_ok)
        
        QMetaObject.invokeMethod(
            self,
            self._warning_message.__name__,
            self._get_connection_type(block),
            Q_ARG(str, title),
            Q_ARG(str, content),
            Q_ARG(str, button_ok)
        )

    def error_message(self,
                      title="Error",
                      content="An error occurred.",
                      button_ok="OK",
                      block:bool = True) -> None:
        """
        Show an `Error` message box with an OK button.

        :param title: The title of the message box.
        :param content: The content of the message box.
        :param button_ok: The text to display on the OK button.
        :param block: Whether to block the current thread until the message box is closed default is True.
        """
        instance = QApplication.instance()
        if instance and QThread.currentThread() == instance.thread():
            return self._error_message(title, content, button_ok)
        
        QMetaObject.invokeMethod(
            self,
            self._error_message.__name__,
            self._get_connection_type(block),
            Q_ARG(str, title),
            Q_ARG(str, content),
            Q_ARG(str, button_ok)
        )

    def combo_box_message(self, 
                          title="Title", 
                          content="Content", 
                          button_ok="OK", 
                          options:Optional[List[str]] = None,
                          block:bool = True) -> str:
        """
        Show a message box with a combo box containing the specified options.
        Returns the selected option.

        :param title: The title of the message box.
        :param content: The content of the message box.
        :param button_ok: The text to display on the OK button.
        :param options: A list of options to display in the combo box.
        :param block: Whether to block the current thread until the message box is closed default is True.

        :return: The selected option.
        """
        if options is None: options = [""]

        # Are we in the main thread already?
        instance = QApplication.instance()

        if instance and QThread.currentThread() == instance.thread():
            # We can call the slot directly
            res =  self._combo_box_message(title, content, button_ok, options)
        else:
            # We must invoke the slot in the main thread, blocking this thread
            res = QMetaObject.invokeMethod(
                self,
                self._combo_box_message.__name__,
                self._get_connection_type(block),
                Q_RETURN_ARG(int),
                Q_ARG(str, title),
                Q_ARG(str, content),
                Q_ARG(str, button_ok),
                Q_ARG(list, options)
            )
        
        return options[res]

    def instruction_message_with_image(self, 
                                       title="Instructions", 
                                       content="Please follow these instructions:",
                                       button_ok="Close",
                                       image_path:Optional[str]=None,
                                       block:bool = True) -> None:
        """
        Show a message box with instructions and an image.

        :param title: The title of the message box.
        :param content: The instructions to display.
        :param button_ok: The text to display on the OK button.
        :param image_path: The path to the image file to display.
        :param block: Whether to block the current thread until the message box is closed default is True.

        :return: None
        """
        # Are we in the main thread already?
        instance = QApplication.instance()
        if instance and QThread.currentThread() == instance.thread():
            return self._instruction_message_with_image(title, content, button_ok, image_path)
        
        QMetaObject.invokeMethod(
            self,
            self._instruction_message_with_image.__name__,
            self._get_connection_type(block),
            Q_ARG(str, title),
            Q_ARG(str, content),
            Q_ARG(str, button_ok),
            Q_ARG(str, image_path)
        )

    @pyqtSlot(str, str, str, str)
    def _instruction_message_with_image(self, title, content, button_ok, image_path) -> None:
        """
        Internal slot that actually shows the QMessageBox in the main thread.
        """
        # Create a custom dialog
        dialog = QDialog(get_active_window(), Qt.WindowType.WindowStaysOnTopHint)
        dialog.setWindowTitle(title)

        # Set up layout
        layout = QVBoxLayout(dialog)

        # Add content label
        label = QLabel(content)
        layout.addWidget(label)

        # Add image if provided
        if image_path:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                image_label = QLabel()
                image_label.setPixmap(pixmap)
                layout.addWidget(image_label)
            else:
                error_label = QLabel("Failed to load image.")
                layout.addWidget(error_label)

        # Add Close button
        close_button = QPushButton(button_ok)
        layout.addWidget(close_button)

        self._set_style(dialog)

        # Create an event loop
        loop = QEventLoop()

        # Slot to handle button click
        def on_close_clicked():
            loop.quit()

        # Connect the signal
        close_button.clicked.connect(on_close_clicked)

        # Show the dialog
        dialog.show()

        # Execute the event loop
        loop.exec_()

        dialog.close()

    @pyqtSlot(str, str, str, list, result=int.__name__)
    def _combo_box_message(self, title, content, button_ok, options) -> int:
        """
        Internal slot that actually shows the QMessageBox in the main thread.
        Returns the selected option.
        """
        if options is None:
            options = []

        # Create a custom dialog
        dialog = QDialog(get_active_window(), Qt.WindowType.WindowStaysOnTopHint)
        dialog.setWindowTitle(title)

        # Set up layout
        layout = QVBoxLayout(dialog)

        # Add content label
        label = QLabel(content)
        layout.addWidget(label)

        # Add combo box
        combo_box = QComboBox()
        combo_box.addItems(options)
        layout.addWidget(combo_box)

        # Add OK button
        ok_button = QPushButton(button_ok)
        layout.addWidget(ok_button)

        self._set_style(dialog)
        
        # Create an event loop
        loop = QEventLoop()

        # Slot to handle button click
        def on_ok_clicked():
            loop.quit()

        # Connect the signal
        ok_button.clicked.connect(on_ok_clicked)

        # Show the dialog
        dialog.show()

        # Execute the event loop
        loop.exec_()

        # After the loop exits, get the selected item
        selected_item = combo_box.currentIndex()
        dialog.close()
        return selected_item

    @pyqtSlot(str, str, str, str, result=bool.__name__)
    def _yes_no_message(self, title, content, yes_text, no_text) -> bool:
        """
        Internal slot that actually shows the QMessageBox in the main thread.
        Returns True if user clicked Yes, else False.
        """
        msg_box = QMessageBox(get_active_window())
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self._set_style(msg_box)
        msg_box.setWindowTitle(title)
        msg_box.setText(content)
        msg_box.setIcon(QMessageBox.Icon.Question)

        yes_btn = msg_box.addButton(yes_text, QMessageBox.ButtonRole.YesRole)
        no_btn = msg_box.addButton(no_text, QMessageBox.ButtonRole.NoRole)

        msg_box.exec_()

        clicked = msg_box.clickedButton()

        return clicked == yes_btn
    
    @pyqtSlot(str, str, str)
    def _info_message(self, title, content, ok_text) -> None:
        """
        Internal slot that actually shows the QMessageBox in the main thread.
        Returns None after closure or Ok button clicked.
        """
        msg_box = QMessageBox(get_active_window())
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        msg_box.setWindowTitle(title)
        msg_box.setText(content)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.addButton(ok_text, QMessageBox.ButtonRole.AcceptRole)
        self._set_style(msg_box)
        msg_box.exec_()

    @pyqtSlot(str, str, str)
    def _warning_message(self, title, content, ok_text) -> None:
        """
        Internal slot that actually shows the QMessageBox in the main thread.
        Returns None after closure or Ok button clicked.
        """
        msg_box = QMessageBox(get_active_window())
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        msg_box.setWindowTitle(title)
        msg_box.setText(content)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.addButton(ok_text, QMessageBox.ButtonRole.AcceptRole)
        self._set_style(msg_box)
        msg_box.exec_()

    @pyqtSlot(str, str, str)
    def _error_message(self, title, content, ok_text) -> None:
        """
        Internal slot that actually shows the QMessageBox in the main thread.
        Returns None after closure or Ok button clicked.
        """
        msg_box = QMessageBox(get_active_window())
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        msg_box.setWindowTitle(title)
        msg_box.setText(content)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.addButton(ok_text, QMessageBox.ButtonRole.AcceptRole)
        self._set_style(msg_box)
        msg_box.exec_()

    @pyqtSlot(str, str, str, str, str, result=int.__name__)
    def _yes_no_continue_message(self, title, content, button_yes, button_no, button_continue) -> int:
        """
        Internal slot that actually shows the QMessageBox in the main thread.
        Returns 0 if user clicked Yes, 1 if user clicked No, 2 if user clicked Continue.
        """
        msg_box = QMessageBox(get_active_window())
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        msg_box.setWindowTitle(title)
        msg_box.setText(content)
        msg_box.setIcon(QMessageBox.Icon.Question)

        # Add custom buttons
        yes_button = msg_box.addButton(button_yes, QMessageBox.ButtonRole.YesRole)
        no_button = msg_box.addButton(button_no, QMessageBox.ButtonRole.NoRole)
        continue_button = msg_box.addButton(button_continue, QMessageBox.ButtonRole.AcceptRole)
        
        self._set_style(msg_box)

        # Create an event loop
        loop = QEventLoop()

        # Slot to handle button clicks
        def on_button_clicked():
            loop.quit()

        # Connect the signal
        msg_box.buttonClicked.connect(on_button_clicked)

        # Show the message box
        msg_box.show()

        # Execute the event loop
        loop.exec_()

        # Determine which button was clicked
        clicked_button = msg_box.clickedButton()

        if clicked_button == yes_button: return 0
        
        elif clicked_button == no_button: return 1

        return 2
    
    def _get_connection_type(self, block:bool) -> Qt.ConnectionType:
        """
        Get the connection type based on the block value.
        """
        return Qt.ConnectionType.BlockingQueuedConnection if block else Qt.ConnectionType.QueuedConnection

    def _set_style(self, widget:QWidget) -> None:
        """
        Set the style of the widget to the specified style.
        """
        if self.style is None: return

        widget.setStyle(self.style)

        if self.bg_color: widget.setStyleSheet(f"background-color: {self.bg_color};")

        widget.ensurePolished()


# Example usage
if __name__ == "__main__":
    handler = MessageBoxHandler()
    
    # Yes/No message
    res = handler.yes_no_message(
                                title="Confirmation",
                                content="Do you want to proceed?",
                                button_yes="Proceed",
                                button_no="Cancel")
    
    print("User selected:", "Yes" if res else "No")
    
    # Information message
    handler.info_message(
        title="Update",
        content="The operation completed successfully.",
        button_ok="Got it"
    )
    
    # Warning message
    handler.warning_message(
        title="Low Disk Space",
        content="You are running low on disk space.",
        button_ok="Understood"
    )
    
    # Error message
    handler.error_message(
        title="Connection Error",
        content="Failed to connect to the server.",
        button_ok="Retry"
    )

        # Yes/No/Continue message
    
    # Yes/No/Continue message
    response = handler.yes_no_continue_message(
        title="Decision",
        content="Please choose an option:",
        button_yes="Yes",
        button_no="No",
        button_continue="Continue"
    )
    print("User selected:", response)

    # Combo box message
    selected_option = handler.combo_box_message(
        title="Select Fruit",
        content="Choose your favorite fruit:",
        options=["Apple", "Banana", "Cherry", "Date"]
    )
    print("User selected:", selected_option)

    # Instruction message with image
    handler.instruction_message_with_image(
        title="Welcome",
        content="Please refer to the image below:",
        image_path=""  # Replace with an actual image path
    )
