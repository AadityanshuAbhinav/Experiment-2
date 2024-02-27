import sys
import csv
import matplotlib.pyplot as plt
from jinja2 import Template

# Function to read the CSV data
def read_csv(filename):
    data = []
    with open(filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data

# Function to calculate total marks
def calculate_total_marks(data):
    total_marks = 0
    for entry in data:
        total_marks += int(entry[' Marks'])
    return total_marks

# Function to calculate average and maximum marks for a course
def calculate_course_statistics(data):
    total_marks = 0
    max_marks = 0
    count = 0
    for entry in data:
        marks = int(entry[' Marks'])
        total_marks += marks
        max_marks = max(max_marks, marks)
        count += 1
    average_marks = total_marks / count
    return {'Average Marks': average_marks, 'Maximum Marks': max_marks}

# Function to generate the HTML page
def generate_html(data, statistics, is_student):
    if is_student:
        template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Student Details</title>
        </head>
        <body>
            <h1>Student Details</h1>
            <table cellspacing="3" border="0" bgcolor="#000000">
                <tr bgcolor="#ffffff">
                    <th>Student id</th>
                    <th>Course id</th>
                    <th>Marks</th>
                </tr>
                {% for row in data %}
                <tr bgcolor="#ffffff">
                    <td>{{ row['Student id'] }}</td>
                    <td>{{ row[' Course id'] }}</td>
                    <td>{{ row[' Marks'] }}</td>
                </tr>
                {% endfor %}
                <tr bgcolor="#ffffff">
                    <td colspan="2">Total Marks</td>
                    <td>{{ statistics['Total Marks'] }}</td>
                </tr>
            </table>
        </body>
        </html>
        """)
    else:
        template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Course Details</title>
        </head>
        <body>
            <h1>Course Details</h1>
            <table cellspacing="3" border="0" bgcolor="#000000">
                <tr bgcolor="#ffffff">
                    <th>Average Marks</th>
                    <th>Maximum Marks</th>
                </tr>
                <tr bgcolor="#ffffff">
                    <td>{{ statistics['Average Marks'] }}</td>
                    <td>{{ statistics['Maximum Marks'] }}</td>
                </tr>
            </table>
            <img src="histogram.png" alt="Histogram">
        </body>
        </html>
        """)

    html_content = template.render(data=data, statistics=statistics)

    with open("output.html", "w") as f:
        f.write(html_content)
        
# Function to generate error page
def generate_error_html():
    template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Assignment 3</title>
    </head>
    <body>
        <h1>Wrong Inputs</h1>
        <p>Something went wrong</p>
    </body>
    </html>
    """)

    html_content = template.render()

    with open("output.html", "w") as f:
        f.write(html_content)


# Check for correct number of command line arguments
if len(sys.argv) != 3:
    generate_error_html()
    sys.exit()

# Parse command line arguments
flag = sys.argv[1]
query_id = int(sys.argv[2])

# Read the CSV data (assuming 'data.csv' is the CSV file)
data = read_csv("data.csv")

# Initialize variables
is_student = False

if flag == "-s":
    is_student = True
    student_data = [entry for entry in data if int(entry['Student id']) == query_id]
    if not student_data:
        generate_error_html()
        sys.exit()
    statistics = {'Total Marks': calculate_total_marks(student_data)}
elif flag == "-c":
    course_data = [entry for entry in data if int(entry[' Course id']) == query_id]
    if not course_data:
        generate_error_html()
        sys.exit()
    statistics = calculate_course_statistics(course_data)
else:
	generate_error_html()
	sys.exit()

# Generate HTML page
generate_html(student_data if is_student else course_data, statistics, is_student)

# Generate histogram if it's a course inquiry
if not is_student:
    marks = [int(entry[' Marks']) for entry in course_data]
    plt.hist(marks, bins=10, alpha=0.5)
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    plt.savefig("histogram.png")
