class Student:
    _id_counter = 1
    
    def __init__(self, name):
        if not name:
            raise ValueError("Name cannot be empty")
        self.student_id = Student._id_counter
        Student._id_counter += 1
        self.name = name
        self.grades = {}
        self.enrolled_courses = []
    
    def __str__(self):
        return f"Student ID: {self.student_id}, Name: {self.name}, Grades: {self.grades}"
    
    def __repr__(self):
        return f"Student({self.student_id}, '{self.name}')"
    
    def enroll_in_course(self, course):
        """Enrolls student in a course."""
        if course in self.enrolled_courses:
            raise ValueError(f"Already enrolled in {course}")
        self.enrolled_courses.append(course)
    
    def add_grade(self, course_id, grade):
        """
        Adds or updates a grade for a specific course.
        
        Args:
            course_id: The unique identifier of the course
            grade: The grade obtained (0-100)
        """
        if course_id not in self.enrolled_courses:
            raise ValueError(f"Not enrolled in course {course_id}")
        if not 0 <= grade <= 100:
            raise ValueError("Grade must be between 0 and 100")
        self.grades[course_id] = grade