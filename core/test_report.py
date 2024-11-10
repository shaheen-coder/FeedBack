from django.db.models import Avg, Count
from core.models import FeedBack
from collections import defaultdict
def calculate_feedback_analysis():
    feedbacks = FeedBack.objects.filter(staff_id=3,subject__subject_code='CS3391')
    
    # Initialize dictionaries to hold calculated data
    avg_scores = defaultdict(float)
    percentage_scores = defaultdict(float)
    score_distribution = defaultdict(lambda: {"5": 0, "3": 0, "1": 0})

    # Count of feedback entries to calculate averages
    feedback_count = feedbacks.count()
    if feedback_count == 0:
        return {}  # Return empty if no feedbacks are available
    
    # Iterate through feedbacks to accumulate category-wise scores
    for feedback in feedbacks:
        for category, score in feedback.categories.items():
            avg_scores[category] += score
            
            # Calculate count for each score type
            if score == 5:
                score_distribution[category]["5"] += 1
            elif score == 3:
                score_distribution[category]["3"] += 1
            elif score == 1:
                score_distribution[category]["1"] += 1

    # Calculate averages and percentages
    analysis_result = {}
    for category, total_score in avg_scores.items():
        # Average score for each category
        avg_score = total_score / feedback_count
        analysis_result[category] = {
            "average": avg_score,
            "percentage": (total_score / (feedback_count * 5)) * 100,  # Assuming 5 is the max score
            "percentage_of_5": (score_distribution[category]["5"] / feedback_count) * 100,
            "percentage_of_3": (score_distribution[category]["3"] / feedback_count) * 100,
            "percentage_of_1": (score_distribution[category]["1"] / feedback_count) * 100,
        }

    return analysis_result
print(calculate_feedback_analysis())