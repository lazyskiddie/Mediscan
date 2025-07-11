#Project Overview: Medicine Scanner App (Python)

Purpose:
Scan the back of a medicine strip or box, detect the medicine name, and show clear, reliable information like:

- Uses
- Dosage
- Side Effects
- Warnings

------------------------------------------------------------------------------------------------------------------------------------------------

Core Components

- OCR (Text Extraction)	Tesseract OCR (pytesseract)
- AI Correction Layer	Gemini Pro Vision API or GPT-4 Vision
- Medicine Info Source	OpenFDA API / Custom database
- Backend Language	Python
- Output Format	Clean, summarized text

--------------------------------------------------------------------------------------------------------------------------------------------------

System Flow

1. User Uploads Image:
Medicine strip or box backside.

2. OCR Processing:
pytesseract extracts raw text from image.

3. AI-Based Correction (Optional but Important):
Use Gemini Pro Vision or GPT-4 Vision API to:
Correct spelling mistakes in detected medicine names.
Identify the correct medicine name from noisy OCR output.

4. Fetch Information:
Use OpenFDA API or pre-built medicine database.
Get information like uses, dosage, side effects.

5. Display Clean Output:
Present structured, readable information in CLI or web app:

<img width="358" height="103" alt="Screenshot 2025-07-11 at 10 43 12 PM" src="https://github.com/user-attachments/assets/7b7e7ea7-670d-4ac6-af33-1814833635d8" />


