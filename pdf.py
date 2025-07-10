import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

# Define your source and destination folders
source_folder = "scraped_data"
destination_folder = "knowledge"

# Create destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

def txt_to_pdf(txt_file_path, pdf_file_path):
    c = canvas.Canvas(pdf_file_path, pagesize=LETTER)
    width, height = LETTER
    y = height - 40  # Starting height from top

    with open(txt_file_path, "r", encoding="utf-8") as file:
        for line in file:
            if y < 40:
                c.showPage()
                y = height - 40
            c.drawString(40, y, line.strip())
            y -= 15  # Line spacing

    c.save()

# Loop through all .txt files and convert them
for filename in os.listdir(source_folder):
    if filename.endswith(".txt"):
        txt_path = os.path.join(source_folder, filename)
        pdf_name = os.path.splitext(filename)[0] + ".pdf"
        pdf_path = os.path.join(destination_folder, pdf_name)
        
        txt_to_pdf(txt_path, pdf_path)
        print(f"Converted: {filename} ➝ {pdf_name}")

print("✅ All TXT files converted to PDF.")
