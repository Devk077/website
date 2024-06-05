from django.contrib import admin
from django.urls import reverse
from .models import Food, MealPlan, Patient, Appointments, MealPlanFood, BodyComposition
from .forms import AppointmentForm, PatientForm, MealPlanForm
from django.utils.html import format_html
from django.contrib import admin
from .models import BodyComposition


# BodyComposition admin
class BodyCompositionAdmin(admin.ModelAdmin):
    list_display = ('Patient_name', 'BMI', 'weight', 'height', 'body_fat', 'age', 'RMR', 'visceral_fat')


admin.site.register(BodyComposition, BodyCompositionAdmin)


# Appointment admin
class AppointmentsAdmin(admin.ModelAdmin):
    # add photo for patients
    list_display = ('patient_name', 'status', 'date_assigned', 'meal_plan_name')
    form = AppointmentForm
    change_form_template = 'admin/appointments_change_form.html'

    def appointment_actions(self, obj):
        if obj.pk:
            return format_html(
                '<a class="button" href="{}">Generate PDF</a>',
                reverse('generate_appointment_pdf', args=[obj.pk])
            )
        return '-'

    appointment_actions.short_description = 'Appointment Actions'

    def patient_name(self, obj):
        return obj.patient.name

    def meal_plan_name(self, obj):
        if obj.meal_plan:
            return obj.meal_plan.name
        else:
            return '-'


admin.site.register(Appointments, AppointmentsAdmin)


# food admin
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories')


admin.site.register(Food, FoodAdmin)


#  Patient admin

class PatientAdmin(admin.ModelAdmin):
    form = PatientForm
    list_display = ('name', 'phone', 'email', 'age', 'sex', 'weight', 'height', 'blood_group',
                    'purpose')  # list of item shown on the home page of the admin panel
    fieldsets = [
        ('Personal Information',
         {'fields': ['name', 'phone', 'email', 'occupation', 'address', 'age', 'sex', 'marital_status']}),
        ('Physical Information', {'fields': ['weight', 'height', 'blood_group']}),
        ('Medical Information', {
            'fields': (('purpose', 'medical_issue'), ('medicine', 'supplement')),
            'classes': ('wide', 'extrapretty'),
        }),
        ('Sleep Information', {
            'fields': (('wake_up_time', 'sleep_time'),
                       ('noon_nap'),),
            'classes': ('wide', 'extrapretty'),
        }),
        ('Family Information', {'fields': ['family_history']}),
        ('Food Information', {
            'fields': (
                ('veg', 'non_veg'),
                ('food_preferences', 'food_taste',), ('beverages', 'food_allergy'),
                ('water_glasses', 'water_quantity'),
                ('eat_outside_food', 'consume_fruits_daily'),
            ),
            'classes': ('wide', 'extrapretty'),
        }),
        ('Health Information', {
            'fields': (
                ('diabetes', 'thyroid', 'pcos', 'hypertension'),
                ('heart_disease', 'constipation', 'diarrhea', 'acidity'),
                ('headache', 'body_pain', 'regular_periods'),
                ('irregular_period_details',),
            ),
            'classes': ('wide', 'extrapretty'),
        }),
        ('Children Information', {'fields': ['has_children', 'number_of_children', 'delivery_type']}),
        ('food Information', {
            'fields': (('oil_or_ghee_brand', 'salt_used',), ('rice_used', 'flour_used'), ('milk_used'), ('sugar_used')),
            'classes': ('wide', 'extrapretty'),
        }),
    ]


admin.site.register(Patient, PatientAdmin)


# MealPlanFood admin
class BreakfastInline(admin.TabularInline):
    model = MealPlanFood
    verbose_name_plural = 'Breakfast'
    classes = ['collapse']
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).filter(timing='breakfast')


class LunchInline(admin.TabularInline):
    model = MealPlanFood
    verbose_name_plural = 'Lunch'
    classes = ['collapse']
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).filter(timing='lunch')


class DinnerInline(admin.TabularInline):
    model = MealPlanFood
    verbose_name_plural = 'Dinner'
    classes = ['collapse']
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).filter(timing='dinner')


class SnacksInline(admin.TabularInline):
    model = MealPlanFood
    verbose_name_plural = 'Snacks'
    classes = ['collapse']
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).filter(timing='snacks')


class After_BedInline(admin.TabularInline):
    model = MealPlanFood
    verbose_name_plural = 'After Bed'
    classes = ['collapse']
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).filter(timing='after_bed')


class pre_workoutInline(admin.TabularInline):
    model = MealPlanFood
    verbose_name_plural = 'Pre-Workout'
    classes = ['collapse']
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).filter(timing='pre_workout')


class post_workoutInline(admin.TabularInline):
    model = MealPlanFood
    verbose_name_plural = 'Post-Workout'
    classes = ['collapse']
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).filter(timing='post_workout')


class Before_BedInline(admin.TabularInline):
    model = MealPlanFood
    verbose_name_plural = 'Before Bed'
    classes = ['collapse']
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).filter(timing='before_bed')


# MealPlan admin
class MealPlanAdmin(admin.ModelAdmin):
    inlines = (
    After_BedInline, BreakfastInline, LunchInline, SnacksInline, DinnerInline, Before_BedInline, pre_workoutInline,
    post_workoutInline)
    list_display = (
    'name', 'After_Bed', 'Breakfast', 'Lunch', 'Snacks', 'Dinner', 'Before_Bed', 'pre_workout', 'post_workout')
    form = MealPlanForm

    def Before_Bed(self, obj):
        before_bed_foods = obj.foods.filter(mealplanfood__timing='before_bed')
        return ", ".join([food.name for food in before_bed_foods])

    def Breakfast(self, obj):
        breakfast_foods = obj.foods.filter(mealplanfood__timing='breakfast')
        return ", ".join([food.name for food in breakfast_foods])

    def Lunch(self, obj):
        lunch_foods = obj.foods.filter(mealplanfood__timing='lunch')
        return ", ".join([food.name for food in lunch_foods])

    def Dinner(self, obj):
        dinner_foods = obj.foods.filter(mealplanfood__timing='dinner')
        return ", ".join([food.name for food in dinner_foods])

    def Snacks(self, obj):
        snacks_foods = obj.foods.filter(mealplanfood__timing='snacks')
        return ", ".join([food.name for food in snacks_foods])

    def After_Bed(self, obj):
        after_bed_foods = obj.foods.filter(mealplanfood__timing='after_bed')
        return ", ".join([food.name for food in after_bed_foods])

    def pre_workout(self, obj):
        pre_workout_foods = obj.foods.filter(mealplanfood__timing='pre_workout')
        return ", ".join([food.name for food in pre_workout_foods])

    def post_workout(self, obj):
        post_workout_foods = obj.foods.filter(mealplanfood__timing='post_workout')
        return ", ".join([food.name for food in post_workout_foods])

    class Media:
        js = ('js/collapse.js',)


admin.site.register(MealPlan, MealPlanAdmin)




