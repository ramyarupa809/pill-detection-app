import pandas as pd

# Creating a dataset for pill details
pill_data = pd.DataFrame({
    "Pill Name": [
        "Dolo_650", "Thyronorm_25", "Omez", "Glibest_M_2", "Mox",
        "Dolojust", "Snezee", "E_D_Phenicol", "Asechlo_p", "Supradyn_daily",
        "Easibreathe", "MultipreX", "Ampoxin_500", "Famocid_20", "Riflux_fortz",
        "Dicoliv_MR", "Moxivir_250", "Dynapar", "Digene", "Aten-25",
        "Sorbitrate_5", "Famocid_40", "Megapen", "Lovolkem", "Bruphen"
    ],
    "Company": [
        "XYZ Ltd", "ABC Pharma", "Omez Ltd", "Glibest Pharma", "Mox Healthcare",
        "DoloMed", "Snezee Inc.", "Phenicol Biotech", "Asechlo Labs", "Supradyn Ltd",
        "EasiMed", "MultipreX Healthcare", "Ampoxin Pharma", "Famocid Ltd", "Riflux Ltd",
        "Dicoliv Pharma", "Moxivir Meds", "Dynapar Biotech", "Digene Healthcare", "Aten Pharma",
        "Sorbitrate Labs", "Famocid Labs", "Megapen Biotech", "Lovolkem Pharma", "Bruphen Meds"
    ],
    "Dosage": [
        "650mg", "25mcg", "20mg", "2mg", "500mg",
        "10mg", "5mg", "250mg", "100mg", "Daily",
        "10mg", "500mg", "500mg", "20mg", "10mg",
        "250mg", "250mg", "50mg", "10mg", "25mg",
        "5mg", "40mg", "500mg", "250mg", "400mg"
    ],
    "Uses": [
        "Fever, Pain", "Thyroid", "Acidity", "Diabetes", "Infection",
        "Pain Relief", "Allergy", "Bacterial Infection", "Anti-inflammatory", "Multivitamin",
        "Respiratory Relief", "Immune Booster", "Antibiotic", "Acid Reflux", "Digestive Aid",
        "Muscle Relaxant", "Antibiotic", "Painkiller", "Digestion", "Hypertension",
        "Heart Disease", "Acid Reducer", "Broad Spectrum Antibiotic", "Anti-inflammatory", "Pain Relief"
    ],
    "Side Effects": [
        "None", "None", "Nausea", "Dizziness", "Stomach Pain",
        "Drowsiness", "Dry Mouth", "Skin Rash", "Headache", "None",
        "Nasal Irritation", "None", "Diarrhea", "Constipation", "Indigestion",
        "Muscle Weakness", "Nausea", "Gastric Irritation", "Constipation", "Dizziness",
        "Flushing", "Headache", "Vomiting", "Liver Effects", "Drowsiness"
    ],
    "Markings": [
        "D650", "T25", "O20", "G2", "M500",
        "D10", "S5", "P250", "A100", "S-D",
        "E10", "M500", "A500", "F20", "R10",
        "D250", "M250", "D50", "D10", "A25",
        "S5", "F40", "M500", "L250", "B400"
    ],
    "Color": [
        "White", "Pink", "Green", "Blue", "White",
        "Yellow", "Red", "Brown", "White", "Orange",
        "Green", "Purple", "Red", "Blue", "Yellow",
        "White", "Green", "Orange", "Pink", "Blue",
        "Red", "Blue", "Green", "White", "Brown"
    ],
    "Shape": [
        "Oval", "Round", "Capsule", "Round", "Tablet",
        "Capsule", "Oval", "Tablet", "Capsule", "Tablet",
        "Capsule", "Tablet", "Capsule", "Capsule", "Tablet",
        "Tablet", "Capsule", "Round", "Round", "Round",
        "Round", "Capsule", "Capsule", "Tablet", "Tablet"
    ],
    "Size": [
        "Medium", "Small", "Small", "Large", "Medium",
        "Small", "Medium", "Medium", "Small", "Medium",
        "Small", "Medium", "Small", "Medium", "Large",
        "Medium", "Small", "Medium", "Small", "Medium",
        "Small", "Medium", "Large", "Medium", "Large"
    ],
    "Components": [
        "Paracetamol", "Thyroxine", "Omeprazole", "Metformin", "Amoxicillin",
        "Ibuprofen", "Levocetirizine", "Chloramphenicol", "Acetaminophen", "Multivitamins",
        "Salbutamol", "Zinc, Vitamin C", "Amoxicillin", "Famotidine", "Magnesium Hydroxide",
        "Dantrolene", "Levofloxacin", "Diclofenac", "Aluminum Hydroxide", "Atenolol",
        "Isosorbide Dinitrate", "Famotidine", "Ampicillin", "Ketoprofen", "Ibuprofen"
    ]
})

# Save the file locally
pill_data.to_csv("pill_details.csv", index=False)
print("CSV file 'pill_details.csv' has been created in the current directory.")
