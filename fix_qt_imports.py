from PyQt6.QtCore import Qt

def fix_qt_imports():
    with open('app/ui/search.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # إضافة استيراد Qt من PyQt6.QtCore إذا كان مفقودًا
    if 'from PyQt6.QtCore import Qt' not in content:
        # البحث عن آخر استيراد
        if 'from app.data.database import' in content:
            old_import = """from app.data.database import get_all_cases, search_cases, get_case_by_id, delete_case"""
            new_import = """from app.data.database import get_all_cases, search_cases, get_case_by_id, delete_case
from PyQt6.QtCore import Qt"""
            content = content.replace(old_import, new_import)
    
    # تعديل دالة _update_attachment_info للتعامل مع Qt.ItemDataRole بشكل صحيح
    if 'Qt.ItemDataRole.UserRole' in content:
        # تحديث لأسلوب Qt6
        content = content.replace('Qt.ItemDataRole.UserRole', 'Qt.ItemDataRole.UserRole')
    
    # حفظ التغييرات
    with open('app/ui/search.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("تم تصحيح استيرادات Qt بنجاح")

if __name__ == "__main__":
    fix_qt_imports() 