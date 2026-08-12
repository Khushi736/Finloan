from django.contrib import admin
from django import forms
from .models import *

# 1. Create a custom form for the LoanCategory
class LoanCategoryForm(forms.ModelForm):

    # Documents Field
    documents_required = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Enter required documents separated by commas (e.g., PAN, Bank Statement)",
        required=False
    )

    # Features Field
    features = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Enter features separated by commas (e.g., Quick Approval, No Hidden Fees)",
        required=False
    )

    # Eligibility Field
    eligibility = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Enter eligibility criteria separated by commas (e.g., Salaried, Age 21+)",
        required=False
    )

    class Meta:
        model = LoanCategory
        fields = '__all__'

    # =========================
    # SHOW CLEAN VALUES IN ADMIN
    # =========================

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Documents
        if self.instance and self.instance.documents_required:
            self.initial['documents_required'] = ", ".join(
                self.instance.documents_required
            )

        # Features
        if self.instance and self.instance.features:
            self.initial['features'] = ", ".join(
                self.instance.features
            )

        # Eligibility
        if self.instance and self.instance.eligibility:

            eligibility = self.instance.eligibility

            if isinstance(eligibility, dict):

                conditions = eligibility.get('conditions', [])

                self.initial['eligibility'] = ", ".join(conditions)

    # =========================
    # SAVE CLEAN JSON
    # =========================

    def clean_documents_required(self):
        data = self.cleaned_data.get('documents_required')

        if isinstance(data, str) and data.strip():

            return [
                item.strip()
                for item in data.split(',')
                if item.strip()
            ]

        return []

    def clean_features(self):
        data = self.cleaned_data.get('features')

        if isinstance(data, str) and data.strip():

            return [
                item.strip()
                for item in data.split(',')
                if item.strip()
            ]

        return []

    def clean_eligibility(self):
        data = self.cleaned_data.get('eligibility')

        if isinstance(data, str) and data.strip():

            conditions = [
                item.strip()
                for item in data.split(',')
                if item.strip()
            ]

            return {
                "conditions": conditions
            }

        return {}


# 3. Attach the custom form to the LoanCategory Admin
class LoanCategoryAdmin(admin.ModelAdmin):
    form = LoanCategoryForm
    list_display = (
        'name',
        'interest_rate',
        'min_amount',
        'max_amount',
        'is_active'
    )
    search_fields = ('name',)


# Register your models
admin.site.register(Signup)
admin.site.register(UserProfile)
admin.site.register(LoanCategory, LoanCategoryAdmin)
admin.site.register(KYCRecord)
admin.site.register(LoanApplication)
admin.site.register(LoanRecommendation)
admin.site.register(EMISchedule)
admin.site.register(Notification)