import spacy
import streamlit as st
import re

# Load a spaCy NER model
nlp = spacy.load("en_core_web_sm")

def recognize_phone_numbers(text):
    # phone_number_pattern = r"(\+\d{1,2}\s?)?(\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|\(\d{3}\)\s?\d{3}[-.\s]?\d{4}|\d{10})"
     phone_number_pattern = r"(\+\d{1,2}\s?)?((\d{1,3}[-.\s]?)+\d{1,3}[-.\s]?\d{2,6})"
    phone_numbers = []
    for match in re.finditer(phone_number_pattern, text):
        phone_numbers.append(match.group())
    return phone_numbers

def recognize_email_addresses(text):
    email_pattern = r"\b[\w\.-]+@[\w\.-]+\.\w+\b"
    email_addresses = []
    for match in re.finditer(email_pattern, text):
        email_addresses.append(match.group())
    return email_addresses

def replace_entities(input_text):
    doc = nlp(input_text)
    
    phone_numbers = recognize_phone_numbers(input_text)
    email_addresses = recognize_email_addresses(input_text)
    
    entity_mapping = {
        "PHONE_NUMBER": "phone-number",
        "EMAIL": "email",
        "NAME": "person-name",
        "ORG": "company-name",
        "GPE": "place",
    }
    
    modified_text = []
    current_entity = None
    
    for token in doc:
        if token.text in phone_numbers:
            modified_text.append(entity_mapping["PHONE_NUMBER"])
            current_entity = "PHONE_NUMBER"
        elif token.text in email_addresses:
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
    
    return " ".join(modified_text)

st.title("Entity Recognition Demo")

input_text = st.text_area("Enter the string you want to work with:")

if st.button("Convert"):
    if input_text:
        modified_text = replace_entities(input_text)
        st.write("Modified Text:")
        st.write(modified_text)
