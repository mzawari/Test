with open('app/ui/attachments_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. تقليل حجم الهوامش للمرفقات
old_margins = """attachments_layout.setContentsMargins(15, 15, 15, 15)"""
new_margins = """attachments_layout.setContentsMargins(10, 10, 10, 10)"""

# 2. تقليل حجم أيقونات المرفقات
old_icon_size = """file_button.setIconSize(QSize(40, 40))"""
new_icon_size = """file_button.setIconSize(QSize(32, 32))"""

# 3. تحسين أسلوب زر إضافة الملفات
old_button_style = """
            background-color: #4CAF50;
            color: white;
            padding: 6px 12px;
            font-size: 10pt;
            border-radius: 4px;
        """

new_button_style = """
            background-color: #4CAF50;
            color: white;
            padding: 5px 10px;
            font-size: 9pt;
            border-radius: 3px;
        """

# 4. تحسين أسلوب زر عرض المرفقات 
old_view_button_style = """
            background-color: #2196F3;
            color: white;
            padding: 6px 12px;
            font-size: 10pt;
            border-radius: 4px;
        """

new_view_button_style = """
            background-color: #2196F3;
            color: white;
            padding: 5px 10px;
            font-size: 9pt;
            border-radius: 3px;
        """

# استبدال النصوص في الملف
new_content = content.replace(old_margins, new_margins)
new_content = new_content.replace(old_icon_size, new_icon_size)
new_content = new_content.replace(old_button_style, new_button_style)
new_content = new_content.replace(old_view_button_style, new_view_button_style)

# حفظ التغييرات
with open('app/ui/attachments_manager.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("تم تحسين واجهة المرفقات وتصغير حجمها") 