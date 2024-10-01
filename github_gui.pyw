import traceback
from github_repositories_model import GithubRepo, GithubRepositoriesModel
import os
import pathlib
import pprint
import sys
import webbrowser
from datetime import datetime
from pprint import pprint
import PySide6.QtCore as core
import PySide6.QtGui as gui
import PySide6.QtWidgets as widgets

import github
import totp

GITHUB_TOKEN = 'GITHUB_TOKEN'
GITHUB_OWNER = 'GITHUB_OWNER'
GITHUB_TOTP = 'GITHUB_TOTP'


def get_github_totp_token():
    return os.environ.get(GITHUB_TOTP, None)


def get_github_token():
    if GITHUB_TOKEN in os.environ:
        return os.environ[GITHUB_TOKEN]
    else:
        raise Exception(f"Environment variable '{GITHUB_TOKEN}' not found.")


def get_github_owner():
    if GITHUB_OWNER in os.environ:    
        return os.environ[GITHUB_OWNER]
    else:
        raise Exception(f"Environment variable '{GITHUB_OWNER}' not found.")


class RepoLoaderThread(core.QThread):
    result = core.Signal(object)
    error = core.Signal(Exception)

    def __init__(self, token: str):
        super().__init__()
        self._token = token

    @core.Slot()
    def run(self):
        try:
            repos = list(github.list_repositories(self._token))
            pprint(repos[0])
            self.result.emit(GithubRepositoriesModel(repos))
        except Exception as e:
            self.error.emit(e)


class MessageDialog(widgets.QDialog):
    def __init__(self, title: str, message: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        buttons = widgets.QDialogButtonBox.StandardButton.Ok
        buttonBox = widgets.QDialogButtonBox(buttons)
        buttonBox.accepted.connect(self.accept)
        self.layout = widgets.QVBoxLayout()
        txt_message = widgets.QTextEdit()
        txt_message.insertPlainText(message)
        txt_message.setReadOnly(True)
        p = txt_message.palette()
        p.setColor(gui.QPalette.ColorRole.Base,
                   gui.QColor.fromRgb(240, 240, 240))
        txt_message.setPalette(p)
        self.layout.addWidget(txt_message)
        self.layout.addWidget(buttonBox)
        self.setLayout(self.layout)
        self.resize(700, 400)


class TableModel(core.QAbstractTableModel):

    def __init__(self, model: GithubRepositoriesModel):
        super().__init__()
        self._model = model

    def headerData(self, section, orientation, role=core.Qt.DisplayRole):
        if orientation == core.Qt.Horizontal and role == core.Qt.DisplayRole:
            return self._model.column_label(section)
        return super().headerData(section, orientation, role)

    def sort(self, column_index: int, sort_order: gui.Qt.SortOrder):
        self._model.sort(column_index, descending=True if sort_order ==
                         gui.Qt.SortOrder.DescendingOrder else False)
        self.layoutChanged.emit()

    def rowCount(self, index):
        # The length of the outer list.
        return self._model.row_count()

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self._model.column_count()

    def data(self, index, role):
        value = self._model.get_data(index.row(), index.column())

        if role == core.Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            # Perform per-type checks and render accordingly.
            if isinstance(value, datetime):
                # Render time to YYY-MM-DD.
                return value.strftime("%d.%m.%Y")
            # if isinstance(value, float):
            #     # Render float to 2 dp
            #     return "%.2f" % value
            # Default (anything not captured above: e.g. int)
            return value

        # elif role == core.Qt.ItemDataRole.BackgroundRole and index.column() == 2:
        #     return gui.QColor(core.Qt.GlobalColor.yellow)

        if role == core.Qt.ItemDataRole.TextAlignmentRole:
            if isinstance(value, int) or isinstance(value, float):
                return core.Qt.AlignmentFlag.AlignVCenter | core.Qt.AlignmentFlag.AlignRight

        # if role == core.Qt.ItemDataRole.FontRole:
        #     ...

        # if role == core.Qt.ItemDataRole.ForegroundRole:
        #     if (isinstance(value, int) or isinstance(value, float)) and value < 0:
        #         return gui.QColor(core.Qt.GlobalColor.red)

        # if role == core.Qt.ItemDataRole.DecorationRole:
        #     if isinstance(value, datetime):
        #         return gui.QIcon(str(curdir / "res" / "calendar-month.png"))
        #     elif isinstance(value, bool):
        #         if value:
        #             return gui.QIcon(str(curdir / "res" / "tick.png"))
        #         else:
        #             return gui.QIcon(str(curdir / "res" / "cross.png"))
        #     elif isinstance(value, int) or isinstance(value, float):
        #         value = int(value)

        #         value = max(-5, value)
        #         value = min(5, value)
        #         value = value+5

        #         return gui.QColor(COLORS[value])


class RepositoryFormWidget(widgets.QWidget):

    def __init__(self):
        super().__init__()

        layout = widgets.QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        row = 0
        layout.addWidget(widgets.QLabel("Repository name: "),
                         row, 0, core.Qt.AlignmentFlag.AlignRight)
        self.txt_repository_name = widgets.QLineEdit()
        # self.txt_repository_name.setFocusPolicy(
        #     core.Qt.FocusPolicy.StrongFocus)
        layout.addWidget(self.txt_repository_name, row, 1)

        row += 1

        layout.addWidget(widgets.QLabel("Repository description:"),
                         row, 0, core.Qt.AlignmentFlag.AlignRight)
        self.txt_repository_description = widgets.QLineEdit(self)
        layout.addWidget(self.txt_repository_description, row, 1)

        row += 1

        layout.addWidget(widgets.QLabel("Private?:"),
                         row, 0, core.Qt.AlignmentFlag.AlignRight)
        self.checkbox_private = widgets.QCheckBox(self)
        self.checkbox_private.setChecked(True)
        layout.addWidget(self.checkbox_private, row, 1)


class RepositoryFormDialog(widgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(500)
        self.setWindowTitle("Edit repository")
        buttons = widgets.QDialogButtonBox.Ok | widgets.QDialogButtonBox.Cancel
        self.buttonBox = widgets.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout = widgets.QVBoxLayout()
        self.repo_form = RepositoryFormWidget()
        self.layout.addWidget(self.repo_form)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class TabRepositoriesTable(widgets.QWidget):

    TITLE = "All Github repositories"

    def __init__(self, window: widgets.QMainWindow):
        super().__init__()

        self._window = window
        self._thread: RepoLoaderThread = None

        layout = widgets.QVBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(20)

        self.btn_load = widgets.QPushButton("Load")
        self.btn_load.clicked.connect(self.handler_btn_load_clicked)
        layout.addWidget(self.btn_load)

        self.table = widgets.QTableView()
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionMode(
            widgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(
            widgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setContextMenuPolicy(
            core.Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(
            self.handler_table_context_menu_requested)
        layout.addWidget(self.table)

    def handler_btn_load_clicked(self):
        self.start_load_repositories()

    def handler_table_context_menu_requested(self, pos: core.QPoint):

        # https://doc.qt.io/qtforpython-6/PySide6/QtCore/QItemSelectionModel.html
        # https://doc.qt.io/qt-6/qitemselectionmodel.html
        sel_model: core.QItemSelectionModel = self.table.selectionModel()
        model_index: core.QModelIndex = sel_model.selectedRows()[0]
        row: int = model_index.row()
        table_model: TableModel = sel_model.model()
        repo = table_model._model.get_repo(row)

        menu = widgets.QMenu(self)

        action = gui.QAction("Copy URL to clipboard", self)
        action.triggered.connect(lambda: gui.QClipboard().setText(repo.url))
        menu.addAction(action)

        action = gui.QAction("Open in web browser", self)
        action.triggered.connect(lambda: webbrowser.open(repo.url))
        menu.addAction(action)

        action = gui.QAction("Edit", self)
        action.triggered.connect(lambda: self.handler_edit_repository(repo))
        menu.addAction(action)

        menu.exec(self.table.mapToGlobal(pos))

    def handler_edit_repository(self, repo: GithubRepo):
        try:
            d = RepositoryFormDialog(self._window)
            d.repo_form.txt_repository_name.setText(repo.name)
            d.repo_form.txt_repository_description.setText(
                repo.description)
            d.repo_form.checkbox_private.setChecked(repo.private)
            if d.exec() == widgets.QDialog.DialogCode.Accepted:
                print("GITHUB EDIT REPO")
                result = github.update_repository(token=get_github_token(),
                                                owner=get_github_owner(),
                                                repo=repo.name,
                                                clone_url=repo.clone_url,
                                                new_name=d.repo_form.txt_repository_name.text(),
                                                new_description=d.repo_form.txt_repository_description.text(),
                                                new_private=d.repo_form.checkbox_private.isChecked())
                MessageDialog("Github repository updated",
                            result, self._window).exec()
        except Exception as e:
            MessageDialog("Error editing repository", "".join(traceback.format_exception(e)), self).exec()


    # override
    def showEvent(self, event: gui.QShowEvent):
        if not self.table.model():
            self.start_load_repositories()

    def start_load_repositories(self):
        token = get_github_token()
        if token is None:
            self._window.statusBar().showMessage(
                f"Environment variable '{GITHUB_TOKEN}' not found. Repositories cannot be generated.")
        self.btn_load.setDisabled(True)
        self._window.statusBar().showMessage("")
        if self.table.model():
            self.table.model().deleteLater()
        self._thread = RepoLoaderThread(token)
        self._thread.result.connect(self.loading_repositories_finished)
        self._thread.error.connect(self.show_loading_error)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

    def show_loading_error(self, e: Exception):
        self.btn_load.setEnabled(True)
        MessageDialog("Error loading repository",
                      "".join(traceback.format_exception(e)),
                      self).exec()

    def loading_repositories_finished(self, model: GithubRepositoriesModel):
        try:
            self.btn_load.setEnabled(True)
            self._window.statusBar().showMessage(
                f"{model.row_count()} repositories found on Github")
            # Last pushed repos should be displayed first
            model.sort_by(lambda r: r.date_pushed)
            self.table.setModel(TableModel(model))
            self.table.resizeColumnsToContents()
        except Exception as e:
            MessageDialog(
                "Error after successfull repositiries loading",
                "".join(traceback.format_exception(e)),
                self).exec()


class TabTOTP(widgets.QWidget):
    TITLE = "TOTP"

    def __init__(self, window: widgets.QMainWindow):
        super().__init__()
        self._window = window
        self.setAutoFillBackground(True)

        self._progress_last = None
        self._totp_value = None

        layout = widgets.QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        lbl = widgets.QLabel("TOTP - Time based one time password")
        lbl.setAlignment(core.Qt.AlignmentFlag.AlignHCenter)
        font = lbl.font()
        font.setPointSize(16)
        lbl.setFont(font)
        layout.addWidget(lbl)

        lbl = widgets.QLabel(
            """
            Click on the button below to copy the TOTP to the clipboard.
            You will need it, for example, to confirm deleting a repository on the Github website.
            """)
        lbl.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)

        btn = widgets.QPushButton("Copy")
        btn.clicked.connect(self.handler_copy_button_clicked)
        layout.addWidget(btn)

        self.lbl_totp = widgets.QLabel("---")
        font = self.lbl_totp.font()
        font.setPixelSize(40)
        self.lbl_totp.setFont(font)
        layout.addWidget(self.lbl_totp, 1, core.Qt.AlignmentFlag.AlignHCenter)

        self.progressbar = widgets.QProgressBar()
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(29)
        layout.addWidget(self.progressbar)

        self.timer = core.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.handler_timeout)
        self._count = 0

    def handler_copy_button_clicked(self):
        clipboard = gui.QClipboard()
        clipboard.setText(self._totp_value)

    def update_widgets(self):
        if self._totp_token is None:
            return
        progress_current = totp.get_progress()
        self.progressbar.setValue(progress_current)
        if self._progress_last != progress_current:
            self._progress_last = progress_current
            self._totp_value = totp.get_totp_token(self._totp_token)
            self.lbl_totp.setText(self._totp_value)

    def handler_timeout(self):
        self._count += 1
        self.update_widgets()

    # def event(self, event: core.QEvent):
    #     print("TAB1", "event", event)

    def showEvent(self, event: gui.QShowEvent):
        print("TAB1", "showEvent", event)
        self._window.statusBar().showMessage("")
        self._totp_token = get_github_totp_token()
        if self._totp_token is None:
            self._window.statusBar().showMessage(
                f"Environment variable '{GITHUB_TOTP}' not found. TOTP cannot be generated.")
            return
        self.update_widgets()
        self.timer.start()

    def hideEvent(self, event: gui.QHideEvent):
        print("TAB1", "hideEvent", event)
        self.timer.stop()


class TabCreateRepository(widgets.QWidget):
    TITLE = "Create new repository"

    def __init__(self, window):
        super().__init__()
        self._window = window

        layout = widgets.QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # row = 0

        repo_form = RepositoryFormWidget()
        layout.addWidget(repo_form)

        btn_create_new_repository = widgets.QPushButton(
            "Create new Github repository")
        layout.addWidget(btn_create_new_repository)

        # row += 1

        txt_info = widgets.QTextEdit(
            """
            Once you've created a new repository, you will see here the GIT commands
            you can use to initialize Git version control for your project.
            These commands are executed in the directory containing your code.
            """)
        txt_info.setReadOnly(True)
        p = txt_info.palette()
        p.setColor(gui.QPalette.ColorRole.Base,
                   gui.QColor.fromRgb(240, 240, 240))
        txt_info.setPalette(p)

        # txt_info.setTextBackgroundColor(gui.QColor(core.Qt.GlobalColor.red))
        # layout.setRowStretch(row, 1)
        layout.addWidget(txt_info)

        if get_github_token() is None:
            self._window.statusBar().showMessage(
                f"Environment variable '{GITHUB_TOKEN}' found.")

        def handler_btn_clicked():
            try:
                github_token = get_github_token()

                if not github_token:
                    widgets.QMessageBox.critical(
                        self, f"{GITHUB_TOKEN} missing", f"System environment variable '{GITHUB_TOKEN}' not found on this computer!")
                    return

                repository_name = repo_form.txt_repository_name.text().strip()
                repository_description = repo_form.txt_repository_description.text().strip()
                if not repository_name:
                    widgets.QMessageBox.critical(
                        self, "Missing input", "Repository name is mandatory")
                    repo_form.txt_repository_name.setFocus()
                    return
                result = github.create_repo(token=github_token,
                                            repo=repository_name,
                                            description=repository_description,
                                            private=repo_form.checkbox_private.isChecked())
                txt_info.clear()
                txt_info.append(f"Github repository '{repository_name}' with description '{
                                repository_description}' created.\n\n")
                txt_info.append(result)
            except Exception as e:
                MessageDialog("Error creating repository", "".join(traceback.format_exception(e))).exec()

        btn_create_new_repository.clicked.connect(handler_btn_clicked)

    def showEvent(self, event: gui.QShowEvent):
        self._window.statusBar().showMessage("")


class MainWindow(widgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Github Repository Manager")

        self.setStatusBar(widgets.QStatusBar())

        self.setMinimumSize(500, 400)
        self.setContentsMargins(10, 10, 10, 10)

        tabs = widgets.QTabWidget()
        tabs.currentChanged.connect(self.handler_tab_page_changed)

        tabs.setTabPosition(widgets.QTabWidget.TabPosition.North)
        # tabs.setMovable(True)

        tab0 = TabCreateRepository(self)
        tabs.addTab(tab0, tab0.TITLE)

        tab1 = TabTOTP(self)
        tabs.addTab(tab1, tab1.TITLE)
        tabs.setTabToolTip(1, tab1.TITLE)

        tab2 = TabRepositoriesTable(self)
        tabs.addTab(tab2, tab2.TITLE)
        tabs.setTabToolTip(2, tab2.TITLE)

        # tabs.setCurrentIndex(2)

        self.setCentralWidget(tabs)

        self.resize(1000, 800)

    def handler_tab_page_changed(self, page_index):
        print("handler_tab_page_changed", "Tab page:", page_index)
        # if page_index == 0:
        #     self.txt_repository_name.setFocus()


os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=0"

app = widgets.QApplication(sys.argv)
app.setStyle("Fusion")


icon = gui.QIcon(str(pathlib.Path(__file__).parent / "github.ico"))
app.setWindowIcon(icon)

font = app.font()
font.setPointSize(12)
app.setFont(font)

window = MainWindow()
window.show()
app.exec()
