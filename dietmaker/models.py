from django.db import models
from django.core.validators import RegexValidator


class Food(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    calories = models.PositiveIntegerField(verbose_name='Calories (Kcals)')

    def __str__(self):
        return self.name


class MealPlan(models.Model):
    name = models.CharField(max_length=100)
    foods = models.ManyToManyField(Food, through='MealPlanFood')
    short_description = models.TextField(default='', verbose_name="Short Description", blank=True, null=True)

    def __str__(self):
        return self.name


class Patient(models.Model):
    # patient_id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, default='', null=True, blank=True,
                             validators=[RegexValidator(r'^\d{1,10}$')])
    email = models.EmailField(max_length=100, default='', null=True, blank=True)
    occupation = models.CharField(max_length=100, default='', null=True, blank=True)
    address = models.TextField(default='', null=True, blank=True)
    age = models.PositiveIntegerField(default=0)
    sex = models.CharField(max_length=10, default='other')
    marital_status = models.CharField(max_length=20, default='single')
    weight = models.DecimalField(max_digits=5, decimal_places=2, default='', null=True, blank=True,
                                 verbose_name="Weight (kg)")
    height = models.DecimalField(max_digits=5, decimal_places=2, default='', null=True, blank=True,
                                 verbose_name="Height (cm)")
    blood_group = models.CharField(max_length=5, default='', null=True, blank=True, verbose_name="Blood Group")

    purpose = models.TextField(default='', null=True, blank=True)
    medical_issue = models.TextField(default='', null=True, blank=True)
    medicine = models.TextField(default='', null=True, blank=True)
    supplement = models.TextField(default='', null=True, blank=True)

    wake_up_time = models.TimeField(null=True, blank=True)
    sleep_time = models.TimeField(null=True, blank=True)
    noon_nap = models.TimeField(null=True, blank=True)

    family_history = models.TextField(default='', null=True, blank=True)

    food_preferences = models.TextField(max_length=100, default='', null=True, blank=True)
    veg = models.BooleanField(default=False)
    non_veg = models.BooleanField(default=False)
    food_taste = models.TextField(max_length=100, default='', null=True, blank=True)

    food_allergy = models.TextField(default='', null=True, blank=True)

    water_glasses = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="Glasses of water")
    water_quantity = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, blank=True,
                                         verbose_name="Water Quantity (L)")

    beverages = models.TextField(default='', null=True, blank=True, verbose_name="Beverages")

    eat_outside_food = models.TextField(default='')
    consume_fruits_daily = models.TextField(default='', null=True, blank=True)

    diabetes = models.BooleanField(default=False)
    thyroid = models.BooleanField(default=False)
    pcos = models.BooleanField(default=False)
    hypertension = models.BooleanField(default=False)
    heart_disease = models.BooleanField(default=False)
    constipation = models.BooleanField(default=False)
    diarrhea = models.BooleanField(default=False)

    acidity = models.BooleanField(default=False, null=True, blank=True)
    headache = models.BooleanField(default=False, null=True, blank=True)
    body_pain = models.BooleanField(default=False, null=True, blank=True)
    regular_periods = models.BooleanField(default=False, null=True, blank=False)
    irregular_period_details = models.TextField(default='', null=True, blank=True)

    has_children = models.BooleanField(default=False, null=True, blank=True)
    number_of_children = models.IntegerField(default=0, null=True, blank=True)
    delivery_type = models.TextField(default='', null=True, blank=True)

    oil_or_ghee_brand = models.TextField(default='', null=True, blank=True)
    salt_used = models.TextField(default='', null=True, blank=True)
    rice_used = models.TextField(default='', null=True, blank=True)
    flour_used = models.TextField(default='', null=True, blank=True)
    milk_used = models.TextField(default='', null=True, blank=True)
    sugar_used = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, blank=True)

    # add photo for patients
    def __str__(self):
        return self.name


class BodyComposition(models.Model):
    Patient_name = models.CharField(max_length=100, default='', verbose_name="Patient Name")
    height = models.FloatField(verbose_name="Height (m)")
    weight = models.FloatField(verbose_name="Weight (kg)")
    body_fat = models.FloatField(verbose_name="Body Fat (%)")
    age = models.PositiveIntegerField(verbose_name="Age")
    BMI = models.FloatField(verbose_name="Body Mass Index")
    RMR = models.FloatField(verbose_name="Resting Metabolic Rate (kcal/day)")
    visceral_fat = models.PositiveIntegerField(verbose_name="Visceral Fat")

    def __str__(self):
        if self.appointments.exists():
            appointment_date = self.appointments.first().date_assigned.strftime('%Y-%m-%d')
            return f"Body Composition - {self.Patient_name} ({appointment_date})"
        else:
            return f"Body Composition - {self.Patient_name}"


class Appointments(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, blank=True, null=True,
                                  related_name='appointments')
    date_assigned = models.DateTimeField()
    body_composition = models.ForeignKey(BodyComposition, on_delete=models.SET_NULL, blank=True, null=True,
                                         related_name='appointments')
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    Appointment_description = models.TextField(default='', verbose_name="Appointment Description", blank=True,
                                               null=True)
    gym_time = models.TimeField(auto_now=False, auto_now_add=False, default='00:00:00')
    sleep_time = models.TimeField(auto_now=False, auto_now_add=False, default='00:00:00')
    wake_up_time = models.TimeField(auto_now=False, auto_now_add=False, default='00:00:00')

    def __str__(self):
        if self.meal_plan:
            return f'{self.patient.name} - {self.meal_plan.name}'
        elif self.status == 'cancelled':
            return f'{self.patient.name} - {self.status}'
        else:
            return f'{self.patient.name}'


class MealPlanFood(models.Model):
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, default='default', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    TIMING_CHOICES = (
        ('after_bed', 'After Bed'),
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snacks', 'Snacks'),
        ('dinner', 'Dinner'),
        ('before_bed', 'Before Bed'),
        ('pre_workout', 'Pre-Workout'),
        ('post_workout', 'Post-Workout'),
    )
    timing = models.CharField(max_length=20, choices=TIMING_CHOICES, verbose_name="Timing", default='')
    time = models.TimeField(auto_now=False, auto_now_add=False, default='00:00:00')
