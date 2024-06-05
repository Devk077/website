from django.shortcuts import render, HttpResponse
from .models import Food
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
import base64
from .models import Food
from django.shortcuts import render
import base64
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from .models import Appointments, Food, MealPlan, Patient
from reportlab.platypus import TableStyle

def generate_meal_plan_table(meal_plan, table_style):
    # Define styles
    styles = getSampleStyleSheet()

    # Define heading style
    heading_style = styles['Heading1']
    heading_style.fontSize = 12
    heading_style.alignment = 1

    # Define normal style
    normal_style = styles['Normal']
    normal_style.alignment = 0
    normal_style.fontSize = 8
    normal_style.leading = 10

    # Create a centered style for the cells
    centered_style = heading_style.clone('centered')
    centered_style.alignment = 0
    centered_style.fontSize = 10
    centered_style.leading = 12
    # centered_style.backColor = colors.Color(196/255, 232/255, 99/255)

    food_styles = styles['Normal']
    food_styles.fontSize = 10
    food_styles.alignment = 0
    food_styles.leading = 12

    food_styles_centered = food_styles.clone('centered')
    food_styles_centered.alignment = 1

    # Create table for meal items
    meal_items_data = []
    idx = 0

    headers = ["Time", "Food", "Quantity"]
    header_row = [Paragraph(header, normal_style) for header in headers]
    meal_items_data.append(header_row)

    for timing in ['after_bed', 'breakfast', 'lunch', 'snacks', 'dinner', 'before_bed', 'pre_workout', 'post_workout']:
        meal_items = meal_plan.foods.filter(mealplanfood__timing=timing)

        if meal_items:
            # Add a row for the timing
            meal_items_data.append(['', [Paragraph(timing.replace('_', ' ').title(), centered_style)]])
            # Set background color for food cells
            for i in range(-5, 0):
                table_style.add('BACKGROUND', (i, len(meal_items_data) - 1), (i, len(meal_items_data) - 1),
                                colors.HexColor('#F09745'))

            for meal_item in meal_items:
                # Set background color of food cells alternately
                background_color = colors.HexColor('#DCDCDC') if idx % 2 == 0 else colors.HexColor('#ffffff')
                idx += 1
                quantity = meal_plan.mealplanfood_set.filter(food=meal_item).first().quantity
                time = meal_plan.mealplanfood_set.filter(food=meal_item).first().time
                time = time.strftime('%I:%M %p')

                # Add a row for the meal item
                meal_items_data.append([
                    Paragraph(str(time)),
                    Paragraph(meal_item.name, food_styles),
                    Paragraph(str(quantity)),
                ])

                # Set background color for food cells
                for i in range(-5, 0):
                    table_style.add('BACKGROUND', (i, len(meal_items_data) - 1), (i, len(meal_items_data) - 1),
                                    background_color)

    # Create the table
    meal_items_table = Table(meal_items_data, repeatRows=1)
    meal_items_table.setStyle(table_style)

    border_color = colors.HexColor('#fbc4ab')
    table_style_border = TableStyle([

        # Outside border
        ('LINEABOVE', (0, 0), (-1, 0), 1, border_color),  # Line grabove the first row
        ('LINEBELOW', (0, -1), (-1, -1), 1, border_color),  # Line below the last row
        ('LINEBEFORE', (0, 0), (0, -1), 1, border_color),  # Line before the first column
        ('LINEAFTER', (-1, 0), (-1, -1), 1, border_color),  # Line after the last column
    ])

    meal_items_table.setStyle(table_style_border)

    return meal_items_table


def create_heading_cell(doctor_name, designation, mobile_number):
    # Define styles
    styles = getSampleStyleSheet()

    # Define heading style for doctor's name
    heading_style = styles['Heading1']
    heading_style.alignment = 0  # Left alignment

    # Define normal style for designation and mobile number
    normal_style = styles['Normal']
    normal_style.alignment = 0  # Left alignment

    # Define a new style for right-aligned text
    right_aligned_style = styles['Normal']
    right_aligned_style.alignment = 0  # Right alignment
    right_aligned_style.leading = 12

    # Create a nested table for doctor's name and designation
    left_table = Table([
        [Paragraph(doctor_name, heading_style)],
        [Paragraph(designation, normal_style)],
    ])

    # Create a table for the mobile number aligned to the right
    mo = 'M.o.:' + mobile_number
    right_table = Table([
        [Paragraph(mo, right_aligned_style)],
    ], colWidths=[100])  # Adjusted column width to accommodate the entire phone number

    # Create the heading cell with the left and right tables
    heading_cell = Table([
        [left_table, Spacer(10, 0), right_table],
    ], style=[('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F09746'))],
        colWidths=[350, '*', 100])  # Adjusted column width

    return heading_cell


def generate_bmi_classification_table():
    # Define the data for the table
    data = [
        ["BMI Range", "Classification"],
        ["Below 18", "Malnutrition 2"],
        ["18.1 - 20", "Malnutrition 1"],
        ["20.1 - 23", "Normal"],
        ["23.1 - 25", "Overweight"],
        ["25.1 - 28", "Obesity grade 1"],
        ["28.1 - 30.0", "Obesity grade 2"],
        ["Over 30", "Obesity grade 3"]
    ]

    # Define the alternating background colors
    white_color = colors.HexColor('#FFFFFF')
    grey_color = colors.HexColor('#DCDCDC')

    # Define column widths
    colWidths = [50, 80]
    # Create the table
    bmi_table = Table(data, colWidths=colWidths)

    # Set the background color for each row individually
    for i in range(0, len(data)):
        row_color = white_color if i % 2 == 0 else grey_color
        bmi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, i), (-1, i), row_color),
        ]))

    # Define the style for the table
    border_color = colors.HexColor('#F09746')
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F09746')),  # Background color for header row
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # Text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alignment
        # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Inner grid lines
        # ('BOX', (0, 0), (-1, -1), 0.5, colors.green),  # Outer border
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.white)  # No inner grid
        ('LINEABOVE', (0, 0), (-1, 0), 1, border_color),  # Line grabove the first row
        ('LINEBELOW', (0, -1), (-1, -1), 1, border_color),  # Line below the last row
        ('LINEBEFORE', (0, 0), (0, -1), 1, border_color),  # Line before the first column
        ('LINEAFTER', (-1, 0), (-1, -1), 1, border_color),
    ]

    # Apply the style to the table
    bmi_table.setStyle(TableStyle(table_style))

    return bmi_table


def generate_body_fat_classification_table():
    # Define the data for the table
    data = [
        ["Normal Body", "Fat Value"],
        ["MEN"],
        ["FIT", "14 - 17"],
        ["FAT", "18 - 25"],
        ["HIGH RISK", "25+"],
        ["WOMEN"],
        ["FIT", "21 - 24"],
        ["FAT", "25 - 31"],
        ["HIGH RISK", "32+"]
    ]

    # Define the alternating background colors
    white_color = colors.HexColor('#FFFFFF')
    grey_color = colors.HexColor('#DCDCDC')

    # Define column widths
    colWidths = [70, 60]

    # Create the table
    body_fat_table = Table(data, colWidths=colWidths)

    # Set the background color for each row individually
    for i in range(1, len(data)):
        row_color = white_color if i % 2 == 0 else grey_color
        body_fat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, i), (-1, i), row_color),
            ('TEXTCOLOR', (0, i), (-1, i), colors.black),
            ('ALIGN', (0, i), (-1, i), 'CENTER')
        ]))

    # Define the style for the table
    border_color = colors.HexColor('#F09746')
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), border_color),  # Background color for header row
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # Text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alignment
        # ('BOX', (0, 0), (-1, -1), 1, colors.green),  # Outer border
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.white)  # No inner grid
        ('LINEABOVE', (0, 0), (-1, 0), 1, border_color),  # Line grabove the first row
        ('LINEBELOW', (0, -1), (-1, -1), 1, border_color),  # Line below the last row
        ('LINEBEFORE', (0, 0), (0, -1), 1, border_color),  # Line before the first column
        ('LINEAFTER', (-1, 0), (-1, -1), 1, border_color),
    ]

    # Apply the style to the table
    body_fat_table.setStyle(TableStyle(table_style))

    return body_fat_table


def generate_health_clinic_table():
    # Define the text content
    header = "A COMPLETE HEALTH CLINIC FOR"
    text = """* Get at least 6-7 hours of sleep each night.
* Drink a minimum of 2 liters of water daily.
* Commit to 45 minutes of regular exercise.
* Cut down on sugary, processed, junk, bakery, and packet foods.
* Incorporate 15 minutes of daily meditation.
* Have dinner before 8 PM.
* Chew your food thoroughly for better digestion.
* Opt for 3-5 small meals throughout the day."""

    # Define the style for the table
    background_color = colors.HexColor('#ffe8d6')
    border_color = colors.HexColor('#fbc4ab')
    table_style = [
        ('BACKGROUND', (0, 0), (-1, -1), background_color),  # Background color for the cell
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # Text color
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alignment
        ('BOX', (0, 0), (-1, -1), 1, border_color),  # Outer border
    ]

    # Create the table with a single cell containing the text
    health_clinic_table = Table([
        [header],
        [text],
    ])

    # Apply the style to the table
    health_clinic_table.setStyle(TableStyle(table_style))

    return health_clinic_table


def generate_body_composition_table(appointment_id):
    appointment = get_object_or_404(Appointments, id=appointment_id)
    body_composition = appointment.body_composition

    # Define the data for the table
    if body_composition:
        data = [
            ["BODY COMPOSITION"],
            ["HEIGHT", f"{round(body_composition.height, 2)}"],
            ["WEIGHT", f"{round(body_composition.weight, 2)} KG"],
            ["BODY FAT", f"{round(body_composition.body_fat, 2)} %"],
            ["AGE", f"{round(body_composition.age, 2)}"],
            ["BMI", f"{round(body_composition.BMI, 2)}"],
            ["RMR", f"{round(body_composition.RMR, 2)}"],
            ["V-FAT %", f"{round(body_composition.visceral_fat, 2)}"],
        ]

    # Define the style for the table
    border_color = colors.HexColor('#F09746')
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), border_color),  # Background color for the header row
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Text color for the header row
        ('LINEABOVE', (0, 0), (-1, 0), 1, border_color),  # Line grabove the first row
        ('LINEBELOW', (0, -1), (-1, -1), 1, border_color),  # Line below the last row
        ('LINEBEFORE', (0, 0), (0, -1), 1, border_color),  # Line before the first column
        ('LINEAFTER', (-1, 0), (-1, -1), 1, border_color),
    ]

    # Define the alternating background colors
    white_color = colors.HexColor('#FFFFFF')
    grey_color = colors.HexColor('#DCDCDC')

    # Apply the style and alternating background colors to the table
    body_composition_table = Table(data, colWidths=[60, 65])
    body_composition_table.setStyle(TableStyle(table_style))

    for i in range(1, len(data)):
        row_color = white_color if i % 2 == 0 else grey_color
        body_composition_table.setStyle(TableStyle([
            ('BACKGROUND', (0, i), (-1, i), row_color),
            ('TEXTCOLOR', (0, i), (-1, i), colors.black),
            ('ALIGN', (0, i), (-1, i), 'LEFT'),
        ]))

    return body_composition_table


###########################################################################################################
def generate_pdf(request, appointment_id):
    # Retrieve data from the database
    appointment = Appointments.objects.get(id=appointment_id)
    patient = appointment.patient
    meal_plan = appointment.meal_plan

    # Create a buffer for the PDF
    buffer = BytesIO()

    # Create PDF
    title = f"{patient.name} - {meal_plan.name}"  # Set the title to patient's name followed by the diet name
    doc = SimpleDocTemplate(buffer, pagesize=letter, title=title)
    elements = []

    # Define table style
    table_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('UPPERPADDING', (0, 0), (-1, -1), 2),
        # ('LINEBELOW', (0, 0), (-1, 0), 0, colors.black),  # Add line below heading row
        # ('LINEBEFORE', (0, 0), (0, -1), 0, colors.black),  # Add line before first column
        # ('LINEAFTER', (-1, 0), (-1, -1), 0, colors.black),  # Add line after last column
        # ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Remove grid lines
    ])
    pink_cell = Table([[None]], style=[('BACKGROUND', (0, 0), (-1, -1), colors.pink)])

    doctor_name = "Dt. Dhwani Khurana"
    doctor_title = "Nutritionist, Healvibe Clinic"
    mobile_number = "+91 9879040001"

    heading_cell = create_heading_cell(doctor_name, doctor_title, mobile_number)

    heading_table = Table([
        [heading_cell],
    ], colWidths=[500, ])

    elements.append(heading_table)
    elements.append(Spacer(1, 10))

    side_left_table = Table([
        [generate_body_composition_table(appointment_id)],
        [Spacer(1, 10)],
        [generate_body_fat_classification_table()],
        [Spacer(1, 10)],
        [generate_bmi_classification_table()],
    ])

    meal_plan_table = generate_meal_plan_table(meal_plan, table_style)

    table = Table([
        [side_left_table, meal_plan_table],
    ], colWidths=[150, 350], style=[('VALIGN', (0, 0), (-1, -1), 'TOP'), ('ALIGN', (0, 0), (-1, -1), 'LEFT')])

    # table.setStyle(table_style)
    elements.append(table)

    conclusion_table = Table([
        [generate_health_clinic_table()],
    ])

    elements.append(Spacer(1, 10))
    elements.append(conclusion_table)

    # Build PDF
    doc.build(elements)

    # Get PDF content
    pdf = buffer.getvalue()
    buffer.close()

    # Return PDF as HTTP response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="preview.pdf"'
    response.write(pdf)
    return response


def index(request):
    return render(request, 'index.html')