import json
import csv
import boto3


class ExportData:

    def __init__(self):

        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name="ap-south-1"
        )

        self.table = self.dynamodb.Table(
            "student_performance"
        )

        self.s3 = boto3.client(
            "s3",
            region_name="ap-south-1"
        )

        self.bucket_name = (
            "student-performance-datasets-ayush"
        )

    # -----------------------------
    # Get All Students
    # -----------------------------

    def get_all_students(self):

        response = self.table.scan()

        return response["Items"]

    # -----------------------------
    # Export JSON
    # -----------------------------

    def export_json(self):

        students = self.get_all_students()

        file_name = (
            "students_export.json"
        )

        with open(
            file_name,
            "w"
        ) as file:

            json.dump(
                students,
                file,
                indent=4,
                default=str
            )

        print(
            f"{file_name} created"
        )

        return file_name

    # -----------------------------
    # Export CSV
    # -----------------------------

    def export_csv(self):

        students = self.get_all_students()

        if not students:

            print(
                "No records found"
            )

            return None

        file_name = (
            "students_export.csv"
        )

        with open(
            file_name,
            "w",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=
                students[0].keys()
            )

            writer.writeheader()

            writer.writerows(
                students
            )

        print(
            f"{file_name} created"
        )

        return file_name

    # -----------------------------
    # Upload to S3
    # -----------------------------

    def upload_to_s3(
        self,
        file_name
    ):

        self.s3.upload_file(

            file_name,

            self.bucket_name,

            f"exports/{file_name}"
        )

        print(
            f"{file_name} uploaded to S3"
        )


if __name__ == "__main__":

    exporter = ExportData()

    while True:

        print("\n")
        print("=" * 50)
        print("EXPORT MENU")
        print("=" * 50)

        print("1. Export JSON")
        print("2. Export CSV")
        print("3. Exit")

        choice = input(
            "\nEnter Choice: "
        )

        if choice == "1":

            file_name = (
                exporter.export_json()
            )

            exporter.upload_to_s3(
                file_name
            )

        elif choice == "2":

            file_name = (
                exporter.export_csv()
            )

            exporter.upload_to_s3(
                file_name
            )

        elif choice == "3":

            break

        else:

            print(
                "Invalid Choice"
            )