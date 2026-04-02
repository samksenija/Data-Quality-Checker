import numpy as np

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def check_for_null_fields_count(df):
    df_is_null = df.isnull()

    null_counts = df_is_null.sum()

    return null_counts.to_dict()

def check_for_null_fields_index_column(df):
    df_is_null = df.isnull()
    array_of_textual_result = []

    rows, cols = np.where(df_is_null)

    for r, c in zip(rows, cols):
        found_at = f"Null found at row index: {df.index[r] + 1}, column: {df.columns[c]}"
        array_of_textual_result.append(found_at)

    return array_of_textual_result

def check_for_duplicate_rows(df):
    duplicate_rows = df[df.duplicated()]
    
    context = {
        "headers": duplicate_rows.columns.tolist(),
        "duplicate_rows": duplicate_rows.values.tolist(),
        "duplicate_count": len(duplicate_rows),
    }

    return context

def check_for_which_columns_schema_needs_to_be_validated(column_mappings):
    column_mappings = [(column, value) for column, value in column_mappings if value != ""]

    return column_mappings

def schema_check_datatypes(df, column_mappings):
    columns_to_be_validates_for_data_type = check_for_which_columns_schema_needs_to_be_validated(column_mappings)
    datatype_conversion_results = []

    for column, data_type in columns_to_be_validates_for_data_type:
        try:
            df[column].astype(data_type)
            validation_result = "Valid"

        except ValueError:
            validation_result = "Invalid"

        validation = {
            "column_name": column,
            "expected_type": data_type,
            "validation_result": validation_result
        }
        
        datatype_conversion_results.append(validation)
  
    return datatype_conversion_results

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