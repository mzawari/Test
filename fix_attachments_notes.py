"""
سكربت لإصلاح مشكلتي عرض المرفقات وحجم الملاحظات
1. إصلاح مشكلة عدم ظهور المرفقات في شاشة التعديل لجميع الحالات
2. تعديل حجم قسم الملاحظات في شاشة عرض الجريح المدني
"""
import sys
import os
import re
from PyQt6.QtWidgets import QApplication, QLayout, QGroupBox, QVBoxLayout

def fix_attachments_and_notes():
    """تصحيح مشكلة عرض المرفقات في شاشة التعديل وحجم الملاحظات في شاشة الجريح المدني"""
    changes_made = False
    
    # 1. إصلاح مشكلة عرض المرفقات في شاشة التعديل
    fix_case_detail_file()
    
    # 2. إصلاح حجم الملاحظات في شاشة عرض الجريح المدني 
    fix_civilian_wounded_notes()
    
    print("تم إصلاح مشكلة عرض المرفقات وحجم الملاحظات بنجاح")

def fix_case_detail_file():
    """إصلاح شاشة تفاصيل الحالة لعرض المرفقات بشكل صحيح"""
    file_path = 'app/ui/case_detail.py'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changes_made = False
        
        # 1. تحسين دالة التحميل الأولي للتأكد من تحميل المرفقات
        if "_load_case_data" in content:
            # تحسين تهيئة المرفقات عند فتح نافذة التعديل
            load_case_pattern = r'def _load_case_data\(self\):(.*?)(?=def|\Z)'
            load_case_match = re.search(load_case_pattern, content, re.DOTALL)
            
            if load_case_match:
                old_load_case = load_case_match.group(0)
                
                # تأكد من أن الدالة تقوم بتحميل المرفقات بشكل صحيح
                if "self._add_attachments_section()" not in old_load_case or "_parse_attachments" not in old_load_case:
                    new_load_case = old_load_case.replace("def _load_case_data(self):", """def _load_case_data(self):
        \"\"\"تحميل بيانات الحالة وتأكيد تحميل المرفقات\"\"\"
        # تهيئة أولية للبيانات
        self.attachment_files = []
        
        # تحميل بيانات الحالة من قاعدة البيانات""")
                    
                    # تأكد من استدعاء دالة تحليل المرفقات في نهاية الدالة
                    if "self._parse_attachments()" not in old_load_case:
                        if "def _edit_case(self):" in content:
                            new_load_case = new_load_case.replace("def _edit_case(self):", """        # تحليل ملفات المرفقات وتهيئتها
        self._parse_attachments()
        
        # تحديث قسم المرفقات
        self._add_attachments_section()
        
def _edit_case(self):""")
                    
                    content = content.replace(old_load_case, new_load_case)
                    changes_made = True
        
        # 2. تحسين دالة تحليل المرفقات
        if "_parse_attachments" in content:
            parse_att_pattern = r'def _parse_attachments\(self\):(.*?)(?=def|\Z)'
            parse_att_match = re.search(parse_att_pattern, content, re.DOTALL)
            
            if parse_att_match:
                old_parse_att = parse_att_match.group(0)
                
                # تحسين دالة تحليل المرفقات
                new_parse_att = """def _parse_attachments(self):
        \"\"\"تحليل المرفقات من بيانات الحالة\"\"\"
        self.attachment_files = []
        
        # التأكد من وجود المرفقات في بيانات الحالة
        if 'attachments' in self.case_data and self.case_data['attachments']:
            attachments_data = self.case_data['attachments']
            print(f"Attachments data: {attachments_data}")
            
            if attachments_data:
                # تقسيم المرفقات المفصولة بفواصل
                self.attachment_files = attachments_data.split(',')
                print(f"Parsed {len(self.attachment_files)} attachments")
            else:
                print("No attachments data found")
        else:
            print("No attachments key in case data")
        
        # التأكد من أن كل الملفات صالحة وموجودة
        valid_files = []
        for file_path in self.attachment_files:
            file_path = file_path.strip()
            if file_path and os.path.exists(file_path):
                valid_files.append(file_path)
            else:
                print(f"Warning: Attachment file does not exist: {file_path}")
        
        self.attachment_files = valid_files
        
        """
                
                content = content.replace(old_parse_att, new_parse_att)
                changes_made = True
        
        # 3. تحسين دالة إضافة قسم المرفقات
        if "_add_attachments_section" in content:
            add_att_pattern = r'def _add_attachments_section\(self\):(.*?)(?=def|\Z)'
            add_att_match = re.search(add_att_pattern, content, re.DOTALL)
            
            if add_att_match:
                old_add_att = add_att_match.group(0)
                
                # تحسين دالة إضافة قسم المرفقات لتعمل بشكل صحيح
                new_add_att = """def _add_attachments_section(self):
        \"\"\"إضافة قسم المرفقات إلى واجهة التفاصيل\"\"\"
        from app.ui.attachments_manager import AttachmentsManager
        
        # العثور على قسم المرفقات إذا كان موجودًا
        attachments_group = None
        for group in self.findChildren(QGroupBox):
            if group.title() == "المرفقات":
                attachments_group = group
                break
        
        if attachments_group:
            # مسح المحتوى السابق
            layout = attachments_group.layout()
            if layout:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
            else:
                layout = QVBoxLayout(attachments_group)
                attachments_group.setLayout(layout)
            
            # إضافة أدوات إدارة المرفقات
            AttachmentsManager.create_attachments_widget(
                self, self.table_name, self.case_id, self.case_data, layout
            )
        else:
            print("Warning: Could not find attachments section in the dialog")
        
        """
                
                content = content.replace(old_add_att, new_add_att)
                changes_made = True
        
        # 4. التأكد من استدعاء تحديث المرفقات عند فتح وضع التعديل 
        if "_edit_case" in content:
            edit_case_pattern = r'def _edit_case\(self\):(.*?)\s+(?=def|\Z)'
            edit_case_match = re.search(edit_case_pattern, content, re.DOTALL)
            
            if edit_case_match:
                old_edit_case = edit_case_match.group(0)
                
                # إضافة استدعاء لتحديث المرفقات في وضع التعديل إذا لم يكن موجودًا
                if "self._add_attachments_section()" not in old_edit_case:
                    new_edit_case = old_edit_case.replace("def _edit_case(self):", """def _edit_case(self):
        \"\"\"فتح وضع تعديل الحالة\"\"\"
        # تحديث قسم المرفقات لضمان عملها في وضع التعديل
        self._add_attachments_section()
        """)
                    
                    content = content.replace(old_edit_case, new_edit_case)
                    changes_made = True
        
        if changes_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("تم تحسين ملف case_detail.py لإظهار المرفقات بشكل صحيح")
    except Exception as e:
        print(f"Error fixing case detail file: {e}")

def fix_civilian_wounded_notes():
    """إصلاح حجم الملاحظات في شاشة عرض الجريح المدني"""
    # 1. البحث عن ملف واجهة التفاصيل
    file_path = 'app/ui/case_detail.py'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = False
    
    # 2. إصلاح مشكلة حجم الملاحظات الكبير
    notes_pattern = r'(\s+)if key == "notes":(.*?)(?=\n\s+el)'
    notes_match = re.search(notes_pattern, content, re.DOTALL)
    
    if notes_match:
        indent = notes_match.group(1)
        old_notes_code = notes_match.group(0)
        
        # تعديل على كود عرض الملاحظات للتأكد من توحيد الحجم لجميع الحالات
        new_notes_code = f"{indent}if key == \"notes\":{indent}    # توحيد حجم حقل الملاحظات لجميع الحالات\n{indent}    value_widget = QTextEdit()\n{indent}    value_widget.setMaximumHeight(100)  # تحديد الحد الأقصى للارتفاع\n{indent}    value_widget.setReadOnly(not self.edit_mode)\n{indent}    value_widget.setText(value if value else \"\")"
        
        content = content.replace(old_notes_code, new_notes_code)
        changes_made = True
    
    # 3. إصلاح حجم حقل الملاحظات المختلف بين أنواع الحالات
    create_forms_pattern = r'def _create_form_fields\(self\):(.*?)(?=def|\Z)'
    create_forms_match = re.search(create_forms_pattern, content, re.DOTALL)
    
    if create_forms_match:
        old_create_forms = create_forms_match.group(0)
        
        # تأكد من أن جميع نوافذ التفاصيل تستخدم نفس طريقة عرض للملاحظات
        if "civilian_wounded" in old_create_forms and "notes" in old_create_forms:
            # إضافة شرط خاص لتوحيد حجم حقل الملاحظات
            new_notes_section = """
        # توحيد حجم الملاحظات بين جميع أنواع الحالات
        for key in self.case_data:
            if key == "notes":
                # إضافة حقل الملاحظات بحجم موحد
                notes_label = QLabel("الملاحظات:")
                notes_edit = QTextEdit()
                notes_edit.setMaximumHeight(100)  # توحيد الارتفاع للملاحظات
                notes_edit.setPlaceholderText("أدخل ملاحظات إضافية هنا...")
                notes_edit.setText(self.case_data.get("notes", ""))
                notes_edit.setReadOnly(not self.edit_mode)
                
                # إضافة إلى التخطيط
                notes_group = QGroupBox("ملاحظات")
                notes_layout = QVBoxLayout()
                notes_layout.addWidget(notes_edit)
                notes_group.setLayout(notes_layout)
                
                self.main_layout.addWidget(notes_group)
                self.field_widgets["notes"] = notes_edit
                break
        """
            
            # إضافة القسم الجديد للملاحظات قبل قسم المرفقات
            if "self._add_attachments_section()" in old_create_forms:
                new_create_forms = old_create_forms.replace("        self._add_attachments_section()", f"{new_notes_section}\n        self._add_attachments_section()")
                content = content.replace(old_create_forms, new_create_forms)
                changes_made = True
    
    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("تم إصلاح مشكلة حجم الملاحظات في شاشة الجريح المدني")

if __name__ == "__main__":
    fix_attachments_and_notes() 