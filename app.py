from flask import Flask
import csv
from flask import render_template
from flask import request
import matplotlib.pyplot as plt

# Function to read the CSV data
def read_csv(filename):
    data = []
    with open(filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data

data=read_csv("data.csv")

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

# Function to scrape out student data
def sd(v):
    student_data = []
    for entry in data:
        if int(entry['Student id']) == v:
            student_data.append(entry)
    return student_data

# Function to scrape out course data
def cd(v):
    course_data = []
    for entry in data:
        if int(entry[' Course id']) == v:
            course_data.append(entry)
    return course_data    

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "GET":
        return render_template("index.html")
    else:
        id_type = request.form.get('ID')
        if id_type == "student_id":
            v = int(request.form['id_value'])
            if sd(v) == []:
                return render_template("wrong_inputs.html")
            else:
                statistics = {'Total Marks': calculate_total_marks(sd(v))}
                return render_template("student_details.html", stats=statistics, student=sd(v))
        elif id_type == "course_id":
            v = int(request.form['id_value'])
            if cd(v) == []:
                return render_template("wrong_inputs.html")
            else:
                marks = [int(entry[' Marks']) for entry in cd(v)]
                plt.clf()
                plt.hist(marks, bins=10, alpha=0.5)
                plt.xlabel("Marks")
                plt.ylabel("Frequency")
                plt.savefig("static/histogram.png")
                statistics = calculate_course_statistics(cd(v))
                return render_template("course_details.html", stats=statistics, course=cd(v), hsource='static/histogram.png')
        else:
            return render_template("wrong_inputs.html")
            
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
	

	
