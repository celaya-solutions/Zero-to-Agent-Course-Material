from streamlit.testing.v1 import AppTest
from zta.storage import root

def test_load_index_predictions_and_refresh(tmp_path,monkeypatch):
    monkeypatch.setenv('ZTA_DATA_DIR',str(tmp_path/'state'))
    app=AppTest.from_file(str(root()/'projects/zta/src/zta/app.py'),default_timeout=20).run()
    assert not app.exception
    next(b for b in app.button if b.label=='Load class binder').click().run()
    next(b for b in app.button if b.label=='Build index').click().run()
    assert not app.exception
    app.text_input(key='nickname').input('Pilot learner').run()
    for i in range(1,6): app.text_area(key=f'expected_{i}').input('Check supplied sources; stop if missing.').run()
    assert all(not b.disabled for b in app.button if b.label.startswith('Run question'))
    fresh=AppTest.from_file(str(root()/'projects/zta/src/zta/app.py'),default_timeout=20).run()
    assert fresh.text_input(key='nickname').value=='Pilot learner'
    assert fresh.text_area(key='expected_1').value.startswith('Check supplied')
    assert not fresh.exception
