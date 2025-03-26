with open('app/ui/case_detail.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the problematic setVerticalSpacing line
new_content = content.replace("details_layout.setVerticalSpacing(12)", "# Vertical spacing controlled by setSpacing above")

with open('app/ui/case_detail.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Layout fixed successfully") 