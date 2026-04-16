import os, sys
from datetime import date

project = "ENPM605 Spring 2026"
author = "Z. Kootbally"
copyright = f"{date.today().year}, {author}"
release = "v1.0"

extensions = [
    "myst_parser",
    "sphinx.ext.autosummary",
    "sphinxcontrib.mermaid",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx_design",
    "sphinx_proof",
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
]

plantuml = 'https://www.plantuml.com/plantuml/png/'
plantuml_output_format = 'png'

# Prerender options for better performance
katex_prerender = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
proof_numbered = {
    "theorem": True,
    "lemma": True,
    "algorithm": True,
    "example": False,
}

todo_include_todos = True

templates_path = ["_templates"]
exclude_patterns = ["assignments/gp2_bak/**"]

# ---------------------------------------------------------------------------
# PyData Sphinx Theme
# ---------------------------------------------------------------------------
html_theme = "pydata_sphinx_theme"

html_theme_options = {
    # Logo (place files in _static/images/)
    "logo": {
        "text": "ENPM605 Spring 2026",
        "image_light": "_static/images/enpm605_logo_light.png",
        "image_dark": "_static/images/enpm605_logo_dark.png",
    },
    # Header / navbar icon links
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/zeidk/enpm605-spring-2026-docs",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
    ],
    "back_to_top_button": True,
    # Light/dark mode toggle
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    # Navigation
    "navigation_depth": 3,
    "show_nav_level": 1,
    "show_toc_level": 1,
    "show_prev_next": True,
    # Footer
    "footer_start": ["copyright"],
    "footer_end": ["theme-version"],
    # Syntax highlighting for light and dark modes
    "pygments_light_style": "igor",
    "pygments_dark_style": "nord-darker",
}

# Edit on GitHub button
html_context = {
    "github_user": "zeidk",
    "github_repo": "enpm818t-spring-2026-docs",
    "github_version": "main",
    "doc_path": "docs/source",
    "default_mode": "dark",
}

numfig = True
numfig_format = {
    "pseudocode": "Algorithm %s",
}

html_static_path = ["_static"]
master_doc = "index"

html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css",
    "my.css",
]

# Use MathJax 2 instead of 3 for file:// protocol compatibility
mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS-MML_HTMLorMML"
