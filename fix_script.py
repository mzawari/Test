with open('app/ui/case_detail.py', 'r', encoding='utf-8') as f: content = f.read(); new_content = content.replace(\
title_text
=
f\\\{self.case_data['case_type']} - معرف {self.case_data['case_id']}\\\\, \title_text
=
f\\\{self.case_data['case_type']} - معرف {self.case_id}\\\\); with open('app/ui/case_detail.py', 'w', encoding='utf-8') as f: f.write(new_content); print('File updated successfully')
