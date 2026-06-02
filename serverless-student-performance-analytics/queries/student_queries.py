import boto3
from boto3.dynamodb.conditions import Attr, Key


class StudentQueries:

    def __init__(self):

        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name="ap-south-1"
        )

        self.table = self.dynamodb.Table(
            "student_performance"
        )

    # -----------------------------------
    # Query 1
    # attendance_percentage > 90
    # -----------------------------------

    def attendance_above_90(self):

        response = self.table.scan(
            FilterExpression=Attr(
                "attendance_percentage"
            ).gt(90)
        )

        students = response["Items"]

        print(
            f"\nStudents with attendance > 90: "
            f"{len(students)}\n"
        )

        for student in students:
            print(student)

        return students

    # -----------------------------------
    # Query 2
    # weekly_self_study_hours > 10
    # -----------------------------------

    def study_hours_above_10(self):

        response = self.table.scan(
            FilterExpression=Attr(
                "weekly_self_study_hours"
            ).gt(10)
        )

        students = response["Items"]

        print(
            f"\nStudents with study hours > 10: "
            f"{len(students)}\n"
        )

        for student in students:
            print(student)

        return students

    # -----------------------------------
    # Query 3
    # Excellent Students
    # -----------------------------------

    def excellent_students(self):

        response = self.table.scan(
            FilterExpression=Attr(
                "performance_category"
            ).eq("Excellent")
        )

        students = response["Items"]

        print(
            f"\nExcellent Students: "
            f"{len(students)}\n"
        )

        for student in students:
            print(student)

        return students

    # -----------------------------------
    # Part 7
    # Top Students in Grade A
    # Uses GSI:
    # grade-score-index
    # -----------------------------------

    def top_students_grade_a(self):

        response = self.table.query(

            IndexName="grade-score-index",

            KeyConditionExpression=
            Key("grade").eq("A"),

            ScanIndexForward=False,

            Limit=10
        )

        students = response["Items"]

        print("\nTop Grade A Students\n")

        for student in students:
            print(student)

        return students

    # -----------------------------------
    # Part 7
    # Highest Scoring Students
    # -----------------------------------

    def highest_scores(self):

        response = self.table.scan()

        students = response["Items"]

        students.sort(
            key=lambda x: float(x["total_score"]),
            reverse=True
        )

        top_students = students[:10]

        print("\nHighest Scoring Students\n")

        for student in top_students:
            print(student)

        return top_students


    # -----------------------------------
    # Advanced Task
    # Top 10 Students Leaderboard
    # -----------------------------------

    def leaderboard(self):

        response = self.table.scan()

        students = response["Items"]

        students.sort(
            key=lambda x: float(
                x["total_score"]
            ),
            reverse=True
        )

        leaderboard = students[:10]

        print("\nTOP 10 STUDENTS\n")

        rank = 1

        for student in leaderboard:

            print(
                f"{rank}. "
                f"Student ID: "
                f"{student['student_id']} "
                f"Score: "
                f"{student['total_score']}"
            )

            rank += 1

        return leaderboard
   

# -----------------------------------
# Main Menu
# -----------------------------------

if __name__ == "__main__":

    query = StudentQueries()

    while True:

        print("\n")
        print("=" * 50)
        print("STUDENT PERFORMANCE QUERY MENU")
        print("=" * 50)

        print("1. Attendance > 90")
        print("2. Study Hours > 10")
        print("3. Excellent Students")
        print("4. Top Grade A Students")
        print("5. Highest Scoring Students")
        print("6. Leaderboard")
        print("7. Exit")

        choice = input("\nEnter Choice: ")

        if choice == "1":

            query.attendance_above_90()

        elif choice == "2":

            query.study_hours_above_10()

        elif choice == "3":

            query.excellent_students()

        elif choice == "4":

            query.top_students_grade_a()

        elif choice == "5":

            query.highest_scores()

        elif choice == "6":

            query.leaderboard()

        elif choice == "7":

            print("Exiting...")
            break

        else:

            print("Invalid Choice")
