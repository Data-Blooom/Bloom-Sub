import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QProgressBar,
    QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QUrl, QEvent
from PyQt5.QtGui import QFont, QDesktopServices

from converter import EncodingDetector, FileConverter


class ClickableComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.installEventFilter(self)
        
    def setLineEdit(self, edit):
        super().setLineEdit(edit)
        if self.lineEdit():
            self.lineEdit().installEventFilter(self)
            self.lineEdit().setCursor(Qt.PointingHandCursor)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.showPopup()
                return True
        return super().eventFilter(watched, event)


class ConversionThread(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(int, int)
    
    def __init__(self, source_dir, target_dir, source_enc, target_enc, is_file=False):
        super().__init__()
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.source_enc = source_enc
        self.target_enc = target_enc
        self.is_file = is_file
        self._is_running = True
        
    def run(self):
        try:
            if self.is_file:
                subtitle_files = [self.source_dir]
            else:
                subtitle_files = []
                for root, _, files in os.walk(self.source_dir):
                    for file in files:
                        if file.lower().endswith(('.srt', '.sub', '.txt', '.ass', '.ssa', '.vtt')):
                            subtitle_files.append(os.path.join(root, file))
            
            if not subtitle_files:
                self.finished.emit(0, 0)
                return
                
            success_count = 0
            total = len(subtitle_files)
            
            for i, file_path in enumerate(subtitle_files):
                if not self._is_running:
                    break
                    
                if self.is_file:
                    target_path = os.path.join(self.target_dir, os.path.basename(file_path))
                else:
                    rel_path = os.path.relpath(file_path, self.source_dir)
                    target_path = os.path.join(self.target_dir, rel_path)
                
                self.status.emit(os.path.basename(file_path))
                
                success, _ = FileConverter.convert_file(
                    file_path, target_path, self.source_enc, self.target_enc
                )
                
                if success:
                    success_count += 1
                    
                self.progress.emit(i + 1)
                
            self.finished.emit(success_count, total)
            
        except Exception as e:
            self.finished.emit(0, 0)
    
    def stop(self):
        self._is_running = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.source_path = ""
        self.target_dir = ""
        self.is_file_mode = False
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Bloom Sub")
        self.setFixedSize(500, 210)  
        
        font = QFont("B Nazanin", 11, QFont.Bold)
        self.setFont(font)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QWidget {
                background-color: #ffffff;
                color: #2d3748;
            }
            QLabel {
                color: #2d3748;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #5a67d8; 
                border: none;
                border-radius: 8px;
                padding: 4px 10px;
                color: white;
                font-family: "Segoe UI", "Tahoma", "B Nazanin";
                font-weight: 900;
                font-size: 12px;
                min-height: 25px;
            }
            QPushButton:hover {
                background-color: #4c51bf;
            }
            QPushButton:pressed {
                background-color: #3c366b;
            }
            QPushButton:disabled {
                background-color: #cbd5e0;
                color: #718096;
            }
            QPushButton#convert {
                background-color: #2f855a; 
                color: white;
                font-size: 13px;
                border-radius: 8px;
            }
            QPushButton#convert:hover {
                background-color: #276749;
            }
            QPushButton#convert:pressed {
                background-color: #1c4532;
            }
            QLineEdit {
                background-color: #f7fafc;
                border: 2px solid #a0aec0; 
                border-radius: 8px;
                padding: 3px 8px;
                color: #000000; 
                font-family: "Segoe UI", "Tahoma", "Arial";
                font-size: 12px; 
                font-weight: bold;
                min-height: 22px;
            }
            QLineEdit:focus {
                border-color: #5a67d8;
                background-color: #ffffff;
            }
            QLineEdit::placeholder {
                color: #000000; 
                font-family: "B Nazanin", "Tahoma";
                font-size: 13px;
            }
            QComboBox {
                background-color: #f7fafc;
                border: 2px solid #a0aec0; 
                border-radius: 8px;
                padding: 2px 8px;
                color: #1a202c;
                font-family: "Segoe UI", "Tahoma", "B Nazanin";
                font-size: 12px;
                font-weight: bold;
                min-height: 24px;
            }
            QComboBox:hover {
                border-color: #5a67d8;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #a0aec0;
                selection-background-color: #5a67d8;
                selection-color: white;
                font-weight: bold;
            }
            QProgressBar {
                border: 2px solid #a0aec0;
                border-radius: 8px;
                text-align: center;
                color: #1a202c;
                background-color: #f7fafc;
                height: 16px;
                font-family: "Segoe UI", "Tahoma";
                font-size: 11px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                           stop: 0 #5a67d8, stop: 1 #48bb78);
                border-radius: 6px;
            }
            QMessageBox {
                background-color: #ffffff;
            }
            QMessageBox QLabel {
                font-family: "Segoe UI", "Tahoma";
                font-size: 12px;
                color: #2d3748;
                font-weight: normal;
            }
            QMessageBox QPushButton {
                min-width: 70px;
                min-height: 20px;
            }
        """)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(6)  
        layout.setContentsMargins(12, 10, 12, 6) 
        
        # ===== ردیف ۱: پوشه مبدا =====
        source_row = QHBoxLayout()
        source_row.setSpacing(6) 
        
        self.source_input = QLineEdit()
        self.source_input.setPlaceholderText("مسیر را انتخاب کنید...")
        self.source_input.setReadOnly(True)
        self.source_input.setLayoutDirection(Qt.LeftToRight)
        self.source_input.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        source_row.addWidget(self.source_input)
        
        self.folder_btn = QPushButton("📁 پوشه")
        self.folder_btn.setFixedWidth(78) 
        source_row.addWidget(self.folder_btn)
        
        self.file_btn = QPushButton("📄 فایل")
        self.file_btn.setFixedWidth(65)
        source_row.addWidget(self.file_btn)
        
        layout.addLayout(source_row)
        
        target_row = QHBoxLayout()
        target_row.setSpacing(6)
        
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("مسیر پوشه مقصد را انتخاب کنید...")
        self.target_input.setReadOnly(True)
        self.target_input.setLayoutDirection(Qt.LeftToRight)
        self.target_input.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        target_row.addWidget(self.target_input)
        
        self.target_btn = QPushButton("انتخاب")
        self.target_btn.setFixedWidth(78) 
        target_row.addWidget(self.target_btn)
        
        layout.addLayout(target_row)
        layout.addSpacing(2)  
        
        row_layout = QHBoxLayout()
        row_layout.setSpacing(8) 
        
        convert_layout = QVBoxLayout()
        convert_layout.setSpacing(0)
        convert_layout.setContentsMargins(0, 20, 0, 0) 
        self.convert_btn = QPushButton("شروع") 
        self.convert_btn.setObjectName("convert")
        self.convert_btn.setMinimumWidth(105)
        self.convert_btn.setFixedHeight(30) 
        convert_layout.addWidget(self.convert_btn)
        row_layout.addLayout(convert_layout)
        
        target_enc_layout = QVBoxLayout()
        target_enc_layout.setSpacing(3) 
        target_enc_label = QLabel("🎯 فرمت خروجی:")
        target_enc_layout.addWidget(target_enc_label)
        
        self.target_enc = ClickableComboBox()
        self.target_enc.setLineEdit(QLineEdit())
        self.target_enc.lineEdit().setReadOnly(True)
        self.target_enc.lineEdit().setAlignment(Qt.AlignCenter)
        self.target_enc.addItems([
            "UTF-8 with BOM",  
            "UTF-8",
            "UTF-16 LE",       
            "UTF-16 BE",       
            "Windows-1256",    
            "ANSI",
            "Unicode"
        ])
        target_enc_layout.addWidget(self.target_enc)
        row_layout.addLayout(target_enc_layout)
        
        source_enc_layout = QVBoxLayout()
        source_enc_layout.setSpacing(3) 
        source_enc_label = QLabel("🔍 فرمت ورودی:")
        source_enc_layout.addWidget(source_enc_label)
        
        self.source_enc = ClickableComboBox()
        self.source_enc.setLineEdit(QLineEdit())
        self.source_enc.lineEdit().setReadOnly(True)
        self.source_enc.lineEdit().setAlignment(Qt.AlignCenter)
        self.source_enc.addItems([
            "تشخیص خودکار",  
            "UTF-8 with BOM",  
            "UTF-8",
            "UTF-16 LE",       
            "UTF-16 BE",       
            "Windows-1256",    
            "ANSI",
            "Unicode"
        ])
        source_enc_layout.addWidget(self.source_enc)
        row_layout.addLayout(source_enc_layout)
        
        layout.addLayout(row_layout)
        layout.addSpacing(2)  
        
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        bottom_row = QHBoxLayout()
        bottom_row.setContentsMargins(0, 2, 0, 0)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.status_label.setStyleSheet("color: #2f855a; font-family: 'Segoe UI', 'Tahoma', 'B Nazanin'; font-size: 11px; font-weight: bold; background: transparent;")
        bottom_row.addWidget(self.status_label, 1)
        
        self.footer_btn = QPushButton("Data Bloom 🌸")
        self.footer_btn.setCursor(Qt.PointingHandCursor)
        self.footer_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #d53f8c; 
                font-family: 'Segoe UI Semibold', 'Arial';
                font-size: 12px; 
                font-weight: bold;
                border: none;
                padding: 0px;
                min-height: 15px;
            }
            QPushButton:hover {
                color: #b83280;
                text-decoration: underline;
            }
        """)
        self.footer_btn.clicked.connect(self.open_linktree)
        bottom_row.addWidget(self.footer_btn, 2, Qt.AlignCenter) 
        
        right_spacer = QLabel("")
        right_spacer.setStyleSheet("background: transparent;")
        bottom_row.addWidget(right_spacer, 1)
        
        layout.addLayout(bottom_row)
        
        self.folder_btn.clicked.connect(lambda: self.select_source(is_file=False))
        self.file_btn.clicked.connect(lambda: self.select_source(is_file=True))
        self.target_btn.clicked.connect(self.select_target)
        self.convert_btn.clicked.connect(self.start_conversion)
        
    def _clean_path(self, path: str) -> str:
        """پاکسازی کامل کاراکترهای یونیکد کنترل جهت از مسیر فایل"""
        return path.replace("\u202a", "").replace("\u202b", "").replace("\u202c", "").strip()

    def open_linktree(self):
        QDesktopServices.openUrl(QUrl("https://linktr.ee/Data_Bloom"))
        
    def select_source(self, is_file=False):
        self.is_file_mode = is_file
        if is_file:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "انتخاب فایل زیرنویس",
                "", "زیرنویس (*.srt *.sub *.txt *.ass *.ssa *.vtt);;همه فایل‌ها (*.*)"
            )
            if file_path:
                self.source_path = os.path.normpath(file_path)
                self.source_input.setText("\u202a" + self.source_path)
        else:
            folder = QFileDialog.getExistingDirectory(self, "انتخاب پوشه مبدا")
            if folder:
                self.source_path = os.path.normpath(folder)
                self.source_input.setText("\u202a" + self.source_path)
                
    def select_target(self):
        folder = QFileDialog.getExistingDirectory(self, "انتخاب پوشه مقصد")
        if folder:
            self.target_dir = os.path.normpath(folder)
            self.target_input.setText("\u202a" + self.target_dir)
            
    def start_conversion(self):
        source_path_clean = self._clean_path(self.source_path)
        target_dir_clean = self._clean_path(self.target_dir)

        if not source_path_clean:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("خطا")
            msg.setText("لطفاً پوشه یا فایل مبدا را انتخاب کنید.")
            msg.setLayoutDirection(Qt.RightToLeft)
            msg.exec_()
            return
            
        if not target_dir_clean:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("خطا")
            msg.setText("لطفاً پوشه مقصد را انتخاب کنید.")
            msg.setLayoutDirection(Qt.RightToLeft)
            msg.exec_()
            return
            
        files = []
        if self.is_file_mode or os.path.isfile(source_path_clean):
            files = [source_path_clean]
        else:
            for root, _, filenames in os.walk(source_path_clean):
                for file in filenames:
                    if file.lower().endswith(('.srt', '.sub', '.txt', '.ass', '.ssa', '.vtt')):
                        files.append(os.path.join(root, file))
                    
        if not files:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("اطلاع")
            msg.setText("هیچ فایل زیرنویسی یافت نشد.")
            msg.setLayoutDirection(Qt.RightToLeft)
            msg.exec_()
            return
            
        base_dir = target_dir_clean
        dir_name = os.path.basename(base_dir)
        if dir_name.startswith("subtitle_") and len(dir_name) > 15:
            base_dir = os.path.dirname(base_dir)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_folder = os.path.join(base_dir, f"subtitle_{timestamp}")
        
        try:
            os.makedirs(output_folder, exist_ok=True)
        except Exception as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("خطای سیستم")
            msg.setText(f"خطا در ایجاد پوشه خروجی:\n{str(e)}")
            msg.setLayoutDirection(Qt.RightToLeft)
            msg.exec_()
            return

        self.target_input.setText("\u202a" + output_folder)
        
        self.convert_btn.setEnabled(False)
        self.folder_btn.setEnabled(False)
        self.file_btn.setEnabled(False)
        self.target_btn.setEnabled(False)
        
        self.progress.setVisible(True)
        self.progress.setMaximum(len(files))
        self.progress.setValue(0)
        
        source_enc = self.source_enc.currentText()
        target_enc = self.target_enc.currentText()
        
        self.thread = ConversionThread(
            source_path_clean, output_folder,
            source_enc, target_enc,
            self.is_file_mode or os.path.isfile(source_path_clean)
        )
        
        self.thread.progress.connect(self.update_progress)
        self.thread.status.connect(self.update_status)
        self.thread.finished.connect(lambda s, t: self.on_finished(s, t, output_folder))
        
        self.thread.start()
        self.status_label.setText("⏳ در حال تبدیل...")
        self.status_label.setStyleSheet("color: #dd6b20; font-family: 'Segoe UI', 'Tahoma', 'B Nazanin'; font-size: 11px; font-weight: bold;")
        
    def update_progress(self, value):
        self.progress.setValue(value)
        
    def update_status(self, text):
        self.status_label.setText(f"📄 {text}")
        
    def on_finished(self, success_count, total, output_folder):
        self.convert_btn.setEnabled(True)
        self.folder_btn.setEnabled(True)
        self.file_btn.setEnabled(True)
        self.target_btn.setEnabled(True)
        
        self.progress.setValue(total)
        
        msg = QMessageBox(self)
        msg.setLayoutDirection(Qt.RightToLeft)
        
        if success_count == total:
            self.status_label.setText(f"✅ {success_count} فایل تبدیل شد")
            self.status_label.setStyleSheet("color: #2f855a; font-family: 'Segoe UI', 'Tahoma', 'B Nazanin'; font-size: 11px; font-weight: bold;")
            
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("پایان عملیات")
            msg.setText(
                f"✅ عملیات با موفقیت کامل شد!\n\n"
                f"📊 تعداد فایل‌های تبدیل شده: {success_count} از {total}\n"
                f"📁 پوشه مقصد:\n{output_folder}"
            )
        else:
            self.status_label.setText(f"⚠️ {total - success_count} خطا")
            self.status_label.setStyleSheet("color: #e53e3e; font-family: 'Segoe UI', 'Tahoma', 'B Nazanin'; font-size: 11px; font-weight: bold;")
            
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("پایان عملیات")
            msg.setText(
                f"⚠️ عملیات با خطاهایی کامل شد.\n\n"
                f"✅ موفق: {success_count}\n"
                f"❌ ناموفق: {total - success_count}"
            )
            
        msg.exec_()
            
        try:
            os.startfile(output_folder)
        except:
            pass
                
        QTimer.singleShot(3000, lambda: self.progress.setVisible(False))
        
    def closeEvent(self, event):
        if self.thread and self.thread.isRunning():
            reply = QMessageBox.question(
                self, "خروج",
                "تبدیل در حال انجام است. آیا مطمئن هستید؟",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.thread.stop()
                self.thread.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("B Nazanin", 11, QFont.Bold)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())