with open('app/ui/case_detail.py', 'r', encoding='utf-8') as f:
    content = f.read()

# تعديل دالة _add_notes_section لإظهار الملاحظات حتى لو كانت فارغة
old_code = """    def _add_notes_section(self, parent_layout, row, col=0):
        \"\"\"Adds a notes section to the layout if notes exist\"\"\"
        if not self.case_data.get('notes'):
            return None
            
        notes_group = QGroupBox("ملاحظات")"""

new_code = """    def _add_notes_section(self, parent_layout, row, col=0):
        \"\"\"Adds a notes section to the layout\"\"\"
        # إظهار قسم الملاحظات حتى لو كانت فارغة
        notes_group = QGroupBox("ملاحظات")"""

new_content = content.replace(old_code, new_code)

with open('app/ui/case_detail.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("تم تعديل دالة عرض الملاحظات بنجاح") 