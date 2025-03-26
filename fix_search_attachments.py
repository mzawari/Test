import os
import sys
from PyQt6.QtWidgets import QApplication, QLayout

def fix_search_attachments():
    with open('app/ui/search.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. تحسين وظيفة التعديل لتأكيد وصول المرفقات بشكل صحيح
    old_edit_code = """    def _edit_case(self, row):
        \"\"\"Edit the selected case\"\"\"
        # Get the case ID and table name from the first column
        id_item = self.results_table.item(row, 0)
        if not id_item:
            QMessageBox.warning(self, "خطأ", "لم يتم العثور على بيانات الحالة")
            return
            
        case_id = id_item.text()
        table_name = id_item.data(Qt.ItemDataRole.UserRole)
        
        if not table_name:
            QMessageBox.warning(self, "خطأ", "نوع الحالة غير معروف")
            return
        
        # Get case data with complete information
        case = get_case_by_id(table_name, case_id)
        if case:
            # Print debug information
            print(f"Editing case {case_id} from table {table_name}")
            print(f"Attachments: {case.get('attachments', 'No attachments found')}")
            
            # Create and show the case detail dialog
            detail_dialog = CaseDetailDialog(self, table_name, case)
            detail_dialog._edit_case()
            # Refresh search results after editing
            self._perform_search()"""

    new_edit_code = """    def _edit_case(self, row):
        \"\"\"Edit the selected case\"\"\"
        # Get the case ID and table name from the first column
        id_item = self.results_table.item(row, 0)
        if not id_item:
            QMessageBox.warning(self, "خطأ", "لم يتم العثور على بيانات الحالة")
            return
            
        case_id = id_item.text()
        table_name = id_item.data(Qt.ItemDataRole.UserRole)
        
        if not table_name:
            QMessageBox.warning(self, "خطأ", "نوع الحالة غير معروف")
            return
        
        # Get case data with complete information
        case = get_case_by_id(table_name, case_id)
        if case:
            # Print debug information
            print(f"Editing case {case_id} from table {table_name}")
            print(f"Attachments: {case.get('attachments', 'No attachments found')}")
            
            # Create and show the case detail dialog
            detail_dialog = CaseDetailDialog(self, table_name, case)
            
            # التأكد من تهيئة المرفقات بشكل صحيح
            self._ensure_attachments_visible(detail_dialog)
            
            # فتح نافذة التعديل
            detail_dialog._edit_case()
            
            # تحديث نتائج البحث بعد التعديل
            self._perform_search()"""

    # 2. إضافة مكان بجوار نتائج البحث لإظهار معلومات المرفقات للحالة المحددة
    counts_end = """        self.case_counters_layout.addWidget(self.prisoners_counter)
        
        main_layout.addLayout(self.case_counters_layout)"""

    attachments_info = """        self.case_counters_layout.addWidget(self.prisoners_counter)
        
        # إضافة معلومات المرفقات المرتبطة بالحالة المحددة
        self.attachments_info = QLabel("المرفقات: -")
        self.attachments_info.setStyleSheet("color: #1976d2; font-weight: bold;")
        self.case_counters_layout.addStretch()
        self.case_counters_layout.addWidget(self.attachments_info)
        
        main_layout.addLayout(self.case_counters_layout)"""

    # 3. تحسين دالة تحديث المرفقات
    attachments_function = """    def _update_attachment_info(self, row=-1):
        \"\"\"تحديث معلومات المرفقات للحالة المحددة\"\"\"
        if row < 0:
            # إعادة تعيين المعلومات إذا لم يتم تحديد أي صف
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
    """

    # 4. تحسين حدث النقر على صف في جدول النتائج لعرض معلومات المرفقات
    row_click = """        # Connect row click event to update selected info
        self.results_table.itemClicked.connect(lambda item: self._update_attachment_info(item.row()))
        self.results_table.itemSelectionChanged.connect(self._update_selection_info)
    """

    selection_info = """    def _update_selection_info(self):
        \"\"\"تحديث معلومات الحالة المحددة\"\"\"
        selected_items = self.results_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            self._update_attachment_info(row)
        else:
            self._update_attachment_info(-1)
    """

    # تطبيق التعديلات
    new_content = content.replace(old_edit_code, new_edit_code)
    new_content = new_content.replace(counts_end, attachments_info)

    # إضافة دالة تحديث معلومات المرفقات
    existing_ensure = """    def _ensure_attachments_visible(self, detail_dialog):"""
    new_content = new_content.replace(existing_ensure, attachments_function + existing_ensure)

    # إضافة حدث النقر على الصف
    table_connect_pattern = """        self.results_table.cellDoubleClicked.connect(self._open_case_detail)
        
        main_layout.addWidget(self.results_table, 1)  # Give the table a stretch factor of 1"""
    
    table_connect_new = """        self.results_table.cellDoubleClicked.connect(self._open_case_detail)
        
        # إضافة أحداث النقر على الصف
        self.results_table.itemClicked.connect(lambda item: self._update_attachment_info(item.row()))
        self.results_table.itemSelectionChanged.connect(self._update_selection_info)
        
        main_layout.addWidget(self.results_table, 1)  # Give the table a stretch factor of 1"""
    
    new_content = new_content.replace(table_connect_pattern, table_connect_new)

    # إضافة دالة تحديث معلومات الصف المحدد
    marker = """    def _show_martyrs_on_startup(self):"""
    new_content = new_content.replace(marker, selection_info + "\n" + marker)

    # حفظ التغييرات
    with open('app/ui/search.py', 'w', encoding='utf-8') as f:
        f.write(new_content)

    # تحسين واجهة إدارة المرفقات للتأكد من عملها بشكل سليم مع شاشة البحث
    with open('app/ui/attachments_manager.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # تحسين وظيفة إضافة وتحديث المرفقات
    old_add_refresh = """        if success:
            # Clear existing preview layout
            while attachments_layout.count() > 0:
                item = attachments_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                elif item.layout():
                    # Clear nested layout
                    while item.layout().count() > 0:
                        nested_item = item.layout().takeAt(0)
                        if nested_item.widget():
                            nested_item.widget().deleteLater()"""

    new_add_refresh = """        if success:
            # تحديث الواجهة لتعكس التغييرات
            QApplication.processEvents()
            
            # Clear existing preview layout
            while attachments_layout.count() > 0:
                item = attachments_layout.takeAt(0)
                if item and item.widget():
                    item.widget().deleteLater()
                elif item and item.layout():
                    # Clear nested layout
                    while item.layout().count() > 0:
                        nested_item = item.layout().takeAt(0)
                        if nested_item and nested_item.widget():
                            nested_item.widget().deleteLater()
                            
            # التأكد من تحديث الواجهة قبل إضافة العناصر الجديدة
            QApplication.processEvents()"""

    widget_content = content.replace(old_add_refresh, new_add_refresh)

    with open('app/ui/attachments_manager.py', 'w', encoding='utf-8') as f:
        f.write(widget_content)

    print("تم تحسين عرض المرفقات في واجهة البحث بنجاح")

if __name__ == "__main__":
    fix_search_attachments() 