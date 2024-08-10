import spacy
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define custom regex patterns for specific entities
patterns = {
    'bedroom': r'(\b(?:at least|more than|less than|up to|no less than|exactly)?\s*\d+\s*bedroom(?:s)?\b)',
    'bathroom': r'(\b(?:at least|more than|less than|up to|no less than|exactly)?\s*\d+\s*bathroom(?:s)?\b)',
    'house_type': r'\b(condo|house|apartment|townhouse)\b',
    'nearby': r'\b(hospital|school|grocery|public transport|recreational park)\b',
    'basement': r'\b(basement)\b',
    'house_size': r'\d+\s*(?:square\s*feet|sqft|square\s*meters|sqm)',
    'land_area': r'\d+\s*(?:square\s*feet|sqft|square\s*meters|sqm)',
    'water': r'\bwater\b',
    'electricity': r'\belectricity\b',
    'financing': r'\bfinancing\b',
    'status': r'\b(available|sold)\b',
    'swimming_pool': r'\bswimming pool\b',
    'property_taxes': r'\bproperty taxes\b',
    'renovation': r'\b(recent renovation|recent upgrades|renovated|upgraded)\b',
    'year_built': r'\b(built|constructed)\b',
    'move_in_ready': r'\b(move-in ready|move in ready)\b',
    'heating': r'\bheating\b',
    'cooling': r'\bcooling\b',
    'parking': r'\bparking\b',
    'repairs_needed': r'\brepairs needed\b',
    'basement': r'\bbasement\b',
    'visit_availability': r'\bvisit availability\b',
    'house_option': r'option\s*(\d+)',
    'payment':r'\$(\d+).*?\b(\d+)\b(?=\s*years)'
    

    

     
}

# Function to extract context
def extract_context(text, match):
    start, end = match.span()
    pre_context = text[max(0, start-50):start].strip()
    post_context = text[end:min(len(text), end+50)].strip()
    return f"{pre_context} {match.group(0)} {post_context}".strip()

# Function to extract entities using spaCy and custom regex
def extract_entities(text):
    doc = nlp(text)
    entities = {
        'bedroom': None,
        'bathroom': None,
        'property_price': None,
        'province': None,
        'city': None,
        'address': None,
        'house_type': None,
        'house_size': None,
        'land_area': None,
        'water': None,
        'electricity': None,
        'financing': None,
        'nearby': [],
        'status': None,
        'swimming_pool': None,
        'property_taxes': None,
        'renovation': None,
        'year_built': None,
        'move_in_ready': None,
        'heating': None,
        'cooling': None,
        'parking': None,
        'repairs_needed': None,
        'basement': None,
        'visit_availability': None,
        'detailed_summary': None,
        'option_number': None,
        'down_payment': None,
        'loan_term': None,
        'visit_date': None
    }

    # Extract entities using spaCy's NER
    for ent in doc.ents:
        if ent.label_ == "GPE":
            entities['city'] = ent.text
        elif ent.label_ == "MONEY":
            entities['property_price'] = ent.text
        elif ent.label_ == "DATE" and re.search(r'\d{4}', ent.text):
            entities['year_built'] = ent.text
    
    # Extract entities using custom regex patterns
    for entity, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            context = extract_context(text, match)
            if entity == 'nearby':
                entities[entity].append(match.group(0)) 
            if entity == 'payment':
                downpayment = match.group(1)  # Captures 350000
                loan_term = match.group(2)     # Captures 15
                downpayment = float(downpayment)
                loan_term = int(loan_term)
                entities['down_payment'] = downpayment
                entities['loan_term'] = loan_term
            #if entity == 'house_option':
            #    entities['option_number'] = int(match.group(1))
           # if entity == 'date_match':
            #    entities['visit_date'] = match.group(0)
            else:
                entities[entity] = match.group(0)
    
    
    # Extract option number for details using custom regex patterns
    option_match = re.search(r'option\s*(\d+)', text, re.IGNORECASE)
    if option_match:
        entities['option_number'] = int(option_match.group(1))
    
    # Extract dates from visit dates
    date_match = re.search(r'(\d{4}[-/]\d{2}[-/]\d{2})', text)
    if date_match:
        entities['visit_date'] = date_match.group(0)
        
    return entities

