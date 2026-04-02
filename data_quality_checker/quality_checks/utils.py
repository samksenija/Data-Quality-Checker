from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(filename, data):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    elements.append(Paragraph("Data Quality Validation Report", styles['Title']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Null Values per Column", styles['Heading2']))
    
    headers = list(data["null_count_per_column"].keys())
    values = list(data["null_count_per_column"].values())

    table_data = [headers, values]

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Duplicate Rows", styles['Heading2']))
    elements.append(Paragraph(f"Total duplicates: {data['duplicate_rows']['duplicate_count']}", styles['Normal']))
    elements.append(Spacer(1, 10))

    dup_headers = data['duplicate_rows']['headers']
    dup_rows = data['duplicate_rows']['duplicate_rows']

    table_data = [dup_headers] + dup_rows

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    if data.get("show_schema_results"):
        elements.append(Paragraph("Schema Validation", styles['Heading2']))

        schema_data = [["Column Name", "Expected Type", "Validation Result"]]

        for row in data["schema_check_datatypes"]:
            schema_data.append([
                row["column_name"],
                row["expected_type"],
                row["validation_result"]
            ])

        table = Table(schema_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ]))

        elements.append(table)

    doc.build(elements)