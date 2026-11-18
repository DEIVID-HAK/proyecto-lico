import sys
from PySide6.QtWidgets import QApplication
from sqlalchemy.orm import sessionmaker

from liquor_pos.infrastructure.persistence.database import get_engine
from liquor_pos.infrastructure.persistence.repositories import SQLAlchemyUserRepository
from liquor_pos.infrastructure.security.password_hasher import BcryptPasswordHasher
from liquor_pos.application.use_cases.auth_service import AuthenticationService

from liquor_pos.presentation.views.main_window import MainWindow
from liquor_pos.presentation.views.pos_view import POSView
from liquor_pos.presentation.viewmodels.pos_viewmodel import POSViewModel
from liquor_pos.presentation.views.login_view import LoginWindow

def main():
    app = QApplication(sys.argv)
    
    # Cargar y aplicar tema global (QSS) para la ventana principal
    try:
        with open("liquor_pos/presentation/assets/style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Warning: style.qss not found. Using default style.")

    # 1. Configurar Base de Datos Real (SQLite local)
    engine = get_engine("sqlite:///liquor_pos.db")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    # 2. Inyección de Dependencias Reales
    user_repo = SQLAlchemyUserRepository(session)
    password_hasher = BcryptPasswordHasher()
    
    # Nuestro Servicio de Autenticación ahora valida contra SQLite usando bcrypt
    auth_service = AuthenticationService(user_repo, password_hasher)
    
    pos_viewmodel = POSViewModel(sale_use_case=None) # type: ignore
    
    # 3. Instanciar Vistas
    pos_view = POSView(viewmodel=pos_viewmodel)
    main_window = MainWindow(pos_view)
    
    login_window = LoginWindow(auth_service)
    
    # Logica de transición de Login a Main
    def on_login_success(user):
        print(f"Login exitoso. Bienvenido {user.username} ({user.role.value})")
        login_window.close()
        # En sistemas POS, la ventana principal suele abrirse maximizada
        main_window.showMaximized() 

    login_window.backend.login_successful.connect(on_login_success)
    
    # Iniciar aplicación mostrando el Login interactivo Web
    login_window.show()
    
    # Limpiar recursos de BD al cerrar
    exit_code = app.exec()
    session.close()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
