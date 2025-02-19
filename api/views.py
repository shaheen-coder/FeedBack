from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from core.models import FeedBack,Staff,Subject,ClassStaff,Student
from django.db.models import Count, FloatField, Value
from django.db.models.functions import Coalesce, Cast
from django.db.models.expressions import ExpressionWrapper
from django.db.models import Prefetch
from django.db.models import Sum
#rest 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from api.serializers import StaffSerializer,SubjectSerializer,ClassStaffSerializer,StudentSerializer
from api.serializers import FeedbackInputSerializer
# other pkg 
from collections import defaultdict
from django.db.models import Q
import pandas as pd 



FEEDBACK_TERMS = [
        "Aids Utilization", "Clarity", "Confidence", "Pacing", 
        "Discipline", "Engagement", "Accessibility", "Punctuality", 
        "Guidance", "Teaching"
    ]

'''
api view for analysis staff class subject
'''
# staff and subject 
class AnalysisCalculator:
    """Utility class for calculating analysis metrics"""
    
    @staticmethod
    def process_feedback(feed_dict):
        """Process a single feedback dictionary"""
        if not isinstance(feed_dict, dict):
            return []
        
        processed_data = []
        for cat_num, value in feed_dict.items():
            if isinstance(value, (int, float)):
                processed_data.append({
                    f'cat_{cat_num}': value
                })
        return processed_data

    @staticmethod
    def compute_metrics(data, terms):
        if not data:
            return {
                "category_averages": {},
                "counts": {},
                "percentages": {},
                "category_percentages": {},
                "terms": terms
            }

        # Initialize counters
        category_sums = defaultdict(float)
        category_counts = defaultdict(int)
        score_counts = defaultdict(int)
        total_items = 0

        # Process the data
        for item in data:
            for cat, value in item.items():
                category_sums[cat] += value
                category_counts[cat] += 1
                score_counts[value] += 1
                total_items += 1

        # Calculate metrics
        category_averages = {
            cat: round(sum_val / category_counts[cat], 2)
            for cat, sum_val in category_sums.items()
        }

        counts = {
            score: count
            for score, count in score_counts.items()
            if score in [1, 3, 5]
        }

        percentages = {
            score: round((count / total_items) * 100, 2)
            for score, count in counts.items()
        }

        category_percentages = {
            cat: round((sum_val / (category_counts[cat] * 5)) * 100, 2)
            for cat, sum_val in category_sums.items()
        }

        return {
            "category_averages": category_averages,
            "counts": counts,
            "percentages": percentages,
            "category_percentages": category_percentages,
            "terms": terms
        }

class Analysis(APIView):
    """API for analysis of class, staff with subject and staff"""
    permission_classes = [permissions.AllowAny]
    
    FEEDBACK_TERMS = [
        "Aids Utilization", "Clarity", "Confidence", "Pacing", 
        "Discipline", "Engagement", "Accessibility", "Punctuality", 
        "Guidance", "Teaching"
    ]

    def post(self, request):
        data = request.data
        
        filter_conditions = {
            'class': Q(student__semester=data['key'], student__dept=data['dept'],status=True),
            'staff_sub': Q(staffd=data['key'],status=True),
            'staff': Q(staffd__staff=data['key'],status=True),
            'status' : True,
        }
        
        if data['mode'] not in filter_conditions:
            return Response({'error': 'Invalid type specified'}, status=400)
        
        feedback_entries = FeedBack.objects.filter(
            filter_conditions[data['mode']]
        ).only('feed1', 'feed2')
        
        if not feedback_entries.exists():
            return Response(AnalysisCalculator.compute_metrics([], self.FEEDBACK_TERMS))
        
        calculator = AnalysisCalculator()
        processed_data = []
        
        for entry in feedback_entries:
            # Process feed1
            if entry.feed1:
                processed_data.extend(calculator.process_feedback(entry.feed1))
            
            # Process feed2
            if entry.feed2:
                processed_data.extend(calculator.process_feedback(entry.feed2))

        return Response(calculator.compute_metrics(processed_data, self.FEEDBACK_TERMS))


class DeptAnalysisCalculator:
    """Utility class for calculating analysis metrics"""
    
    @staticmethod
    def process_feedback(feed_dict):
        """Process a single feedback dictionary"""
        if not isinstance(feed_dict, dict):
            return []
        
        processed_data = []
        for cat_num, value in feed_dict.items():
            if isinstance(value, (int, float)):
                processed_data.append({
                    f'cat_{cat_num}': value
                })
        return processed_data

    @staticmethod
    def compute_metrics(data, terms):
        if not data:
            return {
                "category_averages": {},
                "counts": {},
                "percentages": {},
                "category_percentages": {},
                "terms": terms
            }

        # Initialize counters
        category_sums = defaultdict(float)
        category_counts = defaultdict(int)
        score_counts = defaultdict(int)
        total_items = 0

        # Process the data
        for item in data:
            for cat, value in item.items():
                if cat != 'dept':  # Skip the dept field
                    category_sums[cat] += value
                    category_counts[cat] += 1
                    score_counts[value] += 1
                    total_items += 1

        # Calculate metrics
        category_averages = {
            cat: round(sum_val / category_counts[cat], 2)
            for cat, sum_val in category_sums.items()
        }

        counts = {
            score: count
            for score, count in score_counts.items()
            if score in [1, 3, 5]
        }

        percentages = {
            score: round((count / total_items) * 100, 2)
            for score, count in counts.items()
        }

        category_percentages = {
            cat: round((sum_val / (category_counts[cat] * 5)) * 100, 2)
            for cat, sum_val in category_sums.items()
        }

        return {
            "category_averages": category_averages,
            "counts": counts,
            "percentages": percentages,
            "category_percentages": category_percentages,
            "terms": terms
        }



class DepartmentAnalysis(APIView):
    FEEDBACK_TERMS = [
        "Aids Utilization", "Clarity", "Confidence", "Pacing", 
        "Discipline", "Engagement", "Accessibility", "Punctuality", 
        "Guidance", "Feedback"
    ]

    def get(self, request):
        # Simplified query to avoid select_related/only conflicts
        feedbacks = FeedBack.objects.select_related(
            'staffd'
        ).all()
        
        if not feedbacks.exists():
            return Response({"message": "No feedback data available"}, status=200)
        
        calculator = DeptAnalysisCalculator()
        dept_data = defaultdict(list)
        
        for feedback in feedbacks:
            try:
                dept = feedback.staffd.dept
                
                # Process feed1
                if feedback.feed1:
                    processed_feed1 = calculator.process_feedback(feedback.feed1)
                    for item in processed_feed1:
                        item['dept'] = dept
                        dept_data[dept].append(item)
                
                # Process feed2
                if feedback.feed2:
                    processed_feed2 = calculator.process_feedback(feedback.feed2)
                    for item in processed_feed2:
                        item['dept'] = dept
                        dept_data[dept].append(item)
                        
            except AttributeError as e:
                print(f"Error processing feedback {feedback.id}: {str(e)}")
                continue
        
        results = {}
        for dept, data in dept_data.items():
            if data:  # Only process departments with data
                results[dept] = calculator.compute_metrics(data, self.FEEDBACK_TERMS)
        
        if not results:
            return Response({"message": "No valid feedback data found"}, status=200)
            
        return Response(results)

'''
report api view for class category student wise 
'''

# class report of category wise 
class Report(APIView):
    """API for report generation based on class, staff, staff with subject, and student"""
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def _process_feedback_dict(feed_dict):
        """Process a single feedback dictionary and extract values"""
        if not isinstance(feed_dict, dict):
            return []
        return list(feed_dict.values())

    @staticmethod
    def _compute_metrics(data):
        """Compute percentage metrics for a series of values"""
        total = len(data)
        if total == 0:
            return {
                "percentage_5s": 0,
                "percentage_3s": 0,
                "percentage_1s": 0,
                "average": 0
            }
        
        counts = defaultdict(int)
        sum_values = 0
        
        for value in data:
            counts[value] += 1
            sum_values += value
            
        return {
            "percentage_5s": round((counts[5] / total) * 100, 2),
            "percentage_3s": round((counts[3] / total) * 100, 2),
            "percentage_1s": round((counts[1] / total) * 100, 2),
            "average": round(sum_values / total, 2)
        }

    def post(self, request):
        data = request.data
        
        # Convert key to int if it's for staff or student
        key = int(data['key']) if data['mode'] in ['staff', 'stu'] else data['key']
        
        # Define filter conditions
        filter_conditions = {
            'class': Q(staffd__subject__semester=data['sem'], 
                      staffd__section=key, 
                      staffd__dept=data['dept'],status=True),
            'staff': Q(staffd__staff_id=key, 
                      staffd__dept=data['dept'],status=True),
            'staffsub': Q(staffd_id=key,status=True),
            'stu': Q(student_id=key, 
                    staffd__dept=data['dept'],status=True),
            'status' : True,
        }

        # Validate report type
        if data['mode'] not in filter_conditions:
            return Response(
                {"error": "Invalid report type"},
                status=400
            )

        # Fetch feedback entries
        feedback_entries = FeedBack.objects.filter(
            filter_conditions[data['mode']]
        ).only('feed1', 'feed2')

        if not feedback_entries.exists():
            return Response({"data": {}, 'error': 'No feedback found'})

        # Process feedback data
        category_data = defaultdict(list)
        
        for entry in feedback_entries:
            # Process feed1
            if entry.feed1:
                for cat, value in entry.feed1.items():
                    if isinstance(value, (int, float)):
                        category_data[cat].append(value)
            
            # Process feed2 if it exists
            if entry.feed2:
                for cat, value in entry.feed2.items():
                    if isinstance(value, (int, float)):
                        category_data[cat].append(value)

        # Check if we have any valid data
        if not category_data:
            return Response({"data": {}, 'error': 'No valid category columns found'})

        # Compute metrics for each category
        percentages = {
            category: self._compute_metrics(values)
            for category, values in category_data.items()
        }

        # Compute overall metrics
        all_values = [val for values in category_data.values() for val in values]
        percentages["overall"] = self._compute_metrics(all_values)

        return Response({"data": percentages,'terms':FEEDBACK_TERMS})


class FeedbackMetricsCalculator:
    """Utility class for calculating feedback metrics"""
    
    @staticmethod
    def compute_metrics(scores):
        """Compute percentage metrics for a series of values"""
        if not scores:
            return {
                "5s": 0,
                "3s": 0,
                "1s": 0,
                "avg": 0
            }
        
        total = len(scores)
        counts = defaultdict(int)
        total_sum = 0
        
        for score in scores:
            counts[score] += 1
            total_sum += score
            
        return {
            "5s": round((counts[5] / total) * 100, 2),
            "3s": round((counts[3] / total) * 100, 2),
            "1s": round((counts[1] / total) * 100, 2),
            "avg": round(total_sum / total, 2)
        }

    @staticmethod
    def process_feedback(feed_dict):
        """Process a single feedback dictionary"""
        if not isinstance(feed_dict, dict):
            return []
        return [val for val in feed_dict.values() if isinstance(val, (int, float))]

class StudentReport(APIView):
    def post(self, request):
        data = request.data
        feedbacks = FeedBack.objects.filter(student_id=data['id'],status=True)
        
        if not feedbacks.exists():
            return Response(
                {"detail": "No feedback data available"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        calculator = FeedbackMetricsCalculator()
        subject_feedback = defaultdict(list)
        
        for feedback in feedbacks:
            subject_code = feedback.staffd.subject.code
            
            # Process feed1
            if feedback.feed1:
                subject_feedback[subject_code].extend(
                    calculator.process_feedback(feedback.feed1)
                )
            
            # Process feed2
            if feedback.feed2:
                subject_feedback[subject_code].extend(
                    calculator.process_feedback(feedback.feed2)
                )
        
        # Calculate metrics for each subject
        subject_results = {}
        all_scores = []
        
        for subject_code, scores in subject_feedback.items():
            metrics = calculator.compute_metrics(scores)
            subject_results[subject_code] = [metrics]
            all_scores.extend(scores)
        
        # Calculate overall metrics
        subject_results["overall"] = [calculator.compute_metrics(all_scores)]
        
        return Response(subject_results, status=status.HTTP_200_OK)

class Department(APIView):
    def post(self, request):
        data = request.data
        feedbacks = FeedBack.objects.filter(staffd__dept=data['dept'],status=True)
        
        if not feedbacks.exists():
            return Response(
                {"detail": "No feedback data available"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        calculator = FeedbackMetricsCalculator()
        staff_feedback = defaultdict(list)
        
        for feedback in feedbacks:
            staff_name = feedback.staffd.staff.name
            
            # Process feed1
            if feedback.feed1:
                staff_feedback[staff_name].extend(
                    calculator.process_feedback(feedback.feed1)
                )
            
            # Process feed2
            if feedback.feed2:
                staff_feedback[staff_name].extend(
                    calculator.process_feedback(feedback.feed2)
                )
        
        # Calculate metrics for each staff member
        staff_results = {}
        all_scores = []
        
        for staff_name, scores in staff_feedback.items():
            metrics = calculator.compute_metrics(scores)
            staff_results[staff_name] = [metrics]
            all_scores.extend(scores)
        
        # Calculate overall metrics
        staff_results["overall"] = [calculator.compute_metrics(all_scores)]
        
        return Response(staff_results, status=status.HTTP_200_OK)

class Instruction(APIView):
    def get(self, request):
        feedbacks = FeedBack.objects.select_related('staffd').all()
        
        if not feedbacks.exists():
            return Response(
                {"detail": "No feedback data available"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        calculator = FeedbackMetricsCalculator()
        dept_feedback = defaultdict(list)
        
        for feedback in feedbacks:
            dept_name = feedback.staffd.dept
            
            # Process feed1
            if feedback.feed1:
                dept_feedback[dept_name].extend(
                    calculator.process_feedback(feedback.feed1)
                )
            
            # Process feed2
            if feedback.feed2:
                dept_feedback[dept_name].extend(
                    calculator.process_feedback(feedback.feed2)
                )
        
        # Calculate metrics for each department
        dept_results = {}
        all_scores = []
        
        for dept_name, scores in dept_feedback.items():
            metrics = calculator.compute_metrics(scores)
            dept_results[dept_name] = [metrics]
            all_scores.extend(scores)
        
        # Calculate overall metrics
        dept_results["overall"] = [calculator.compute_metrics(all_scores)]
        
        return Response(dept_results, status=status.HTTP_200_OK)

class UniversalSearchAPIView(APIView):
    """
    API view to provide a universal search across Staff, Subject, and ClassStaff models.
    Supports multiple search parameters in POST request.
    """
    def get_year(self,year):
        years = {
            1 : (1,2),
            2 : (3,4),
            3 : (5,6),
            4 : (7,8),
        }
        return years.get(year)
    def post(self, request):
        """
        Search method supporting multiple parameters:
        - name: Search by name (partial match)
        - dept* : Filter by department
        - gender: Filter by gender (1 for male, 0 for female)
        - subject_code: Search by subject code
        - section: Filter by section
        - semester: Filter by semester
        - course_type: Filter by course type (mcourse, ecourse, oecourse)
        """
        # Extract POST data
        data = request.data
        name = data.get('name', None)
        dept = data.get('dept', None)
        gender = data.get('gender', None)
        subject_code = data.get('subject_code', None)
        section = data.get('section', None)
        semester = data.get('semester', None)
        course_type = data.get('course_type', None)
        mode = data.get('mode', None)

        # Determine semesters for the given year
        # Results dictionary
        results = {}

        # Apply filters based on the mode
        if mode == 'staff':
            # Filter Staff model
            staff_queryset = Staff.objects.all()
            if name:
                staff_queryset = staff_queryset.filter(name__icontains=name)
            if dept:
                staff_queryset = staff_queryset.filter(dept=dept)
            if gender:
                staff_queryset = staff_queryset.filter(gender=int(gender))
            results['datas'] = StaffSerializer(staff_queryset, many=True).data

        elif mode == 'sub':
            # Filter Subject model
            subject_queryset = Subject.objects.all()
            if subject_code:
                subject_queryset = subject_queryset.filter(code__icontains=subject_code)
            if dept:
                subject_queryset = subject_queryset.filter(dept=dept)
            if semester:
                subject_queryset = subject_queryset.filter(semester=semester)
            if course_type:
                course_type_filters = {
                    "mcourse": Q(mcourse=True),
                    "ecourse": Q(ecourse=True),
                    "oecourse": Q(oecourse=True)
                }
                if course_type in course_type_filters:
                    subject_queryset = subject_queryset.filter(course_type_filters[course_type])
            results['datas'] = SubjectSerializer(subject_queryset, many=True).data

        elif mode == 'staffsub':
            # Filter ClassStaff model
            class_staff_queryset = ClassStaff.objects.all()
            if section:
                class_staff_queryset = class_staff_queryset.filter(section__iexact=section)
            if dept:
                class_staff_queryset = class_staff_queryset.filter(dept=dept)
            if semester:
                class_staff_queryset = class_staff_queryset.filter(semester=semester)
            if subject_code:
                class_staff_queryset = class_staff_queryset.filter(subject__code__icontains=subject_code)
            results['datas'] = ClassStaffSerializer(class_staff_queryset, many=True).data

        else:
            # Invalid mode
            results['error'] = "Invalid mode specified."

        return Response(results)


class StudentSearch(APIView):
    def post(self,request):
        name = request.data.get('name',None)
        dept = request.data.get('dept',None)
        sec = request.data.get('section',None)
        sem = request.data.get('sem',None)
        students = Student.objects.filter(dept=dept,status=True)
        if not dept: return Response({'error':'department field is must !! '},status=status.HTTP_400_BAD_REQUEST)
        if sem: students = students.filter(semester=sem)
        if sec: students = students.filter(section=sec)
        if name : students = students.filter(name__icontains=name)
        datas = {}
        datas['student'] = StudentSerializer(students,many=True).data
        return Response(datas,status=status.HTTP_200_OK)

class ClassSerchApi(APIView):
    def post(self,request):
        dept = request.data.get('dept',None)
        section = request.data.get('sec',None)
        sem = request.data.get('sem',None)
        if not dept : return Response({'error':'department field missing'},status=status.HTTP_400_BAD_REQUEST)
        queryset = ClassStaff.objects.filter(dept=dept)
        if sem:
            queryset = queryset.filter(semester=sem)
        else :
            sem = queryset[0].semester
        a = True if queryset.filter(section='A').exists() else False
        b = True if queryset.filter(section='B').exists() else False
        return Response({'dept':dept,'sem':sem,'A':a,'B':b})


class FeedSearch(APIView):
    def get(self,request,id,cid,subid):
        student = Student.objects.get(id=id)
        if subid != 'null':
            datas = ClassStaff.objects.get(dept=student.dept,subject=subid,section=student.section,semester=student.semester)
            datas = ClassStaffSerializer(datas).data
            return Response({'data':datas})
        else :
            print(f'student : {student} and course id : {cid}')
            mcourse = True if cid == 1 else False 
            ecourse =  True if cid == 2 else False 
            oecourse =  True if cid == 3 else False 
            staffs = ClassStaff.objects.filter(dept=student.dept,semester=student.semester,section=student.section,subject__mcourse=mcourse,subject__ecourse=ecourse,subject__oecourse=oecourse)
            print(f'datas : {staffs}')
            datas = ClassStaffSerializer(staffs,many=True).data
            return Response({'data':datas})


class FeedBackApi(APIView):
    def post(self, request):
        serializer = FeedbackInputSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Feedback successfully created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentApi(APIView):
    def get(self, request, sid):
        try:
            feedbacks = FeedBack.objects.filter(student_id=sid)

            if not feedbacks:
                return Response({"message": "No feedback found for this student."}, status=status.HTTP_404_NOT_FOUND)

            # Prepare the data in the desired format
            feedback_data = []
            for feedback in feedbacks:
                subject_name = feedback.staffd.subject.name #Access the subject name
                subject_code = feedback.staffd.subject.code #Access the subject code

                feedback_data.append({
                    "msg": feedback.msg,
                    "subject_name": subject_name,
                    "subject_code": subject_code,
                })

            return Response(feedback_data, status=status.HTTP_200_OK)

        except FeedBack.DoesNotExist:
            return Response({"message": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e: # Catch other potential errors
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
