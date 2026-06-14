from PySide6.QtCore import QObject, Signal

class CommConnector(QObject):
    phone_data_ready = Signal(dict, str)
binder = CommConnector()
        