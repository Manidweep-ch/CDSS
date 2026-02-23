"""
Generate Sample Lab Report PDFs for Testing
Creates 10 diverse PDF samples covering different medical scenarios
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime, timedelta
import random
import os

# Create output directory
OUTPUT_DIR = "sample_pdfs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_lab_report_pdf(filename, patient_info, test_results, report_title):
    """Create a formatted lab report PDF"""
    
    pdf_path = os.path.join(OUTPUT_DIR, filename)
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c5aa0'),
        spaceAfter=12
    )
    
    # Header
    story.append(Paragraph("MEDICAL LABORATORY", title_style))
    story.append(Paragraph("Clinical Diagnostic Center", styles['Normal']))
    story.append(Paragraph("123 Healthcare Ave, Medical City, MC 12345", styles['Normal']))
    story.append(Paragraph("Phone: (555) 123-4567 | Fax: (555) 123-4568", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Report Title
    story.append(Paragraph(report_title, heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Patient Information
    story.append(Paragraph("PATIENT INFORMATION", heading_style))
    patient_data = [
        ["Patient Name:", patient_info['name']],
        ["Patient ID:", patient_info['id']],
        ["Age:", str(patient_info['age'])],
        ["Gender:", patient_info['gender']],
        ["Collection Date:", patient_info['collection_date']],
        ["Report Date:", patient_info['report_date']]
    ]
    
    patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Test Results
    story.append(Paragraph("LABORATORY TEST RESULTS", heading_style))
    
    # Create results table
    results_data = [["Test Name", "Result", "Unit", "Reference Range"]]
    for test in test_results:
        results_data.append([
            test['name'],
            str(test['value']),
            test['unit'],
            test['reference']
        ])
    
    results_table = Table(results_data, colWidths=[2.5*inch, 1*inch, 1*inch, 2*inch])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    story.append(results_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("This report is electronically generated and valid without signature.", 
                          styles['Italic']))
    story.append(Paragraph("For questions, please contact your healthcare provider.", 
                          styles['Italic']))
    
    # Build PDF
    doc.build(story)
    print(f"✓ Generated: {filename}")
    return pdf_path


# Sample 1: Normal Diabetes Panel
def generate_sample_1():
    patient_info = {
        'name': 'John Smith',
        'id': 'PT001234',
        'age': 45,
        'gender': 'Male',
        'collection_date': '2024-02-15',
        'report_date': '2024-02-16'
    }
    
    test_results = [
        {'name': 'Fasting Glucose', 'value': 95, 'unit': 'mg/dL', 'reference': '70-100 mg/dL'},
        {'name': 'HbA1c', 'value': 5.4, 'unit': '%', 'reference': '<5.7%'},
    ]
    
    create_lab_report_pdf(
        "sample_01_normal_diabetes.pdf",
        patient_info,
        test_results,
        "DIABETES SCREENING PANEL"
    )


# Sample 2: Pre-Diabetes
def generate_sample_2():
    patient_info = {
        'name': 'Sarah Johnson',
        'id': 'PT002345',
        'age': 52,
        'gender': 'Female',
        'collection_date': '2024-02-16',
        'report_date': '2024-02-17'
    }
    
    test_results = [
        {'name': 'Fasting Glucose', 'value': 115, 'unit': 'mg/dL', 'reference': '70-100 mg/dL'},
        {'name': 'HbA1c', 'value': 6.2, 'unit': '%', 'reference': '<5.7%'},
    ]
    
    create_lab_report_pdf(
        "sample_02_prediabetes.pdf",
        patient_info,
        test_results,
        "DIABETES SCREENING PANEL"
    )


# Sample 3: Diabetes Confirmed
def generate_sample_3():
    patient_info = {
        'name': 'Michael Brown',
        'id': 'PT003456',
        'age': 58,
        'gender': 'Male',
        'collection_date': '2024-02-17',
        'report_date': '2024-02-18'
    }
    
    test_results = [
        {'name': 'Fasting Glucose', 'value': 145, 'unit': 'mg/dL', 'reference': '70-100 mg/dL'},
        {'name': 'HbA1c', 'value': 7.8, 'unit': '%', 'reference': '<5.7%'},
    ]
    
    create_lab_report_pdf(
        "sample_03_diabetes_confirmed.pdf",
        patient_info,
        test_results,
        "DIABETES SCREENING PANEL"
    )


# Sample 4: Normal Cardiovascular Panel
def generate_sample_4():
    patient_info = {
        'name': 'Emily Davis',
        'id': 'PT004567',
        'age': 35,
        'gender': 'Female',
        'collection_date': '2024-02-18',
        'report_date': '2024-02-19'
    }
    
    test_results = [
        {'name': 'Total Cholesterol', 'value': 180, 'unit': 'mg/dL', 'reference': '<200 mg/dL'},
        {'name': 'HDL Cholesterol', 'value': 58, 'unit': 'mg/dL', 'reference': '>40 mg/dL (M), >50 mg/dL (F)'},
        {'name': 'LDL Cholesterol', 'value': 95, 'unit': 'mg/dL', 'reference': '<100 mg/dL'},
        {'name': 'Triglycerides', 'value': 135, 'unit': 'mg/dL', 'reference': '<150 mg/dL'},
        {'name': 'Systolic BP', 'value': 118, 'unit': 'mmHg', 'reference': '<120 mmHg'},
        {'name': 'Diastolic BP', 'value': 76, 'unit': 'mmHg', 'reference': '<80 mmHg'},
    ]
    
    create_lab_report_pdf(
        "sample_04_normal_cardio.pdf",
        patient_info,
        test_results,
        "CARDIOVASCULAR RISK PANEL"
    )


# Sample 5: High Cardiovascular Risk
def generate_sample_5():
    patient_info = {
        'name': 'Robert Wilson',
        'id': 'PT005678',
        'age': 62,
        'gender': 'Male',
        'collection_date': '2024-02-19',
        'report_date': '2024-02-20'
    }
    
    test_results = [
        {'name': 'Total Cholesterol', 'value': 265, 'unit': 'mg/dL', 'reference': '<200 mg/dL'},
        {'name': 'HDL Cholesterol', 'value': 35, 'unit': 'mg/dL', 'reference': '>40 mg/dL (M), >50 mg/dL (F)'},
        {'name': 'LDL Cholesterol', 'value': 175, 'unit': 'mg/dL', 'reference': '<100 mg/dL'},
        {'name': 'Triglycerides', 'value': 275, 'unit': 'mg/dL', 'reference': '<150 mg/dL'},
        {'name': 'Systolic BP', 'value': 152, 'unit': 'mmHg', 'reference': '<120 mmHg'},
        {'name': 'Diastolic BP', 'value': 95, 'unit': 'mmHg', 'reference': '<80 mmHg'},
    ]
    
    create_lab_report_pdf(
        "sample_05_high_cardio_risk.pdf",
        patient_info,
        test_results,
        "CARDIOVASCULAR RISK PANEL"
    )


# Sample 6: Normal Kidney Function
def generate_sample_6():
    patient_info = {
        'name': 'Linda Martinez',
        'id': 'PT006789',
        'age': 48,
        'gender': 'Female',
        'collection_date': '2024-02-20',
        'report_date': '2024-02-21'
    }
    
    test_results = [
        {'name': 'Serum Creatinine', 'value': 0.9, 'unit': 'mg/dL', 'reference': '0.6-1.2 mg/dL'},
        {'name': 'Blood Urea', 'value': 18, 'unit': 'mg/dL', 'reference': '7-20 mg/dL'},
        {'name': 'eGFR', 'value': 95, 'unit': 'mL/min/1.73m²', 'reference': '>90 mL/min/1.73m²'},
    ]
    
    create_lab_report_pdf(
        "sample_06_normal_kidney.pdf",
        patient_info,
        test_results,
        "KIDNEY FUNCTION PANEL"
    )


# Sample 7: Impaired Kidney Function
def generate_sample_7():
    patient_info = {
        'name': 'James Anderson',
        'id': 'PT007890',
        'age': 68,
        'gender': 'Male',
        'collection_date': '2024-02-21',
        'report_date': '2024-02-22'
    }
    
    test_results = [
        {'name': 'Serum Creatinine', 'value': 2.4, 'unit': 'mg/dL', 'reference': '0.6-1.2 mg/dL'},
        {'name': 'Blood Urea', 'value': 45, 'unit': 'mg/dL', 'reference': '7-20 mg/dL'},
        {'name': 'eGFR', 'value': 38, 'unit': 'mL/min/1.73m²', 'reference': '>90 mL/min/1.73m²'},
    ]
    
    create_lab_report_pdf(
        "sample_07_impaired_kidney.pdf",
        patient_info,
        test_results,
        "KIDNEY FUNCTION PANEL"
    )


# Sample 8: Comprehensive Panel - All Normal
def generate_sample_8():
    patient_info = {
        'name': 'Patricia Taylor',
        'id': 'PT008901',
        'age': 42,
        'gender': 'Female',
        'collection_date': '2024-02-22',
        'report_date': '2024-02-23'
    }
    
    test_results = [
        # Diabetes
        {'name': 'Fasting Glucose', 'value': 92, 'unit': 'mg/dL', 'reference': '70-100 mg/dL'},
        {'name': 'HbA1c', 'value': 5.3, 'unit': '%', 'reference': '<5.7%'},
        # Cardiovascular
        {'name': 'Total Cholesterol', 'value': 185, 'unit': 'mg/dL', 'reference': '<200 mg/dL'},
        {'name': 'HDL Cholesterol', 'value': 62, 'unit': 'mg/dL', 'reference': '>40 mg/dL (M), >50 mg/dL (F)'},
        {'name': 'LDL Cholesterol', 'value': 98, 'unit': 'mg/dL', 'reference': '<100 mg/dL'},
        {'name': 'Triglycerides', 'value': 125, 'unit': 'mg/dL', 'reference': '<150 mg/dL'},
        {'name': 'Systolic BP', 'value': 115, 'unit': 'mmHg', 'reference': '<120 mmHg'},
        {'name': 'Diastolic BP', 'value': 72, 'unit': 'mmHg', 'reference': '<80 mmHg'},
        # Kidney
        {'name': 'Serum Creatinine', 'value': 0.8, 'unit': 'mg/dL', 'reference': '0.6-1.2 mg/dL'},
        {'name': 'Blood Urea', 'value': 15, 'unit': 'mg/dL', 'reference': '7-20 mg/dL'},
        {'name': 'eGFR', 'value': 98, 'unit': 'mL/min/1.73m²', 'reference': '>90 mL/min/1.73m²'},
    ]
    
    create_lab_report_pdf(
        "sample_08_comprehensive_normal.pdf",
        patient_info,
        test_results,
        "COMPREHENSIVE METABOLIC PANEL"
    )


# Sample 9: Comprehensive Panel - Multiple Issues
def generate_sample_9():
    patient_info = {
        'name': 'David Thompson',
        'id': 'PT009012',
        'age': 65,
        'gender': 'Male',
        'collection_date': '2024-02-23',
        'report_date': '2024-02-24'
    }
    
    test_results = [
        # Diabetes - Elevated
        {'name': 'Fasting Glucose', 'value': 138, 'unit': 'mg/dL', 'reference': '70-100 mg/dL'},
        {'name': 'HbA1c', 'value': 7.2, 'unit': '%', 'reference': '<5.7%'},
        # Cardiovascular - High Risk
        {'name': 'Total Cholesterol', 'value': 245, 'unit': 'mg/dL', 'reference': '<200 mg/dL'},
        {'name': 'HDL Cholesterol', 'value': 38, 'unit': 'mg/dL', 'reference': '>40 mg/dL (M), >50 mg/dL (F)'},
        {'name': 'LDL Cholesterol', 'value': 165, 'unit': 'mg/dL', 'reference': '<100 mg/dL'},
        {'name': 'Triglycerides', 'value': 210, 'unit': 'mg/dL', 'reference': '<150 mg/dL'},
        {'name': 'Systolic BP', 'value': 148, 'unit': 'mmHg', 'reference': '<120 mmHg'},
        {'name': 'Diastolic BP', 'value': 92, 'unit': 'mmHg', 'reference': '<80 mmHg'},
        # Kidney - Moderate Impairment
        {'name': 'Serum Creatinine', 'value': 1.8, 'unit': 'mg/dL', 'reference': '0.6-1.2 mg/dL'},
        {'name': 'Blood Urea', 'value': 32, 'unit': 'mg/dL', 'reference': '7-20 mg/dL'},
        {'name': 'eGFR', 'value': 52, 'unit': 'mL/min/1.73m²', 'reference': '>90 mL/min/1.73m²'},
    ]
    
    create_lab_report_pdf(
        "sample_09_comprehensive_multiple_issues.pdf",
        patient_info,
        test_results,
        "COMPREHENSIVE METABOLIC PANEL"
    )


# Sample 10: Borderline Values (Edge Cases)
def generate_sample_10():
    patient_info = {
        'name': 'Jennifer White',
        'id': 'PT010123',
        'age': 50,
        'gender': 'Female',
        'collection_date': '2024-02-24',
        'report_date': '2024-02-25'
    }
    
    test_results = [
        # Diabetes - Borderline
        {'name': 'Fasting Glucose', 'value': 105, 'unit': 'mg/dL', 'reference': '70-100 mg/dL'},
        {'name': 'HbA1c', 'value': 5.8, 'unit': '%', 'reference': '<5.7%'},
        # Cardiovascular - Borderline
        {'name': 'Total Cholesterol', 'value': 205, 'unit': 'mg/dL', 'reference': '<200 mg/dL'},
        {'name': 'HDL Cholesterol', 'value': 48, 'unit': 'mg/dL', 'reference': '>40 mg/dL (M), >50 mg/dL (F)'},
        {'name': 'LDL Cholesterol', 'value': 128, 'unit': 'mg/dL', 'reference': '<100 mg/dL'},
        {'name': 'Triglycerides', 'value': 155, 'unit': 'mg/dL', 'reference': '<150 mg/dL'},
        {'name': 'Systolic BP', 'value': 128, 'unit': 'mmHg', 'reference': '<120 mmHg'},
        {'name': 'Diastolic BP', 'value': 82, 'unit': 'mmHg', 'reference': '<80 mmHg'},
        # Kidney - Borderline
        {'name': 'Serum Creatinine', 'value': 1.3, 'unit': 'mg/dL', 'reference': '0.6-1.2 mg/dL'},
        {'name': 'Blood Urea', 'value': 22, 'unit': 'mg/dL', 'reference': '7-20 mg/dL'},
        {'name': 'eGFR', 'value': 72, 'unit': 'mL/min/1.73m²', 'reference': '>90 mL/min/1.73m²'},
    ]
    
    create_lab_report_pdf(
        "sample_10_borderline_values.pdf",
        patient_info,
        test_results,
        "COMPREHENSIVE METABOLIC PANEL"
    )


def main():
    print("=" * 60)
    print("Generating Sample Lab Report PDFs")
    print("=" * 60)
    print()
    
    try:
        # Generate all samples
        generate_sample_1()   # Normal Diabetes
        generate_sample_2()   # Pre-Diabetes
        generate_sample_3()   # Diabetes Confirmed
        generate_sample_4()   # Normal Cardiovascular
        generate_sample_5()   # High Cardiovascular Risk
        generate_sample_6()   # Normal Kidney
        generate_sample_7()   # Impaired Kidney
        generate_sample_8()   # Comprehensive Normal
        generate_sample_9()   # Comprehensive Multiple Issues
        generate_sample_10()  # Borderline Values
        
        print()
        print("=" * 60)
        print(f"✓ Successfully generated 10 sample PDFs in '{OUTPUT_DIR}/' directory")
        print("=" * 60)
        print()
        print("Sample Overview:")
        print("  1. Normal Diabetes Panel")
        print("  2. Pre-Diabetes")
        print("  3. Diabetes Confirmed")
        print("  4. Normal Cardiovascular Panel")
        print("  5. High Cardiovascular Risk")
        print("  6. Normal Kidney Function")
        print("  7. Impaired Kidney Function")
        print("  8. Comprehensive Panel - All Normal")
        print("  9. Comprehensive Panel - Multiple Issues")
        print(" 10. Borderline Values (Edge Cases)")
        print()
        print("You can now upload these PDFs to test the system!")
        
    except Exception as e:
        print(f"✗ Error generating PDFs: {str(e)}")
        print("Make sure 'reportlab' is installed: pip install reportlab")


if __name__ == "__main__":
    main()
