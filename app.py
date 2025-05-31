import os
from documents.generatePDF import HtmlPDF
from flask import Flask, jsonify, send_file, send_from_directory
from cv_exp import CvXp
import certificados as cert
import responses
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/certifications')
@app.route('/certifications/<lang>')
def certiciation(lang='es'):
    image_files = cert.getImagePaths('static/certifications')
    type_response = 200
    response_body = ''
    error_msg = ''
    if image_files:
        response_body = cert.info(image_files, lang, 'cert')
    else:
        type_response = 501
        error_msg = responses.ERROR_501
    response = responses.generate(type=type_response,error=error_msg, response=response_body)
    return jsonify(response)

@app.route('/cv')
@app.route('/cv/')
@app.route('/cv/<lang>')
def cv(lang="esp"):
    type_response = 200
    response_body = ''
    error_msg = ''
    cv = CvXp.getCV(lang)
    if cv:
        response_body = cv
    else:
        type_response = 501
        error_msg = responses.ERROR_501
    response = responses.generate(type=type_response, error=error_msg, response=response_body)
    return jsonify(response)

@app.route('/constancias')
@app.route('/constancias/<lang>')
def constancia(lang='es'):
    type_response = 200
    response_body = ''
    error_msg = ''
    image_files = cert.getImagePaths('static/constancias')
    if image_files:
        response_body = cert.info(image_files, lang, 'cons')
    else:
        type_response = 501
        error_msg = responses.ERROR_501
    response = responses.generate(type=type_response, error=error_msg, response=response_body)
    return jsonify(response)

@app.route('/pdf')
def archivo_pdf():
    return send_file('static/certifications/0.jpg')

@app.route('/experience')
@app.route('/experience/')
@app.route('/experience/<lang>')
def experience(lang="esp"):
    type_response = 200
    response_body = ''
    error_msg = ''
    xp = CvXp.getXp(lang)
    if xp:
        response_body = xp
    else:
        type_response = 501
        error_msg = responses.ERROR_501
    response = responses.generate(type=type_response, error=error_msg, response=response_body)
    return jsonify(response)

@app.route('/downloadcv/<lang>')
def generar_pdf(lang="esp"):
    html = HtmlPDF(lang)
    response = html.generate()
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=CV_Raul_Reyes.pdf'
    return response

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'icon.ico'
    )

@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(error):
    response = responses.generate(int(error.code), error=str(error.description))
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
