from import_export import resources
from core.models import Subject

class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject
        import_id_fields = ['code']  # Use 'code' as the unique identifier
        fields = ('name', 'code', 'dept', 'semester', 'mcourse', 'ecourse', 'oecourse')  # Define fields to include
