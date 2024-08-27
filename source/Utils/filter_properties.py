from typing import Optional, Dict, List
import pandas as pd
import re


#col_names = [House Type	Parking	Status	Move-in-ready	Swimming Pool	Heating	Cooling
 #     Repairs needed?	Basement	Water	Electricity	Financing	Year built	
 #     Visit availability date time	primary contact	inhouse amenities	Nearby	
 #     province  City	address	Bathroom	Bedroom	Price	House Size]

def extract_number(value: Optional[str]) -> Optional[int]:
    if isinstance(value, str):
        numbers = re.findall(r'\d+', value)
        return int(numbers[0]) if numbers else None
    elif isinstance(value, (int, float)):
        return int(value)
    return None

def filter_by_city(properties: pd.DataFrame, city: Optional[str]) -> pd.DataFrame:
    if not city:
        return properties
    return properties[properties['City'].str.lower() == city.lower()]

def filter_properties(entities: Dict, property_df: pd.DataFrame) -> pd.DataFrame:
    filtered = property_df

    # Apply city filter (handled by spaCy)
    filtered = filter_by_city(filtered, entities.get('city'))

    # Bedroom filter
    if entities.get('bedroom'):
        bedrooms = extract_number(entities['bedroom'])
        if bedrooms:
            filtered = filtered[filtered['Bedroom'] >= bedrooms]

    # Bathroom filter
    if entities.get('bathroom'):
        bathrooms = extract_number(entities['bathroom'])
        if bathrooms:
            filtered = filtered[filtered['Bathroom'] >= bathrooms]

    # Property price filter
    if entities.get('property_price'):
        max_price = extract_number(entities['property_price'])
        if max_price:
            filtered = filtered[filtered['Price'] <= max_price]

    # House type filter
    if entities.get('house_type'):
        filtered = filtered[filtered['House Type'].str.lower() == entities['house_type'].lower()]

    # Swimming pool filter
    if entities.get('swimming_pool'):
        filtered = filtered[filtered['Swimming Pool'] == (entities['swimming_pool'].lower() == 'yes')]

    # Parking filter
    if entities.get('parking'):
        filtered = filtered[filtered['Parking'] == (entities['parking'].lower() == 'yes')]

    # Year built filter
    if entities.get('year_built'):
        year = extract_number(entities['year_built'])
        if year:
            filtered = filtered[filtered['Year built'] >= year]

    # Basement filter
    if entities.get('basement'):
        filtered = filtered[filtered['Basement'] == (entities['basement'].lower() == 'yes')]

    # House size filter
    if entities.get('house_size'):
        size = extract_number(entities['house_size'])
        if size:
            filtered = filtered[filtered['House Size'].apply(extract_number) >= size]
    # Nearby amenities filter
    if entities.get('nearby'):
        filtered = filtered[filtered['Nearby'].apply(lambda x: any(amenity.lower() in [a.lower() for a in x] for amenity in entities['nearby']))]

    # Status filter
    if entities.get('status'):
        filtered = filtered[filtered['Status'].str.lower() == entities['status'].lower()]

    # Return the filtered properties with specified columns
    if filtered.empty:
        return ["No properties found"]
    #return filtered
    result = []
    for _, row in filtered.iterrows():
        result.append(row.to_dict())

    return result