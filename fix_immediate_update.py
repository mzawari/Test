with open('app/ui/case_detail.py', 'r', encoding='utf-8') as f:
    content = f.read()

# تحسين طريقة إعادة تحميل المرفقات بعد الإضافة
old_code = """                    # تحديث البيانات المحلية لعرض المرفق الجديد
                    print("Updating local data to show new attachment")
                    
                    # استخدام AttachmentsManager لإعادة إنشاء قسم المرفقات
                    from app.ui.attachments_manager import AttachmentsManager
                    
                    # البحث عن كافة أقسام المرفقات في النافذة
                    groups = self.findChildren(QGroupBox)
                    for group in groups:
                        if group.title() == "المرفقات":
                            # حفظ الأب والمؤشر للقسم
                            parent_layout = group.parent().layout()
                            index = parent_layout.indexOf(group)
                            
                            # حذف القسم القديم
                            group.deleteLater()
                            
                            # إنشاء قسم مرفقات جديد
                            new_group = AttachmentsManager.create_attachments_widget(
                                self, self.table_name, self.case_id, self.case_data
                            )
                            
                            # إضافة القسم الجديد إلى نفس مكان القديم
                            parent_layout.addWidget(new_group)"""

new_code = """                    # تحديث البيانات المحلية لعرض المرفق الجديد
                    print("Updating local data to show new attachment")
                    
                    # استخدام AttachmentsManager لإعادة إنشاء قسم المرفقات
                    from app.ui.attachments_manager import AttachmentsManager
                    
                    # تحديث فوري لقائمة المرفقات
                    # البحث عن مجموعة المرفقات بشكل أكثر دقة باستخدام اسم الكائن
                    attachments_group = self.findChild(QGroupBox, "attachments_group")
                    if attachments_group:
                        print("Found attachments_group, updating it")
                        # حفظ معلومات تخطيط الأب
                        parent_widget = attachments_group.parent()
                        parent_layout = parent_widget.layout()
                        if parent_layout:
                            index = parent_layout.indexOf(attachments_group)
                            
                            # حذف المجموعة القديمة
                            attachments_group.setParent(None)
                            attachments_group.deleteLater()
                            
                            # إنشاء مجموعة مرفقات جديدة
                            new_group = AttachmentsManager.create_attachments_widget(
                                self, self.table_name, self.case_id, self.case_data
                            )
                            
                            # الإضافة إلى نفس المكان في التخطيط
                            parent_layout.insertWidget(index, new_group)
                    else:
                        print("Warning: attachments_group not found, searching by title")
                        # محاولة العثور على المجموعة بالعنوان كطريقة احتياطية
                        groups = self.findChildren(QGroupBox)
                        for group in groups:
                            if group.title() == "المرفقات":
                                print("Found group by title")
                                parent_layout = group.parent().layout()
                                if parent_layout:
                                    index = parent_layout.indexOf(group)
                                    group.deleteLater()
                                    
                                    new_group = AttachmentsManager.create_attachments_widget(
                                        self, self.table_name, self.case_id, self.case_data
                                    )
                                    
                                    parent_layout.insertWidget(index, new_group)
                                    break"""

# استبدال الكود القديم بالجديد
new_content = content.replace(old_code, new_code)

# حفظ التغييرات
with open('app/ui/case_detail.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("تم تحسين طريقة التحديث الفوري للمرفقات") 