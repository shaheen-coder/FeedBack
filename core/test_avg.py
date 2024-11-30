import pandas as pd
from django.db.models import F
from your_app.models import FeedBack, Subject

def calculate_category_statistics(subject_code):
    # Fetch all feedback entries for the subject
    feedback_entries = FeedBack.objects.filter(staffd__subject__code=subject_code).values('feed')
    
    # Convert feedback entries into a list of dictionaries
    feedback_list = [entry['feed'] for entry in feedback_entries]
    
    # Flatten the JSON structure
    feedback_flattened = []
    for feedback in feedback_list:
        for key, value in feedback.items():
            feedback_flattened.extend(value)  # Extend with list of dictionaries
    
    # Convert to Pandas DataFrame
    df = pd.DataFrame(feedback_flattened)
    
    # Calculate averages for each category
    category_averages = df.mean(axis=0).apply(float).to_dict()  # Convert to float
    
    # Count occurrences of 5, 3, and 1 for all categories
    counts = {score: int((df == score).sum().sum()) for score in [5, 3, 1]}  # Convert to int
    
    # Total number of feedback items across all categories
    total_feedback_items = df.size  # Rows * Columns
    
    # Calculate percentage of each score (5, 3, 1) across all categories
    percentages = {score: round((count / total_feedback_items) * 100, 2) for score, count in counts.items()}
    
    # Calculate percentage of each category based on max possible score
    max_possible_score = df.shape[0] * 5  # Rows * max score per category
    category_percentages = (df.sum(axis=0) / max_possible_score * 100).apply(float).to_dict()  # Convert to float
    
    return {
        "category_averages": category_averages,
        "counts": counts,
        "percentages": percentages,
        "category_percentages": category_percentages,
    }

# Example usage
subject_code = "CS101"  # Replace with your subject code
stats = calculate_category_statistics(subject_code)
print("Category Averages:", stats["category_averages"])
print("Counts of 5, 3, 1:", stats["counts"])
print("Percentages of 5, 3, 1:", stats["percentages"])
print("Category Percentages:", stats["category_percentages"])
