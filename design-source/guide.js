'use strict';
const $=s=>document.querySelector(s);
const scrollTool=()=>$('#tool').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth',block:'start'});
const fireAction=action=>{window.dispatchEvent(new CustomEvent('gpa-guide-action',{detail:{action}}));scrollTool();};
document.querySelectorAll('[data-gpa-action]').forEach(button=>button.addEventListener('click',()=>fireAction(button.dataset.gpaAction)));
document.querySelectorAll('[data-tool-focus]').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('.nav-dropdown.open').forEach(el=>{el.classList.remove('open');el.querySelector('button').setAttribute('aria-expanded','false');});$('.site-header').classList.remove('menu-open');$('.mobile-toggle').setAttribute('aria-expanded','false');scrollTool();setTimeout(()=>$('#tool input')?.focus({preventScroll:true}),300);}));
document.querySelectorAll('.nav-dropdown').forEach(menu=>menu.querySelector('button').addEventListener('click',()=>{const wasOpen=menu.classList.contains('open');document.querySelectorAll('.nav-dropdown').forEach(el=>{el.classList.remove('open');el.querySelector('button').setAttribute('aria-expanded','false');});if(!wasOpen){menu.classList.add('open');menu.querySelector('button').setAttribute('aria-expanded','true');}}));
const closeMenus=()=>document.querySelectorAll('.nav-dropdown.open').forEach(el=>{el.classList.remove('open');el.querySelector('button').setAttribute('aria-expanded','false');});
document.addEventListener('click',event=>{if(!event.target.closest('.nav-dropdown'))closeMenus();});
$('.mobile-toggle').addEventListener('click',()=>{const open=$('.site-header').classList.toggle('menu-open');$('.mobile-toggle').setAttribute('aria-expanded',String(open));$('.mobile-toggle').setAttribute('aria-label',open?'Close menu':'Open menu');});
document.addEventListener('keydown',event=>{if(event.key==='Escape'){closeMenus();$('.site-header').classList.remove('menu-open');$('.mobile-toggle').setAttribute('aria-expanded','false');}if((event.key==='Enter'||event.key===' ')&&event.target.matches('#tool [role=button]')){event.preventDefault();event.target.click();}});
document.querySelectorAll('#college-example tbody tr').forEach(row=>row.addEventListener('click',()=>{document.querySelectorAll('#college-example tbody tr').forEach(el=>{el.classList.remove('selected');el.querySelector('button').setAttribute('aria-pressed','false');});row.classList.add('selected');row.querySelector('button').setAttribute('aria-pressed','true');$('#example-row-name').textContent=row.dataset.name;$('#example-points').textContent=row.dataset.points;$('#example-credits').textContent=row.dataset.credits;$('#example-total').textContent=row.dataset.total;}));
document.querySelectorAll('.gpa-faq details').forEach(details=>details.addEventListener('toggle',()=>{if(details.open)document.querySelectorAll('.gpa-faq details').forEach(other=>{if(other!==details)other.open=false;});}));
const relatedTrack=$('#related-tools-track');
if(relatedTrack){
  const previous=$('.previous-tools'),next=$('.next-tools');
  const updateRelatedButtons=()=>{
    previous.disabled=relatedTrack.scrollLeft<=2;
    next.disabled=relatedTrack.scrollLeft>=relatedTrack.scrollWidth-relatedTrack.clientWidth-2;
  };
  const moveRelated=direction=>{
    const first=relatedTrack.querySelector('li');
    const stride=first.getBoundingClientRect().width+parseFloat(getComputedStyle(relatedTrack).columnGap);
    const page=Math.max(1,Math.floor((relatedTrack.clientWidth+16)/stride));
    relatedTrack.scrollBy({left:direction*page*stride,behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'});
  };
  previous.addEventListener('click',()=>moveRelated(-1));
  next.addEventListener('click',()=>moveRelated(1));
  relatedTrack.addEventListener('scroll',updateRelatedButtons,{passive:true});
  new ResizeObserver(updateRelatedButtons).observe(relatedTrack);
  updateRelatedButtons();
}
