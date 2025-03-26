import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from app.ui.search import SearchDialog
from app.ui.case_detail import CaseDetailDialog

def improve_search_dialog():
    with open('app/ui/search.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. تحسين مظهر مجموعات البحث لتتوافق مع مظهر شاشة التفاصيل
    old_groupbox_style = """            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                background-color: #f5f5f5;
            }"""

    new_groupbox_style = """            QGroupBox {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                margin-top: 15px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background-color: white;
                color: #444444;
                font-size: 14px;
            }"""

    # 2. تحسين مظهر النتائج في الجدول
    old_table_style = """            QTableWidget {
                border: 1px solid #cccccc;
                border-radius: 5px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                padding: 6px;
                border: 1px solid #cccccc;
                font-weight: bold;
            }"""

    new_table_style = """            QTableWidget {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                gridline-color: #f0f0f0;
                background-color: white;
            }
            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #2c3e50;
            }
            QHeaderView::section {
                background-color: #f5f8fa;
                padding: 8px;
                border: 1px solid #e0e0e0;
                color: #2c3e50;
                font-weight: bold;
                font-size: 12px;
            }"""

    # 3. تحسين مظهر الأزرار لتطابق أزرار شاشة التفاصيل
    old_button_style = """            QPushButton {
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                opacity: 0.8;
            }"""

    new_button_style = """            QPushButton {
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QPushButton:pressed {
                opacity: 1;
            }"""

    # 4. تحسين التباعد والهوامش في النتائج
    old_spacing = """        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)"""

    new_spacing = """        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)"""

    # 5. تعديل نمط زر البحث ليكون مطابقًا لأزرار شاشة التفاصيل
    old_search_button = """        search_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")"""
    
    new_search_button = """        search_button.setStyleSheet(\"\"\"
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        \"\"\")"""

    # 6. تحسين طريقة عرض النتائج للتمكن من إضافة المرفقات بسهولة
    old_open_case = """    def _open_case_detail(self, row, column):
        \"\"\"Open case detail window for the selected case\"\"\"
        # Get case ID and table from the first column
        id_item = self.results_table.item(row, 0)
        if not id_item:
            QMessageBox.warning(self, "خطأ", "لم يتم العثور على بيانات الحالة")
            return"""

    new_open_case = """    def _open_case_detail(self, row, column):
        \"\"\"Open case detail window for the selected case\"\"\"
        # Get case ID and table from the first column
        id_item = self.results_table.item(row, 0)
        if not id_item:
            QMessageBox.warning(self, "خطأ", "لم يتم العثور على بيانات الحالة")
            return"""

    # تطبيق التعديلات
    new_content = content.replace(old_groupbox_style, new_groupbox_style)
    new_content = new_content.replace(old_table_style, new_table_style)
    new_content = new_content.replace(old_button_style, new_button_style)
    new_content = new_content.replace(old_spacing, new_spacing)
    new_content = new_content.replace(old_search_button, new_search_button)

    # دالة إضافية لعرض المرفقات في نافذة البحث
    additional_code = """    def _ensure_attachments_visible(self, detail_dialog):
        \"\"\"التأكد من ظهور المرفقات في نافذة التفاصيل\"\"\"
        # تأكد من وجود المرفقات في قاعدة البيانات
        if hasattr(detail_dialog, 'attachment_files') and detail_dialog.attachment_files:
            print(f"Found {len(detail_dialog.attachment_files)} attachments")
            # استخدام AttachmentsManager للتأكد من عرض المرفقات بشكل صحيح
            from app.ui.attachments_manager import AttachmentsManager
            attachments_layout = detail_dialog.findChild(QLayout, "attachments_layout")
            if attachments_layout:
                AttachmentsManager._add_and_refresh(
                    detail_dialog, 
                    detail_dialog.table_name, 
                    detail_dialog.case_id, 
                    detail_dialog.case_data, 
                    attachments_layout
                )
    """

    # إضافة الدالة الجديدة بعد نهاية دالة _edit_case
    marker = "    def _delete_case(self, row):"
    new_content = new_content.replace(marker, additional_code + "\n" + marker)

    # تحسين طريقة عرض النتائج عند النقر على زر البحث
    old_perform_search = """    def _perform_search(self):
        \"\"\"Perform search based on current criteria\"\"\"
        search_term = self.search_term.text().strip()
        case_type = self.case_type.currentText()
        
        # Clear existing results
        self.results_table.setRowCount(0)"""

    new_perform_search = """    def _perform_search(self):
        \"\"\"Perform search based on current criteria\"\"\"
        search_term = self.search_term.text().strip()
        case_type = self.case_type.currentText()
        
        # تحسين شريط الحالة لإظهار أن عملية البحث جارية
        self.results_counter.setText("جاري البحث...")
        self.results_counter.setStyleSheet("font-weight: bold; font-size: 14px; color: #2196F3; margin: 10px 0;")
        QApplication.processEvents()  # تحديث الواجهة فورًا
        
        # Clear existing results
        self.results_table.setRowCount(0)"""

    new_content = new_content.replace(old_perform_search, new_perform_search)

    # تحسين دالة فتح تفاصيل الحالة بإضافة تنشيط المرفقات
    old_open_end = """        # Open the case detail dialog
        detail_dialog = CaseDetailDialog(self, table_name, case_data)
        detail_dialog.showMaximized()"""

    new_open_end = """        # Open the case detail dialog with improved attachments handling
        detail_dialog = CaseDetailDialog(self, table_name, case_data)
        
        # التأكد من ظهور المرفقات بشكل صحيح
        self._ensure_attachments_visible(detail_dialog)
        
        # عرض النافذة بالحجم الكامل
        detail_dialog.showMaximized()"""

    new_content = new_content.replace(old_open_end, new_open_end)

    # حفظ التغييرات
    with open('app/ui/search.py', 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("تم تحسين واجهة البحث بنجاح")

if __name__ == "__main__":
    improve_search_dialog() 