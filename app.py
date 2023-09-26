import ast
import os
import streamlit as st
from gpt import is_compliant
from rules import murabahah_rules, mudarabah_rules, credit_debit_rules, ijara_rules
from extract_text import extract_text_from_image, extract_text_from_pdf
from highlight import highlight_text
import tempfile

rules = ""

st.title("Transaction Checker for Shariyah Compliance")
st.subheader("Your documents")
include_murabahah = st.checkbox("Include Murabahah")
include_mudarabah = st.checkbox("Include Mudarabah")
include_card = st.checkbox("Include Card Rules")
include_ijara = st.checkbox("Include Ijara Rules")
docs = st.file_uploader(
    "Upload your documents here and click on 'Process'", accept_multiple_files=True)
if st.button("Process"):
    if docs:
        with st.spinner("Processing"):
            #include rules as per user selection
            if include_murabahah:
                rules += murabahah_rules
            if include_mudarabah:
                rules += mudarabah_rules    
            if include_card:
                rules += credit_debit_rules
            if include_ijara:    
                rules += ijara_rules

            extracted_text = []
            for doc in docs:
                if doc.name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    text_from_image = extract_text_from_image(doc)
                    if text_from_image:
                        extracted_text.append([doc.name, f"File Name: {doc.name}\n{text_from_image}\n\n"])
                elif doc.name.lower().endswith('.pdf'):
                    text_from_doc = extract_text_from_pdf(doc)
                    if text_from_doc:
                        extracted_text.append([doc.name, f"File Name: {doc.name}\n{text_from_doc}\n\n"])    
                else:
                    st.warning(f"Unsupported file format: {doc.name}")
            if extracted_text:
                st.subheader("Result:")
                for doc in extracted_text:
                    compliance_result = is_compliant(doc[1], rules)
                    st.write(f"Compliance Result for {doc[0]}: {compliance_result}")
                    with tempfile.TemporaryDirectory() as temp_dir:
                        image_folder = os.path.join(temp_dir, "highlighted_images")
                    # to convert the list enclosed in string (given by gpt) to a normal list
                        try:
                            result = ast.literal_eval(compliance_result)
                        except (SyntaxError, ValueError) as e:
                            result = compliance_result  
                        compliance_result = result
                    # Create the folder
                    os.makedirs(image_folder)
                    if isinstance(compliance_result, list):
                        file_name, text_to_highlight = compliance_result[0], compliance_result[1]
                        image_path = os.path.join(image_folder, os.path.basename(file_name))
                        original_file = ""
                        for doc in extracted_text:
                            if doc[0] == compliance_result[0]: # finding the file with same name as the one in the result
                                original_file = doc[1]
                                break  # Exit the loop once a match is found

                        highlighted_data_html_file = highlight_text(original_file, text_to_highlight)
                        output_filename = "{}.html".format(file_name)
                        with open(output_filename, "w") as f:
                            f.write(highlighted_data_html_file)

                    elif not isinstance(compliance_result, list): #this will run when no violations found
                       st.write("No violations found")
