import random
from django.utils.text import slugify
from core.models import Staff, Subject, ClassStaff

# List of department codes (first element of the DEPT tuple)
depts = ['CSE', 'IT', 'EEE', 'ICE', 'ECE', 'MECH', 'CIVIL']

for dept in depts:
    # -------------------------------
    # Task 1: Create 5 Staff for each dept
    # -------------------------------
    staff_objs = []
    for i in range(1, 6):
        name = f"Staff_{dept}_{i}"
        # Randomly choose gender: 1 for male, 0 for female
        gender = random.choice([1, 0])
        staff = Staff.objects.create(name=name, dept=dept, gender=gender)
        staff_objs.append(staff)

    # -------------------------------
    # Task 2: Create Subjects for each dept & semester
    # -------------------------------
    # We will create subjects for semesters 1 through 8.
    # For semesters 1-4: create 3 normal subjects.
    # For semesters 4-8: create 3 normal subjects plus 3 course subjects (one each for mcourse, ecourse, oecourse).
    for sem in range(1, 9):
        # Create the 3 normal subjects
        for sub_num in range(1, 4):
            # Generate a unique code (for example: first two letters of dept, semester, counter, and 'N' for normal)
            subject_code = f"{dept[:2].upper()}{sem}0{sub_num}N"
            subject_name = f"{dept} Semester {sem} Subject {sub_num}"
            Subject.objects.create(
                name=subject_name,
                code=subject_code,
                dept=dept,
                semester=sem,
                mcourse=False,
                ecourse=False,
                oecourse=False
            )
        # For semesters 4-8 add course subjects
        if sem >= 4:
            # Define a mapping for course types and a short letter for code generation.
            course_types = {
                'mcourse': 'M',
                'ecourse': 'E',
                'oecourse': 'O'
            }
            for course_field, letter in course_types.items():
                subject_code = f"{dept[:2].upper()}{sem}{letter}C"
                subject_name = f"{dept} Semester {sem} {course_field.upper()} Course"
                # Create the subject and set the corresponding flag to True.
                kwargs = {
                    'name': subject_name,
                    'code': subject_code,
                    'dept': dept,
                    'semester': sem,
                    'mcourse': False,
                    'ecourse': False,
                    'oecourse': False,
                }
                kwargs[course_field] = True
                Subject.objects.create(**kwargs)

    # -------------------------------
    # Task 3: Create ClassStaff records.
    # For every subject of this dept, choose a random staff from this dept,
    # set the section to "A" (always uppercase), and add the subject.
    # -------------------------------
    subjects = Subject.objects.filter(dept=dept)
    for subj in subjects:
        chosen_staff = random.choice(staff_objs)
        ClassStaff.objects.create(
            staff=chosen_staff,
            subject=subj,
            section='A',
            semester=subj.semester,
            dept=dept
        )
