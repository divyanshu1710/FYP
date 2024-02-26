from flask import Flask, render_template, request
import qrcode
import random
from datetime import datetime, timedelta
from PIL import Image
import io
import base64

app = Flask(__name__)

# List of real medicine names
medicine_names = [
    "Acetaminophen", "Acetylsalicylic Acid (Aspirin)", "Albuterol", "Amlodipine", "Amoxicillin",
    "Atorvastatin", "Azithromycin", "Cetirizine", "Ciprofloxacin", "Clopidogrel", "Dexamethasone",
    "Diclofenac", "Digoxin", "Diphenhydramine", "Enalapril", "Escitalopram", "Esomeprazole",
    "Furosemide", "Gabapentin", "Hydrochlorothiazide", "Ibuprofen", "Insulin (Regular)", "Insulin (NPH)",
    "Levothyroxine", "Lisinopril", "Loratadine", "Losartan", "Metformin", "Metoprolol", "Montelukast",
    "Naproxen", "Omeprazole", "Paracetamol", "Pantoprazole", "Pregabalin", "Prednisone", "Propranolol",
    "Quetiapine", "Ramipril", "Ranitidine", "Rosuvastatin", "Salbutamol", "Sertraline", "Simvastatin",
    "Sildenafil", "Tadalafil", "Tamsulosin", "Tramadol", "Venlafaxine", "Warfarin", "Acarbose",
    "Alendronate", "Atenolol", "Baclofen", "Carvedilol", "Cefixime", "Cefuroxime", "Celecoxib",
    "Cetirizine", "Cimetidine", "Desloratadine", "Desvenlafaxine", "Diltiazem", "Donepezil", "Doxycycline",
    "Duloxetine", "Enoxaparin", "Erythromycin", "Ezetimibe", "Famotidine", "Fluconazole", "Fluticasone",
    "Folic Acid", "Glimepiride", "Glipizide", "Haloperidol", "Hydrocortisone", "Hydroxyzine", "Indapamide",
    "Ipratropium", "Isosorbide", "Ketoconazole", "Labetalol", "Lamotrigine", "Lansoprazole", "Levocetirizine",
    "Levofloxacin", "Levetiracetam", "Liraglutide", "Lisdexamfetamine", "Loperamide", "Losartan/Hydrochlorothiazide",
    "Meloxicam", "Memantine", "Methylphenidate", "Metronidazole", "Mirtazapine", "Mometasone", "Moxifloxacin",
    "Nifedipine"
]

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert PIL image to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return img_bytes.getvalue()

@app.route('/')
def index():
    return render_template('index.html', medicine_names=medicine_names)

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    medicine_name = request.form['medicine_name']

    batch_number = f"BATCH-{random.randint(1000, 9999)}"

    manufacture_date = datetime.now() - timedelta(days=random.randint(1, 365))
    manufacture_date = manufacture_date.strftime("%Y-%m-%d")

    expiry_date = datetime.now() + timedelta(days=random.randint(1, 365))
    expiry_date = expiry_date.strftime("%Y-%m-%d")

    manufacturer = f"Manufacturer-{random.randint(1, 10)}"

    serial_number = f"{random.randint(10000, 99999)}"

    medication_data = {
        "product_name": medicine_name,
        "batch_number": batch_number,
        "manufacture_date": manufacture_date,
        "expiry_date": expiry_date,
        "manufacturer": manufacturer,
        "serial_number": serial_number
    }

    data_to_encode = "\n".join([f"{key}: {value}" for key, value in medication_data.items()])

    img = generate_qr_code(data_to_encode)

    # Convert image bytes to base64 for embedding in HTML
    qr_img = base64.b64encode(img).decode('utf-8')

    return render_template('index.html', medicine_name=medicine_name, qr_img=qr_img)

if __name__ == '__main__':
    app.run(debug=True)

