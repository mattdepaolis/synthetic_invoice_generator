import streamlit as st
import os
import json
import zipfile

# Dummy function for example
def another_invoice_template(path):
    return "header2", "items2", "summary2"

# Sidebar
st.sidebar.header("Invoice Generator")
invoice_template = st.sidebar.selectbox(
    'Select Invoice Template',
    ['Garage Invoice Template', 'Another Invoice Template']
)

num_invoices = st.sidebar.text_input("Enter number of invoices", "1")  # Default value is "1"
num_invoices = int(num_invoices) if num_invoices.isdigit() else 1  # Convert to integer if it's a digit, else default to 1

# Main
st.title("Invoice Generator")
st.write(f"Generate {num_invoices} invoice(s)")

# Progress Bar
progress_bar = st.progress(0)

# Generate button
generate = st.button("Generate Invoices")

if generate:
    # Create a temporary directory to hold the PDFs and JSONs
    temp_dir = './temp_invoices'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    for i in range(num_invoices):
        invoice_name = f"invoice_{i+1}.pdf"
        json_name = f"invoice_{i+1}.json"

        invoice_path = os.path.join(temp_dir, invoice_name)
        json_path = os.path.join(temp_dir, json_name)

        # Select the generation function based on dropdown choice
        if invoice_template == 'Garage Invoice Template':
            from pdf_generation_module import generate_invoice
            header, items, summary = generate_invoice(invoice_path)
        elif invoice_template == 'Another Invoice Template':
            header, items, summary = another_invoice_template(invoice_path)

        # Create your data dictionary
        invoice_data = {
            "gt_parse": {
                "header": header,
                "items": items,
                "summary": summary
            }
        }

        # Serialize Python dictionary to JSON and write to the file
        with open(json_path, 'w') as json_file:
            json.dump(invoice_data, json_file, indent=4)

        # Update progress bar
        progress_bar.progress((i + 1) / num_invoices)

    # Create a ZIP file to hold all the PDFs and JSONs
    zip_name = 'all_invoices.zip'
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                zipf.write(os.path.join(root, file), file)

    # Allow user to download the ZIP file
    with open(zip_name, 'rb') as f:
        zip_bytes = f.read()
        st.download_button(
            label=f"Download All Invoices and JSONs",
            data=zip_bytes,
            file_name=zip_name,
            mime='application/zip'
        )

    st.write("Generation complete!")
