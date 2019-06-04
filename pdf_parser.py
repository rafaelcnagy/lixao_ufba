import re

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, resolve1  # process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument


from io import StringIO


def pdf_to_text(pdfname):
    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Extract text
    with open(pdfname, 'rb') as fp:
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
        fp.close()

    # Get text from StringIO
    text = sio.getvalue()

    # Cleanup
    device.close()
    sio.close()

    return text

def pdf_page_count(pdfname):
    with open(pdfname, 'rb') as fp:
        parser = PDFParser(fp)
        document = PDFDocument(parser)

        # This will give you the count of pages
        print(resolve1(document.catalog['Pages'])['Count'])
        return resolve1(document.catalog['Pages'])['Count']



path = '/home/nagy/UFBA/2019.1/Engenharia de Software 1/vagaturma.pdf'
pdf = pdf_to_text(path).splitlines()
paginas = pdf_page_count(path)

turmas = []
disciplinas = []
universidade = pdf[0]
colegiado = pdf[2]
data = re.compile('^\d{1,2}\/\d{2}\/\d{4} \d{1,2}:\d{2}$')
numero = re.compile('^\d+$')

idx = 0
first = True
for pagina in range(1):
    disci_completas = len(turmas)


    idx += 6

    for line in pdf[idx:]:
        idx += 1
        if line == '':
            continue
        if data.match(line):
            break
        else:
            disciplinas.append(line)

    idx += 5

    disci = disci_completas
    step = 1
    turmas_completas = len(turmas)
    idx_turma = turmas_completas

    for line in pdf[idx:]:
        idx += 1
        if line == '':
            idx_turma = turmas_completas
            step += 1
            first = False
            if numero.match(pdf[idx]):
                print('parou em', idx, pdf[idx])
                break
        if numero.match(line):
            if step == 1:
                turmas.append({'disciplina': disciplinas[disci],
                               'vagas-oferecidas': {'veterano': line, 'calouro': ''},
                               'vagas-preenchidas': {'veterano': '', 'calouro': ''},
                               'saldo': ''})
            elif step == 2:
                turmas[idx_turma]['vagas-oferecidas']['calouro'] = line
            elif step == 3:
                turmas[idx_turma]['vagas-preenchidas']['veterano'] = line
            elif step == 4:
                turmas[idx_turma]['vagas-preenchidas']['calouro'] = line
            elif step == 5:
                turmas[idx_turma]['saldo'] = line
            idx_turma += 1

    ignore = True

    turmas_completas = len(turmas)
    idx_turma = turmas_completas
    step = 1
    disci = 0

    for line in pdf[idx:]:
        idx += 1
        if line == '':
            if ignore:
                ignore = False
                disci += 1
                if disci >= len(disciplinas):
                    print('mudou em', idx, pdf[idx])
                    disci = 0
                    idx_turma = turmas_completas
                    step += 1
                    ignore = True
            else:
                ignore = True

        elif line.startswith('Pág'):
            break

        elif not ignore and numero.match(line):
            if step == 1:
                turmas.append({'disciplina': disciplinas[disci],
                               'vagas-oferecidas': {'veterano': line, 'calouro': ''},
                               'vagas-preenchidas': {'veterano': '', 'calouro': ''},
                               'saldo': ''})
            elif step == 2:
                turmas[idx_turma]['vagas-oferecidas']['calouro'] = line
            elif step == 3:
                turmas[idx_turma]['vagas-preenchidas']['veterano'] = line
            elif step == 4:
                turmas[idx_turma]['vagas-preenchidas']['calouro'] = line
            elif step == 5:
                turmas[idx_turma]['saldo'] = line
            idx_turma += 1

    idx += 2
    idx_turma = turmas_completas

    for line in pdf[idx:]:
        idx += 1
        if idx_turma >= len(turmas):
            print('parou em', idx, pdf[idx])
            break
        if numero.match(line):
            turmas[idx_turma]['turma'] = line
            idx_turma += 1


for item in turmas:
    print(item)
