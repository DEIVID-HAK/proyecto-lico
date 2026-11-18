import os
from PySide6.QtCore import QObject, Slot, Signal, QUrl
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel

from liquor_pos.application.use_cases.auth_service import AuthenticationService

class WebBackend(QObject):
    login_successful = Signal(object) # Envía el objeto de usuario

    def __init__(self, auth_service: AuthenticationService):
        super().__init__()
        self.auth_service = auth_service

    @Slot(str, str, result=dict)
    def authenticate(self, username, password):
        try:
            if self.auth_service:
                user = self.auth_service.login(username, password)
            else:
                # Dummy login para previsualización UI
                if username == "admin" and password == "123":
                    user = {"username": "admin", "role": "ADMIN"}
                else:
                    return {"success": False, "error": "Credenciales inválidas (Prueba con admin / 123)"}
            
            self.login_successful.emit(user)
            return {"success": True, "error": ""}
        except Exception as e:
            return {"success": False, "error": str(e)}

class LoginWindow(QMainWindow):
    def __init__(self, auth_service: AuthenticationService):
        super().__init__()
        self.setWindowTitle("Login - Liquor POS")
        self.resize(1000, 700) # Tamaño razonable para ver el background
        
        # Eliminar márgenes de la ventana para que el HTML ocupe todo
        self.setContentsMargins(0, 0, 0, 0)

        # Setup WebEngineView
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # Setup WebChannel para comunicación JS <-> Python
        self.channel = QWebChannel()
        self.backend = WebBackend(auth_service)
        self.channel.registerObject("backend", self.backend)
        self.browser.page().setWebChannel(self.channel)

        # Cargar el HTML local
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'web_login', 'index.html'))
        self.browser.setUrl(QUrl.fromLocalFile(html_path))
