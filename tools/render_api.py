#!/usr/bin/env python3
"""Extract the API reference body and contents tree from the locally-built
_code_source.html.

Generates two committed artifacts:

* ``docs/source/assignments/final_project/_code_api.html`` -- the article
  body, embedded by ``code.rst`` via ``.. raw:: html``.
* ``docs/source/_templates/api-toc-sidebar.html`` -- a Jinja sidebar
  template (configured in ``conf.py``'s ``html_sidebars`` for the code
  page) that renders a search box plus a hierarchical TOC linking to
  every autodoc anchor on the page.

Workflow:

    cd docs && sphinx-build -b html source build/html
    python tools/render_api.py
    git add docs/source/assignments/final_project/_code_api.html \\
            docs/source/_templates/api-toc-sidebar.html
    git commit && git push
"""

import html as html_lib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "docs/build/html/assignments/final_project/_code_source.html"
BODY_DST = REPO / "docs/source/assignments/final_project/_code_api.html"
SIDEBAR_DST = REPO / "docs/source/_templates/api-toc-sidebar.html"


def collect_signatures(content: str) -> list[tuple[str, str]]:
    """Return ``(fqn, kind)`` pairs for every autodoc signature in body order.

    Each ``<dl class="py X">`` marks the kind (class, method, function,
    attribute, ...) of the immediately following
    ``<dt class="sig sig-object py" id="...">``, so a single linear pass
    is enough to label every signature.
    """
    pattern = re.compile(
        r'<dl class="py (?P<kind>\w+)">'
        r'|<dt class="sig sig-object py" id="(?P<id>[^"]+)">'
    )
    sigs: list[tuple[str, str]] = []
    current_kind: str | None = None
    for m in pattern.finditer(content):
        if m.group("kind"):
            current_kind = m.group("kind")
        else:
            sigs.append((m.group("id"), current_kind or ""))
    return sigs


def render_toc(sigs: list[tuple[str, str]]) -> str:
    """Render the hierarchical TOC <ul> tree (no <details>, no wrapper)."""
    if not sigs:
        return ""

    sig_ids = {sig for sig, _ in sigs}

    def parent(sig_id: str) -> tuple[str, str]:
        parts = sig_id.split(".")
        for i in range(len(parts) - 1, 0, -1):
            cand = ".".join(parts[:i])
            if cand in sig_ids:
                return cand, "sig"
        return ".".join(parts[:-1]), "module"

    modules: dict[str, list[tuple[str, str]]] = {}
    members: dict[str, list[tuple[str, str]]] = {}
    module_order: list[str] = []
    seen: set[str] = set()

    for sig_id, kind in sigs:
        par, par_kind = parent(sig_id)
        if par_kind == "sig":
            members.setdefault(par, []).append((sig_id, kind))
        else:
            if par not in seen:
                seen.add(par)
                module_order.append(par)
            modules.setdefault(par, []).append((sig_id, kind))

    def leaf(fqn: str) -> str:
        return html_lib.escape(fqn.rsplit(".", 1)[-1])

    def kind_badge(kind: str) -> str:
        # Module-level callables come through as "function" from
        # Sphinx; relabel to "method" in the TOC for terminology
        # consistency with class members.
        if kind == "function":
            kind = "method"
        return (
            f' <span class="api-toc-kind">{html_lib.escape(kind)}</span>'
            if kind else ""
        )

    spacer = '<span class="api-toc-toggle-spacer" aria-hidden="true"></span>'
    toggle = (
        '<button class="api-toc-toggle" type="button" '
        'aria-expanded="false" aria-label="Toggle members"></button>'
    )

    out: list[str] = ['<ul class="api-toc-tree">']
    for mod in module_order:
        out.append(
            '<li class="api-toc-module">'
            f'<code class="api-toc-module-name">{html_lib.escape(mod)}</code>'
        )
        out.append('<ul class="api-toc-symbols">')
        for sig_id, kind in modules[mod]:
            children = members.get(sig_id)
            link = (
                f'<a href="#{html_lib.escape(sig_id)}">{leaf(sig_id)}</a>'
            )
            row = (
                '<span class="api-toc-row">'
                f"{toggle if children else spacer}{link}{kind_badge(kind)}"
                "</span>"
            )
            li_class = (
                "api-toc-symbol api-toc-has-children"
                if children else "api-toc-symbol"
            )
            out.append(
                f'<li class="{li_class}" '
                f'data-fqn="{html_lib.escape(sig_id.lower())}">'
                f"{row}"
            )
            if children:
                out.append('<ul class="api-toc-members" hidden>')
                for child_id, child_kind in children:
                    child_link = (
                        f'<a href="#{html_lib.escape(child_id)}">'
                        f"{leaf(child_id)}</a>"
                    )
                    out.append(
                        '<li class="api-toc-symbol" '
                        f'data-fqn="{html_lib.escape(child_id.lower())}">'
                        '<span class="api-toc-row">'
                        f"{spacer}{child_link}{kind_badge(child_kind)}"
                        "</span></li>"
                    )
                out.append("</ul>")
            out.append("</li>")
        out.append("</ul></li>")
    out.append("</ul>")
    return "\n".join(out)


SIDEBAR_TEMPLATE = """\
{# Auto-generated by tools/render_api.py. Do not edit by hand. #}
<div class="sidebar-primary-item api-toc-sidebar">
  <p class="sidebar-header-items__title" role="heading" aria-level="2">
    API reference
  </p>
  <div class="api-toc-search-wrap">
    <input
      id="api-toc-search"
      type="search"
      placeholder="Filter symbols..."
      autocomplete="off"
      spellcheck="false"
    />
    <span id="api-toc-search-count" aria-live="polite"></span>
  </div>
__TOC__
</div>
<script>
(function () {
  function init() {
    var tocRoot = document.querySelector('.api-toc-sidebar .api-toc-tree');
    if (!tocRoot) return;
    var input = document.getElementById('api-toc-search');
    var count = document.getElementById('api-toc-search-count');

    var leaves = Array.from(tocRoot.querySelectorAll('li[data-fqn]'));
    var classRows = Array.from(
      tocRoot.querySelectorAll('li.api-toc-has-children')
    );
    var bodyTopDls = Array.from(
      document.querySelectorAll('article.bd-article dl.py')
    ).filter(function (dl) {
      return !dl.parentElement.closest('dl.py');
    });

    function setExpanded(li, open) {
      var btn = li.querySelector(':scope > .api-toc-row > .api-toc-toggle');
      var ul = li.querySelector(':scope > ul.api-toc-members');
      if (!btn || !ul) return;
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) ul.removeAttribute('hidden');
      else ul.setAttribute('hidden', '');
    }

    /* Click a caret to toggle just that class. */
    tocRoot.addEventListener('click', function (e) {
      var btn = e.target.closest('.api-toc-toggle');
      if (!btn || !tocRoot.contains(btn)) return;
      e.preventDefault();
      var li = btn.closest('li.api-toc-has-children');
      if (!li) return;
      var open = btn.getAttribute('aria-expanded') === 'true';
      setExpanded(li, !open);
    });

    function filterDl(dl, query) {
      var ownDt = dl.querySelector(':scope > dt.sig.sig-object.py');
      var match = !query || (ownDt && ownDt.id.toLowerCase().indexOf(query) !== -1);
      var children = dl.querySelectorAll(':scope > dd > dl.py');
      var anyChild = false;
      children.forEach(function (child) {
        if (filterDl(child, query)) anyChild = true;
      });
      var visible = match || anyChild;
      dl.style.display = visible ? '' : 'none';
      return visible;
    }

    function filterTocList(ul, query) {
      var anyVisible = false;
      Array.from(ul.children).forEach(function (li) {
        var fqn = (li.getAttribute('data-fqn') || '').toLowerCase();
        var hasOwnLink = !!fqn;
        var leafMatch = hasOwnLink && (!query || fqn.indexOf(query) !== -1);
        var nestedUl = li.querySelector(':scope > ul');
        var nestedAny = false;
        if (nestedUl) nestedAny = filterTocList(nestedUl, query);
        var visible = leafMatch || nestedAny;
        li.style.display = visible ? '' : 'none';
        if (visible) anyVisible = true;
      });
      return anyVisible;
    }

    function run() {
      var query = input ? input.value.trim().toLowerCase() : '';
      bodyTopDls.forEach(function (dl) { filterDl(dl, query); });
      filterTocList(tocRoot, query);

      /* Expand classes whose subtree has a visible match; collapse all
         when the query is cleared. */
      classRows.forEach(function (li) {
        if (!query) {
          setExpanded(li, false);
        } else if (li.style.display !== 'none') {
          setExpanded(li, true);
        }
      });

      if (!count) return;
      if (!query) {
        count.textContent = '';
        return;
      }
      var visibleLeaves = leaves.filter(function (li) {
        return li.style.display !== 'none';
      }).length;
      count.textContent = visibleLeaves === 1
        ? '1 symbol'
        : visibleLeaves + ' symbols';
    }

    if (input) {
      input.addEventListener('input', run);
      input.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { input.value = ''; run(); input.blur(); }
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>
"""


def main() -> int:
    if not SRC.exists():
        sys.stderr.write(
            f"{SRC} not found.\n"
            f"Build the docs first:\n"
            f"  cd docs && sphinx-build -b html source build/html\n"
        )
        return 1

    html = SRC.read_text(encoding="utf-8")

    article = re.search(
        r'<article[^>]*class="bd-article"[^>]*>(.*?)</article>',
        html,
        re.DOTALL,
    )
    if not article:
        sys.stderr.write('Could not find <article class="bd-article">.\n')
        return 1

    content = article.group(1).strip()
    content = re.sub(
        r'^\s*<section[^>]*>\s*<h1>.*?</h1>',
        '',
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = re.sub(r'</section>\s*$', '', content).strip()

    sigs = collect_signatures(content)
    toc_html = render_toc(sigs)

    BODY_DST.write_text(
        "<!-- Auto-generated by tools/render_api.py. Do not edit. -->\n"
        + content + "\n",
        encoding="utf-8",
    )
    SIDEBAR_DST.parent.mkdir(parents=True, exist_ok=True)
    SIDEBAR_DST.write_text(
        SIDEBAR_TEMPLATE.replace("__TOC__", toc_html),
        encoding="utf-8",
    )

    print(
        f"Wrote {BODY_DST.relative_to(REPO)} ({len(content):,} bytes)\n"
        f"Wrote {SIDEBAR_DST.relative_to(REPO)} "
        f"({len(sigs)} symbols, {toc_html.count('<a href=')} TOC links)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
