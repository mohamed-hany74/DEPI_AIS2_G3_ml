from student import Student

class Course:
    """Represents a course that students can enroll in"""

    _id_counter = 1

    def __init__(self, name):
        """Create a new course with a unique ID and name"""
        self.course_id = Course._id_counter
        Course._id_counter += 1
        self.name = name
        self.enrolled_students = []

    def __str__(self):
        """Return course information as a string"""
        return f"course ID : {self.course_id}, Name : {self.name}, Enrolled: {len(self.enrolled_students)}"

    def __repr__(self):
        """Return course representation for debugging"""
        return f"course ID : {self.course_id}, Name : {self.name}, Enrolled: {len(self.enrolled_students)}"

    def enroll_student(self, student):
        """Add a student to the course if not already enrolled"""
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)
            print(f"student enrolled successfully in {self.name}")
        else:
            print(f"student is already enrolled in {self.name}")

    def remove_student(self, student):
        """Remove a student from the course if enrolled"""
        if student in self.enrolled_students:
            self.enrolled_students.remove(student)
            print(f"student removed from {self.name}")
        else:
            print(f"student is not enrolled in {self.name}")
