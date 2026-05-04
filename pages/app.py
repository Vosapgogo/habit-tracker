from PySide6.QtWidgets import QMainWindow, QStackedWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from .constants import BG
from .welcome_p import WelcomePage
from .signup_p import SignUpPage
from .login_p import LoginPage
from .done_p import DonePage
from .home_p import HomePage
import models.user_session 

# ── Page indices in QStackedWidget ───────────────────────────────────
IDX_WELCOME = 0
IDX_SIGNUP  = 1
IDX_LOGIN   = 2
IDX_DONE    = 3
IDX_HOME    = 4


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyApp")
        self.setMinimumSize(390, 780)
        self.setMaximumSize(390, 780)
        self.setStyleSheet(f"QMainWindow {{ background: {BG}; }}")

        # ── Stack ─────────────────────────────────────────────────────
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Instantiate pages
        self.welcome_page = WelcomePage()
        self.signup_page  = SignUpPage()
        self.login_page   = LoginPage()
        self.done_page    = DonePage()
        self.home_page    = HomePage()

        self.stack.addWidget(self.welcome_page)   # 0
        self.stack.addWidget(self.signup_page)    # 1
        self.stack.addWidget(self.login_page)     # 2
        self.stack.addWidget(self.done_page)      # 3
        self.stack.addWidget(self.home_page)      # 4

        # ── Connect signals ───────────────────────────────────────────
        # WelcomePage
        self.welcome_page.go_signup.connect(lambda: self._go(IDX_SIGNUP))
        self.welcome_page.go_login.connect(lambda: self._go(IDX_LOGIN))

        # SignUpPage
        self.signup_page.go_login.connect(lambda: self._go(IDX_LOGIN))
        self.signup_page.go_success.connect(self._after_register)

        # LogInPage
        self.login_page.go_signup.connect(lambda: self._go(IDX_SIGNUP))
        self.login_page.go_home.connect(self._after_login)

        # DonePage
        self.done_page.go_home.connect(self._open_home)

        # HomePage
        #self.home_page.logout.connect(lambda: self._go(IDX_WELCOME))

        # ── Startup logic ─────────────────────────────────────────────
        self._startup()

    # ── Navigation helpers ────────────────────────────────────────────

    def _go(self, index: int):
        self.stack.setCurrentIndex(index)

    def _startup(self):
        """If a saved session exists → go straight to home."""
        session = models.user_session.load_session()
        if session:
            self.home_page.set_user(session)
            self._go(IDX_HOME)
        else:
            self._go(IDX_WELCOME)

    def _after_register(self, name: str):
        """Show Done page with user's name after successful registration."""
        self.done_page.set_name(name)
        self._go(IDX_DONE)

    def _after_login(self):
        """After login → straight to home."""
        self._open_home()

    def _open_home(self):
        if models.user_session.load_session():
            self.home_page.set_user(models.user_session.load_session())
        self._go(IDX_HOME)
