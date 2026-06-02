from student_crud import StudentCRUD

crud = StudentCRUD()

crud.update_student(

    student_id="1000",

    weekly_self_study_hours=20,

    attendance_percentage=98,

    class_participation=10,

    total_score=99,

    grade="A"
)
