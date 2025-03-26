with open('app/ui/case_detail.py', 'r', encoding='utf-8') as f:
    content = f.read()

# تعديل دالة _add_attachment لإزالة إعادة تحميل النافذة واستخدام طريقة أفضل للتحديث
old_code = """                # إعادة تحميل النافذة لتحديث العرض
                    print("Refreshing dialog to show updated attachments")
                    self.close()
                    from app.ui.case_detail import CaseDetailDialog
                    refreshed_dialog = CaseDetailDialog(self.parent(), self.table_name, self.case_data)
                    refreshed_dialog.showMaximized()"""

new_code = """                    # تحديث البيانات المحلية لعرض المرفق الجديد
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

new_content = content.replace(old_code, new_code)

with open('app/ui/case_detail.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("تم تعديل طريقة تحديث المرفقات بنجاح") 