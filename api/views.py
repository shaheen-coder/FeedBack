from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from core.models import FeedBack,Staff,Subject,ClassStaff
#rest 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
# other pkg 
import pandas as pd 

'''
api view for analysis staff class subject
'''
# staff and subject 

class Analysis(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        data = request.data 
        if data['type'] == 'class':
            feedback_entries = FeedBack.objects.filter(student__semester=data['id']).only('feed')
        elif data['type'] == 'staff_sub':
            feedback_entries = FeedBack.objects.filter(staffd=data['id']).only('feed')
        elif data['type'] == 'staff' :
            feedback_entries = FeedBack.objects.filter(staffd__staff=data['id']).only('feed')
        else :
            return Response({'error':'needs to specify type'})
        feedback_list = [entry.feed for entry in feedback_entries]
        feedback_flattened = []
        for feedback in feedback_list:
            for key, value in feedback.items():
                feedback_flattened.extend(value)  
        df = pd.DataFrame(feedback_flattened)
        category_averages = df.mean(axis=0).apply(float).to_dict()  
        counts = {score: int((df == score).sum().sum()) for score in [5, 3, 1]}  
        
        total_feedback_items = df.size  
        percentages = {score: round((count / total_feedback_items) * 100, 2) for score, count in counts.items()}
        
        max_possible_score = df.shape[0] * 5  
        category_percentages = (df.sum(axis=0) / max_possible_score * 100).apply(float).to_dict()
        
        return Response({
            "category_averages": category_averages,
            "counts": counts,
            "percentages": percentages,
            "category_percentages": category_percentages,
            "terms" : ["Aids Utilization","Clarity","Confidence","Pacing","Discipline","Engagement","Accessibility",
                        "Punctuality",
                        "Guidance",
                        "Feedback"
                    ],
        })    

'''
report api view for class category student wise 
'''

# class report of category wise 

class Report(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        data = request.data
        if data["type"] == 'class':
            feedback_entries = FeedBack.objects.filter(staffd__section=data['key']).only('feed')
        elif data["type"] == 'staff':
            feedback_entries = FeedBack.objects.filter(staffd__staff=data['key']).only('feed')
        elif data["type"] == 'student':
            feedback_entries = FeedBack.objects.filter(student=data['key']).only('feed')
        feedback_list = [entry.feed for entry in feedback_entries]
        feedback_flattened = []
        for feedback in feedback_list:
            for key, value in feedback.items():
                feedback_flattened.extend(value)
        df = pd.DataFrame(feedback_flattened)
        counts = {score: int((df == score).sum().sum()) for score in [5, 3, 1]}
        category_columns = [f'cat_{i}' for i in range(1, 11)]
        # Calculate percentages for 5s, 3s, and 1s for each category
        percentages = {}
        for col in category_columns:
            percentages[col] = {
                "percentage_5s": round((df[col].value_counts().get(5, 0) / len(df)) * 100, 2),
                "percentage_3s": round((df[col].value_counts().get(3, 0) / len(df)) * 100, 2),
                "percentage_1s": round((df[col].value_counts().get(1, 0) / len(df)) * 100, 2),
                "average": round(df[col].mean(), 2),
            }
        percentages["count"] = counts
        return Response({"data": percentages})


class Student(APIView):
    def get(self, request):
        # Fetch all feedback records
        data = request.data
        feedbacks = FeedBack.objects.filter(student__id=data['id'])
        if not feedbacks.exists():
            return Response({"detail": "No feedback data available"}, status=status.HTTP_404_NOT_FOUND)
        
        subject_feedback = {}

        for feedback in feedbacks:
            subject_name = feedback.staffd.subject.code  
            if subject_name not in subject_feedback:
                subject_feedback[subject_name] = []
            for category, values in feedback.feed.items():
                subject_feedback[subject_name].extend(values)

        subject_results = {}
        all_scores = []  

        for subject_name, feedback_list in subject_feedback.items():
            scores = []
            for feedback in feedback_list:
                scores.extend(feedback.values())
            
            score_series = pd.Series(scores)
            total_responses = len(score_series)
            if total_responses == 0:
                subject_results[subject_name] = [{"5s": 0, "3s": 0, "1s": 0, "avg": 0}]
            else:
                subject_results[subject_name] = [{
                    "5s": (score_series.value_counts().get(5, 0) / total_responses) * 100,
                    "3s": (score_series.value_counts().get(3, 0) / total_responses) * 100,
                    "1s": (score_series.value_counts().get(1, 0) / total_responses) * 100,
                    "avg": score_series.mean(),
                }]
            
            all_scores.extend(scores)


        all_score_series = pd.Series(all_scores)
        total_all_responses = len(all_score_series)

        if total_all_responses == 0:
            subject_results["overall"] = [{"5s": 0, "3s": 0, "1s": 0, "avg": 0}]
        else:
            subject_results["overall"] = [{
                "5s": (all_score_series.value_counts().get(5, 0) / total_all_responses) * 100,
                "3s": (all_score_series.value_counts().get(3, 0) / total_all_responses) * 100,
                "1s": (all_score_series.value_counts().get(1, 0) / total_all_responses) * 100,
                "avg": all_score_series.mean(),
            }]
        
        return Response(subject_results, status=status.HTTP_200_OK)

class Department(APIView):
    def get(self, request):
        # Fetch all feedback records
        feedbacks = FeedBack.objects.filter(staffd__dept='CSE')
        if not feedbacks.exists():
            return Response({"detail": "No feedback data available"}, status=status.HTTP_404_NOT_FOUND)
        
        subject_feedback = {}

        for feedback in feedbacks:
            subject_name = feedback.staffd.staff.name 
            if subject_name not in subject_feedback:
                subject_feedback[subject_name] = []
            for category, values in feedback.feed.items():
                subject_feedback[subject_name].extend(values)

        subject_results = {}
        all_scores = []  

        for subject_name, feedback_list in subject_feedback.items():
            scores = []
            for feedback in feedback_list:
                scores.extend(feedback.values())
            
            score_series = pd.Series(scores)
            total_responses = len(score_series)
            if total_responses == 0:
                subject_results[subject_name] = [{"5s": 0, "3s": 0, "1s": 0, "avg": 0}]
            else:
                subject_results[subject_name] = [{
                    "5s": (score_series.value_counts().get(5, 0) / total_responses) * 100,
                    "3s": (score_series.value_counts().get(3, 0) / total_responses) * 100,
                    "1s": (score_series.value_counts().get(1, 0) / total_responses) * 100,
                    "avg": score_series.mean(),
                }]
            
            all_scores.extend(scores)


        all_score_series = pd.Series(all_scores)
        total_all_responses = len(all_score_series)

        if total_all_responses == 0:
            subject_results["overall"] = [{"5s": 0, "3s": 0, "1s": 0, "avg": 0}]
        else:
            subject_results["overall"] = [{
                "5s": (all_score_series.value_counts().get(5, 0) / total_all_responses) * 100,
                "3s": (all_score_series.value_counts().get(3, 0) / total_all_responses) * 100,
                "1s": (all_score_series.value_counts().get(1, 0) / total_all_responses) * 100,
                "avg": all_score_series.mean(),
            }]
        
        return Response(subject_results, status=status.HTTP_200_OK)
