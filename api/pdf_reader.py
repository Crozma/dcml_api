from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from io import StringIO


def parse_pdf(page: int) -> list:
    page_num = page + 3
    body = list()

    with open('references/pauld.pdf', 'rb') as pdf_file:
        rsmgr = PDFResourceManager()
        return_str = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsmgr, return_str, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsmgr, device)

        for index, page in enumerate(PDFPage.get_pages(pdf_file)):
            if index == page_num:
                interpreter.process_page(page)

                data = return_str.getvalue()

                linebreak_check = False
                space_check = False
                part = str()

                for part_index, char in enumerate(data, 1):
                    if part_index == len(data):
                        part += char
                        body.append(part)
                        part = str()
                    elif linebreak_check:
                        if char == '\n':
                            body.append(part)
                            part = str()
                        else:
                            part += f'\n{char}'
                            linebreak_check = False
                    elif char == '\n':
                        linebreak_check = True
                        continue
                    elif space_check:
                        if char != ' ':
                            part += char
                        linebreak_check = False
                        space_check = False
                    else:
                        if char == ' ':
                            space_check = True
                        part += char
                        linebreak_check = False

        return body
