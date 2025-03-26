with open('app/ui/attachments_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# تعديل دالة create_attachments_widget لإضافة اسم مميز لصندوق المرفقات
old_code = """        # Create group box
        attachments_group = QGroupBox("المرفقات")"""

new_code = """        # Create group box
        attachments_group = QGroupBox("المرفقات")
        attachments_group.setObjectName("attachments_group")"""

new_content = content.replace(old_code, new_code)

with open('app/ui/attachments_manager.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("تم إضافة اسم مميز لصندوق المرفقات بنجاح") 