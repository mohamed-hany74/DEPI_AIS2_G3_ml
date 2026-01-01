from student import Student
from course import Course

class SystemManager:
    """Manages students and courses in the system"""

    def __init__(self):
        """Initialize the system with empty student and course records"""
        self.students = {}  
        self.courses = {}   

    def add_student(self, name):
        """Add a new student and return its ID"""
        student = Student(name)
        self.students[student.student_id] = student
        print("Student added successfully.")
        return student.student_id

    def remove_student(self, student_id):
        """Remove a student if they are not enrolled in any course"""
        if student_id in self.students:
            student = self.students[student_id]
            if not student.enrolled_courses:
                del self.students[student_id]
                print("Student removed successfully.")
            else:
                print("Student has enrolled courses. Cannot remove.")
        else:
            print("Invalid student ID.")

    def add_course(self, name):
        """Add a new course and return its ID"""
        course = Course(name)
        self.courses[course.course_id] = course
        print("Course added successfully.")
        return course.course_id

    def remove_course(self, course_id):
        """Remove a course if no students are enrolled"""
        if course_id in self.courses:
            course = self.courses[course_id]
            if not course.enrolled_students:
                del self.courses[course_id]
                print("Course removed successfully.")
            else:
                print("Course has enrolled students. Cannot remove.")
        else:
            print("Invalid course ID.")

    def enroll_course(self, student_id, course_id):
        """Enroll a student in a course if both exist and student not already enrolled"""
        if student_id in self.students and course_id in self.courses:
            student = self.students[student_id]
            course = self.courses[course_id]
            if course.name not in student.enrolled_courses:   
                student.enroll_in_course(course.name)
                course.enroll_student(student.name)
                print("Student enrolled in course successfully.")
            else:
                print("Student is already enrolled in the course.")
        else:
            print("Invalid student or course ID.")

    def search_courses(self, search_name):
        """Return a list of courses matching the search name (case-insensitive)"""
        result = []
        for course in self.courses.values():
            if search_name.lower() == course.name.lower():
                result.append(course.name)
        return result

    def record_grade(self, student_id, course_id, grade):
        """Record a grade for a student in a specific course"""
        if student_id in self.students and course_id in self.courses:
            student = self.students[student_id]
            course = self.courses[course_id]
            student.add_grade(course.name, grade)
            print("Grade recorded successfully.")
        else:
            print("Invalid student or course ID.")

    def get_all_students(self):
        """Return a list of all student objects"""
        return list(self.students.values())

    def get_all_courses(self):
        """Return a list of all course objects"""
        return list(self.courses.values())
