import docx2pdf
import win32com.client



def convert_docx2pdf():
    
    win32com.client.pythoncom.CoInitialize()
    result = docx2pdf.convert('static/result_document.docx', 'static/result_document.pdf')
    print(result)
    win32com.client.pythoncom.CoUninitialize()

    return result
