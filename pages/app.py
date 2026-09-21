from PySide6.QtWidgets import QMainWindow, QStackedWidget

from pages.account_p import AccountPage
from pages.settings_p import SettingsPage
from pages.utils.errors import UserNotFoundError, ValidationError, DataStorageError
from pages.utils.helpers import strip_whitespaces

from .constants import BG

from .welcome_p import WelcomePage
from .signup_p import SignUpPage
from .login_p import LoginPage
from .done_p import DonePage
from .home_p import HomePage
from .habits_p import HabitsPage
from .goals_p import GoalsPageHome
from .progress_p import ProgressPage
from .progress_goal_p import GoalsPage

import models.user_session

# Page indices
IDX_WELCOME = 0
IDX_SIGNUP = 1
IDX_LOGIN = 2
IDX_DONE = 3
IDX_HOME = 4
IDX_HABITS = 5
IDX_GOALS = 6
IDX_PROGRESS = 7
IDX_PROGRESS_GOALS = 8
IDX_SETTINGS = 9
IDX_ACCOUNT = 10


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HabitTracker")
        self.setMinimumSize(390, 780)
        self.setMaximumSize(390, 780)
        self.setStyleSheet(f"QMainWindow {{ background: {BG}; }}")

        # Stack
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Instantiate pages
        self.welcome_page = WelcomePage()
        self.signup_page = SignUpPage()
        self.login_page = LoginPage()
        self.done_page = DonePage()
        self.home_page = HomePage()
        self.habits_page = HabitsPage()
        self.goals_page = GoalsPageHome()
        self.progress_page = ProgressPage()
        self.progress_goals_page = GoalsPage()
        self.settings_page = SettingsPage()
        self.account_page = AccountPage()

        self.stack.addWidget(self.welcome_page)
        self.stack.addWidget(self.signup_page)
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.done_page)
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.habits_page)
        self.stack.addWidget(self.goals_page)
        self.stack.addWidget(self.progress_page)
        self.stack.addWidget(self.progress_goals_page)
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.account_page)

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
        self.home_page.create_habit_requested.connect(self._handle_create_habit)
        self.home_page.see_all_habits.connect(self._see_all_habits)
        self.home_page.see_all_goals.connect(self._see_goals_page)
        self.home_page.update_habit_requested.connect(self._handle_update_habit)
        self.home_page.delete_habit_requested.connect(self._handle_delete_habit)
        self.home_page.refresh_requested.connect(self._open_home)

        # ProgressPage
        self.progress_page.see_all_goals.connect(self._open_progress_goals)

        # ProgressGoalPage
        self.progress_goals_page.go_progress.connect(lambda: self._go(IDX_PROGRESS))
        self.progress_goals_page.go_home.connect(self._open_progress)

        # GoalsPage
        self.goals_page.go_home.connect(self._open_home)
        self.goals_page.update_habit_requested.connect(self._handle_update_habit)
        self.goals_page.delete_habit_requested.connect(self._handle_delete_habit)

        # HabitsPage
        self.habits_page.go_home.connect(self._open_home)
        self.habits_page.update_habit_requested.connect(self._handle_update_habit)
        self.habits_page.delete_habit_requested.connect(self._handle_delete_habit)

        # SettingsPage
        self.settings_page.go_account.connect(self._open_account)
        self.settings_page.go_welcome.connect(self._handle_logout)
        self.settings_page.delete_account_requested.connect(self._handle_delete_account)

        # AccountPage
        self.account_page.go_settings.connect(lambda: self._go(IDX_SETTINGS))
        self.account_page.update_account_requested.connect(self._handle_update_account)

        self.home_page.nav_requested.connect(self._handle_nav)
        self.progress_page.nav_requested.connect(self._handle_nav)
        self.settings_page.nav_requested.connect(self._handle_nav)

        # Startup logic
        self._startup()

    # Navigation helpers
    def _refresh_current_data(self):
        session = self._load_session_safe()
        if session:
            self.home_page.set_user(session)
            self.habits_page.set_user(session)
            self.goals_page.set_user(session)
            self.progress_page.set_user(session)

    def _load_session_safe(self):
        try:
            return models.user_session.load_session()
        except DataStorageError as e:
            print(f"[DATA STORAGE ERROR] {e}")
            models.user_session.clear_session()
            return None

    def _go(self, index):
        if index == IDX_SIGNUP:
            if hasattr(self.signup_page, "clear_fields"):
                self.signup_page.clear_fields()
        elif index == IDX_LOGIN:
            if hasattr(self.login_page, "clear_fields"):
                self.login_page.clear_fields()

        self.stack.setCurrentIndex(index)

    def _startup(self):
        session = models.user_session.load_session()
        if session:
            self.home_page.set_user(session)
            self._go(IDX_HOME)
        else:
            self._go(IDX_WELCOME)

    def _after_register(self, name):
        self.done_page.set_name(name)
        self._go(IDX_DONE)

    def _after_login(self):
        self._open_home()

    def _open_home(self):
        session = models.user_session.load_session()
        if session:
            self.home_page.set_user(session)
        self._go(IDX_HOME)

    def _open_progress(self):
        session = models.user_session.load_session()
        if session:
            self.progress_page.set_user(session)
        self._go(IDX_PROGRESS)

    def _open_progress_goals(self, goals_to_show):
        self.progress_goals_page.set_specific_goals(goals_to_show)
        self._go(IDX_PROGRESS_GOALS)

    def _open_account(self):
        session = models.user_session.load_session()
        if session:
            self.account_page.set_user(session)
        self._go(IDX_ACCOUNT)

    def _see_all_habits(self):
        session = models.user_session.load_session()
        self.habits_page.set_user(session)
        self._go(IDX_HABITS)

    def _see_all_goals(self, goals_to_show):
        self.progress_goals_page.set_specific_goals(goals_to_show)
        self._go(IDX_PROGRESS_GOALS)

    def _see_goals_page(self):
        session = models.user_session.load_session()
        if session:
            all_goals = session.get("goals", [])
            self.goals_page.set_specific_goals(all_goals)
        self._go(IDX_GOALS)

    @strip_whitespaces
    def _handle_create_habit(self, goal, name, period, habit_type):
        session = models.user_session.load_session()
        email = session.get("email") if session else None

        if email:
            try:
                models.user_session.create_goal_habit(
                    email=email,
                    goal=goal,
                    habit_name=name,
                    period=period,
                    habit_type=habit_type,
                )

                fresh_session = models.user_session.load_session()

                if fresh_session:
                    self.home_page.set_user(fresh_session)

            except UserNotFoundError as e:
                print(f"Error creating habit: {e}")
                self._handle_logout()

    @strip_whitespaces
    def _handle_update_habit(self, habit_id, goal, name, period, habit_type):
        session = models.user_session.load_session()
        email = session.get("email") if session else None
        if email:
            try:
                models.user_session.update_habit(
                    email, habit_id, name, goal, period, habit_type
                )
                self._refresh_current_data()

            except UserNotFoundError as e:
                print(f"Error updating habit: {e}")
                self._handle_logout()

    @strip_whitespaces
    def _handle_delete_habit(self, habit_id):
        session = models.user_session.load_session()
        email = session.get("email") if session else None
        if email:
            try:
                models.user_session.delete_habit(email, habit_id)
                self._refresh_current_data()

            except UserNotFoundError as e:
                print(f"Error deleting habit: {e}")
                self._handle_logout()

    def _handle_nav(self, tab_name):
        nav_map = {
            "Home": self._open_home,
            "Activity": self._open_progress,
            "Settings": lambda: self._go(IDX_SETTINGS),
        }

        action = nav_map.get(tab_name)
        if action:
            action()

        self._update_nav(tab_name)

    def _update_nav(self, active_tab):
        current_page = self.stack.currentWidget()
        if hasattr(current_page, "nav"):
            current_page.nav.set_active_tab(active_tab)

    @strip_whitespaces
    def _handle_update_account(self, name, email, password):
        session = models.user_session.load_session()
        if not session:
            return

        old_email = session.get("email")

        if old_email:
            try:
                models.user_session.update_user(old_email, name, email, password)
                self._refresh_current_data()

                self._go(IDX_SETTINGS)

            except UserNotFoundError as e:
                print(f"Error updating account: {e}")
                self._handle_logout()

            except ValidationError as e:
                self.account_page.error_lbl.setText(str(e))

    def _handle_logout(self):
        models.user_session.clear_session()

        self.home_page.user = None
        self.habits_page.user = None
        self.goals_page.user = None
        self.progress_page.user = None

        self._go(IDX_WELCOME)

    def _handle_delete_account(self):
        session = models.user_session.load_session()
        email = session.get("email") if session else None

        if email:
            try:
                if hasattr(models.user_session, "delete_user"):
                    models.user_session.delete_user(email)
            except UserNotFoundError as e:
                print(f"Error deleting account backend data: {e}")

        models.user_session.clear_session()

        self.home_page.user = None
        self.habits_page.user = None
        self.goals_page.user = None
        self.progress_page.user = None
