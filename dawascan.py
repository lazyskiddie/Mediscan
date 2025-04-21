import pytesseract
from PIL import Image
import requests
import google.generativeai as genai
import io
import os
import openai
import json

# CONFIGURE GEMINI API KEY
genai.configure(api_key="")  # put your own Gemini API key 

# OCR CORRECTION MAP
medicine_corrections = {
    "lisipreari": "lisinopril",
    "paracetamo1": "paracetamol",
    "ciproflaxin": "ciprofloxacin",
    "amoxilin": "amoxicillin",
    "metformine": "metformin",
    "atorvastine": "atorvastatin",
}

# OCR TEXT EXTRACTION
def get_ocr_text(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

# CLEAN OCR OUTPUT
def extract_medicine_name(text):
    words = text.lower().split()
    for word in words:
        if len(word) > 4:
            return word
    return "unknown"

def correct_ocr_name(name):
    return medicine_corrections.get(name, name)

# GEMINI VISION
def get_gemini_medicine_name(image_path):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        with open(image_path, "rb") as img_file:
            image_bytes = img_file.read()
        pil_image = Image.open(io.BytesIO(image_bytes))
        response = model.generate_content([
            "This is an image of the back side of a medicine strip. Identify the exact name of the medicine written on it. Only return the name, nothing else.",
            pil_image
        ])
        return response.text.strip().lower()
    except Exception as e:
        print(f"❌ Error with Gemini API: {e}")
        return "unknown"

# OPENFDA MEDICINE INFO
def query_openfda(medicine_name):
    try:
        url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:{medicine_name}"
        response = requests.get(url)
        data = response.json().get("results", [])
        if data:
            result = data[0]
            uses = result.get("indications_and_usage", ["Not found"])[0]
            dosage = result.get("dosage_and_administration", ["Not found"])[0]
            side_effects = result.get("adverse_reactions", ["Not found"])[0]
            return uses, dosage, side_effects
        else:
            return None, None, None
    except Exception as e:
        print(f"❌ Error querying OpenFDA: {e}")
        return None, None, None

# DISPLAY SUMMARY
def display_summary(name, uses, dosage, side_effects):
    divider = "\n" + "-" * 50 + "\n"
    print(f"""{divider}
🔎 Final Medicine Report
{divider}
💊 Medicine Name: {name.upper()}

✅ Uses:
{uses if uses else 'No information available.'}

💉 Dosage:
{dosage if dosage else 'No information available.'}

⚠️ Side Effects:
{side_effects if side_effects else 'No information available.'}
{divider}""")


# MAIN FUNCTION
def main():
    image_path = input("📁 Enter the full path of the medicine image:\n> ").strip()

    if not os.path.exists(image_path):
        print("🚫 File not found. Please check the path and try again.")
        return

    print("\n🔍 Step 1: Extracting text with OCR...")
    ocr_text = get_ocr_text(image_path)
    print("🧾 OCR Raw Text:\n", ocr_text)

    ocr_name = extract_medicine_name(ocr_text)
    corrected_name = correct_ocr_name(ocr_name)
    if ocr_name != corrected_name:
        print(f"🛠️ OCR Correction Applied: {ocr_name} → {corrected_name}")
    else:
        print(f"✅ OCR Result: {corrected_name}")

    print("\n👁️‍🗨️ Step 2: Identifying with Gemini Vision...")
    gemini_name = get_gemini_medicine_name(image_path)
    if gemini_name != "unknown":
        print(f"🤖 Gemini Result: {gemini_name}")
    else:
        print("❌ Gemini couldn't detect the medicine name.")

    best_guess = gemini_name if gemini_name != "unknown" else corrected_name
    print(f"\n🔍 Final Detected Name: {best_guess.upper()}")

    print("\n🧪 Step 3: Fetching medicine info from OpenFDA...")
    uses, dosage, side_effects = query_openfda(best_guess)

    display_summary(best_guess, uses, dosage, side_effects)

# Always keep this at the end bacause if main() runs before reaching import os, it doesn't know what os is — hence the NameError will got.
if __name__ == "__main__":
    main()
