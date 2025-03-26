"""
سكربت لإصلاح مشكلة حجم حقل الملاحظات في شاشة الجريح المدني
"""
import re
from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QGroupBox, QLabel

def fix_notes_field():
    """إصلاح مشكلة حجم حقل الملاحظات"""
    file_path = 'app/ui/case_detail.py'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. تعديل معالجة حقل الملاحظات في الدالة الرئيسية
        if 'def _create_form_fields' in content:
            # البحث عن جزء معالجة الملاحظات
            notes_pattern = r'(\s+)if key == ["\']notes["\']:(.*?)(?=\s+(?:el|if|#|def|"""))'
            notes_match = re.search(notes_pattern, content, re.DOTALL)
            
            if notes_match:
                indent = notes_match.group(1)
                old_notes_code = notes_match.group(0)
                
                # استبدال الكود القديم بكود جديد يتحكم في حجم حقل الملاحظات
                new_notes_code = f"""        # إنشاء مجموعة الملاحظات بحجم ثابت
        notes_group = QGroupBox("ملاحظات")
        notes_layout = QVBoxLayout()
        
        # إنشاء حقل الملاحظات بحجم محدد
        notes_edit = QTextEdit()
        notes_edit.setMaximumHeight(80)  # تحديد الارتفاع الأقصى
        notes_edit.setMinimumHeight(60)   # تحديد الارتفاع الأدنى
        notes_edit.setPlaceholderText("أدخل ملاحظات إضافية هنا...")
        notes_edit.setText(self.case_data.get('notes', ''))
        notes_edit.setReadOnly(not self.edit_mode)
        
        # إضافة حقل الملاحظات إلى المجموعة
        notes_layout.addWidget(notes_edit)
        notes_group.setLayout(notes_layout)
        
        # إضافة مجموعة الملاحظات إلى التخطيط الرئيسي
        self.main_layout.addWidget(notes_group)
        self.field_widgets['notes'] = notes_edit"""
                
                # استبدال الكود القديم بالجديد
                content = content.replace(old_notes_code, new_notes_code)
        
        # 2. التأكد من أن حقل الملاحظات يظهر في نفس المكان لجميع أنواع الحالات
        form_fields_pattern = r'def _create_form_fields\(self\):(.*?)(?=def|\Z)'
        form_fields_match = re.search(form_fields_pattern, content, re.DOTALL)
        
        if form_fields_match:
            old_form_fields = form_fields_match.group(0)
            
            # إضافة معالجة موحدة لحقل الملاحظات
            if 'notes_group = QGroupBox("ملاحظات")' not in old_form_fields:
                # إضافة كود معالجة الملاحظات قبل قسم المرفقات
                new_form_fields = old_form_fields.replace(
                    'self._add_attachments_section()',
                    new_notes_code + '\n        self._add_attachments_section()'
                )
                content = content.replace(old_form_fields, new_form_fields)
        
        # حفظ التغييرات
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("تم إصلاح مشكلة حجم حقل الملاحظات بنجاح")
        
    except Exception as e:
        print(f"حدث خطأ أثناء إصلاح حجم حقل الملاحظات: {e}")

if __name__ == "__main__":
    fix_notes_field() 