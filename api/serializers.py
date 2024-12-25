from rest_framework import serializers
from core.models import Staff, Subject, ClassStaff,Student,FeedBack

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'name', 'dept', 'gender', 'profile_pic']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'dept', 'semester', 'mcourse', 'ecourse', 'oecourse']

class ClassStaffSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = ClassStaff
        fields = ['id', 'staff', 'subject', 'section', 'dept']
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id','name','dept','section','semester'] 


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = ['student', 'staff', 'feedback', 'message']

class FeedbackInputSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    feed_count = serializers.IntegerField()
    feeds = serializers.ListField(
        child=serializers.DictField(), allow_empty=False
    )

    def create(self, validated_data):
        student_id = validated_data.get('student_id')
        feeds = validated_data.get('feeds')
        feedback_objects = []

        student_instance = Student.objects.get(id=student_id)

        for feed in feeds:
            staff_id = feed['staff_id']
            feedback_data = feed['feedback']
            message = feed['message']

            staff_instance = ClassStaff.objects.get(pk=staff_id)

            existing_feedback = FeedBack.objects.filter(
                student_id=student_id,
                staffd=staff_instance
            ).first()

            if existing_feedback:
                existing_feedback.feed2 = feedback_data
                existing_feedback.msg = message  
                existing_feedback.save()
                student_instance.feed2_status = True
            else:
                feedback_objects.append(
                    FeedBack(
                        student_id=student_id,
                        staffd=staff_instance,
                        feed1=feedback_data,
                        msg=message,
                    )
                )
                student_instance.feed1_status = True

        student_instance.save()

        return FeedBack.objects.bulk_create(feedback_objects)
