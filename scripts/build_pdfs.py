"""Build portable Letter PDFs from canonical Markdown with no external service."""
import html
import re
import textwrap
from pathlib import Path
from xml.etree import ElementTree as ET
import markdown
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Preformatted,KeepTogether
from reportlab.lib.pagesizes import letter

ROOT=Path(__file__).resolve().parents[1]
CURRENT_SOURCE=ROOT/"README.md"
styles=getSampleStyleSheet()
styles['BodyText'].fontName='Helvetica';styles['BodyText'].fontSize=9;styles['BodyText'].leading=13
styles['BodyText'].spaceAfter=7
for key in ['Title','Heading1','Heading2','Heading3']:
    styles[key].textColor=colors.HexColor('#19392e');styles[key].keepWithNext=True
styles.add(ParagraphStyle(name='Cell',parent=styles['BodyText'],fontSize=7.8,leading=10.5,spaceAfter=1))
styles.add(ParagraphStyle(name='CodeSmall',fontName='Courier',fontSize=7,leading=9,spaceAfter=9))
WIDTH=letter[0]-88

def normalize(text):
    return text.replace('\u2011','-').replace('\u2013','-').replace('\u2014','-').replace('→',' -> ').replace('←',' <- ').replace('×',' x ').replace('✓','yes').replace('☐','[ ]')

def inline(element):
    text=html.escape(element.text or '')
    for child in element:
        if child.tag=='a':
            href=html.escape(child.get('href',''),quote=True)
            if not href.startswith(('https://','http://','mailto:','#')):
                # Absolute source URLs also work when Rails serves a PDF through
                # an authenticated resource route. Publish this tag before release.
                from urllib.parse import quote
                part, _, anchor = child.get('href','').partition('#')
                path = (CURRENT_SOURCE.parent / part).resolve().relative_to(ROOT)
                href = 'https://github.com/celaya-solutions/Zero-to-Agent-Course-Material/blob/v1.3.0-rc.1/' + quote(path.as_posix()) + ('#' + anchor if anchor else '')
            text+=f'<link href="{href}" color="#236346">{inline(child)}</link>'
        elif child.tag in {'strong','b'}:text+='<b>'+inline(child)+'</b>'
        elif child.tag in {'em','i'}:text+='<i>'+inline(child)+'</i>'
        elif child.tag=='code':text+='<font name="Courier">'+inline(child)+'</font>'
        elif child.tag=='br':text+='<br/>'
        elif child.tag=='img':text+=html.escape(child.get('alt','Illustration'))
        else:text+=inline(child)
        text+=html.escape(child.tail or '')
    return text

def convert(elements):
    out=[]
    for e in elements:
        tag=e.tag
        if re.fullmatch('h[1-6]',tag):
            style='Title' if tag=='h1' else 'Heading'+str(min(int(tag[1])-1,3))
            out.append(Paragraph(inline(e),styles[style]))
        elif tag=='p':out.append(Paragraph(inline(e),styles['BodyText']))
        elif tag in {'ul','ol'}:
            for i,item in enumerate(e,1):
                label=f'{i}.' if tag=='ol' else '-'
                out.append(Paragraph(label+' '+inline(item),styles['BodyText']))
        elif tag=='pre':
            raw=''.join(e.itertext());lines=[]
            for line in raw.splitlines():lines.extend(textwrap.wrap(line,width=94,replace_whitespace=False,drop_whitespace=False) or [''])
            out.append(Preformatted('\n'.join(lines),styles['CodeSmall']))
        elif tag=='table':
            rows=[]
            for row in e.iter('tr'):rows.append([Paragraph(inline(cell),styles['Cell']) for cell in row])
            if rows:
                cols=max(map(len,rows));widths=[WIDTH/cols]*cols
                first_header=next(e.iter("tr"))[0]
                if cols==3 and "".join(first_header.itertext()).strip()=="#":widths=[WIDTH*.06,WIDTH*.48,WIDTH*.46]
                table=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
                table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7e9dd')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOX',(0,0),(-1,-1),0.4,colors.HexColor('#b6c1b3')),('INNERGRID',(0,0),(-1,-1),0.3,colors.HexColor('#c5cbbf')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
                out.extend([table,Spacer(1,10)])
        elif tag=='blockquote':out.extend(convert(e))
        elif tag=='hr':out.append(Spacer(1,12))
        else:out.extend(convert(e))
    return out

def footer(canvas,doc):
    canvas.saveState();canvas.setFont('Helvetica',7);canvas.setFillColor(colors.HexColor('#456c59'))
    canvas.drawString(44,25,'ZERO TO AGENT | CELAYA SOLUTIONS LEARNING | v1.3.0-rc.1 REVIEW CANDIDATE')
    canvas.drawRightString(letter[0]-44,25,str(doc.page));canvas.restoreState()

def main():
    global CURRENT_SOURCE
    sources=sorted((ROOT/'courses/project-lab').rglob('*.md'))+sorted((ROOT/'preparation').glob('*.md'))+[ROOT/'README.md',*sorted((ROOT/'projects').glob('*/README.md'))]
    for source in sources:
        CURRENT_SOURCE=source
        rendered=markdown.markdown(normalize(source.read_text(encoding="utf-8")),extensions=['tables','fenced_code'],output_format='xhtml')
        tree=ET.fromstring('<root>'+rendered+'</root>')
        output=source.with_suffix('.pdf')
        SimpleDocTemplate(str(output),pagesize=letter,rightMargin=44,leftMargin=44,topMargin=40,bottomMargin=40,title=next(iter(tree)).text or source.stem,author='Celaya Solutions').build(convert(tree),onFirstPage=footer,onLaterPages=footer)
    print(f'Built {len(sources)} PDFs from canonical Markdown.')
if __name__=='__main__':main()
