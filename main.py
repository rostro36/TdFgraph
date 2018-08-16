
# coding: utf-8
#libs used
import PyPDF2 as pypdf
import urllib3
import io
from pdfprocess import process
from graph import plot
import data

http = urllib3.PoolManager()
data.init()
 #gather the data
for etape in range(1,5): #change range back to 22
    etapestring=(str(hex(etape))[2:]).zfill(2)
    print('working on stage:'+str(etape))
    URL = 'http://azure.tissottiming.com/File/00031001070101'+etapestring+'FFFFFFFFFFFFFF00'
    #download the data
    r = http.request('GET',URL)
#   #check if press-release is ready/a PDF
    if r.info()['Content-type']!='application/pdf':
        print (str(etape)+' not ready')
        break
    #open the file
    data.newstage(etape)
    read_pdf = pypdf.PdfFileReader(io.BytesIO(r.data))
    #read_pdf=pypdf.PdfFileReader('cat.pdf')
    #process each page
    for pagenum in range(read_pdf.getNumPages()):
        process(read_pdf.getPage(pagenum).extractText())
    print(str(etape)+' is processed')
print('processing done')
plot()
