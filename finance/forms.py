from django import forms
from .models import Fee, Payment, Scholarship

class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['name', 'amount', 'semester', 'description', 'due_date', 'is_active']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'fee', 'amount_paid', 'payment_method', 'transaction_id', 'receipt_number', 'notes']
        
    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        fee = cleaned_data.get('fee')
        amount_paid = cleaned_data.get('amount_paid')
        
        if student and fee and amount_paid:
            # Check if the payment amount exceeds the fee amount
            if amount_paid > fee.amount:
                raise forms.ValidationError("Payment amount cannot exceed the fee amount.")
            
            # Check if the fee is applicable for the student's current semester
            current_semester = student.studentacademicinfo_set.first().current_semester
            if fee.semester != current_semester:
                raise forms.ValidationError("This fee is not applicable for the student's current semester.")
        
        return cleaned_data

class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = ['name', 'student', 'amount', 'start_date', 'end_date', 'description', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
