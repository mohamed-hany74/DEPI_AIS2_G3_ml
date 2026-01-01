class Student:
    """Represents a student with courses and grades"""

    _id_counter = 1

    def __init__(self, name):
        """Create a new student with a unique ID and name"""
        if not name:
            raise ValueError("Name cannot be empty")

        self.student_id = Student._id_counter
        Student._id_counter += 1
        self.name = name
        self.grades = {}
        self.enrolled_courses = []

    def __str__(self):
        """Return student information as a readable string"""
        return f"Student ID : {self.student_id}, Name : {self.name}, Grades: {self.grades}"

    def __repr__(self):
        """Return student representation for debugging"""
        return f"Student ID : {self.student_id}, Name : {self.name}, Grades: {self.grades}"

    def add_grade(self, course_id, grade):
        """Add or update the grade for a specific course"""
        if not 0 <= grade <= 100:
            raise ValueError("grades must be between 0 and 100")
        self.grades[course_id] = grade

    def enroll_in_course(self, course):
        """Enroll the student in a course if not already enrolled"""
        if course in self.enrolled_courses:
            print(f"{self.name} is already enrolled in {course}")
        else:
            self.enrolled_courses.append(course)
