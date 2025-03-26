with open('app/ui/case_detail.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the problematic line with the correct method
new_content = content.replace(
    "delete_button.clicked.connect(self._handle_delete_button_click)",
    "delete_button.clicked.connect(self._delete_case)"
)

with open('app/ui/case_detail.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Delete button handler fixed successfully") 