from flask import Flask, render_template, request, send_file, redirect, flash
from http.server import BaseHTTPRequestHandler
from PyPDF2 import PdfReader, PdfFileWriter
from werkzeug.utils import secure_filename
from zipfile import ZipFile
from os.path import basename
import os
import time
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/src/upload')
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'static/src/download')
today = time.strftime("%d-%m-%Y")
FILE_ZIP_PATH = os.path.join(os.getcwd(),'static/src/zip_file')
FILE_ZIP = os.path.join(FILE_ZIP_PATH,'Contracheques_{}.zip'.format(today))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload(): 
    # file = request.files['arquivo']
    # if file:
    #     # savePath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    #     # file.save(savePath)
    #     # split_file(savePath)
    #     # empty_zip_folder()
    #     # zip_files()
    #     # empty_donwload_folder()
    #     # print("teste")
    #     return "teste"
    #     # return send_file(FILE_ZIP, as_attachment=True)
    # else:
    #     flash("Nenhum arquivo selecionado")
    #     return redirect('/')
    return redirect('/')
     
    

@app.route('/split_file')
def split_file(uploadFilePath):
    pdf = PdfReader(uploadFilePath)

    for i in range(pdf.numPages): 
        page = pdf.pages[i]
        text = page.extract_text()
        posicao_nome = text.find('Nome')
        posicao_competencia = text.find('Competência')
        nome = text[posicao_nome + 4:posicao_competencia]
        competencia = text[posicao_competencia + 11:posicao_competencia + 21]
        competencia = competencia.replace('/','_')
        nome_arquivo_separado = nome.strip() + '_' + competencia.strip()
        downloadFilePath = os.path.join(DOWNLOAD_FOLDER, nome_arquivo_separado)
        output = PdfFileWriter()
        output.addPage(pdf.getPage(i))
        with open(downloadFilePath + ".pdf", "wb") as outputStream:
            output.write(outputStream)

@app.route('/zip_files')
def zip_files():
    with ZipFile(FILE_ZIP, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(DOWNLOAD_FOLDER):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, basename(filePath))

def empty_donwload_folder():
    for f in os.listdir(DOWNLOAD_FOLDER):
        os.remove(os.path.join(DOWNLOAD_FOLDER, f))

def empty_zip_folder():
    for f in os.listdir(FILE_ZIP_PATH):
        os.remove(os.path.join(FILE_ZIP_PATH, f))        

if __name__ == '__main__':
    app.debug = True
    app.run()
