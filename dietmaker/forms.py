from django import forms
from .models import MealPlan, Patient, Appointments


# Food form
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = '__all__'
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'Appointment_description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 8, 'cols': 100, 'placeholder': 'Appointment Description', }),
        }


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Name'}),
            'phone': forms.TextInput(attrs={'type': 'tel', 'placeholder': "Enter Phone Number"}),

            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),

            'occupation': forms.TextInput(attrs={'placeholder': 'Enter Occupation'}),
            'address': forms.Textarea(attrs={'rows': 5, 'cols': 100, 'placeholder': 'Enter Address'}),
            'age': forms.TextInput(attrs={'type': 'number', 'placeholder': '18'}),
            'sex': forms.Select(choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))),
            'marital_status': forms.Select(choices=(
                ('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed'))
            ),

            'height': forms.TextInput(attrs={'type': 'number', 'placeholder': 'Enter height in cm'}),
            'weight': forms.TextInput(attrs={'type': 'number', 'placeholder': 'Enter weight in kg'}),
            'blood_group': forms.Select(choices=(
                ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'),
                ('O-', 'O-'))
            ),

            'purpose': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter Purpose'}),
            'medical_issue': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter Medical Issue(if any?)'}),
            'medicine': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter Medicine(if any?)'}),
            'supplement': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter Supplement(if any?)'}),

            'family_history': forms.Textarea(
                attrs={'rows': 5, 'cols': 100, 'placeholder': 'Enter Family History(if any?)'}),

            'wake_up_time': forms.TimeInput(format='%H:%M', attrs={'placeholder': 'HH:MM(24 hrs)', }),
            'sleep_time': forms.TimeInput(format='%H:%M', attrs={'placeholder': 'HH:MM(24 hrs)'}),
            'noon_nap': forms.TimeInput(format='%H:%M', attrs={'placeholder': 'HH:MM(24 hrs)'}),

            'food_preferences': forms.Textarea(
                attrs={'placeholder': 'Veg or Non-Veg or Egg or Chicken or Vegan or Jain or Sea Food or Other',
                       'rows': 5}),
            'food_taste': forms.Textarea(
                attrs={'placeholder': 'Spicy or Sweet or Salty or Bitter or Sour or Purgent or Other', 'rows': 5}),
            'food_allergy': forms.Textarea(attrs={'placeholder': 'Enter Food Allergy(if any?)', 'rows': 5}),

            'water_glasses': forms.TextInput(attrs={'type': 'number', 'placeholder': 'Enter number of glasses'}),
            'water_quantity': forms.TextInput(attrs={'type': 'number', 'placeholder': 'Enter quantity in Litres'}),

            'beverages': forms.Textarea(attrs={'placeholder': 'Tea or Coffee or Milk(if any?)', 'rows': 5}),

            'eat_outside_food': forms.Textarea(attrs={'placeholder': 'Yes or No(if yes how often?)', 'rows': 5}),
            'consume_fruits_daily': forms.Textarea(
                attrs={'placeholder': 'Yes or No(if yes how much?What type?)', 'rows': 5}),

            'diabetes': forms.CheckboxInput(),
            'thyroid': forms.CheckboxInput(),
            'pcos': forms.CheckboxInput(),
            'hypertension': forms.CheckboxInput(),
            'heart_disease': forms.CheckboxInput(),
            'constipation': forms.CheckboxInput(),
            'diarrhea': forms.CheckboxInput(),
            'acidity': forms.CheckboxInput(),
            'headache': forms.CheckboxInput(),
            'body_pain': forms.CheckboxInput(),
            'regular_periods': forms.CheckboxInput(),
            'irregular_period_details': forms.Textarea(
                attrs={'placeholder': 'Enter details about irregular periods(if any?)', 'rows': 5}),
            'has_children': forms.CheckboxInput(),
            'delivery_type': forms.Textarea(attrs={'placeholder': 'Normal or C-Section or Other', 'rows': 5}),
            'oil_or_ghee_brand': forms.Textarea(attrs={'placeholder': 'Yes or No(if yes which brand?)', 'rows': 5}),
            'salt_used': forms.Textarea(attrs={'placeholder': 'Enter Salt Used', 'rows': 5}),
            'rice_used': forms.Textarea(attrs={'placeholder': 'Enter Rice Used', 'rows': 5}),
            'flour_used': forms.Textarea(attrs={'placeholder': 'Enter Flour Used', 'rows': 5}),
            'milk_used': forms.Textarea(attrs={'placeholder': 'Enter Milk Used', 'rows': 5}),
            'sugar_used': forms.Textarea(attrs={'type': 'number', 'placeholder': 'Enter Sugar Used ', 'rows': 5}),

        }


class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Name'}),
            'short_description': forms.Textarea(
                attrs={'rows': 5, 'cols': 100, 'placeholder': 'Enter Short Description'}),
        }
