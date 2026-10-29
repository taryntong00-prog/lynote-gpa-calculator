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

// Review carousel: three cards on desktop, two on tablet, one on mobile.
const reviewsTrack=$('#gpa-reviews-track');
if(reviewsTrack){
  const carousel=reviewsTrack.closest('.gpa-reviews-carousel');
  const previous=carousel.querySelector('.review-previous'),next=carousel.querySelector('.review-next');
  const dots=carousel.querySelector('.review-dots'),status=carousel.querySelector('.review-page-status');
  const cards=Array.from(reviewsTrack.children);
  let perView=0,pageCount=0,currentPage=0;
  const stride=()=>cards[0].getBoundingClientRect().width+parseFloat(getComputedStyle(reviewsTrack).columnGap);
  const moveTo=page=>{
    const bounded=Math.max(0,Math.min(pageCount-1,page));
    reviewsTrack.scrollTo({left:bounded*perView*stride(),behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'});
  };
  const update=()=>{
    currentPage=Math.max(0,Math.min(pageCount-1,Math.round(reviewsTrack.scrollLeft/(stride()*perView))));
    previous.disabled=currentPage===0;next.disabled=currentPage===pageCount-1;
    Array.from(dots.children).forEach((dot,index)=>dot.setAttribute('aria-current',String(index===currentPage)));
    const start=currentPage*perView+1,end=Math.min(cards.length,start+perView-1);
    status.textContent=`Examples ${start}–${end} of ${cards.length}`;
  };
  const resize=()=>{
    const visible=parseInt(getComputedStyle(carousel).getPropertyValue('--reviews-per-view'),10)||1;
    if(visible!==perView){
      const firstVisible=currentPage*perView;
      perView=visible;pageCount=Math.ceil(cards.length/perView);dots.replaceChildren();
      for(let i=0;i<pageCount;i++){
        const dot=document.createElement('button');dot.type='button';dot.setAttribute('aria-label',`Show examples ${i*perView+1}–${Math.min(cards.length,(i+1)*perView)}`);dot.setAttribute('aria-controls','gpa-reviews-track');dot.addEventListener('click',()=>moveTo(i));dots.append(dot);
      }
      reviewsTrack.scrollTo({left:Math.floor(firstVisible/perView)*perView*stride(),behavior:'instant'});
    }
    update();
  };
  previous.addEventListener('click',()=>moveTo(currentPage-1));next.addEventListener('click',()=>moveTo(currentPage+1));
  reviewsTrack.addEventListener('scroll',update,{passive:true});
  reviewsTrack.addEventListener('keydown',event=>{
    if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
    event.preventDefault();moveTo(event.key==='Home'?0:event.key==='End'?pageCount-1:currentPage+(event.key==='ArrowRight'?1:-1));
  });
  new ResizeObserver(resize).observe(reviewsTrack);resize();
}
