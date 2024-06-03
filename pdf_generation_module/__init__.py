import os
import random
from faker import Faker
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

global line_items
global items


# your_pdf_generation_module.py
def generate_invoice(invoice_name):
    # Initialize Faker with Swiss German locale
    fake = Faker('de_CH')
    global line_item_data
    line_item_data = []
    global items
    items = []
    # Header Information
    header_info = {
        'InvoiceNumber': fake.random_int(min=100000, max=999999),
        'ChassisNumber': fake.bothify(text='????????#########', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        'CarModel': fake.random_element(['Tesla Model S', 'Audi A4', 'BMW X3', 'Mercedes C-Class',
                                         'Ford Mustang', 'Chevrolet Camaro', 'Dodge Charger', 'Nissan Altima',
                                         'Volkswagen Golf', 'Honda Civic', 'Toyota Corolla', 'Subaru Impreza',
                                         'Hyundai Elantra', 'Mazda 3', 'Kia Optima', 'Jeep Wrangler',
                                         'Land Rover Discovery', 'Cadillac Escalade', 'Volvo XC90', 'Porsche 911',
                                         'Ferrari 488', 'Lamborghini Huracan', 'Aston Martin Vantage',
                                         'Rolls Royce Phantom',
                                         'Bentley Continental', 'Maserati Quattroporte', 'Alfa Romeo Giulia',
                                         'Jaguar F-Type',
                                         'McLaren 720S', 'Audi Q8', 'BMW M5', 'Mercedes G-Class', 'Tesla Model Y',
                                         'Chevrolet Corvette', 'Ford F-150', 'Volkswagen Passat', 'Honda Accord',
                                         'Toyota Camry', 'Nissan Maxima', 'Hyundai Sonata']),
        'NumberPlate': fake.bothify(text='??####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        'CompletionDate': fake.date_this_decade().strftime('%d.%m.%Y'),
        'OrderNumber': fake.random_int(min=10000, max=99999),
        'ImmatriculationDate': fake.date_this_decade().strftime('%d.%m.%Y'),
        'Mileage': fake.random_int(min=1000, max=99999),
        # Optional
        'Kunden-Nr': fake.random_int(min=10000000, max=99999999),
        'Annahme': fake.date_this_decade().strftime('%d.%m.%Y'),
        'Mod. Schlüssel': fake.bothify(text='??######', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        'Telefon': fake.random_int(min=100000, max=999999),
        'Fert. Zeit': fake.time_object(end_datetime=None).strftime('%H:%M'),
        'Komm.-Nr': fake.random_int(min=100000, max=999999),
        'Ihr Berater': fake.name()
    }

    # Line items
    global line_items
    line_items = []
    for i in range(random.randint(2, 5)):
        item = {
            'Item Name': fake.catch_phrase().upper(),
            'Item ID': fake.random_int(min=10000000, max=99999999),
            'Cost (Net)': round(random.uniform(50.0, 300.0), 2),
            'Cost (Gross)': round(random.uniform(300.0, 600.0), 2),
            'Discount': round(random.uniform(1, 15)),
            'Amount': round(random.uniform(1, 10))
        }
        line_items.append(item)

    # Summary
    summary = {
        'Tax Amount': round(random.uniform(10.0, 50.0), 2),
        'Gross Amount': round(random.uniform(500.0, 2000.0), 2),
        'Net Amount': round(random.uniform(400.0, 1500.0), 2)
    }

    # Compile all data
    structured_invoice_data = {
        'Header Information': header_info,
        'Items': line_items,
        'Summary': summary
    }

    def draw_footer(canvas, doc):
        canvas.saveState()

        summary_data = [
            ["Betrag exkl.", "Steuer", "MWST", "RDiff", "", "TOTAL"],
            [str(summary['Gross Amount']), "7.70%", str(summary['Tax Amount']), "0.01", "CHF",
             str(summary['Net Amount'])]
        ]

        summary_table = Table(summary_data, [8 * cm, 2 * cm, 2 * cm, 1 * cm, 2 * cm, 2 * cm])
        summary_table.setStyle(TableStyle([
            # ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (5, 0), (5, -1), 'Helvetica-Bold'),  # Make "TOTAL" bold
            ('FONTNAME', (4, -1), (4, -1), 'Helvetica-Bold'),
            ('FONTNAME', (0, 0), (3, 0), 'Helvetica'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
            ('TOPPADDING', (0, -1), (-1, -1), 0),
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black)
        ]))

        # Draw the table at the bottom of the canvas (page)
        summary_table.wrapOn(canvas, 0, 0)
        summary_table.drawOn(canvas, doc.rightMargin, 1 * cm)

        canvas.restoreState()

    # Create a PDF document
    pdf_path = invoice_name
    pdf_structured = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        topMargin=9 * cm,
        leftMargin=3 * cm,
        bottomMargin=1 * cm
    )

    # Initialize styles
    styles = getSampleStyleSheet()

    # Initialize PDF elements
    elements = []
    # Header Title
    header_table_title_data = [
        ["R e c h n u n g", "", "Nr." + str(header_info['InvoiceNumber']) + " / " + str(header_info['CompletionDate'])]
    ]

    header_table_title = Table(header_table_title_data, [5 * cm, 7 * cm, 5 * cm])
    header_table_title.setStyle(TableStyle([
        # ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 16),
        ('BOTTOMPADDING', (0, 0), (0, 0), 10),  # Set height of other rows
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black)
    ]))

    elements.append(header_table_title)

    # Header Table
    header_table_data = [
        ["Auftrags-Nr.", str(header_info['OrderNumber']), "Amtl. Kennz.", str(header_info['NumberPlate']), "Kunden-Nr.",
         str(header_info['Kunden-Nr'])],
        ["Annahme", str(header_info['Annahme']), "Mod. Schlüssel", str(header_info['Mod. Schlüssel']), "Telefon",
         str(header_info['Telefon'])],
        ["Fert. Tag", str(header_info['CompletionDate']), "Fahrgestell-Nr.", str(header_info['ChassisNumber'])],
        ["Fert. Zeit", str(header_info['Fert. Zeit']), "Komm.-Nr", str(header_info['Komm.-Nr']), "Vertrags-Nr."],
        ["KM-Stand", str(header_info['Mileage']), "Zul. Datum", str(header_info['ImmatriculationDate']), "Auftraggeber",
         str(fake.company())],
        ["Ihr Berater", str(header_info['Ihr Berater']), "Typ", str(header_info['CarModel'])]
    ]

    header_table = Table(header_table_data, [2 * cm, 3 * cm, 3 * cm, 4 * cm, 2 * cm, 3 * cm])
    header_table.setStyle(TableStyle([
        # ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('FONTNAME', (3, 0), (3, -1), 'Helvetica-Bold'),
        ('FONTNAME', (5, 0), (5, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, 0), 4),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black)
    ]))

    elements.append(header_table)

    # TABLE TITLE
    # Sample data for the table
    line_item_data = [["Arbeiten/Teile", "Bezeichnung", "Preis", "Einzelpr.", "Menge", "Betrag"],
                      ["ARBEITEN GEMÄSS ABSPRACHE AUSGEFÜHRT"]]

    # Define the table
    table = Table(line_item_data, [3 * cm, 8 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm])

    # Add TableStyle for formatting
    table.setStyle(TableStyle([
        # ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('FONTSIZE', (0, -1), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 1),
        ('TOPPADDING', (0, 0), (-1, -1), 3)
    ]))

    # Add table to the elements to build
    elements.append(table)

    # SUBTITLE
    # Add subtitle as a Paragraph with left alignment
    styles.add(ParagraphStyle(name='LeftAlignedBoldBodyText',
                              parent=styles['BodyText'],
                              fontName='Helvetica-Bold',
                              alignment=0))  # 0 is for left alignment

    # LINE ITEMS
    # Function to generate a random paragraph and table
    def generate_random_paragraph_and_table():
        global items
        global line_item_data
        elements = []
        # Add subtitle as a Paragraph with left alignment
        subtitle = Paragraph(fake.text(max_nb_chars=30), styles['LeftAlignedBoldBodyText'])
        elements.append(subtitle)

        # Add a random number of line items to a table
        line_item_data = []
        for _ in range(random.randint(2, 5)):
            # Generate random data for each line item
            item_id = fake.random_int(min=10000000, max=99999999)
            item_name = fake.catch_phrase().upper()[:35]
            cost_gross = round(random.uniform(300.0, 600.0), 2)
            discount = round(random.uniform(1, 15))
            amount = round(random.uniform(1, 10))
            cost_single = round(random.uniform(10.0, 300.0), 2)
            cost_net = round(random.uniform(10.0, 300.0), 2)

            line_item_data.append(
                [item_id, item_name, f"{cost_gross}  {discount}.00%", f"{cost_single}", f"{amount}.00", cost_net])

            new_item = {"ItemName": item_name,
                        "ItemID": item_id,
                        "CostNet": cost_net,
                        "CostGross": f"{cost_gross}",
                        "Discount": f"{discount}.00%",
                        "Amount": f"{amount}.00"
                        }
            items.append(new_item)

        # Add an additional row for "Summe" and a random number
        summe_value = round(random.uniform(500.0, 2000.0), 2)
        line_item_data.append(["", "", "Summe", "", "", summe_value])

        table = Table(line_item_data, [3 * cm, 7 * cm, 2.5 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm])
        table.setStyle(TableStyle([
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('ALIGN', (3, 0), (3, -1), 'CENTER'),
            ('ALIGN', (4, 0), (4, -1), 'CENTER'),
            ('ALIGN', (5, 0), (5, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('LINEABOVE', (-1, -1), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)
        return elements

    num_paragraphs = random.randint(2, 5)
    # Initialize an empty list to hold the items

    for _ in range(num_paragraphs):
        elements += generate_random_paragraph_and_table()

    # Generate the PDF, adding the draw_footer function as the onFirstPage and onLaterPages callback
    pdf_structured.build(elements, onFirstPage=draw_footer, onLaterPages=draw_footer)
    # Generate the PDF

    # CREATE JSON FILE
    # Sample data from your invoice, usually you would pull this from your application
    header = {
        "InvoiceNumber": str(header_info['InvoiceNumber']),
        "ChassisNumber": str(header_info['ChassisNumber']),
        "CarModel": str(header_info['CarModel']),
        "NumberPlate": str(header_info['NumberPlate']),
        "CompletionDate": str(header_info['CompletionDate']),
        "OrderNumber": str(header_info['OrderNumber']),
        "ImmatriculationDate": str(header_info['ImmatriculationDate']),
        "Mileage": str(header_info['Mileage'])
    }

    summary = {
        "TaxAmount1": str(summary['Tax Amount']),
        "GrossAmount": str(summary['Gross Amount']),
        "NetAmount1": str(summary['Net Amount'])
    }

    # Create your data dictionary
    invoice_data = {
        "gt_parse": {
            "header": header,
            "items": items,
            "summary": summary
        }
    }

    print(invoice_data)
    return header, items, summary


def main():
    # Create the 'generated_invoices' directory if it doesn't exist
    if not os.path.exists('./generated_invoices'):
        os.makedirs('./generated_invoices')

    # Generate a sample invoice
    generate_invoice("sample_invoice.pdf")


if __name__ == "__main__":
    main()
