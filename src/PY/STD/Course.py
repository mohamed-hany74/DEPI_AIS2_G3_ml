class Course   :
    _id_counter = 1
    def __init__(self ,  name):
        self.course_id = Course._id_counter
        Course._id_counter += 1
        self.name =name
        self.enrolled_students = []
    def __str__(self):
          
          return f'course id : {self.course_id}  name: {self.name}  enrolled {len(self.enrolled_students)}'


    def enroll_student (self ,  student):
        """
        Enrolls a student in the course
        """

        if  student   not in self.enrolled_students :
                   self.enrolled_students .append(student)
                   print(f" enrolled succflly: in {self.name}")
        else :      
              print(f"is enrolled in {self.name}") 

    def   remove_student(self , student) :
          """
            Removes a student from the course.
            
          """
          if student in self.enrolled_students :
                self.enrolled_students.remove(student)
                print(f"Student removed from{self.name} ")
          else :
                print (f"Student is enrolled in {self.name}")      
                      