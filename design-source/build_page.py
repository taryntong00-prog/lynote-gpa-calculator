from pathlib import Path
import re, json, shutil, hashlib
from lxml import html

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[1]
SOURCE = ROOT / 'source/demo'
DIST = ROOT / 'dist'
ASSETS = DIST / 'assets'
PAGE = DIST / 'gpa-calculator'
PAGE.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)

for item in ['vendor', 'fonts', 'tokens', 'assets']:
    shutil.copytree(SOURCE / item, ASSETS / 'demo' / item, dirs_exist_ok=True)
for item in ['support.js', '_ds_bundle.js', 'styles.css']:
    shutil.copy2(SOURCE / item, ASSETS / 'demo' / item)
# The original demo's typefaces are self-hosted. No external font request is needed.
demo_css = ASSETS / 'demo/styles.css'
demo_css.write_text(re.sub(r"@import url\([^;]+;", '', demo_css.read_text()))
shared = ROOT / 'source/shared'
shutil.copytree(ROOT / 'source/related', ASSETS / 'related', dirs_exist_ok=True)
shutil.copy2(shared / 'styles.css', ASSETS / 'shared.css')
for item in ['inter-400.woff2', 'inter-500.woff2', 'inter-600.woff2', 'inter-700.woff2', 'lynote.png']:
    shutil.copy2(shared / item, ASSETS / item)
for item in ['gpa.css', 'guide.js']:
    shutil.copy2(ROOT / item, ASSETS / item)

previous = html.fromstring((ROOT / 'source/navigation-source.html').read_text())
header = previous.xpath('//header')[0]
footer = previous.xpath('//footer')[0]
urls = {
    '../word-counter/': 'https://taryntong00-prog.github.io/lynote-word-counter/word-counter/',
    '../invisible-character/': 'https://taryntong00-prog.github.io/lynote-invisible-character/invisible-character/',
    'http://localhost:8765/learning-path-generator': 'https://taryntong00-prog.github.io/lynote-learning-path-generator/learning-path-generator/',
}
for tree in [header, footer]:
    for element in tree.iter():
        if element.get('href') in urls:
            element.set('href', urls[element.get('href')])
        if element.get('aria-current'):
            element.attrib.pop('aria-current')
header_text = html.tostring(header, encoding='unicode')
header_text = header_text.replace('Count words, characters and reading time.', 'Count words and characters instantly.').replace('Copy blank text and invisible spaces.', 'Copy blank text for names, bios and messages.').replace('Turn your materials into step-by-step learning.', 'Turn your study materials into a personalized learning path.')
gpa_nav = '<a class="tools-mega-link" href="#tool"><span class="tools-mega-copy"><span class="tools-mega-title">GPA Calculator <span class="nav-new-badge">New</span></span><span class="tools-mega-description">Calculate semester and cumulative GPA from grades and credits.</span></span></a>'
header_text = header_text.replace('<h3>Study &amp; Notes</h3>', '<h3>Study &amp; Notes</h3>' + gpa_nav)
footer_text = html.tostring(footer, encoding='unicode').replace('<h3>Learn</h3>', '<h3>Learn</h3><a href="#tool">GPA Calculator</a>')

original = (SOURCE / 'index.html').read_text()
start = original.index('<section style="max-width:960px;')
end = original.index('</section>', start) + len('</section>')
template = original[start:end]
template = re.sub(r'^<section[^>]+>', '<section class="calc-section" aria-label="GPA calculator"><div class="calculator-frame"><div class="calculator-cap"><span><svg viewBox="0 0 24 24"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 11h2m4 0h2M8 15h2m4 0h2"/></svg>GPA calculator</span><small>College &amp; high school</small></div>', template)
template = template.replace('</section>', '</div></section>')
template = template.replace('<div style="background:#fff;border:1px solid var(--border);', '<div class="calc-grid" data-mode="{{ mode }}" style="background:#fff;border:1px solid var(--border);', 1)
template = template.replace('<div style="min-width:0;border-bottom:', '<div class="input-pane" style="min-width:0;border-bottom:', 1)
template = template.replace('<div style="min-width:0;background:var(--gray-50);', '<div class="result-pane" aria-label="Your GPA results" aria-live="polite" style="min-width:0;background:var(--gray-50);', 1)
template = template.replace('<div style="display:flex;flex-direction:column;gap:8px;">', '<div class="rows-wrap" style="display:flex;flex-direction:column;gap:8px;">', 1)
template = template.replace('<div style="display:grid;grid-template-columns:{{ cols }};gap:8px;font-size:12px;', '<div class="course-headings" style="display:grid;grid-template-columns:{{ cols }};gap:8px;font-size:12px;')
template = template.replace('<div style="display:grid;grid-template-columns:{{ cols }};gap:8px;align-items:center;">', '<div class="course-fields" style="display:grid;grid-template-columns:{{ cols }};gap:8px;align-items:center;">')
template = template.replace('onClick="{{ r.onDel }}"', 'class="delete-course" onClick="{{ r.onDel }}"')
template = template.replace('<div style="display:flex;align-items:center;justify-content:space-between;gap:10px;min-height:32px;">', '<div class="year-header" style="display:flex;align-items:center;justify-content:space-between;gap:10px;min-height:32px;">')
template = re.sub(r'<x-import component-from-global-scope="LynoteDesignSystem_5037c1.SegmentedTabs"[^>]*></x-import>', '<div class="mode-tabs" role="tablist" aria-label="Education level"><button type="button" role="tab" aria-selected="{{ isCollege }}" onClick="{{ chooseCollege }}">College</button><button type="button" role="tab" aria-selected="{{ isHs }}" onClick="{{ chooseHs }}">High school</button></div>', template)
template = re.sub(r'<span(?=[^>]*onClick=)', '<span role="button" tabindex="0"', template)
template = template.replace('<input value="{{ r.name }}"', '<input aria-label="{{ r.nameLabel }}" value="{{ r.name }}"')
template = template.replace('<select value="{{ r.grade }}"', '<select aria-label="{{ r.gradeLabel }}" value="{{ r.grade }}"')
template = template.replace('<select value="{{ r.credits }}"', '<select aria-label="{{ r.creditsLabel }}" value="{{ r.credits }}"')
template = template.replace('<select value="{{ r.level }}"', '<select aria-label="{{ r.levelLabel }}" value="{{ r.level }}"')
template = template.replace('name="{{ r', 'name="{{ r')
template = template.replace('title="Remove class"', 'title="Remove class" aria-label="Remove class"')
template = template.replace('Classes this term', 'Classes this term')

logic_tag = re.search(r'<script type="text/x-dc"[^>]*>.*?</script>', original, re.S).group(0)
logic_tag = logic_tag.replace("cols:hs?'minmax(0,1fr) 84px 70px 100px 28px':'minmax(0,1fr) 92px 76px 28px'", "cols:hs?'minmax(110px,1fr) 76px 64px 90px 24px':'minmax(0,1fr) 82px 66px 24px'")
logic_tag = logic_tag.replace('mode:s.mode,setMode:this.setMode,isHs:hs,isCollege:!hs,', "mode:s.mode,setMode:this.setMode,chooseCollege:()=>this.setMode('college'),chooseHs:()=>this.setMode('hs'),isHs:hs,isCollege:!hs,")
logic_tag = logic_tag.replace("return {...r,ref:this.rowRef(r.id)", "return {...r,nameLabel:'Course '+(i+1),gradeLabel:'Grade for '+(r.name||'class '+(i+1)),creditsLabel:'Credits for '+(r.name||'class '+(i+1)),levelLabel:'Level for '+(r.name||'class '+(i+1)),ref:this.rowRef(r.id)")
logic_tag = logic_tag.replace('src="assets/logo-lockup.png"', 'src="../assets/demo/assets/logo-lockup.png"')
old_mount = "componentDidMount(){ if(this.props.demo&&this.props.demo!=='live') this.applyDemo(this.props.demo); }"
new_mount = """componentDidMount(){
    if(this.props.demo&&this.props.demo!=='live') this.applyDemo(this.props.demo);
    this._guide=e=>{
      const action=e.detail&&e.detail.action;
      if(action==='hs'){ this.setMode('hs'); return; }
      if(action==='previous'){ this.setState({showPrev:true},()=>{this.gpaRef.current&&this.gpaRef.current.focus({preventScroll:true});}); return; }
      if(action==='scale'){ this.setState({scaleOpen:true}); return; }
      if(action==='sample'){
        const target=this.state.mode==='college'?this.state:((this.state.saved||{}).college||{});
        const hasEntries=(target.rows||[]).some(r=>r.name||r.grade||r.credits)||target.prevGpa||target.prevCr;
        const load=()=>{this.setMode('college');setTimeout(()=>this.trySample(),0);};
        if(!hasEntries){load();return;}
        const dialog=document.getElementById('sample-dialog');
        if(dialog){dialog.returnValue='cancel';dialog.addEventListener('close',()=>{if(dialog.returnValue==='replace')load();},{once:true});dialog.showModal();}
      }
    };
    window.addEventListener('gpa-guide-action',this._guide);
  }"""
assert old_mount in logic_tag
logic_tag = logic_tag.replace(old_mount, new_mount).replace('componentWillUnmount(){ clearTimeout(this._t); }', "componentWillUnmount(){ clearTimeout(this._t); window.removeEventListener('gpa-guide-action',this._guide); }")

guide = (ROOT / 'guide.html').read_text()
marketing = (ROOT / 'marketing.html').read_text()
faq_marker = '<section class="guide-section gpa-faq"'
assert guide.count(faq_marker) == 1
guide = guide.replace(faq_marker, marketing + '\n' + faq_marker)
parsed_guide = html.fromstring('<div>'+guide+'</div>')
faq = {'@context':'https://schema.org','@type':'FAQPage','mainEntity':[]}
for item in parsed_guide.xpath('//*[@id="faq"]/details'):
    faq['mainEntity'].append({'@type':'Question','name':item.find('summary').text_content(),'acceptedAnswer':{'@type':'Answer','text':item.find('p').text_content()}})

page = '''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Free GPA Calculator for College &amp; High School | Lynote</title><meta name="description" content="Calculate your GPA from grades and credits. Check the GPA scale and follow examples for semester, cumulative, weighted and unweighted GPA."><meta name="theme-color" content="#865eff"><link rel="icon" href="../assets/lynote.png"><link rel="stylesheet" href="../assets/demo/styles.css"><link rel="stylesheet" href="../assets/shared.css"><link rel="stylesheet" href="../assets/gpa.css"><script src="../assets/demo/vendor/react.production.min.js"></script><script src="../assets/demo/vendor/react-dom.production.min.js"></script><script src="../assets/demo/support.js"></script><script src="../assets/demo/_ds_bundle.js"></script><script defer src="../assets/guide.js"></script></head><body class="gpa-page"><a class="sr-only" href="#main">Skip to content</a>'''
product_placeholder = '<section class="calc-section" aria-label="产品功能区"><div class="product-placeholder"><p>产品功能区，以 Molly 为准</p></div></section>'
page += header_text + '<main id="main"><section class="gpa-hero" id="tool"><div class="gpa-heading"><h1>Free <span>GPA Calculator</span></h1><p>Calculate your college or high school GPA from grades and credits.<br>Check your cumulative GPA or compare weighted and unweighted results.</p></div>' + product_placeholder + '</section>' + guide + '</main>' + footer_text
for script in ['vendor/react.production.min.js', 'vendor/react-dom.production.min.js', 'support.js', '_ds_bundle.js']:
    page = page.replace(f'<script src="../assets/demo/{script}"></script>', '')
page += '<script type="application/ld+json">' + json.dumps(faq,ensure_ascii=False) + '</script></body></html>'
for filename, attribute in [('gpa.css', 'href'), ('guide.js', 'src')]:
    version = hashlib.sha256((ASSETS / filename).read_bytes()).hexdigest()[:10]
    page = page.replace(f'{attribute}="../assets/{filename}"', f'{attribute}="../assets/{filename}?v={version}"')
(PAGE / 'index.html').write_text(page)
(DIST / 'index.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url=./gpa-calculator/"><title>Lynote GPA Calculator</title></head><body><a href="./gpa-calculator/">Open GPA Calculator</a></body></html>')
print('Built dist/gpa-calculator/index.html with product placeholder and GPA guide.')
