from pathlib import Path
from html import escape

from PySide6.QtCore import QModelIndex, Qt, QUrl
from PySide6.QtGui import QDesktopServices, QDragEnterEvent, QDropEvent, QGuiApplication
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QLayout,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QStatusBar,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from app.constants import (
    APP_TITLE,
    APP_VERSION,
    GITHUB_URL,
    KEM_ALGORITHM,
    SIGNATURE_ALGORITHM,
)
from app.database import Database
from app.i18n import I18n
from crypto import container as qsec
from crypto import keys as keyops
from crypto import signatures as sigops

STYLE = """
QMainWindow, QDialog { background:#080c12; color:#dbe7f3; }
QWidget { color:#dbe7f3; font-family:"Segoe UI"; }
QLabel#Title { font-size:25px; font-weight:800; letter-spacing:1px; color:#f3f8ff; }
QLabel#Subtitle { color:#65e7c5; font-size:11px; font-weight:700; letter-spacing:1px; }
QLabel#Status { color:#65e7c5; font-weight:700; }
QTabWidget::pane { border:1px solid #243244; top:-1px; background:#0d131c; }
QTabBar::tab { background:#111a26; border:1px solid #243244; padding:11px 17px; font-weight:700; }
QTabBar::tab:selected { background:#172536; color:#65e7c5; }
QGroupBox { border:1px solid #243244; border-radius:8px; margin-top:14px; padding:13px; font-weight:700; }
QGroupBox::title { subcontrol-origin:margin; left:12px; padding:0 6px; color:#65e7c5; }
QLineEdit, QPlainTextEdit, QComboBox, QTextBrowser, QTableWidget {
    background:#070b10; border:1px solid #26364a; border-radius:6px; padding:7px; color:#e7eff8;
    selection-background-color:#284f64;
}
QLineEdit:focus, QPlainTextEdit:focus, QComboBox:focus { border:1px solid #65e7c5; }
QPushButton {
    background:#152232; border:1px solid #31445c; border-radius:6px; padding:9px 13px;
    font-weight:700; color:#eaf2fa;
}
QPushButton:hover { background:#1d3045; border-color:#65e7c5; }
QPushButton#Primary { background:#163b36; border-color:#2d7569; color:#dffff6; }
QPushButton#Danger { background:#402027; border-color:#75404a; }
QHeaderView::section { background:#111a26; color:#dbe7f3; border:0; border-right:1px solid #243244; padding:7px; font-weight:700; }
QTableWidget { gridline-color:#1e2a38; }
QStatusBar { background:#070b10; border-top:1px solid #243244; }
"""


class DropLineEdit(QLineEdit):
    def __init__(self) -> None:
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        urls = event.mimeData().urls()
        if urls and urls[0].isLocalFile():
            self.setText(urls[0].toLocalFile())
            event.acceptProposedAction()


class InfoDialog(QDialog):
    def __init__(self, parent: QWidget | None, i18n: I18n, database_path: Path) -> None:
        super().__init__(parent)
        self.i18n = i18n
        self.database_path = database_path
        self.resize(760, 700)
        layout = QVBoxLayout(self)
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        layout.addWidget(self.browser)
        self.close_btn = QPushButton("OK")
        self.close_btn.clicked.connect(self.accept)
        layout.addWidget(self.close_btn)
        self.retranslate()

    def retranslate(self) -> None:
        self.setWindowTitle(self.i18n.t("info_title"))
        info = self.i18n.t("info_text").replace("__DB_PATH__", escape(str(self.database_path)))
        self.browser.setHtml(info)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.db = Database()
        saved_lang = self.db.get_setting("language", "de")
        self.i18n = I18n(saved_lang)
        self.setWindowTitle(f"{APP_TITLE} v{APP_VERSION}")
        self.resize(1220, 850)
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(STYLE)
        self._build_ui()
        self.retranslate()
        self.refresh_database()

    def _build_ui(self) -> None:
        central = QWidget()
        outer = QVBoxLayout(central)
        outer.setContentsMargins(18, 16, 18, 10)
        outer.setSpacing(12)

        top = QHBoxLayout()
        title_box = QVBoxLayout()
        self.title_label = QLabel(APP_TITLE.upper())
        self.title_label.setObjectName("Title")
        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("Subtitle")
        title_box.addWidget(self.title_label)
        title_box.addWidget(self.subtitle_label)
        top.addLayout(title_box)
        top.addStretch()

        self.lang_btn = QPushButton()
        self.lang_btn.clicked.connect(self.toggle_language)
        self.github_btn = QPushButton()
        self.github_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(GITHUB_URL)))
        self.info_btn = QPushButton()
        self.info_btn.clicked.connect(self.show_info)
        top.addWidget(self.lang_btn)
        top.addWidget(self.github_btn)
        top.addWidget(self.info_btn)
        outer.addLayout(top)

        self.tabs = QTabWidget()
        self.text_tab = self._build_text_tab()
        self.file_tab = self._build_file_tab()
        self.keys_tab = self._build_keys_tab()
        self.sign_tab = self._build_sign_tab()
        self.database_tab = self._build_database_tab()
        for tab in [self.text_tab, self.file_tab, self.keys_tab, self.sign_tab, self.database_tab]:
            self.tabs.addTab(tab, "")
        outer.addWidget(self.tabs)

        self.setCentralWidget(central)
        status = QStatusBar()
        self.status_label = QLabel()
        self.status_label.setObjectName("Status")
        status.addWidget(self.status_label)
        status.addPermanentWidget(QLabel(f"DB: {self.db.path}"))
        status.addPermanentWidget(QLabel(f"v{APP_VERSION}"))
        self.setStatusBar(status)

    def _build_text_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        controls = QGroupBox()
        form = QFormLayout(controls)

        self.text_mode_label = QLabel()
        self.text_mode = QComboBox()
        self.text_password_label = QLabel()
        self.text_password = QLineEdit()
        self.text_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.text_pub_label = QLabel()
        self.text_pub = QLineEdit()
        self.text_pub_btn = QPushButton()
        pubrow = QHBoxLayout()
        pubrow.addWidget(self.text_pub)
        pubrow.addWidget(self.text_pub_btn)
        self.text_pub_btn.clicked.connect(lambda: self._pick_key(self.text_pub, "*.qpub"))

        self.text_priv_label = QLabel()
        self.text_priv = QLineEdit()
        self.text_priv_btn = QPushButton()
        privrow = QHBoxLayout()
        privrow.addWidget(self.text_priv)
        privrow.addWidget(self.text_priv_btn)
        self.text_priv_btn.clicked.connect(lambda: self._pick_key(self.text_priv, "*.qkey"))

        form.addRow(self.text_mode_label, self.text_mode)
        form.addRow(self.text_password_label, self.text_password)
        form.addRow(self.text_pub_label, self._wrap(pubrow))
        form.addRow(self.text_priv_label, self._wrap(privrow))
        layout.addWidget(controls)

        editors = QHBoxLayout()
        left = QVBoxLayout()
        self.source_label = QLabel()
        self.source = QPlainTextEdit()
        left.addWidget(self.source_label)
        left.addWidget(self.source)
        right = QVBoxLayout()
        self.result_label = QLabel()
        self.result = QPlainTextEdit()
        right.addWidget(self.result_label)
        right.addWidget(self.result)
        editors.addLayout(left)
        editors.addLayout(right)
        layout.addLayout(editors, 1)

        actions = QHBoxLayout()
        self.text_encrypt_btn = QPushButton()
        self.text_encrypt_btn.setObjectName("Primary")
        self.text_decrypt_btn = QPushButton()
        self.text_decrypt_btn.setObjectName("Primary")
        self.text_copy_btn = QPushButton()
        self.text_clear_btn = QPushButton()
        self.text_encrypt_btn.clicked.connect(self.encrypt_text)
        self.text_decrypt_btn.clicked.connect(self.decrypt_text)
        self.text_copy_btn.clicked.connect(self.copy_result)
        self.text_clear_btn.clicked.connect(lambda: (self.source.clear(), self.result.clear()))
        actions.addWidget(self.text_encrypt_btn)
        actions.addWidget(self.text_decrypt_btn)
        actions.addStretch()
        actions.addWidget(self.text_copy_btn)
        actions.addWidget(self.text_clear_btn)
        layout.addLayout(actions)
        return tab

    def _build_file_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        box = QGroupBox()
        form = QFormLayout(box)

        self.file_mode_label = QLabel()
        self.file_mode = QComboBox()
        self.file_password_label = QLabel()
        self.file_password = QLineEdit()
        self.file_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.input_file_label = QLabel()
        self.input_file = DropLineEdit()
        self.input_file_btn = QPushButton()
        inrow = QHBoxLayout()
        inrow.addWidget(self.input_file)
        inrow.addWidget(self.input_file_btn)
        self.input_file_btn.clicked.connect(self.pick_input_file)

        self.output_file_label = QLabel()
        self.output_file = QLineEdit()
        self.output_file_btn = QPushButton()
        outrow = QHBoxLayout()
        outrow.addWidget(self.output_file)
        outrow.addWidget(self.output_file_btn)
        self.output_file_btn.clicked.connect(self.pick_output_file)

        self.file_pub_label = QLabel()
        self.file_pub = QLineEdit()
        self.file_pub_btn = QPushButton()
        pubrow = QHBoxLayout()
        pubrow.addWidget(self.file_pub)
        pubrow.addWidget(self.file_pub_btn)
        self.file_pub_btn.clicked.connect(lambda: self._pick_key(self.file_pub, "*.qpub"))

        self.file_priv_label = QLabel()
        self.file_priv = QLineEdit()
        self.file_priv_btn = QPushButton()
        privrow = QHBoxLayout()
        privrow.addWidget(self.file_priv)
        privrow.addWidget(self.file_priv_btn)
        self.file_priv_btn.clicked.connect(lambda: self._pick_key(self.file_priv, "*.qkey"))

        form.addRow(self.file_mode_label, self.file_mode)
        form.addRow(self.input_file_label, self._wrap(inrow))
        form.addRow(self.output_file_label, self._wrap(outrow))
        form.addRow(self.file_password_label, self.file_password)
        form.addRow(self.file_pub_label, self._wrap(pubrow))
        form.addRow(self.file_priv_label, self._wrap(privrow))
        layout.addWidget(box)

        self.drop_info = QLabel()
        self.drop_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_info.setMinimumHeight(150)
        self.drop_info.setStyleSheet("border:1px dashed #39536d;border-radius:10px;color:#7f97ad;font-size:15px;")
        layout.addWidget(self.drop_info, 1)

        actions = QHBoxLayout()
        self.file_encrypt_btn = QPushButton()
        self.file_encrypt_btn.setObjectName("Primary")
        self.file_decrypt_btn = QPushButton()
        self.file_decrypt_btn.setObjectName("Primary")
        self.file_encrypt_btn.clicked.connect(self.encrypt_file)
        self.file_decrypt_btn.clicked.connect(self.decrypt_file)
        actions.addWidget(self.file_encrypt_btn)
        actions.addWidget(self.file_decrypt_btn)
        actions.addStretch()
        layout.addLayout(actions)
        return tab

    def _build_keys_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.kem_group = QGroupBox()
        kem_form = QFormLayout(self.kem_group)
        self.key_desc = QLabel()
        self.key_desc.setWordWrap(True)
        self.key_folder_label = QLabel()
        self.key_folder = QLineEdit()
        self.key_folder_btn = QPushButton()
        kem_folder_row = QHBoxLayout()
        kem_folder_row.addWidget(self.key_folder)
        kem_folder_row.addWidget(self.key_folder_btn)
        self.key_folder_btn.clicked.connect(lambda: self.pick_folder(self.key_folder))
        self.key_name_label = QLabel()
        self.key_name = QLineEdit("quantum_identity")
        self.key_password_label = QLabel()
        self.key_password = QLineEdit()
        self.key_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.generate_keys_btn = QPushButton()
        self.generate_keys_btn.setObjectName("Primary")
        self.generate_keys_btn.clicked.connect(self.generate_kem_keys)
        self.key_fingerprint_label = QLabel()
        self.key_fingerprint = QLineEdit()
        self.key_fingerprint.setReadOnly(True)
        self.kem_pub_path_label = QLabel()
        self.kem_pub_path = QLineEdit()
        self.kem_pub_path.setReadOnly(True)
        self.kem_priv_path_label = QLabel()
        self.kem_priv_path = QLineEdit()
        self.kem_priv_path.setReadOnly(True)
        kem_form.addRow(self.key_desc)
        kem_form.addRow(self.key_folder_label, self._wrap(kem_folder_row))
        kem_form.addRow(self.key_name_label, self.key_name)
        kem_form.addRow(self.key_password_label, self.key_password)
        kem_form.addRow("", self.generate_keys_btn)
        kem_form.addRow(self.key_fingerprint_label, self.key_fingerprint)
        kem_form.addRow(self.kem_pub_path_label, self.kem_pub_path)
        kem_form.addRow(self.kem_priv_path_label, self.kem_priv_path)

        self.sig_group = QGroupBox()
        sig_form = QFormLayout(self.sig_group)
        self.sig_desc = QLabel()
        self.sig_desc.setWordWrap(True)
        self.sig_folder_label = QLabel()
        self.sig_folder = QLineEdit()
        self.sig_folder_btn = QPushButton()
        sig_folder_row = QHBoxLayout()
        sig_folder_row.addWidget(self.sig_folder)
        sig_folder_row.addWidget(self.sig_folder_btn)
        self.sig_folder_btn.clicked.connect(lambda: self.pick_folder(self.sig_folder))
        self.sig_name_label = QLabel()
        self.sig_name = QLineEdit("quantum_signature")
        self.sig_password_label = QLabel()
        self.sig_password = QLineEdit()
        self.sig_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.generate_sig_keys_btn = QPushButton()
        self.generate_sig_keys_btn.setObjectName("Primary")
        self.generate_sig_keys_btn.clicked.connect(self.generate_signature_keys)
        self.sig_fingerprint_label = QLabel()
        self.sig_fingerprint = QLineEdit()
        self.sig_fingerprint.setReadOnly(True)
        self.sig_pub_path_label = QLabel()
        self.sig_pub_path = QLineEdit()
        self.sig_pub_path.setReadOnly(True)
        self.sig_priv_path_label = QLabel()
        self.sig_priv_path = QLineEdit()
        self.sig_priv_path.setReadOnly(True)
        sig_form.addRow(self.sig_desc)
        sig_form.addRow(self.sig_folder_label, self._wrap(sig_folder_row))
        sig_form.addRow(self.sig_name_label, self.sig_name)
        sig_form.addRow(self.sig_password_label, self.sig_password)
        sig_form.addRow("", self.generate_sig_keys_btn)
        sig_form.addRow(self.sig_fingerprint_label, self.sig_fingerprint)
        sig_form.addRow(self.sig_pub_path_label, self.sig_pub_path)
        sig_form.addRow(self.sig_priv_path_label, self.sig_priv_path)

        layout.addWidget(self.kem_group)
        layout.addWidget(self.sig_group)
        layout.addStretch()
        return tab

    def _build_sign_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        box = QGroupBox()
        form = QFormLayout(box)

        self.sign_file_label = QLabel()
        self.sign_file_input = DropLineEdit()
        self.sign_file_btn = QPushButton()
        row1 = QHBoxLayout()
        row1.addWidget(self.sign_file_input)
        row1.addWidget(self.sign_file_btn)
        self.sign_file_btn.clicked.connect(lambda: self._pick_any(self.sign_file_input))

        self.signature_file_label = QLabel()
        self.signature_file_input = QLineEdit()
        self.signature_file_btn = QPushButton()
        row2 = QHBoxLayout()
        row2.addWidget(self.signature_file_input)
        row2.addWidget(self.signature_file_btn)
        self.signature_file_btn.clicked.connect(self.pick_signature_file)

        self.sign_priv_label = QLabel()
        self.sign_priv = QLineEdit()
        self.sign_priv_btn = QPushButton()
        row3 = QHBoxLayout()
        row3.addWidget(self.sign_priv)
        row3.addWidget(self.sign_priv_btn)
        self.sign_priv_btn.clicked.connect(lambda: self._pick_key(self.sign_priv, "*.qsigkey"))

        self.sign_pub_label = QLabel()
        self.sign_pub = QLineEdit()
        self.sign_pub_btn = QPushButton()
        row4 = QHBoxLayout()
        row4.addWidget(self.sign_pub)
        row4.addWidget(self.sign_pub_btn)
        self.sign_pub_btn.clicked.connect(lambda: self._pick_key(self.sign_pub, "*.qsigpub"))

        self.sign_password_label = QLabel()
        self.sign_password = QLineEdit()
        self.sign_password.setEchoMode(QLineEdit.EchoMode.Password)

        form.addRow(self.sign_file_label, self._wrap(row1))
        form.addRow(self.signature_file_label, self._wrap(row2))
        form.addRow(self.sign_priv_label, self._wrap(row3))
        form.addRow(self.sign_pub_label, self._wrap(row4))
        form.addRow(self.sign_password_label, self.sign_password)
        layout.addWidget(box)

        actions = QHBoxLayout()
        self.sign_btn = QPushButton()
        self.sign_btn.setObjectName("Primary")
        self.verify_btn = QPushButton()
        self.verify_btn.setObjectName("Primary")
        self.sign_btn.clicked.connect(self.sign_selected_file)
        self.verify_btn.clicked.connect(self.verify_selected_file)
        actions.addWidget(self.sign_btn)
        actions.addWidget(self.verify_btn)
        actions.addStretch()
        layout.addLayout(actions)
        layout.addStretch()
        return tab

    def _build_database_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.db_group = QGroupBox()
        db_box = QVBoxLayout(self.db_group)
        self.db_desc = QLabel()
        self.db_desc.setWordWrap(True)
        db_box.addWidget(self.db_desc)

        path_row = QHBoxLayout()
        self.db_path_label = QLabel()
        self.db_path = QLineEdit(str(self.db.path))
        self.db_path.setReadOnly(True)
        path_row.addWidget(self.db_path_label)
        path_row.addWidget(self.db_path, 1)
        db_box.addLayout(path_row)
        layout.addWidget(self.db_group)

        self.db_table = QTableWidget(0, 6)
        self.db_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.db_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.db_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.db_table.verticalHeader().setVisible(False)
        self.db_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.db_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.db_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.db_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.db_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.db_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.db_table.doubleClicked.connect(self._on_database_double_clicked)
        layout.addWidget(self.db_table, 1)

        actions = QHBoxLayout()
        self.db_refresh_btn = QPushButton()
        self.db_load_btn = QPushButton()
        self.db_load_btn.setObjectName("Primary")
        self.db_export_btn = QPushButton()
        self.db_delete_btn = QPushButton()
        self.db_delete_btn.setObjectName("Danger")
        self.db_refresh_btn.clicked.connect(self.refresh_database)
        self.db_load_btn.clicked.connect(self.load_selected_database_key)
        self.db_export_btn.clicked.connect(self.export_selected_database_key)
        self.db_delete_btn.clicked.connect(self.delete_selected_database_key)
        actions.addWidget(self.db_refresh_btn)
        actions.addWidget(self.db_load_btn)
        actions.addWidget(self.db_export_btn)
        actions.addStretch()
        actions.addWidget(self.db_delete_btn)
        layout.addLayout(actions)
        return tab

    def _on_database_double_clicked(self, _index: QModelIndex) -> None:
        self.load_selected_database_key()

    @staticmethod
    def _wrap(layout: QLayout) -> QWidget:
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def _msg(self, icon: QMessageBox.Icon, text: str, title_key: str | None = None) -> None:
        box = QMessageBox(self)
        box.setIcon(icon)
        if title_key:
            box.setWindowTitle(self.i18n.t(title_key))
        elif icon == QMessageBox.Icon.Critical:
            box.setWindowTitle(self.i18n.t("error"))
        else:
            box.setWindowTitle(self.i18n.t("success"))
        box.setText(text)
        box.exec()

    def _error(self, exc: Exception) -> None:
        self._msg(QMessageBox.Icon.Critical, str(exc))

    def _ok(self, text: str) -> None:
        self.status_label.setText(text)
        self._msg(QMessageBox.Icon.Information, text)

    def toggle_language(self) -> None:
        lang = self.i18n.toggle()
        self.db.save_setting("language", lang)
        self.retranslate()
        self.refresh_database()

    def retranslate(self) -> None:
        t = self.i18n.t
        self.subtitle_label.setText(t("app_subtitle"))
        self.lang_btn.setText(t("lang"))
        self.github_btn.setText(t("github"))
        self.info_btn.setText(t("info"))
        self.tabs.setTabText(0, t("text_tab"))
        self.tabs.setTabText(1, t("file_tab"))
        self.tabs.setTabText(2, t("keys_tab"))
        self.tabs.setTabText(3, t("sign_tab"))
        self.tabs.setTabText(4, t("database_tab"))

        for combo in [self.text_mode, self.file_mode]:
            current = combo.currentIndex()
            combo.clear()
            combo.addItems([t("password_mode"), t("pq_mode")])
            combo.setCurrentIndex(max(0, current))

        self.text_mode_label.setText(t("mode"))
        self.text_password_label.setText(t("password"))
        self.text_pub_label.setText(t("public_key"))
        self.text_priv_label.setText(t("private_key"))
        self.text_pub_btn.setText(t("browse"))
        self.text_priv_btn.setText(t("browse"))
        self.source_label.setText(t("source_text"))
        self.result_label.setText(t("result_text"))
        self.text_encrypt_btn.setText(t("encrypt_text"))
        self.text_decrypt_btn.setText(t("decrypt_text"))
        self.text_copy_btn.setText(t("copy"))
        self.text_clear_btn.setText(t("clear"))

        self.file_mode_label.setText(t("mode"))
        self.input_file_label.setText(t("input_file"))
        self.output_file_label.setText(t("output_file"))
        self.file_password_label.setText(t("password"))
        self.file_pub_label.setText(t("public_key"))
        self.file_priv_label.setText(t("private_key"))
        for btn in [self.input_file_btn, self.output_file_btn, self.file_pub_btn, self.file_priv_btn]:
            btn.setText(t("browse"))
        self.file_encrypt_btn.setText(t("encrypt_file"))
        self.file_decrypt_btn.setText(t("decrypt_file"))
        self.drop_info.setText(t("drop_hint"))

        self.kem_group.setTitle(t("key_title"))
        self.key_desc.setText(t("key_desc"))
        self.key_folder_label.setText(t("key_folder"))
        self.key_name_label.setText(t("key_name"))
        self.key_password_label.setText(t("key_password"))
        self.key_folder_btn.setText(t("browse"))
        self.generate_keys_btn.setText(t("generate_keys"))
        self.key_fingerprint_label.setText(t("fingerprint"))
        self.kem_pub_path_label.setText(t("generated_public"))
        self.kem_priv_path_label.setText(t("generated_private"))

        self.sig_group.setTitle(t("sig_key_title"))
        self.sig_desc.setText(t("sig_key_desc"))
        self.sig_folder_label.setText(t("sig_folder"))
        self.sig_name_label.setText(t("sig_name"))
        self.sig_password_label.setText(t("key_password"))
        self.sig_folder_btn.setText(t("browse"))
        self.generate_sig_keys_btn.setText(t("generate_sig_keys"))
        self.sig_fingerprint_label.setText(t("fingerprint"))
        self.sig_pub_path_label.setText(t("generated_public"))
        self.sig_priv_path_label.setText(t("generated_private"))

        self.sign_file_label.setText(t("sign_file"))
        self.signature_file_label.setText(t("signature_file"))
        self.sign_priv_label.setText(t("sign_private_key"))
        self.sign_pub_label.setText(t("sign_public_key"))
        self.sign_password_label.setText(t("password"))
        for btn in [self.sign_file_btn, self.signature_file_btn, self.sign_priv_btn, self.sign_pub_btn]:
            btn.setText(t("browse"))
        self.sign_btn.setText(t("sign"))
        self.verify_btn.setText(t("verify"))

        self.db_group.setTitle(t("database_title"))
        self.db_desc.setText(t("database_desc"))
        self.db_path_label.setText(t("database_path"))
        self.db_refresh_btn.setText(t("db_refresh"))
        self.db_load_btn.setText(t("db_load"))
        self.db_export_btn.setText(t("db_export"))
        self.db_delete_btn.setText(t("db_delete"))
        self.db_table.setHorizontalHeaderLabels([
            t("db_id"), t("db_name"), t("db_type"), t("db_algorithm"), t("db_fingerprint"), t("db_created")
        ])
        self.status_label.setText(t("status_ready"))

    def show_info(self) -> None:
        InfoDialog(self, self.i18n, self.db.path).exec()

    def copy_result(self) -> None:
        QGuiApplication.clipboard().setText(self.result.toPlainText())
        self.status_label.setText(self.i18n.t("copied"))

    def _pick_key(self, target: QLineEdit, pattern: str) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, self.i18n.t("browse"), "", f"Quantum Security Keys ({pattern});;All files (*)"
        )
        if path:
            target.setText(path)

    def _pick_any(self, target: QLineEdit) -> None:
        path, _ = QFileDialog.getOpenFileName(self, self.i18n.t("select_file"), "", "All files (*)")
        if path:
            target.setText(path)

    def pick_input_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, self.i18n.t("select_file"), "", "All files (*)")
        if path:
            self.input_file.setText(path)
            self.output_file.setText(str(Path(path).with_suffix("")) if path.lower().endswith(".qsec") else path + ".qsec")

    def pick_output_file(self) -> None:
        source = self.input_file.text().strip()
        if source.lower().endswith(".qsec"):
            path, _ = QFileDialog.getSaveFileName(
                self, self.i18n.t("save_file"), str(Path(source).with_suffix("")), "All files (*)"
            )
        else:
            path, _ = QFileDialog.getSaveFileName(
                self, self.i18n.t("save_qsec"), source + ".qsec" if source else "", "QSEC (*.qsec)"
            )
        if path:
            self.output_file.setText(path)

    def pick_folder(self, target: QLineEdit) -> None:
        path = QFileDialog.getExistingDirectory(self, self.i18n.t("select_folder"))
        if path:
            target.setText(path)

    def pick_signature_file(self) -> None:
        current = self.sign_file_input.text().strip()
        default = current + ".qsig" if current else ""
        path, _ = QFileDialog.getSaveFileName(
            self, self.i18n.t("save_signature"), default, "QSEC Signature (*.qsig);;All files (*)"
        )
        if path:
            self.signature_file_input.setText(path)

    def encrypt_text(self) -> None:
        try:
            source = self.source.toPlainText()
            if not source:
                raise ValueError(self.i18n.t("need_text"))
            if self.text_mode.currentIndex() == 0:
                password = self.text_password.text()
                if not password:
                    raise ValueError(self.i18n.t("need_password"))
                out = qsec.encrypt_text_password(source, password)
            else:
                pub = self.text_pub.text().strip()
                if not pub:
                    raise ValueError(self.i18n.t("need_public"))
                out = qsec.encrypt_text_pq(source, pub)
            self.result.setPlainText(out)
            self.status_label.setText(self.i18n.t("done_encrypt"))
        except Exception as exc:
            self._error(exc)

    def decrypt_text(self) -> None:
        try:
            source = self.source.toPlainText()
            if not source:
                raise ValueError(self.i18n.t("need_text"))
            if self.text_mode.currentIndex() == 0:
                password = self.text_password.text()
                if not password:
                    raise ValueError(self.i18n.t("need_password"))
                out = qsec.decrypt_text_password(source, password)
            else:
                priv = self.text_priv.text().strip()
                password = self.text_password.text()
                if not priv:
                    raise ValueError(self.i18n.t("need_private"))
                if not password:
                    raise ValueError(self.i18n.t("need_password"))
                out = qsec.decrypt_text_pq(source, priv, password)
            self.result.setPlainText(out)
            self.status_label.setText(self.i18n.t("done_decrypt"))
        except Exception as exc:
            self._error(exc)

    def encrypt_file(self) -> None:
        try:
            src, dst = self.input_file.text().strip(), self.output_file.text().strip()
            if not src:
                raise ValueError(self.i18n.t("need_file"))
            if not dst:
                raise ValueError(self.i18n.t("need_output"))
            if self.file_mode.currentIndex() == 0:
                password = self.file_password.text()
                if not password:
                    raise ValueError(self.i18n.t("need_password"))
                qsec.encrypt_file_password(src, dst, password)
            else:
                pub = self.file_pub.text().strip()
                if not pub:
                    raise ValueError(self.i18n.t("need_public"))
                qsec.encrypt_file_pq(src, dst, pub)
            self._ok(self.i18n.t("done_encrypt"))
        except Exception as exc:
            self._error(exc)

    def decrypt_file(self) -> None:
        try:
            src, dst = self.input_file.text().strip(), self.output_file.text().strip()
            if not src:
                raise ValueError(self.i18n.t("need_file"))
            if not dst:
                raise ValueError(self.i18n.t("need_output"))
            if self.file_mode.currentIndex() == 0:
                password = self.file_password.text()
                if not password:
                    raise ValueError(self.i18n.t("need_password"))
                qsec.decrypt_file_password(src, dst, password)
            else:
                priv = self.file_priv.text().strip()
                password = self.file_password.text()
                if not priv:
                    raise ValueError(self.i18n.t("need_private"))
                if not password:
                    raise ValueError(self.i18n.t("need_password"))
                qsec.decrypt_file_pq(src, dst, priv, password)
            self._ok(self.i18n.t("done_decrypt"))
        except Exception as exc:
            self._error(exc)

    def generate_kem_keys(self) -> None:
        try:
            folder = self.key_folder.text().strip()
            name = self.key_name.text().strip()
            password = self.key_password.text()
            self._validate_key_form(folder, name, password)
            pub_path, priv_path, fp = keyops.create_kem_keypair(folder, name, password)
            self.db.save_keypair_files(name, "KEM", KEM_ALGORITHM, fp, pub_path, priv_path)
            self.key_fingerprint.setText(fp)
            self.kem_pub_path.setText(str(pub_path))
            self.kem_priv_path.setText(str(priv_path))
            self.text_pub.setText(str(pub_path))
            self.text_priv.setText(str(priv_path))
            self.file_pub.setText(str(pub_path))
            self.file_priv.setText(str(priv_path))
            self.refresh_database()
            self._ok(self.i18n.t("done_keys"))
        except Exception as exc:
            self._error(exc)

    def generate_signature_keys(self) -> None:
        try:
            folder = self.sig_folder.text().strip()
            name = self.sig_name.text().strip()
            password = self.sig_password.text()
            self._validate_key_form(folder, name, password)
            pub_path, priv_path, fp = keyops.create_signature_keypair(folder, name, password)
            self.db.save_keypair_files(name, "SIGNATURE", SIGNATURE_ALGORITHM, fp, pub_path, priv_path)
            self.sig_fingerprint.setText(fp)
            self.sig_pub_path.setText(str(pub_path))
            self.sig_priv_path.setText(str(priv_path))
            self.sign_pub.setText(str(pub_path))
            self.sign_priv.setText(str(priv_path))
            self.refresh_database()
            self._ok(self.i18n.t("done_keys"))
        except Exception as exc:
            self._error(exc)

    def _validate_key_form(self, folder: str, name: str, password: str) -> None:
        if not folder:
            raise ValueError(self.i18n.t("need_folder"))
        if not name or any(c in name for c in r'\/:*?"<>|'):
            raise ValueError(self.i18n.t("need_name"))
        if not password:
            raise ValueError(self.i18n.t("need_password"))

    def sign_selected_file(self) -> None:
        try:
            src = self.sign_file_input.text().strip()
            sig = self.signature_file_input.text().strip()
            priv = self.sign_priv.text().strip()
            password = self.sign_password.text()
            if not src:
                raise ValueError(self.i18n.t("need_file"))
            if not sig:
                sig = src + ".qsig"
                self.signature_file_input.setText(sig)
            if not priv:
                raise ValueError(self.i18n.t("need_private"))
            if not password:
                raise ValueError(self.i18n.t("need_password"))
            sigops.sign_file(src, priv, password, sig)
            self._ok(self.i18n.t("done_sign"))
        except Exception as exc:
            self._error(exc)

    def verify_selected_file(self) -> None:
        try:
            src = self.sign_file_input.text().strip()
            sig = self.signature_file_input.text().strip()
            pub = self.sign_pub.text().strip()
            if not src or not sig or not pub:
                raise ValueError(self.i18n.t("need_file"))
            valid = sigops.verify_file(src, pub, sig)
            if valid:
                self._ok(self.i18n.t("valid_sig"))
            else:
                self._msg(QMessageBox.Icon.Warning, self.i18n.t("invalid_sig"), "warning")
        except Exception as exc:
            self._error(exc)

    def refresh_database(self) -> None:
        rows = self.db.list_keypairs()
        self.db_table.setRowCount(len(rows))
        for row_index, record in enumerate(rows):
            values = [
                str(record["id"]),
                record["name"],
                record["key_type"],
                record["algorithm"],
                record["fingerprint"],
                record["created_at"].replace("T", " ")[:19],
            ]
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                if col == 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.db_table.setItem(row_index, col, item)
        self.db_table.resizeRowsToContents()

    def _selected_database_id(self) -> int:
        row = self.db_table.currentRow()
        if row < 0:
            raise ValueError(self.i18n.t("db_select"))

        item = self.db_table.item(row, 0)
        if item is None:
            raise ValueError(self.i18n.t("db_select"))

        return int(item.text())

    def load_selected_database_key(self) -> None:
        try:
            key_id = self._selected_database_id()
            pub_path, priv_path, record = self.db.materialize_keypair(key_id)
            if record["key_type"] == "KEM":
                for field in [self.text_pub, self.file_pub, self.kem_pub_path]:
                    field.setText(str(pub_path))
                for field in [self.text_priv, self.file_priv, self.kem_priv_path]:
                    field.setText(str(priv_path))
                self.key_name.setText(record["name"])
                self.key_fingerprint.setText(record["fingerprint"])
            elif record["key_type"] == "SIGNATURE":
                self.sign_pub.setText(str(pub_path))
                self.sign_priv.setText(str(priv_path))
                self.sig_pub_path.setText(str(pub_path))
                self.sig_priv_path.setText(str(priv_path))
                self.sig_name.setText(record["name"])
                self.sig_fingerprint.setText(record["fingerprint"])
            self.status_label.setText(self.i18n.t("db_loaded"))
            self._msg(QMessageBox.Icon.Information, self.i18n.t("db_loaded"))
        except Exception as exc:
            self._error(exc)

    def export_selected_database_key(self) -> None:
        try:
            key_id = self._selected_database_id()
            folder = QFileDialog.getExistingDirectory(self, self.i18n.t("select_folder"))
            if not folder:
                return
            self.db.export_keypair(key_id, folder)
            self._ok(self.i18n.t("db_exported"))
        except Exception as exc:
            self._error(exc)

    def delete_selected_database_key(self) -> None:
        try:
            key_id = self._selected_database_id()
            answer = QMessageBox.question(
                self,
                self.i18n.t("confirm"),
                self.i18n.t("db_delete_confirm"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if answer != QMessageBox.StandardButton.Yes:
                return
            self.db.delete_keypair(key_id)
            self.refresh_database()
            self.status_label.setText(self.i18n.t("db_deleted"))
        except Exception as exc:
            self._error(exc)
