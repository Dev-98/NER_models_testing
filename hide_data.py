import spacy
import streamlit as st
import re


nlp = spacy.load("en_core_web_sm")

def recognize_numbers(text):
    phone_number_pattern = r"(\+\d{1,2}\s?)?(\d{1,3}[-.\s]?)+\d{1,3}[-.\s]?\d{2,6}"
    formatted_text = re.sub(phone_number_pattern, "NUMBER", text)
    return formatted_text

def recognize_email_addresses(text):
    email_pattern = r"\b[\w\.-]+@[\w\.-]+\.\w+\b"
    email_addresses = []
    for match in re.finditer(email_pattern, text):
        email_addresses.append(match.group())
    return email_addresses

def replace_entities(input_text):
    doc = nlp(input_text)
    
    email_addresses = recognize_email_addresses(input_text)
    
    entity_mapping = {
        "EMAIL": "MAIL",
        "PERSON": "NAME",
        "ORG": "ORGANIZATION",
        "GPE": "PLACE",
    }
    
    modified_text = []
    current_entity = None

    
    for token in doc:
        if token.text in email_addresses:
            modified_text.append(entity_mapping["EMAIL"])
            current_entity = "EMAIL"

        elif token.ent_type_ in entity_mapping:
            if current_entity == entity_mapping[token.ent_type_]:
                continue
            else:
                modified_text.append(entity_mapping[token.ent_type_])
                current_entity = entity_mapping[token.ent_type_]
        else:
            modified_text.append(token.text)
            current_entity = None
    
    modified_text = recognize_numbers(" ".join(modified_text))
    
    return modified_text

st.title("PDF-BOT")
input_text = st.text_area("Enter the string you want to work with:")

if st.button("Convert"):
    if input_text:
        modified_text = replace_entities(input_text)
        st.write("Modified Text:")
        st.write(modified_text)
