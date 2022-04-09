import PyPDF2


pdf_file_object = open('pdf_reader/Lower extremity muscles.pdf', 'rb')

pdf_reader = PyPDF2.PdfFileReader(pdf_file_object)

print(pdf_reader.documentInfo)

count = pdf_reader.numPages
for i in range(count):
    page = pdf_reader.getPage(i)
    print(page.extractText())
