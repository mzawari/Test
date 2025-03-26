with open('app/ui/case_detail.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Change the layout from QVBoxLayout to QGridLayout
new_content = content.replace("details_layout = QVBoxLayout(details_widget)", "details_layout = QGridLayout(details_widget)")

# Restore the vertical spacing since it's valid for QGridLayout
new_content = new_content.replace("# Vertical spacing controlled by setSpacing above", "details_layout.setVerticalSpacing(12)")

with open('app/ui/case_detail.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Layout changed to QGridLayout successfully") 