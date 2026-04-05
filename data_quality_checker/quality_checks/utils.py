import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm


def check_for_null_fields_count(df):
    df_is_null = df.isnull()

    null_counts = df_is_null.sum()

    return null_counts.to_dict()

def check_for_null_fields_index_column(df):
    df_is_null = df.isnull()
    array_of_null_details_result = []
    found_at = {}

    rows, cols = np.where(df_is_null)

    for r, c in zip(rows, cols):
        found_at = {"row": df.index[r] + 1, "column": df.columns[c]}
        array_of_null_details_result.append(found_at)

    return array_of_null_details_result

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
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    elements = []
    styles = getSampleStyleSheet()

    page_width = A4[0] - doc.leftMargin - doc.rightMargin

    def create_table(data, col_count):
        col_widths = [page_width / col_count] * col_count

        table = Table(
            data,
            colWidths=col_widths,
            repeatRows=1 
        )

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))

        return table

    def wrap_cell(value):
        return Paragraph(str(value), styles['Normal'])

    elements.append(Paragraph("Data Quality Validation Report", styles['Title']))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("Null Values per Column", styles['Heading2']))

    headers = list(data["null_count_per_column"].keys())
    values = list(data["null_count_per_column"].values())

    table_data = [
        [wrap_cell(h) for h in headers],
        [wrap_cell(v) for v in values],
    ]

    elements.append(create_table(table_data, len(headers)))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("Duplicate Rows", styles['Heading2']))
    elements.append(
        Paragraph(
            f"Total duplicates: {data['duplicate_rows']['duplicate_count']}",
            styles['Normal']
        )
    )
    elements.append(Spacer(1, 10))

    dup_headers = data['duplicate_rows']['headers']
    dup_rows = data['duplicate_rows']['duplicate_rows']

    table_data = [
        [wrap_cell(h) for h in dup_headers]
    ] + [
        [wrap_cell(cell) for cell in row] for row in dup_rows
    ]

    elements.append(create_table(table_data, len(dup_headers)))
    elements.append(Spacer(1, 15))

    if data.get("show_schema_results"):
        elements.append(Paragraph("Schema Validation", styles['Heading2']))

        schema_data = [[
            wrap_cell("Column Name"),
            wrap_cell("Expected Type"),
            wrap_cell("Validation Result")
        ]]

        for row in data["schema_check_datatypes"]:
            schema_data.append([
                wrap_cell(row["column_name"]),
                wrap_cell(row["expected_type"]),
                wrap_cell(row["validation_result"])
            ])

        elements.append(create_table(schema_data, 3))

    doc.build(elements)
    
def results_context(null_count_per_column, duplicate_rows, show_schema_results, schema_result):
    return {"null_count_per_column": null_count_per_column,
            "duplicate_rows": duplicate_rows,
            "show_schema_results": show_schema_results,
            "schema_check_datatypes": schema_result}