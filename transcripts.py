import json
import pdfkit

# Load JSON data
with open('students_data_associates.json', 'r', encoding='utf-8') as file:
    students_data = json.load(file)
    
# reading and printing html template to debug
html_template = ""
with open('template.html', 'r', encoding='utf-8') as file:
    html_template = file.read()

print("HTML Template:")
print(html_template)  # Print the template to inspect its content

# options = {
#     'page-size': 'A4',
#     'encoding': 'UTF-8',
# }

# # read HTML template
# html_template = ""
# with open('template.html', 'r', encoding='utf-8') as file:
#     html_template = file.read()

# for student in students_data:
#     # Calculate total credits earned
#     total_credits_earned = sum(course['credits'] for period in student['periods'] for course in period['courses'])

#     courses_html = ""
#     for period in student['periods']:
#         courses_html += f"<h3>{period['name']}</h3><ul>"
#         for course in period['courses']:
#             courses_html += f"<li>{course['name']} - {course['grade']} ({course['credits']} credits)</li>"
#         courses_html += "</ul>"

#     student_html = html_template.format(
#         name=student['name'],
#         program=student['program'],
#         credits_earned_str=student['credits_earned'],
#         total_credits_earned_str=total_credits_earned,
#         gpa_str=student['gpa'], 
#         periods=courses_html  # Assuming 'periods' is the key in your template
#     )

#     #file path
#     pdf_file_path = f"C:\\Users\\ejibr\\miftaah_transcripts\\{student['name'].replace(' ', '_')}_transcript.pdf"

#     pdfkit.from_string(student_html, pdf_file_path, options=options)
