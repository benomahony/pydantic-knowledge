// pydantic-knowledge runtime. Every page is complete HTML; this only enhances it.
(() => {
  const shared = window.PYDANTIC_KNOWLEDGE_DATA;
  if (!shared) return;
  const body = document.body;
  const single = body.dataset.target === 'single';
  const prefix = body.dataset.prefix || '';
  const byId = Object.fromEntries(shared.concepts.map(c => [c.id, c]));
  const pages = document.querySelector('.pages');
  const store = (kind, key) => {
    const area = kind === 'local' ? window.localStorage : window.sessionStorage;
    return {
      get() { try { return JSON.parse(area.getItem(key)); } catch { return null; } },
      set(value) { try { value == null ? area.removeItem(key) : area.setItem(key, JSON.stringify(value)); } catch { /* storage unavailable */ } },
    };
  };
  const profileStore = store('local', 'pydantic-knowledge-profile:' + shared.title);
  const journeyStore = store('session', 'pydantic-knowledge-journey:' + shared.title);
  const focusStore = store('session', 'pydantic-knowledge-focus:' + shared.title);
  const href = (id, fragment) => single ? '#' + id + (fragment ? '--' + fragment : '') : prefix + byId[id].href + (fragment ? '#' + fragment : '');
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const humanise = kind => kind.replaceAll('_', ' ');
  let current = body.dataset.page || shared.home;
  const pageEl = () => single ? document.getElementById(current) : document.querySelector('.page');

  // --- Single-file routing: CSS :target already works without JS; this keeps state in sync.
  function route() {
    if (!single) return;
    const hash = decodeURIComponent(location.hash.slice(1));
    const target = hash && document.getElementById(hash);
    const page = target?.closest('.page');
    current = page ? page.dataset.concept : shared.home;
    pages.dataset.current = current;
    pages.querySelectorAll('.page.is-current').forEach(p => p.classList.remove('is-current'));
    document.getElementById(current)?.classList.add('is-current');
    document.title = byId[current].title + ' · ' + shared.title;
    const links = [...document.querySelectorAll('.sidebar .nav-link')];
    links.forEach(a => { a.toggleAttribute('aria-current', a.dataset.concept === current); if (a.dataset.concept === current) a.setAttribute('aria-current', 'page'); });
    // A page can sit under a goal and under its domain; open its canonical (last) place.
    const canonical = links.filter(a => a.dataset.concept === current).at(-1);
    let d = canonical?.closest('details');
    while (d) { d.open = true; d = d.parentElement.closest('details'); }
    if (!page || target === page) window.scrollTo(0, 0);
  }

  // --- Shared widgets are moved into the current page's slots.
  const widgets = {
    profile: document.getElementById('profile'),
    decision: document.getElementById('decision'),
    strip: document.getElementById('journey-strip'),
    next: document.getElementById('journey-next'),
  };
  function mount() {
    const page = pageEl();
    if (!page) return;
    const put = (slot, el) => { const s = page.querySelector(slot); if (s && el && el.parentElement !== s) s.append(el); };
    if (page.hasAttribute('data-adaptive')) put('.profile-slot', widgets.profile);
    else if (widgets.profile) document.getElementById('widgets').append(widgets.profile);
    put('.decision-slot', widgets.decision);
    put('.journey-slot', widgets.strip);
    put('.next-slot', widgets.next);
  }

  // --- Contextual composition (mirrors compose.py) over server-rendered blocks.
  const KIND_ORDER = { definition: 0, mental_model: 1, procedure: 2, example: 3, failure: 4, tradeoff: 5, note: 6, reference: 7 };
  const CONTEXT = ['intent', 'experience', 'preference', 'depth'];
  const selects = Object.fromEntries(CONTEXT.map(k => [k, document.getElementById(k)]));
  const list = (el, name) => (el.dataset[name] || '').split(' ').filter(Boolean);
  function score(el, ctx) {
    let s = Number(el.dataset.weight || 0);
    const pairs = [['intents', ctx.intent, 8, -20], ['experiences', ctx.experience, 4, -4], ['preferences', ctx.preference, 3, -2], ['depths', ctx.depth, 3, -2]];
    for (const [name, value, hit, miss] of pairs) { const v = list(el, name); if (v.length) s += v.includes(value) ? hit : miss; }
    return s;
  }
  function applyProfile() {
    const page = pageEl();
    const doc = page?.querySelector('.doc-body');
    if (!doc) return;
    const profile = profileStore.get();
    const blocks = [...doc.querySelectorAll(':scope > .knowledge-block')];
    if (!doc._order) doc._order = [...doc.children];
    const tailored = profile && page.hasAttribute('data-adaptive');
    if (!tailored) {
      doc.dataset.view = 'complete';
      blocks.forEach(b => { b.hidden = false; });
      doc._order.forEach(el => doc.append(el));
    } else {
      doc.dataset.view = 'tailored';
      const scored = blocks.map(b => [score(b, profile), b]).filter(([s]) => s >= -2);
      scored.sort((a, b) => b[0] - a[0] || KIND_ORDER[a[1].dataset.kind] - KIND_ORDER[b[1].dataset.kind] || a[1].dataset.block.localeCompare(b[1].dataset.block));
      const chosen = scored.slice(0, { quick: 3, normal: 6, deep: 100 }[profile.depth]);
      chosen.sort((a, b) => KIND_ORDER[a[1].dataset.kind] - KIND_ORDER[b[1].dataset.kind] || b[0] - a[0] || a[1].dataset.block.localeCompare(b[1].dataset.block));
      const keep = new Set(chosen.map(([, b]) => b));
      blocks.forEach(b => { b.hidden = !keep.has(b); });
      // Authored order is replaced by reading order; figures and related links stay after the first block.
      const others = doc._order.filter(el => !blocks.includes(el));
      const sequence = chosen.map(([, b]) => b);
      [...sequence.slice(0, 1), ...others.filter(el => !el.classList.contains('related')), ...sequence.slice(1), ...others.filter(el => el.classList.contains('related'))].forEach(el => doc.append(el));
    }
    const summary = document.getElementById('profile-summary');
    const complete = document.getElementById('profile-complete');
    const change = widgets.profile?.querySelector('.profile-change > summary');
    if (summary) {
      summary.textContent = tailored ? 'Viewing for: ' + CONTEXT.map(k => shared.labels[k][profile[k]]).join(' · ') : 'Complete page';
      change.textContent = tailored ? 'Change' : 'Tailor this page';
      complete.hidden = !tailored;
    }
    if (profile) CONTEXT.forEach(k => { if (selects[k]) selects[k].value = profile[k]; });
    syncToc();
  }
  CONTEXT.forEach(k => selects[k]?.addEventListener('change', () => {
    profileStore.set(Object.fromEntries(CONTEXT.map(n => [n, selects[n].value])));
    applyProfile();
  }));
  document.getElementById('profile-complete')?.addEventListener('click', () => { profileStore.set(null); applyProfile(); });
  document.addEventListener('click', e => {
    const open = widgets.profile?.querySelector('.profile-change[open]');
    if (open && !open.contains(e.target)) open.open = false;
  });

  // --- On this page: hide entries for hidden blocks; highlight the section in view.
  let observer;
  function syncToc() {
    const page = pageEl();
    const links = [...(page?.querySelectorAll('.toc a[href^="#"]') || [])];
    links.forEach(a => {
      const target = document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)));
      a.parentElement.hidden = !!target?.closest('.knowledge-block[hidden], .doc-body[data-view="complete"] > .knowledge-block:not([data-complete])');
    });
    observer?.disconnect();
    if (!links.length || !('IntersectionObserver' in window)) return;
    const headings = links.map(a => document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)))).filter(Boolean);
    observer = new IntersectionObserver(() => {
      let active = headings[0];
      for (const h of headings) if (h.offsetParent && h.getBoundingClientRect().top < 140) active = h;
      links.forEach(a => a.toggleAttribute('aria-current', a.getAttribute('href') === '#' + active.id));
      const label = page.querySelector('.toc-current'); if (label) label.textContent = active.id.endsWith('top') ? 'Overview' : active.textContent;
      links.forEach(a => { if (a.hasAttribute('aria-current')) a.setAttribute('aria-current', 'true'); });
    }, { rootMargin: '-64px 0px -60% 0px', threshold: [0, 1] });
    headings.forEach(h => observer.observe(h));
  }

  // --- Search: concepts and their sections; ordinary retrieval, no model.
  const input = document.getElementById('search');
  const results = document.getElementById('search-results');
  const entries = [
    ...shared.concepts.map(c => ({ title: c.title, context: c.summary, href: single ? c.href : prefix + c.href, terms: (c.title + ' ' + c.aliases.join(' ')).toLowerCase(), extra: c.summary.toLowerCase(), boost: 2 })),
    ...shared.sections.map(([i, title, url]) => ({ title, context: shared.concepts[i].title, href: single ? url : prefix + url, terms: title.toLowerCase(), extra: '', boost: 0 })),
  ];
  let selected = -1;
  function search() {
    const q = input.value.trim().toLowerCase();
    if (!q) { results.innerHTML = '<p class="empty">Search pages and sections by title.</p>'; return; }
    const words = q.split(/\s+/);
    const hits = entries.map(e => {
      let s = 0;
      if (e.terms.startsWith(q)) s += 6; else if (e.terms.includes(q)) s += 4;
      for (const w of words) { if (e.terms.includes(w)) s += 2; else if (e.extra.includes(w)) s += 1; else return [0, e]; }
      return [s + e.boost, e];
    }).filter(([s]) => s > 0).sort((a, b) => b[0] - a[0]).slice(0, 14);
    // Group like the upstream search dialog: a page, then its matching sections.
    const groups = new Map();
    for (const [, e] of hits) {
      const page = e.boost ? e.title : e.context;
      if (!groups.has(page)) groups.set(page, { page: null, sections: [] });
      if (e.boost) groups.get(page).page = e; else groups.get(page).sections.push(e);
    }
    let i = 0;
    const row = (e, cls, label, note) => `<a role="option" class="${cls}" href="${esc(e.href)}" aria-selected="${i++ === 0}"><strong>${esc(label)}</strong>${note ? `<small>${esc(note)}</small>` : ''}</a>`;
    results.innerHTML = hits.length ? [...groups.entries()].map(([page, g]) => {
      const head = g.page ? row(g.page, 'sr-page', page, g.page.context) : `<div class="sr-page sr-label"><strong>${esc(page)}</strong></div>`;
      return `<div class="sr-group">${head}${g.sections.map(e => row(e, 'sr-section', e.title)).join('')}</div>`;
    }).join('') : '<div class="empty">No results</div>';
    selected = hits.length ? 0 : -1;
  }
  function move(delta) {
    const options = [...results.querySelectorAll('a')];
    if (!options.length) return;
    selected = (selected + delta + options.length) % options.length;
    options.forEach((o, i) => o.setAttribute('aria-selected', String(i === selected)));
    options[selected].scrollIntoView({ block: 'nearest' });
  }
  const dialog = document.getElementById('search-dialog');
  function openSearch() { if (!dialog.open) dialog.showModal(); input.focus(); input.select(); }
  function closeSearch() { if (dialog.open) dialog.close(); }
  document.getElementById('search-open')?.addEventListener('click', openSearch);
  dialog?.querySelector('.sd-close')?.addEventListener('click', closeSearch);
  dialog?.addEventListener('click', e => { if (e.target === dialog) closeSearch(); });
  input?.addEventListener('input', search);
  input?.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
    else if (e.key === 'Enter') { const a = results.querySelectorAll('a')[selected]; if (a) { e.preventDefault(); a.click(); } }
  });
  results?.addEventListener('click', e => { if (e.target.closest('a')) closeSearch(); });
  document.addEventListener('keydown', e => {
    if (((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') || (e.key === '/' && !/input|textarea|select/i.test(document.activeElement.tagName))) {
      e.preventDefault(); openSearch();
    }
  });

  // --- Journeys: a path chosen on the "How these docs are organised" page follows the reader.
  function renderStrip() {
    const strip = widgets.strip;
    if (!strip) return;
    const active = journeyStore.get();
    const journey = (shared.journeys || []).find(j => j.id === active);
    const steps = journey ? journey.steps.map(s => s.concept_id) : [];
    if (!journey || !steps.includes(current)) { strip.replaceChildren(); return; }
    strip.innerHTML = `<strong>${esc(journey.title)}</strong><ol>${journey.steps.map(s => `<li><a href="${esc(href(s.concept_id))}"${s.concept_id === current ? ' aria-current="step"' : ''}>${esc(byId[s.concept_id].title)}</a></li>`).join('')}</ol><button type="button">Leave path</button>`;
    strip.querySelector('button').addEventListener('click', () => { journeyStore.set(null); renderStrip(); });
  }
  document.addEventListener('click', e => {
    const start = e.target.closest('[data-start-journey]');
    if (start) { journeyStore.set(start.dataset.startJourney); setTimeout(renderStrip); }
    const focus = e.target.closest('[data-focus]');
    if (focus) focusStore.set(focus.dataset.focus);
  });

  // --- Concept map.
  function ontology(root) {
    const svg = root.querySelector('.o-svg');
    const detail = root.querySelector('.o-detail');
    const defaultDetail = detail.innerHTML;
    const toolbar = root.querySelector('.o-toolbar');
    const picker = root.querySelector('.o-journey-picker');
    const filter = root.querySelector('[data-filter]');
    toolbar.hidden = false;
    const nodes = [...svg.querySelectorAll('.o-node')];
    const edges = [...svg.querySelectorAll('.o-edge')];
    const labels = Object.fromEntries([...svg.querySelectorAll('.o-label')].map(l => [l.dataset.edge, l]));
    const jobs = [...svg.querySelectorAll('.o-job')];
    const jobLinks = [...svg.querySelectorAll('.o-joblink')];
    const state = { view: 'concepts', node: null, job: null, journey: shared.journeys?.[0]?.id || null };
    const relsFor = id => shared.relationships.filter(r => r.source === id || r.target === id);

    const visible = edge => {
      const value = filter.value;
      if (value === 'all') return true;
      const kinds = edge.dataset.kinds.split(' ');
      return value === 'structural' ? edge.classList.contains('is-structural') : kinds.includes(value);
    };

    function jobConcepts(jobId) {
      const job = shared.jobs.find(j => j.id === jobId);
      const ids = [...job.expected_concepts];
      shared.journeys.filter(j => j.job_id === jobId).forEach(j => ids.push(...j.steps.map(s => s.concept_id)));
      return [...new Set(ids)];
    }

    function apply() {
      root.dataset.view = state.view;
      root.querySelectorAll('.o-views button').forEach(b => b.setAttribute('aria-selected', String(b.dataset.view === state.view)));
      picker.hidden = state.view !== 'journeys';
      edges.forEach(e => { const show = visible(e); e.classList.toggle('is-filtered', !show); labels[e.dataset.edge]?.classList.toggle('is-filtered', !show); });
      const near = new Set();
      svg.classList.remove('has-focus', 'has-route');
      edges.forEach(e => { e.classList.remove('is-near'); labels[e.dataset.edge]?.classList.remove('is-near'); });
      if (state.view === 'concepts' && state.node) {
        near.add(state.node);
        edges.forEach(e => {
          if (visible(e) && (e.dataset.source === state.node || e.dataset.target === state.node)) {
            e.classList.add('is-near'); labels[e.dataset.edge]?.classList.add('is-near');
            near.add(e.dataset.source); near.add(e.dataset.target);
          }
        });
        svg.classList.add('has-focus');
      }
      if (state.view === 'jobs' && state.job) { jobConcepts(state.job).forEach(id => near.add(id)); svg.classList.add('has-route'); }
      if (state.view === 'journeys' && state.journey) {
        shared.journeys.find(j => j.id === state.journey).steps.forEach(s => near.add(s.concept_id));
        svg.classList.add('has-route');
      }
      nodes.forEach(n => { n.classList.toggle('is-near', near.has(n.dataset.id)); n.classList.toggle('is-selected', state.view === 'concepts' && n.dataset.id === state.node); });
      jobs.forEach(j => { const on = j.dataset.job === state.job; j.classList.toggle('is-selected', on); j.classList.toggle('is-dim', !!state.job && !on); j.setAttribute('aria-pressed', String(on)); });
      jobLinks.forEach(l => { l.classList.toggle('is-active', l.dataset.job === state.job); l.classList.toggle('is-dim', !!state.job && l.dataset.job !== state.job); });
      svg.querySelectorAll('.o-journey').forEach(g => g.classList.toggle('is-active', state.view === 'journeys' && g.dataset.journey === state.journey));
      picker.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.journey === state.journey)));
      fit(false);
      describe();
    }

    function describe() {
      if (state.view === 'concepts' && state.node) {
        const c = byId[state.node];
        const pairKey = r => r.source + '>' + r.target;
        const structuralPairs = new Set(relsFor(c.id).filter(r => r.kind !== 'related_to').map(pairKey));
        const rels = relsFor(c.id).filter(r => r.source !== r.target && (r.kind !== 'related_to' || !structuralPairs.has(pairKey(r))))
          .sort((a, b) => (a.kind === 'related_to') - (b.kind === 'related_to'));
        const seen = new Set();
        const chips = rels.map(r => {
          const out = r.source === c.id, other = byId[out ? r.target : r.source], label = r.label || humanise(r.kind);
          const key = (out ? '>' : '<') + other.id + label;
          if (seen.has(key)) return '';
          seen.add(key);
          return `<li><span class="o-rel">${out ? esc(label) + ' →' : '← ' + esc(label)}</span> <button type="button" data-select="${esc(other.id)}">${esc(other.title)}</button></li>`;
        }).join('');
        detail.innerHTML = `<p class="o-sel-meta">${esc(c.domain || c.kind)}</p><p class="o-sel-title"><a href="${esc(href(c.id))}">${esc(c.title)}</a></p>${c.summary ? `<p>${esc(c.summary)}</p>` : ''}${chips ? `<ul class="o-sel-rels">${chips}</ul>` : ''}<p><a class="o-open" href="${esc(href(c.id))}">Open ${esc(c.title)} →</a></p>`;
      } else if (state.view === 'jobs') {
        if (!state.job) { detail.innerHTML = '<p class="o-hint">Jobs to be done are the outcomes readers arrive with. Select one to see the journeys that realise it and the concepts they rely on.</p>'; return; }
        const job = shared.jobs.find(j => j.id === state.job);
        const routes = shared.journeys.filter(j => j.job_id === job.id);
        const concepts = jobConcepts(job.id).map(id => `<li><a class="o-chip" href="${esc(href(id))}">${esc(byId[id].title)}</a></li>`).join('');
        detail.innerHTML = `<p class="o-sel-meta">Job to be done</p><p class="o-sel-title">${esc(job.title)}</p><p>${esc(job.outcome)}</p>${routes.length ? `<p>Realised by ${routes.map(j => `<button type="button" class="o-link" data-show-journey="${esc(j.id)}">${esc(j.title)}</button>`).join(', ')}</p>` : ''}<ul class="o-sel-rels">${concepts}</ul>`;
      } else if (state.view === 'journeys' && state.journey) {
        const j = shared.journeys.find(x => x.id === state.journey);
        const job = shared.jobs.find(x => x.id === j.job_id);
        detail.innerHTML = `<p class="o-sel-meta">Journey${job ? ' · realises “' + esc(job.title) + '”' : ''}</p><p class="o-sel-title">${esc(j.title)}</p><p>${esc(j.summary)}</p><ol class="o-steps">${j.steps.map(s => `<li><a href="${esc(href(s.concept_id))}">${esc(byId[s.concept_id].title)}</a> <small>${esc(s.reason)}</small></li>`).join('')}</ol><p><a class="o-open" href="${esc(href(j.steps[0].concept_id))}" data-start-journey="${esc(j.id)}">Start this journey →</a></p>`;
      } else {
        detail.innerHTML = defaultDetail;
      }
    }

    // View box: fit to the current layer; zoom and pan only change the view box.
    let box = null;
    const parse = s => s.split(' ').map(Number);
    function setBox(b) { box = b; svg.setAttribute('viewBox', b.map(v => v.toFixed(1)).join(' ')); }
    function fit(force = true) {
      const target = parse(state.view === 'jobs' ? svg.dataset.jobsBox : svg.dataset.conceptsBox);
      if (force || !box || box._view !== state.view) { setBox(target); box._view = state.view; }
    }
    function zoom(factor, cx, cy) {
      const [x, y, w, h] = box;
      const nw = Math.min(Math.max(w * factor, 240), parse(svg.dataset.jobsBox)[2] * 1.5), nh = nw * h / w;
      cx ??= x + w / 2; cy ??= y + h / 2;
      const view = box._view;
      setBox([cx - (cx - x) * nw / w, cy - (cy - y) * nh / h, nw, nh]);
      box._view = view;
    }
    root.querySelectorAll('[data-zoom]').forEach(b => b.addEventListener('click', () => {
      if (b.dataset.zoom === 'fit') { state.node = null; state.job = null; apply(); fit(true); }
      else zoom(b.dataset.zoom === 'in' ? 0.8 : 1.25);
    }));
    svg.addEventListener('wheel', e => {
      if (!(e.ctrlKey || e.metaKey)) return;
      e.preventDefault();
      const pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
      const p = pt.matrixTransform(svg.getScreenCTM().inverse());
      zoom(e.deltaY > 0 ? 1.1 : 0.9, p.x, p.y);
    }, { passive: false });
    let drag = null;
    svg.addEventListener('pointerdown', e => {
      if (e.button !== 0 || e.target.closest('.o-node, .o-job')) return;
      drag = { x: e.clientX, y: e.clientY, box: [...box], moved: false, view: box._view };
    });
    window.addEventListener('pointermove', e => {
      if (!drag) return;
      const scale = drag.box[2] / svg.getBoundingClientRect().width;
      const dx = (e.clientX - drag.x) * scale, dy = (e.clientY - drag.y) * scale;
      if (Math.abs(dx) + Math.abs(dy) > 2) { drag.moved = true; root.querySelector('.o-canvas').classList.add('is-panning'); }
      setBox([drag.box[0] - dx, drag.box[1] - dy, drag.box[2], drag.box[3]]); box._view = drag.view;
    });
    window.addEventListener('pointerup', () => {
      if (drag && !drag.moved && state.view === 'concepts' && state.node) { state.node = null; apply(); }
      drag = null; root.querySelector('.o-canvas').classList.remove('is-panning');
    });

    // Selecting a concept highlights it; selecting it again (or a modified click) opens its page.
    nodes.forEach(n => n.addEventListener('click', e => {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
      if (state.view === 'concepts' && state.node === n.dataset.id) return;
      e.preventDefault();
      if (state.view !== 'concepts') state.view = 'concepts';
      state.node = n.dataset.id;
      apply();
    }));
    jobs.forEach(j => {
      const choose = () => { state.job = state.job === j.dataset.job ? null : j.dataset.job; apply(); };
      j.addEventListener('click', choose);
      j.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); choose(); } });
    });
    detail.addEventListener('click', e => {
      const sel = e.target.closest('[data-select]');
      if (sel) { state.node = sel.dataset.select; apply(); svg.querySelector(`.o-node[data-id="${CSS.escape(state.node)}"]`)?.focus(); }
      const show = e.target.closest('[data-show-journey]');
      if (show) { state.view = 'journeys'; state.journey = show.dataset.showJourney; apply(); }
    });
    root.querySelectorAll('.o-views button').forEach(b => b.addEventListener('click', () => { state.view = b.dataset.view; apply(); fit(true); }));
    picker.querySelectorAll('button').forEach(b => b.addEventListener('click', () => { state.journey = b.dataset.journey; apply(); }));
    filter.addEventListener('change', apply);
    root.addEventListener('keydown', e => { if (e.key === 'Escape') { state.node = null; state.job = null; apply(); } });

    const focus = focusStore.get();
    if (focus?.startsWith('job:') && jobs.some(j => j.dataset.job === focus.slice(4))) { state.view = 'jobs'; state.job = focus.slice(4); focusStore.set(null); }
    else if (focus && byId[focus] && nodes.some(n => n.dataset.id === focus)) { state.node = focus; focusStore.set(null); }
    apply();
    fit(true);
    if (state.node) root.scrollIntoView({ block: 'start' });
  }

  const COPY = '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3" fill="none" stroke="currentColor" stroke-width="1.7"/></svg>';
  function addCopyButtons(page) {
    page.querySelectorAll('.highlight:not([data-copy])').forEach(block => {
      const pre = block.querySelector('pre');
      if (!pre) return;
      block.dataset.copy = '';
      const button = document.createElement('button');
      button.type = 'button'; button.className = 'copy-code'; button.innerHTML = COPY; button.setAttribute('aria-label', 'Copy code');
      button.style.top = (pre.offsetTop + 10) + 'px';
      button.addEventListener('click', async () => {
        const code = pre.cloneNode(true);
        code.querySelectorAll('.code-annotation').forEach(b => b.remove());
        try {
          await navigator.clipboard.writeText(code.textContent.replace(/\s+$/, ''));
          button.classList.add('is-copied'); button.setAttribute('aria-label', 'Copied');
          setTimeout(() => { button.classList.remove('is-copied'); button.setAttribute('aria-label', 'Copy code'); }, 1500);
        } catch { /* clipboard unavailable */ }
      });
      block.append(button);
    });
  }

  function enhancePage() {
    const page = pageEl();
    if (page) addCopyButtons(page);
    page?.querySelectorAll('[data-ontology]').forEach(root => { if (!root._ready) { root._ready = true; ontology(root); } });
  }

  function refresh() {
    route();
    mount();
    applyProfile();
    renderStrip();
    enhancePage();
    window.dispatchEvent(new CustomEvent('knowledge-concept', { detail: current }));
  }
  if (single) {
    window.PYDANTIC_KNOWLEDGE_OPEN = id => { location.hash = id; };
    window.addEventListener('hashchange', refresh);
  }
  window.PYDANTIC_KNOWLEDGE_PAGE = { id: current };
  refresh();
})();
