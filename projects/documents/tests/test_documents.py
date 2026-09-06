import io
import json
import pytest
from pypdf import PdfWriter
from reportlab.pdfgen import canvas
from zta.documents import CLASS_FILES, build_index, extract, retrieve, inventory
from zta.evidence import QUESTIONS
from zta.storage import root

@pytest.fixture
def index(tmp_path):
    assets=root()/"courses/project-lab/level-01/assets"
    path=tmp_path/"index.sqlite3"
    build_index(path,[(n,(assets/n).read_bytes()) for n in CLASS_FILES])
    return path

def test_actual_binder_retrieves_needed_documents(index):
    needed=[{CLASS_FILES[0]}, {CLASS_FILES[0]}, {CLASS_FILES[0],CLASS_FILES[1]}, {CLASS_FILES[1]}, {CLASS_FILES[2],CLASS_FILES[3]}]
    for q,expected in zip(QUESTIONS,needed):
        found=retrieve(index,q,4)
        assert expected.issubset({p['source'] for p in found}), (q,found)
        assert len(found)<=4

def test_controlled_exercise_exposes_missing_evidence(index):
    before=retrieve(index,QUESTIONS[4],1)
    after=retrieve(index,QUESTIONS[4],4)
    assert len(before)==1
    assert {CLASS_FILES[2],CLASS_FILES[3]}.issubset({p['source'] for p in after})

def test_keyword_query_is_not_sql_or_fts_syntax(index):
    assert retrieve(index,'" OR *); DROP TABLE passages; --',4)==[]
    assert inventory(index)

def test_no_cross_binder_contamination(index):
    build_index(index,[("fresh.txt",b"Only a zebra lives here.")])
    assert retrieve(index,"El Paso Texas")==[]
    assert len(inventory(index))==1

def test_bad_document_does_not_replace_index(index):
    original=inventory(index)
    with pytest.raises(ValueError): build_index(index,[("image.pdf",b"not a pdf")])
    assert inventory(index)==original

@pytest.mark.parametrize('name,data',[("empty.md",b""),("binary.txt",b"\xff"),("bad.exe",b"words"),("big.txt",b"a"*(10*1024*1024+1))])
def test_rejects_unreadable_or_large(name,data):
    with pytest.raises(ValueError): extract(name,data)

def test_pdf_retains_real_page_number():
    stream=io.BytesIO(); pdf=canvas.Canvas(stream)
    pdf.drawString(20,700,"First page evidence");pdf.showPage()
    pdf.drawString(20,700,"Second page evidence");pdf.save()
    passages=extract("example.pdf",stream.getvalue())
    assert [p['page'] for p in passages]==[1,2]
    assert 'Second page' in passages[1]['text']

def test_rejects_scan_and_encrypted_pdf():
    for encrypted in [False,True]:
        writer=PdfWriter();writer.add_blank_page(width=100,height=100)
        if encrypted: writer.encrypt('class')
        stream=io.BytesIO();writer.write(stream)
        with pytest.raises(ValueError):extract('scan.pdf',stream.getvalue())

def test_metadata_is_not_retrieved(index):
    assert retrieve(index,"SHA256 Author License")==[]
    assert {p['class'] for p in inventory(index)}=={'public','training-only'}
