with open('app/ui/case_detail.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the problematic line with the correct method
new_content = content.replace(
    "self.edit_button.clicked.connect(self._handle_edit_button_click)",
    "self.edit_button.clicked.connect(self._edit_case)"
)

with open('app/ui/case_detail.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Edit button handler fixed successfully") 