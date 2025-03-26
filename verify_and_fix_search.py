import re

def verify_and_fix_search():
    with open('app/ui/search.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = False
    
    # 1. التحقق من استيراد Qt من PyQt6.QtCore
    if 'from PyQt6.QtCore import Qt' not in content:
        if 'from app.data.database import' in content:
            old_import = """from app.data.database import get_all_cases, search_cases, get_case_by_id, delete_case"""
            new_import = """from app.data.database import get_all_cases, search_cases, get_case_by_id, delete_case
from PyQt6.QtCore import Qt"""
            content = content.replace(old_import, new_import)
            changes_made = True
    
    # 2. تصحيح مشكلة في استدعاء Qt.ItemDataRole
    # في PyQt6، استدعاء الصحيح هو Qt.UserRole أو Qt.ItemDataRole.UserRole 
    # حسب إصدار PyQt6 المستخدم
    if 'table_name = id_item.data(Qt.ItemDataRole.UserRole)' in content:
        content = content.replace('table_name = id_item.data(Qt.ItemDataRole.UserRole)', 
                                 'table_name = id_item.data(Qt.UserRole)')
        changes_made = True
    
    # 3. التأكد من إضافة الاستيراد اللازم لدالة get_case_by_id في دالة _update_attachment_info
    if '_update_attachment_info' in content and 'get_case_by_id' in content:
        if 'from app.data.database import get_all_cases, search_cases, delete_case' in content:
            old_import = """from app.data.database import get_all_cases, search_cases, delete_case"""
            new_import = """from app.data.database import get_all_cases, search_cases, get_case_by_id, delete_case"""
            content = content.replace(old_import, new_import)
            changes_made = True
    
    # 4. تحسين دالة _ensure_attachments_visible لتعمل بشكل أفضل
    if '_ensure_attachments_visible' in content:
        old_func = r'def _ensure_attachments_visible\(self, detail_dialog\):(.*?)def'
        new_func = """def _ensure_attachments_visible(self, detail_dialog):
        \"\"\"التأكد من ظهور المرفقات في نافذة التفاصيل\"\"\"
        try:
            # التأكد من وجود المرفقات في قاعدة البيانات
            if hasattr(detail_dialog, 'case_id') and hasattr(detail_dialog, 'table_name'):
                case_id = detail_dialog.case_id
                table_name = detail_dialog.table_name
                
                # جلب معلومات الحالة الكاملة من قاعدة البيانات
                case = get_case_by_id(table_name, case_id)
                
                if case and 'attachments' in case and case['attachments']:
                    print(f"Case has attachments: {case['attachments']}")
                    
                    # استدعاء طريقة إعادة تحميل المرفقات
                    if hasattr(detail_dialog, '_add_attachments_section'):
                        detail_dialog._add_attachments_section()
                        
                    # تحديث الواجهة
                    QApplication.processEvents()
        except Exception as e:
            print(f"Error ensuring attachments visibility: {e}")
    
    def"""
        
        # استخدام التعبير النمطي للعثور على الدالة واستبدالها
        pattern = re.compile(old_func, re.DOTALL)
        match = pattern.search(content)
        if match:
            new_content = pattern.sub(new_func, content)
            if new_content != content:
                content = new_content
                changes_made = True
    
    # 5. تحسين دالة _update_attachment_info للتعامل مع أخطاء Qt.UserRole
    if '_update_attachment_info' in content:
        old_func = r'def _update_attachment_info\(self, row=-1\):(.*?)def'
        new_func = """def _update_attachment_info(self, row=-1):
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
        
        # الحصول على اسم الجدول المخزن في خاصية UserRole
        try:
            # استخدام Qt.UserRole بدلاً من Qt.ItemDataRole.UserRole لتوافق أفضل
            table_name = id_item.data(Qt.UserRole)
            
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
        except Exception as e:
            print(f"Error updating attachment info: {e}")
            self.attachments_info.setText("المرفقات: خطأ في العرض")
            self.attachments_info.setStyleSheet("color: #f44336; font-weight: bold;")
    
    def"""
        
        # استخدام التعبير النمطي للعثور على الدالة واستبدالها
        pattern = re.compile(old_func, re.DOTALL)
        match = pattern.search(content)
        if match:
            new_content = pattern.sub(new_func, content)
            if new_content != content:
                content = new_content
                changes_made = True
    
    # حفظ التغييرات إذا تم إجراء أي تعديلات
    if changes_made:
        with open('app/ui/search.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("تم تصحيح وتحسين شاشة البحث بنجاح")
    else:
        print("لم يتم العثور على مشاكل تحتاج للتصحيح")

if __name__ == "__main__":
    verify_and_fix_search() 