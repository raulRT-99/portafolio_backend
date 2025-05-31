import io
import json
from flask import make_response
from reportlab.lib.colors import blue
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table

with open('documents/CV/cv.json', 'r', encoding='utf-8') as file:
    data_cv = json.load(file)

pdfmetrics.registerFont(TTFont('DejaVuSans', 'documents/fonts/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'documents/fonts/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Oblique', 'documents/fonts/DejaVuSans-Oblique.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Light', 'documents/fonts/DejaVuSans-ExtraLight.ttf'))


class HtmlPDF():
    def __init__(self, lang="esp"):
        self.lang = lang
        self.vacio = Paragraph("", ParagraphStyle(name='Italic', fontName='Times-Italic', fontSize=5))
        self.name_style = ParagraphStyle(
            name='Nombre',
            fontName='DejaVuSans-Bold',
            fontSize=37
        )
        self.normal_style = ParagraphStyle(
            name='Normal',
            fontName='DejaVuSans',
            fontSize=10
        )
        self.normal_bold_style = ParagraphStyle(
            name='Normal-Bold',
            fontName='DejaVuSans-Bold',
            fontSize=10
        )
        self.titles = ParagraphStyle(
            name='Titulos',
            fontName='DejaVuSans-Bold',
            fontSize=12,
            textColor=blue
        )
        self.subtitles = ParagraphStyle(
            name='Subtitulos',
            fontName='DejaVuSans-Light',
            fontSize=9
        )

    def getName(self):
        return Paragraph("Raúl Reyes Torres", self.name_style)

    def getContact(self):
        text = data_cv[self.lang]['location'] +'<br></br>'+ data_cv[self.lang]['cel'] +'<br></br>'+ data_cv[self.lang]['email']
        return Paragraph(text, self.normal_style)

    def getDegree(self):
        return Paragraph(data_cv[self.lang]['degree'], self.normal_style)

    def getExperience(self):
        xp = []
        for x in data_cv[self.lang]["experience"]:
            xp.append(x)
        titulo=Paragraph('EXPERIENCIA' if self.lang == 'esp' else 'EXPERIENCE', self.titles)
        list_xp = []
        list_xp.append(titulo)
        list_xp.append(self.vacio)
        list_xp.append(self.vacio)
        for exp in xp:
            lugar = Paragraph(exp['place'], self.normal_bold_style)
            fecha = Paragraph(exp['date'] + ', '+exp['location'], self.subtitles)
            todo = Paragraph(exp['todo'], self.normal_style)
            list_xp.append(lugar)
            list_xp.append(fecha)
            list_xp.append(todo)
            list_xp.append(self.vacio)
            list_xp.append(self.vacio)
        list_xp.append(self.vacio)
        list_xp.append(self.vacio)
        list_xp.append(self.vacio)
        return list_xp

    def getSchooling(self):
        schools = []
        for studies in data_cv[self.lang]['studies']:
            schools.append(studies)
        titulo = Paragraph('FORMACIÓN' if self.lang == 'esp' else 'SCHOOLING', self.titles)
        list_Schools = []
        list_Schools.append(titulo)
        list_Schools.append(self.vacio)
        list_Schools.append(self.vacio)
        for sch in schools:
            degree = Paragraph(sch['degree'], self.normal_bold_style)
            escuela = Paragraph(sch['school'], self.normal_style)
            date = Paragraph(sch['date'], self.subtitles)
            list_Schools.append(degree)
            list_Schools.append(escuela)
            list_Schools.append(date)
            list_Schools.append(self.vacio)
            list_Schools.append(self.vacio)
        list_Schools.append(self.vacio)
        list_Schools.append(self.vacio)
        return list_Schools

    def getAptitudes(self):
        apts = []
        for apt in data_cv[self.lang]['aptitudes']:
            apts.append(apt)
        list_apts = []
        list_apts.append(self.vacio)
        for apt in apts:
            aptitude = Paragraph(apt, self.normal_style)
            list_apts.append(aptitude)
        return list_apts

    def getLanguages(self):
        langs = []
        for lang in data_cv[self.lang]['speaks']:
            langs.append(lang)
        list_langs = []
        list_langs.append(self.vacio)
        for lang in langs:
            language = Paragraph(lang['language'] + ' -- ' + str(lang['level']) + '%', self.normal_style)
            list_langs.append(language)
        return list_langs

    def getKnowledge(self):
        knows = []
        for know in data_cv[self.lang]['knowledge']:
            knows.append(know)
        list_knows = []
        list_knows.append(self.vacio)
        for know in knows:
            know = Paragraph(know['skill'] + ' -- ' + str(know['level']) + '%', self.normal_style)
            list_knows.append(know)
        return list_knows

    def getAdditional(self):
        additions = []
        for add in data_cv[self.lang]['additional']:
            additions.append(add)

    def adjustListSize(self, list_items, size):
        if len(list_items) == size:
            return list_items
        else:
            list_items.append(self.vacio)
            return self.adjustListSize(list_items, size)

    def generate(self):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer,
                                pagesize=A4,
                                topMargin=20,
                                bottomMargin=30,
                                leftMargin=50,
                                rightMargin=40)

        nombre = self.getName()
        contacto = self.getContact()
        carrera = self.getDegree()
        list_exp = self.getExperience()
        list_schools = self.getSchooling()
        list_apts = self.getAptitudes()
        list_langs = self.getLanguages()
        list_knows = self.getKnowledge()
        list_size = max(len(list_apts), len(list_langs), len(list_knows))
        list_apts = self.adjustListSize(list_apts, list_size)
        list_langs = self.adjustListSize(list_langs, list_size)
        list_knows = self.adjustListSize(list_knows, list_size)

        top_data = [
            [nombre, self.vacio],
            [carrera, contacto],
            [self.vacio, self.vacio],
            [self.vacio, self.vacio],
            [self.vacio, self.vacio],
            [self.vacio, self.vacio],
            [self.vacio, self.vacio],
            [self.vacio, self.vacio],
            [self.vacio, self.vacio]
        ]
        for x in list_exp:
            top_data.append([x,self.vacio])
        for x in list_schools:
            top_data.append([x, self.vacio])

        apt = Paragraph('APTITUDES', self.titles)
        languages = Paragraph('IDIOMAS' if self.lang == 'esp' else 'LANGUAGES', self.titles)
        knows = Paragraph('CONOCIMIENTO' if self.lang == 'esp' else 'KNOWLEDGE', self.titles)
        mid_data = [
            [apt, knows, languages]
        ]
        for Apt,Know,Lang in zip(list_apts, list_knows, list_langs):
            mid_data.append([Apt, Know, Lang])

        top_table = Table(top_data, colWidths=[420,170])
        mid_table = Table(mid_data, colWidths=[195,195,195])

        story = []
        story.append(top_table)
        story.append(mid_table)

        doc.build(story)

        buffer.seek(0)
        response = make_response(buffer.read())

        return response