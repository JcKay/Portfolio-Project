from gtts import gTTS
import os
import PyPDF2
from time import sleep

#
book_name = input("Enter Book fullpath Name: ")
BOOKNAME = book_name.split("/")[-1].split(".")[0]
pdf_file = open(book_name, 'rb')
read_pdf = PyPDF2.PdfFileReader(pdf_file)

# Find the number of pages in the PDF Document
pages = read_pdf.numPages

# Creates the text from the pdf files
pdf_string = ""
for i in range(pages):
    page = read_pdf.pages[i]
    page_content = page.extract_text()
    pdf_string += page_content
    print(f"reading : {100 * i / pages:.1f}%")
    if i == pages - 1:
        print("Analysing PDF Complete")


sleep(2)
print(pdf_string)
# Speech the pdf
tts = gTTS(text=pdf_string, lang='en')
tts.save(f"{BOOKNAME}-audiobook.mp3")
os.system(f"mpg321 {BOOKNAME}audiobook.mp3")
