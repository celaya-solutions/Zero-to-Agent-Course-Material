"""The course is read on borrowed laptops, so one fixed light palette must survive
a viewer whose system is set to dark. White text on a light panel is the failure
this guards against."""
import re
import pytest
from zta import ui


def luminance(hex_colour):
    parts = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    channels = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in parts]
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(front, back):
    a, b = luminance(front), luminance(back)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


@pytest.mark.parametrize("front,back,floor", [
    (ui.INK, ui.PAPER, 4.5),
    (ui.INK, ui.PANEL, 4.5),
    (ui.MUTED, ui.PAPER, 4.5),
    (ui.MUTED, ui.PANEL, 4.5),
    (ui.ACCENT, ui.PAPER, 4.5),
    ("#ffffff", ui.ACCENT, 4.5),
])
def test_every_text_and_background_pair_is_readable(front, back, floor):
    assert contrast(front, back) >= floor, f"{front} on {back} is {contrast(front, back):.2f}:1"


def test_no_course_surface_is_dark():
    """A dark page with Gradio's near-white text is what puts white on our light panels."""
    for surface in (ui.PAPER, ui.PANEL):
        assert luminance(surface) > 0.5, f"{surface} is a dark background"


def test_white_is_never_placed_on_a_light_surface():
    for surface in (ui.PAPER, ui.PANEL):
        assert contrast("#ffffff", surface) < 1.5
        assert f"color: #ffffff" not in _rule_for(surface)


def _rule_for(surface):
    """The CSS rules that paint this surface, so a white colour beside it is visible here."""
    return "\n".join(block for block in ui.CSS.split("}") if surface in block)


def test_no_colour_changes_when_the_viewer_is_in_dark_mode():
    """Sizes and shadows may differ; a colour that flips is what breaks the page."""
    checked = 0
    for name, value in vars(ui.THEME).items():
        if not name.endswith("_dark") or not re.search(r"color|fill|background", name):
            continue
        light = getattr(ui.THEME, name[:-5], None)
        # Gradio spells "no fill" as both None and "none"; that pair is not a colour flip.
        if light is None or value is None:
            continue
        checked += 1
        assert value == light, f"{name} is {value} but {name[:-5]} is {light}"
    assert checked >= 20, "the theme pins too few colours for dark mode"


def test_the_page_clears_the_dark_class_on_load():
    assert "classList.remove('dark')" in ui.FORCE_LIGHT
    assert "__theme" in ui.FORCE_LIGHT


def test_custom_classes_state_their_own_colour():
    """Inheriting a colour is how white text reached a light panel."""
    for name in (".zta-side", ".zta-passage", ".zta-answer", ".zta-fixed", ".zta-kicker"):
        rules = [b for b in ui.CSS.split("}") if name in b.split("{")[0]]
        assert rules, f"{name} has no rule"
        assert any(re.search(r"(^|[;{\s])color:", b) for b in rules), f"{name} sets no colour"


def test_a_page_can_be_built_from_the_shared_palette():
    page = ui.blocks("Test page")
    assert page.title == "Test page"
