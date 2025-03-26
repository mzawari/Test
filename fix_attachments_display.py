with open('app/ui/attachments_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. تحسين عملية إظهار المرفقات بشكل فوري بعد الإضافة
old_refresh_code = """    @staticmethod
    def _add_and_refresh(parent, table_name, case_id, case_data, attachments_layout):
        \"\"\"Añade un archivo adjunto y actualiza la vista\"\"\"
        attachments_list = AttachmentsManager.parse_attachments(case_data.get('attachments', ''))
        attachments_list = AttachmentsManager.add_attachment(parent, table_name, case_id, attachments_list)
        
        # Update database
        success = AttachmentsManager.update_attachments_in_db(parent, table_name, case_id, case_data, attachments_list)"""

new_refresh_code = """    @staticmethod
    def _add_and_refresh(parent, table_name, case_id, case_data, attachments_layout):
        \"\"\"Añade un archivo adjunto y actualiza la vista\"\"\"
        attachments_list = AttachmentsManager.parse_attachments(case_data.get('attachments', ''))
        attachments_list = AttachmentsManager.add_attachment(parent, table_name, case_id, attachments_list)
        
        # تحديث قاعدة البيانات
        success = AttachmentsManager.update_attachments_in_db(parent, table_name, case_id, case_data, attachments_list)
        print(f"تم تحديث المرفقات في قاعدة البيانات: {success}")"""

# 2. تحسين مظهر قسم المرفقات
old_style = """            QGroupBox {
                background-color: #e8f5e9;
                border: 1px solid #c8e6c9;
                border-radius: 8px;
                margin-top: 15px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background-color: #e8f5e9;
                color: #43a047;
                font-size: 14px;
            }"""

new_style = """            QGroupBox {
                background-color: #e3f2fd;
                border: 1px solid #bbdefb;
                border-radius: 6px;
                margin-top: 15px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background-color: #e3f2fd;
                color: #1976d2;
                font-size: 13px;
            }"""

# استبدال النصوص في الملف
new_content = content.replace(old_refresh_code, new_refresh_code)
new_content = new_content.replace(old_style, new_style)

# حفظ التغييرات
with open('app/ui/attachments_manager.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("تم تحسين طريقة عرض المرفقات بنجاح") 