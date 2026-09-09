"""One fixed light palette for every course screen.

The course is taught from a projector and read on borrowed laptops, so every
learner must see the same page. Gradio otherwise follows the viewer's system
setting and paints a dark page with near-white text; our own panels stay light,
which leaves white text on a light background. So the dark tokens are set to the
same values as the light ones, and the dark class is neutralised in CSS.
"""
import gradio as gr

PAPER = "#f6f2e9"
PANEL = "#e7e9dd"
INK = "#192a25"
MUTED = "#45594f"
ACCENT = "#236346"
BORDER = "#829285"
ERROR = "#8c2f22"

THEME = gr.themes.Base(
    primary_hue=gr.themes.colors.green,
    font=[gr.themes.GoogleFont("Source Sans 3"), "system-ui", "sans-serif"],
    font_mono=[gr.themes.GoogleFont("Source Code Pro"), "monospace"],
).set(
    body_background_fill=PAPER, body_background_fill_dark=PAPER,
    body_text_color=INK, body_text_color_dark=INK,
    body_text_color_subdued=MUTED, body_text_color_subdued_dark=MUTED,
    background_fill_primary=PAPER, background_fill_primary_dark=PAPER,
    background_fill_secondary=PANEL, background_fill_secondary_dark=PANEL,
    block_background_fill=PAPER, block_background_fill_dark=PAPER,
    block_label_background_fill=PAPER, block_label_background_fill_dark=PAPER,
    block_label_text_color=INK, block_label_text_color_dark=INK,
    block_title_text_color=INK, block_title_text_color_dark=INK,
    block_border_color=BORDER, block_border_color_dark=BORDER,
    border_color_primary=BORDER, border_color_primary_dark=BORDER,
    border_color_accent=ACCENT, border_color_accent_dark=ACCENT,
    input_background_fill=PANEL, input_background_fill_dark=PANEL,
    input_border_color=BORDER, input_border_color_dark=BORDER,
    input_placeholder_color=MUTED, input_placeholder_color_dark=MUTED,
    link_text_color=ACCENT, link_text_color_dark=ACCENT,
    link_text_color_hover=ACCENT, link_text_color_hover_dark=ACCENT,
    link_text_color_visited=ACCENT, link_text_color_visited_dark=ACCENT,
    link_text_color_active=ACCENT, link_text_color_active_dark=ACCENT,
    button_primary_background_fill=ACCENT, button_primary_background_fill_dark=ACCENT,
    button_primary_border_color=ACCENT, button_primary_border_color_dark=ACCENT,
    button_primary_text_color="#ffffff", button_primary_text_color_dark="#ffffff",
    button_secondary_background_fill=PANEL, button_secondary_background_fill_dark=PANEL,
    button_secondary_border_color=BORDER, button_secondary_border_color_dark=BORDER,
    button_secondary_text_color=INK, button_secondary_text_color_dark=INK,
    panel_background_fill=PAPER, panel_background_fill_dark=PAPER,
    panel_border_color=BORDER, panel_border_color_dark=BORDER,
    table_odd_background_fill=PANEL, table_odd_background_fill_dark=PANEL,
    table_even_background_fill=PAPER, table_even_background_fill_dark=PAPER,
    color_accent=ACCENT,
    color_accent_soft=PANEL, color_accent_soft_dark=PANEL,
    # Gradio's own dark defaults for these are a dark panel or near-white text, which is
    # how a black code block and unreadable white-on-light error text reached the page.
    code_background_fill=PANEL, code_background_fill_dark=PANEL,
    checkbox_background_color=PAPER, checkbox_background_color_dark=PAPER,
    checkbox_border_color=BORDER, checkbox_border_color_dark=BORDER,
    checkbox_border_color_hover=ACCENT, checkbox_border_color_hover_dark=ACCENT,
    error_background_fill=PANEL, error_background_fill_dark=PANEL,
    error_border_color=ERROR, error_border_color_dark=ERROR,
    error_text_color=ERROR, error_text_color_dark=ERROR,
    error_icon_color=ERROR, error_icon_color_dark=ERROR,
    input_border_color_focus=ACCENT, input_border_color_focus_dark=ACCENT,
    stat_background_fill=PANEL, stat_background_fill_dark=PANEL,
    table_border_color=BORDER, table_border_color_dark=BORDER,
    button_cancel_text_color_hover=INK, button_cancel_text_color_hover_dark=INK,
    button_primary_background_fill_hover=ACCENT, button_primary_background_fill_hover_dark=ACCENT,
    button_secondary_background_fill_hover=PANEL, button_secondary_background_fill_hover_dark=PANEL,
    button_secondary_border_color_hover=ACCENT, button_secondary_border_color_hover_dark=ACCENT,
)

# Every rule below states its own colour. Nothing inherits a colour from Gradio,
# because in dark mode that colour is near-white and our panels are not.
CSS = f"""
.zta-app, body, body.dark, .gradio-container {{
    color-scheme: light;
    background: {PAPER} !important;
    color: {INK} !important;
}}
body.dark .zta-app, body.dark .gradio-container {{ color: {INK} !important; }}
.zta-app h1, .zta-app h2, .zta-app h3, .zta-app h4 {{
    font-family: Georgia, serif;
    color: {INK} !important;
}}
.zta-app p, .zta-app li, .zta-app strong, .zta-app em, .zta-app label,
.zta-app span, .zta-app td, .zta-app th {{ color: {INK}; }}
.zta-app a {{ color: {ACCENT} !important; text-decoration: underline; }}
.zta-app code {{ background: {PANEL}; color: {INK} !important; }}
.zta-kicker, .zta-kicker p, .zta-kicker span {{
    letter-spacing: .08em;
    font-size: .8rem;
    color: {MUTED} !important;
}}
.zta-side {{ background: {PANEL} !important; padding: 1rem; border-radius: 3px; }}
.zta-side, .zta-side p, .zta-side h3, .zta-side strong, .zta-side span, .zta-side label {{
    color: {INK} !important;
}}
.zta-side .zta-kicker, .zta-side .zta-kicker p {{ color: {MUTED} !important; }}
.zta-passage, .zta-answer, .zta-fixed {{
    white-space: pre-wrap;
    background: {PAPER} !important;
    color: {INK} !important;
    border-left: 3px solid {ACCENT};
    padding: .75rem 1rem;
    line-height: 1.65;
}}
.zta-passage, .zta-fixed {{ font-family: var(--font-mono); }}
.zta-app :is(input, textarea, select) {{
    background: {PANEL} !important;
    color: {INK} !important;
    caret-color: {INK};
}}
.zta-app :is(input, textarea)::placeholder {{ color: {MUTED} !important; opacity: 1; }}
.zta-app button {{
    color: {INK};
    /* Gradio zeroes the border width, which leaves a secondary button looking like plain text. */
    border-width: 1px !important;
    border-style: solid !important;
    border-color: {BORDER} !important;
    border-radius: 3px;
}}
.zta-app button.secondary {{ background: {PANEL} !important; }}
.zta-app button.primary {{ border-color: {ACCENT} !important; }}
.zta-app button:disabled {{ color: {MUTED}; background: {PAPER}; border-style: dashed; opacity: 1; }}
.zta-app button.primary, .zta-app button[variant="primary"] {{ color: #ffffff !important; }}
.zta-app [role="tab"] {{ color: {INK} !important; opacity: 1; }}
.zta-app [role="tab"].selected, .zta-app [role="tab"][aria-selected="true"] {{
    color: {ACCENT} !important;
    font-weight: 600;
}}
/* Selection menus mount outside the app container. */
[role="listbox"], [role="option"], .options, ul.options li {{
    background: {PAPER} !important;
    color: {INK} !important;
}}
[role="option"]:is([data-focused], [aria-selected="true"], .active, :hover) {{
    background: {PANEL} !important;
    color: {INK} !important;
}}
"""

# Gradio reads this on load; without it the viewer's system setting wins and the
# first paint is dark before any CSS applies.
FORCE_LIGHT = """
() => {
    document.body.classList.remove('dark');
    document.documentElement.classList.remove('dark');
    const url = new URL(window.location);
    if (url.searchParams.get('__theme') !== 'light') {
        url.searchParams.set('__theme', 'light');
        window.history.replaceState({}, '', url);
    }
}
"""


def blocks(title, **kwargs):
    """A course page: one palette, no analytics, and never the viewer's dark mode."""
    return gr.Blocks(theme=THEME, css=CSS, js=FORCE_LIGHT, title=title,
                     elem_classes="zta-app", analytics_enabled=False, **kwargs)
