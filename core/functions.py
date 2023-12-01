from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml


def add_line_numbering_to_docx(doc):
    # * aplicar numeración de líneas a todas las secciones del documento
    for section in doc.sections:
        # * crear un nuevo objeto OxmlElement para cada sección
        lineNumbering = parse_xml(r'<w:lnNumType %s w:countBy="1" w:restart="continuous"/>' % nsdecls('w'))
        sectPr = section._sectPr
        sectPr.append(lineNumbering)