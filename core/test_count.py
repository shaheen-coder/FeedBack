from django.db.models import Q
from core.models import Staff,FeedBack
def calculate_feedback_per_category(staff):
    feedbacks = FeedBack.objects.filter(staff=staff)

    category_counts = {
        'cat1': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat2': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat3': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat4': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat5': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat6': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat7': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat8': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat9': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat10': {5: 0, 4: 0, 3: 0, 2: 0},
    }

    for feedback in feedbacks:
        for cat in range(1, 11): 
            value = getattr(feedback, f'cat{cat}')
            if value in category_counts[f'cat{cat}']:
                category_counts[f'cat{cat}'][value] += 1

    return category_counts

def display_feedback_log(staff):
    # Get the category counts
    counts = calculate_feedback_per_category(staff)

    # Display the output in the requested format
    print(f'name : {staff.fname} - {staff.subject.subject_code}')  # Example staff attributes
    print(f'data : {counts}')
    #for cat in counts: print(f'data : {cat}')



staff_instance = Staff.objects.get(id=1)  # Replace with your staff instance
display_feedback_log(staff_instance)
