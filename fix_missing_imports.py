import re

def fix_missing_imports():
    with open('app/ui/search.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. التأكد من استيراد QApplication
    if 'from PyQt6.QtWidgets import QApplication' not in content:
        old_import = """from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QPushButton, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QLabel, QWidget
)"""
        new_import = """from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QPushButton, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QLabel, QWidget, QApplication, QLayout
)"""
        content = content.replace(old_import, new_import)
    
    # 2. التأكد من دالة تحديث معلومات حالة التحديد
    if '_update_selection_info' not in content:
        selection_function = """    def _update_selection_info(self):
        \"\"\"تحديث معلومات الحالة المحددة\"\"\"
        selected_items = self.results_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            self._update_attachment_info(row)
        else:
            self._update_attachment_info(-1)
    """
        # إضافة الدالة قبل دالة _show_martyrs_on_startup
        marker = """    def _show_martyrs_on_startup(self):"""
        if marker in content and selection_function not in content:
            content = content.replace(marker, selection_function + "\n" + marker)
    
    # 3. تصحيح استدعاء دالة _update_attachment_info في حدث النقر على صف في الجدول
    if 'self.results_table.itemClicked.connect' in content and '._update_attachment_info' not in content:
        old_connect = """        # Connect double-click event
        self.results_table.cellDoubleClicked.connect(self._open_case_detail)"""
        
        new_connect = """        # Connect double-click event
        self.results_table.cellDoubleClicked.connect(self._open_case_detail)
        
        # إضافة أحداث النقر على الصف
        self.results_table.itemClicked.connect(lambda item: self._update_attachment_info(item.row()))
        self.results_table.itemSelectionChanged.connect(self._update_selection_info)"""
        
        content = content.replace(old_connect, new_connect)
    
    # 4. التأكد من وجود دالة _ensure_attachments_visible
    if '_ensure_attachments_visible' not in content:
        ensure_function = """    def _ensure_attachments_visible(self, detail_dialog):
        \"\"\"التأكد من ظهور المرفقات في نافذة التفاصيل\"\"\"
        # تأكد من وجود المرفقات في قاعدة البيانات
        if hasattr(detail_dialog, 'attachment_files') and detail_dialog.attachment_files:
            print(f"Found {len(detail_dialog.attachment_files)} attachments")
            try:
                # استخدام AttachmentsManager للتأكد من عرض المرفقات بشكل صحيح
                from app.ui.attachments_manager import AttachmentsManager
                groups = detail_dialog.findChildren(QGroupBox)
                for group in groups:
                    if group.title() == "المرفقات":
                        parent_widget = group.parent()
                        if parent_widget and parent_widget.layout():
                            # تحديث المرفقات في قسم المرفقات
                            AttachmentsManager.create_attachments_widget(
                                detail_dialog, 
                                detail_dialog.table_name, 
                                detail_dialog.case_id, 
                                detail_dialog.case_data
                            )
                            return
            except Exception as e:
                print(f"Error ensuring attachments are visible: {e}")
    """
        
        # إضافة الدالة قبل دالة _update_selection_info
        if '_update_selection_info' in content and ensure_function not in content:
            content = content.replace("    def _update_selection_info", ensure_function + "\n    def _update_selection_info")
        else:
            marker = """    def _show_martyrs_on_startup(self):"""
            content = content.replace(marker, ensure_function + "\n" + marker)
    
    # 5. تحسين استدعاء _ensure_attachments_visible في دالة _open_case_detail
    pattern = r'detail_dialog = CaseDetailDialog\(.*?\)[ \t]*\n[ \t]*detail_dialog\.showMaximized\(\)'
    if re.search(pattern, content):
        replacement = """detail_dialog = CaseDetailDialog(self, table_name, case_data)
        
        # التأكد من ظهور المرفقات بشكل صحيح
        try:
            self._ensure_attachments_visible(detail_dialog)
        except Exception as e:
            print(f"Error ensuring attachments visibility: {e}")
        
        # عرض النافذة بالحجم الكامل
        detail_dialog.showMaximized()"""
        
        content = re.sub(pattern, replacement, content)
    
    # 6. إضافة متغير attachments_info إذا كان مفقودًا
    if 'self.attachments_info' not in content:
        old_counters = """        self.case_counters_layout.addWidget(self.prisoners_counter)
        
        main_layout.addLayout(self.case_counters_layout)"""
        
        new_counters = """        self.case_counters_layout.addWidget(self.prisoners_counter)
        
        # إضافة معلومات المرفقات المرتبطة بالحالة المحددة
        self.attachments_info = QLabel("المرفقات: -")
        self.attachments_info.setStyleSheet("color: #1976d2; font-weight: bold;")
        self.case_counters_layout.addStretch()
        self.case_counters_layout.addWidget(self.attachments_info)
        
        main_layout.addLayout(self.case_counters_layout)"""
        
        content = content.replace(old_counters, new_counters)
    
    # 7. إضافة دالة _update_attachment_info إذا كانت مفقودة
    if '_update_attachment_info' not in content:
        update_function = """    def _update_attachment_info(self, row=-1):
        \"\"\"تحديث معلومات المرفقات للحالة المحددة\"\"\"
        if row < 0 or not hasattr(self, 'attachments_info'):
            # إعادة تعيين المعلومات إذا لم يتم تحديد أي صف
            if hasattr(self, 'attachments_info'):
                self.attachments_info.setText("المرفقات: -")
            return

        # الحصول على بيانات الحالة المحددة
        id_item = self.results_table.item(row, 0)
        if not id_item:
            return
            
        case_id = id_item.text()
        table_name = id_item.data(Qt.ItemDataRole.UserRole)
        
        if not table_name:
            return
        
        try:
            # جلب معلومات الحالة الكاملة من قاعدة البيانات
            case = get_case_by_id(table_name, case_id)
            if case and 'attachments' in case and case['attachments']:
                attachments = case['attachments'].split(',')
                # عرض عدد المرفقات في شريط الحالة
                self.attachments_info.setText(f"المرفقات: {len(attachments)}")
                self.attachments_info.setStyleSheet("color: #1976d2; font-weight: bold;")
            else:
                self.attachments_info.setText("المرفقات: لا يوجد")
                self.attachments_info.setStyleSheet("color: #9e9e9e; font-weight: bold;")
        except Exception as e:
            print(f"Error updating attachment info: {e}")
            self.attachments_info.setText("المرفقات: خطأ في العرض")
            self.attachments_info.setStyleSheet("color: #f44336; font-weight: bold;")
    """
        
        if '_ensure_attachments_visible' in content:
            content = content.replace("    def _ensure_attachments_visible", update_function + "\n    def _ensure_attachments_visible")
        else:
            marker = """    def _update_selection_info(self):"""
            content = content.replace(marker, update_function + "\n" + marker)
            
    # حفظ التغييرات
    with open('app/ui/search.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # تحسين ملف attachments_manager.py
    with open('app/ui/attachments_manager.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # إضافة استيراد QApplication إذا كان مفقودًا
    if 'from PyQt6.QtWidgets import QApplication' not in content:
        old_import = """from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QFileDialog, QMessageBox, QInputDialog, QGroupBox
)"""
        new_import = """from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QFileDialog, QMessageBox, QInputDialog, QGroupBox,
    QApplication
)"""
        content = content.replace(old_import, new_import)
    
    # حفظ التغييرات لملف attachments_manager.py
    with open('app/ui/attachments_manager.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("تم تصحيح مشاكل الاستيراد والدوال المفقودة بنجاح")

if __name__ == "__main__":
    fix_missing_imports() 