// guizang-ppt-editor.js v4 — add image & text, fixed selectors, drag, resize, save
(function(){
'use strict';

let editMode=false, currentSlide=0, slides=[], selectedEl=null;
let dragState=null, resizeState=null;

// ─── Inject styles ───
const S=document.createElement('style');
S.id='ed-styles';
S.textContent=`
#ed-bar{position:fixed;top:0;left:0;right:0;z-index:9999;display:flex;align-items:center;gap:8px;padding:8px 16px;background:rgba(15,23,42,.95);backdrop-filter:blur(12px);color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:13px;box-shadow:0 2px 12px rgba(0,0,0,.3)}
#ed-bar .s{width:1px;height:24px;background:rgba(255,255,255,.15);margin:0 4px}
#ed-bar button{display:flex;align-items:center;gap:5px;padding:6px 12px;border:1px solid rgba(255,255,255,.15);border-radius:6px;background:rgba(255,255,255,.06);color:#e2e8f0;font-size:13px;cursor:pointer;transition:all .15s ease;white-space:nowrap}
#ed-bar button:hover{background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.25)}
#ed-bar button.on{background:#3b82f6;border-color:#3b82f6;color:#fff}
#ed-bar button.sav{background:#059669;border-color:#059669;color:#fff}
#ed-bar .t{font-weight:600;font-size:14px;margin-right:8px}
#ed-bar .n{color:#94a3b8;font-variant-numeric:tabular-nums}
#ed-bar .sp{flex:1}
#ed-bar kbd{font-size:11px;padding:1px 5px;border-radius:3px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);color:#94a3b8}

.ed-sel{outline:2px solid #3b82f6!important;outline-offset:3px;position:relative;overflow:visible!important}
.ed-sel::before{content:'';position:absolute;top:4px;left:4px;width:24px;height:24px;background:#3b82f6;border-radius:6px;z-index:600;cursor:grab;opacity:.85;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2'%3E%3Ccircle cx='9' cy='5' r='1'/%3E%3Ccircle cx='9' cy='12' r='1'/%3E%3Ccircle cx='9' cy='19' r='1'/%3E%3Ccircle cx='15' cy='5' r='1'/%3E%3Ccircle cx='15' cy='12' r='1'/%3E%3Ccircle cx='15' cy='19' r='1'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:center;background-size:14px}
.ed-drag{opacity:.85;z-index:500;cursor:grabbing!important;box-shadow:0 8px 32px rgba(0,0,0,.25);outline-color:#f59e0b!important}
.ed-text{outline-color:#10b981!important;background:rgba(16,185,129,.04);cursor:text}

/* Resize handles */
.ed-rz{position:absolute;width:12px;height:12px;background:#fff;border:2px solid #3b82f6;border-radius:2px;z-index:600;display:none}
.ed-rz-tl{top:-6px;left:-6px;cursor:nw-resize}.ed-rz-tr{top:-6px;right:-6px;cursor:ne-resize}
.ed-rz-bl{bottom:-6px;left:-6px;cursor:sw-resize}.ed-rz-br{bottom:-6px;right:-6px;cursor:se-resize}
.ed-sel>.ed-rz{display:block}

/* Image overlay */
.ed-iover{position:absolute;inset:0;background:rgba(0,0,0,.35);display:none;align-items:center;justify-content:center;gap:8px;z-index:100;border-radius:4px}
.ed-sel>.ed-iover{display:flex}
.ed-ibtn{padding:6px 14px;background:rgba(0,0,0,.7);color:#fff;border:none;border-radius:6px;font-size:12px;cursor:pointer;font-family:inherit}
.ed-ibtn:hover{background:rgba(0,0,0,.85)}

/* New element styles */
.ed-new-img{position:absolute;background:#f1f5f9;border:2px dashed #94a3b8;border-radius:4px;overflow:hidden;z-index:50}
.ed-new-img img{width:100%;height:100%;object-fit:cover}
.ed-new-text{position:absolute;z-index:50;padding:12px 16px;background:rgba(255,255,255,.9);border:1px solid rgba(0,0,0,.08);border-radius:4px;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;font-size:18px;line-height:1.6;color:#1e293b;min-width:120px;min-height:40px;outline:none}
`;
document.head.appendChild(S);

// ─── Toolbar ───
document.body.insertAdjacentHTML('beforeend',`
<div id="ed-bar">
  <span class="t">PPT 编辑器</span><div class="s"></div>
  <button id="eb-edit"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg> 编辑</button>
  <div class="s"></div>
  <button id="eb-prev">◀</button><span class="n" id="eb-num">1/17</span><button id="eb-next">▶</button>
  <div class="s"></div>
  <button id="eb-addimg"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg> 🖼 添加图片</button>
  <button id="eb-addtxt"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/></svg> 📝 添加文本</button>
  <button id="eb-del" style="color:#f87171">🗑 删除页</button>
  <div class="sp"></div>
  <span style="color:#64748b;font-size:12px"><kbd>E</kbd>编辑 <kbd>←→</kbd>翻页 <kbd>DblClick</kbd>文字 <kbd>Del</kbd>删除</span>
  <div class="s"></div>
  <input type="file" id="ed-addimg-fi" accept="image/*" style="display:none">
  <div class="s"></div>
  <button id="eb-save" class="sav">💾 保存</button>
</div>
<input type="file" id="ed-fi" accept="image/*" style="display:none">
`);

const $=id=>document.getElementById(id);
const btnE=$('eb-edit'),btnP=$('eb-prev'),btnN=$('eb-next'),btnS=$('eb-save'),btnD=$('eb-del'),fi=$('ed-fi');
const btnAddImg=$('eb-addimg'),btnAddTxt=$('eb-addtxt'),addImgFi=$('ed-addimg-fi');
let pendingImgEl=null;

// ─── Init ───
function init(){
  slides=Array.from(document.querySelectorAll('#deck .slide'));
  updNum();
  if(typeof window.go==='function'&&!window._origGo){
    window._origGo=window.go;
    window.go=n=>{if(editMode)return;window._origGo(n);syncIdx()};
  }
}
function syncIdx(){
  const d=document.getElementById('deck');if(!d)return;
  const m=(d.style.transform||'').match(/translateX\((-?\d+)/);
  if(m)currentSlide=Math.min(Math.round(Math.abs(+m[1])/100),slides.length-1);
  updNum();
}
function updNum(){const e=$('eb-num');if(e)e.textContent=`${currentSlide+1}/${slides.length}`}

// ─── Determine if an element is a meaningful content block ───
function isContentBlock(el){
  if(!el||el===document||el===document.body||el.tagName==='SCRIPT'||el.tagName==='STYLE')return false;
  if(el.id==='editor-toolbar'||el.id==='ed-bar'||el.id==='ed-fi')return false;
  const tag=el.tagName;
  // Skip tiny inline elements
  if(tag==='BR'||tag==='HR'||tag==='SVG'||tag==='USE'||tag==='CANVAS')return false;
  // Skip elements inside toolbar
  if(el.closest('#ed-bar'))return false;
  // Must be inside current slide
  if(editMode && !slides[currentSlide]?.contains(el))return false;
  // Has content: text, images, or children with content
  const hasText=el.textContent.trim().length>1;
  const hasImg=el.querySelector('img');
  const isImg=el.tagName==='IMG'||el.classList.contains('frame-img')||el.classList.contains('img-slot');
  return hasText||hasImg||isImg;
}

// Walk up to find the nearest meaningful editable block
function findEditableBlock(target, slide){
  let el=target;
  const skip=new Set(['SECTION','SCRIPT','STYLE','SVG','USE','CANVAS','NAV']);
  while(el && el!==slide && !skip.has(el.tagName)){
    if(el.matches('.chrome,.foot'))return null; // don't make header/footer draggable
    // Stop at meaningful layout containers or content elements
    if(el.matches(
      '.frame-img,figure.tile,.img-slot,'+
      '.stat-card,.step,.callout,'+
      '.pipeline,.pipeline-section'
    ))return el;
    // Match bare <img> only if NOT inside a .frame-img or figure.tile
    if(el.matches('img') && !el.closest('.frame-img') && !el.closest('figure.tile'))return el;
    // Match newly added elements
    if(el.matches('.ed-new-img,.ed-new-text'))return el;
    // Stop at text elements with direct content
    if(el.matches(
      '.h-hero,.h-xl,.h-sub,.h-md,.h1-zh,.h2-zh,.h3-zh,'+
      '.kicker,.lead,.meta,.tag,.sign,'+
      '.display,.display-zh,.body-zh,.body-serif,'+
      '.stat-label,.stat-nb,.stat-note,.stat-unit,'+
      '.step-nb,.step-title,.step-desc,'+
      '.q-big,.callout-src,.meta-row,'+
      '.pipeline-label,'+
      'p,ul,li,h1,h2,h3,h4'
    ) && el !== slide)return el;
    el=el.parentElement;
  }
  return null;
}

// ─── Edit mode ───
function syncSlide(){
  const d=document.getElementById('deck');if(!d)return;
  const m=(d.style.transform||'').match(/translateX\((-?\d+)/);
  if(m)currentSlide=Math.min(Math.round(Math.abs(+m[1])/100),slides.length-1);
}
function toggle(){
  editMode=!editMode;
  btnE.classList.toggle('on',editMode);
  btnE.querySelector('svg').nextSibling.textContent=editMode?' 编辑中':' 编辑';
  if(editMode){
    syncSlide(); // ensure currentSlide matches actual position
    slides[currentSlide]&&(slides[currentSlide].style.overflow='visible');
    addImgControls(slides[currentSlide]);
  } else {
    deselect();
    // Clean up ALL slides (user may have visited multiple slides)
    slides.forEach(s=>{cleanupImgControls(s);s.style.overflow='';});
  }
}

function addImgControls(slide){
  if(!slide)return;
  slide.querySelectorAll('.frame-img,figure.tile').forEach(el=>{
    if(el.querySelector('.ed-rz'))return;
    ['tl','tr','bl','br'].forEach(p=>{
      const h=document.createElement('div');
      h.className='ed-rz ed-rz-'+p;
      h.addEventListener('mousedown',onResizeStart);
      el.appendChild(h);
    });
    const ov=document.createElement('div');
    ov.className='ed-iover';
    ov.innerHTML='<button class="ed-ibtn" data-a="replace">📷 替换</button><button class="ed-ibtn" data-a="delete">🗑 删除</button>';
    ov.querySelectorAll('.ed-ibtn').forEach(b=>{
      b.addEventListener('click',e=>{
        e.stopPropagation();
        if(b.dataset.a==='replace')doReplaceImg(el);
        else doDeleteImg(el);
      });
    });
    el.appendChild(ov);
  });
}

function cleanupImgControls(slide){
  if(!slide)return;
  slide.querySelectorAll('.ed-rz,.ed-iover').forEach(e=>e.remove());
  slide.querySelectorAll('.ed-sel,.ed-drag,.ed-text').forEach(e=>{
    e.classList.remove('ed-sel','ed-drag','ed-text');
    e.removeAttribute('contenteditable');
  });
}

// ─── Selection via event delegation ───
document.addEventListener('mousedown',function(e){
  if(!editMode)return;
  if(e.target.closest('#ed-bar')||e.target.closest('.ed-iover'))return;

  const slide=slides[currentSlide];
  if(!slide||!slide.contains(e.target))return;

  const block=findEditableBlock(e.target,slide);
  if(!block)return;

  // If clicking the drag handle (::before pseudo on .ed-sel)
  const sel=document.querySelector('.ed-sel');
  if(sel){
    const rect=sel.getBoundingClientRect();
    if(e.clientX>=rect.left&&e.clientX<=rect.left+28&&e.clientY>=rect.top&&e.clientY<=rect.top+28){
      startDrag(e,sel);
      return;
    }
  }

  select(block);
  e.preventDefault();
},true);

// Double click = text edit
document.addEventListener('dblclick',function(e){
  if(!editMode)return;
  const slide=slides[currentSlide];if(!slide)return;
  const block=findEditableBlock(e.target,slide);
  if(!block)return;
  // Don't text-edit image containers
  if(block.matches('.frame-img,figure.tile,.img-slot,img'))return;
  select(block);
  block.setAttribute('contenteditable','true');
  block.classList.add('ed-text');
  block.focus();
  // Select all text inside
  const range=document.createRange();
  range.selectNodeContents(block);
  const sel=window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
},true);

function select(el){
  deselect();
  selectedEl=el;
  el.classList.add('ed-sel');
}
function deselect(){
  if(selectedEl){
    selectedEl.classList.remove('ed-sel','ed-drag','ed-text');
    selectedEl.removeAttribute('contenteditable');
    selectedEl=null;
  }
}

// Click outside = deselect
document.addEventListener('mousedown',function(e){
  if(!editMode)return;
  const slide=slides[currentSlide];
  if(!slide)return;
  if(e.target.closest('#ed-bar'))return;
  if(!slide.contains(e.target)){deselect();return;}
  // If click is on slide background (not on a block)
  if(!findEditableBlock(e.target,slide))deselect();
});

// ─── Drag ───
function startDrag(e,el){
  e.preventDefault();e.stopPropagation();
  const tx=parseFloat(el.dataset.edX)||0;
  const ty=parseFloat(el.dataset.edY)||0;
  dragState={el,sx:e.clientX,sy:e.clientY,ox:tx,oy:ty,moved:false};
  el.classList.add('ed-drag');
  document.addEventListener('mousemove',onDrag);
  document.addEventListener('mouseup',endDrag);
}
function onDrag(e){
  if(!dragState)return;
  const dx=e.clientX-dragState.sx, dy=e.clientY-dragState.sy;
  if(!dragState.moved&&(Math.abs(dx)<4&&Math.abs(dy)<4))return;
  dragState.moved=true;
  const nx=dragState.ox+dx, ny=dragState.oy+dy;
  dragState.el.dataset.edX=nx;
  dragState.el.dataset.edY=ny;
  dragState.el.style.transform=`translate(${nx}px,${ny}px)`;
}
function endDrag(){
  if(dragState)dragState.el.classList.remove('ed-drag');
  dragState=null;
  document.removeEventListener('mousemove',onDrag);
  document.removeEventListener('mouseup',endDrag);
}

// ─── Resize ───
function onResizeStart(e){
  e.preventDefault();e.stopPropagation();
  const el=e.target.closest('.frame-img,figure.tile,.ed-new-img');
  if(!el)return;
  resizeState={el,sx:e.clientX,sy:e.clientY,w:el.offsetWidth,h:el.offsetHeight};
  document.addEventListener('mousemove',onResize);
  document.addEventListener('mouseup',endResize);
}
function onResize(e){
  if(!resizeState)return;
  const dx=e.clientX-resizeState.sx, dy=e.clientY-resizeState.sy;
  resizeState.el.style.width=Math.max(60,resizeState.w+dx)+'px';
  resizeState.el.style.height=Math.max(40,resizeState.h+dy)+'px';
  resizeState.el.style.flex='none';
}
function endResize(){
  resizeState=null;
  document.removeEventListener('mousemove',onResize);
  document.removeEventListener('mouseup',endResize);
}

// ─── Image actions ───
function doReplaceImg(el){
  pendingImgEl=el;
  fi.onchange=e=>{
    const f=e.target.files[0];if(!f||!pendingImgEl)return;
    const r=new FileReader();
    r.onload=ev=>{
      let img=pendingImgEl.querySelector('img');
      if(!img){img=document.createElement('img');img.style.cssText='width:100%;height:100%;object-fit:cover;object-position:top center';pendingImgEl.prepend(img);}
      img.src=ev.target.result;img.style.display='';
    };
    r.readAsDataURL(f);fi.value='';
  };
  fi.click();
}
function doDeleteImg(el){el.style.display='none';deselect();}

// ─── Navigation ───
function nav(d){
  if(editMode){cleanupImgControls(slides[currentSlide]);deselect();}
  currentSlide=Math.max(0,Math.min(slides.length-1,currentSlide+d));
  if(window._origGo)window._origGo(currentSlide);
  updNum();
  if(editMode)addImgControls(slides[currentSlide]);
}
function delSlide(){
  if(slides.length<=1)return;
  if(editMode){cleanupImgControls(slides[currentSlide]);deselect();}
  slides[currentSlide].remove();
  slides=Array.from(document.querySelectorAll('#deck .slide'));
  document.getElementById('deck').style.width=(slides.length*100)+'vw';
  const nav=document.getElementById('nav');nav.innerHTML='';
  slides.forEach((_,i)=>{const b=document.createElement('button');b.className='dot';b.dataset.i=i;b.onclick=()=>{if(!editMode)nav(i-currentSlide)};nav.appendChild(b)});
  currentSlide=Math.min(currentSlide,slides.length-1);
  if(window._origGo)window._origGo(currentSlide);
  updNum();
  if(editMode)addImgControls(slides[currentSlide]);
}

// ─── Save ───
function save(){
  const wasEdit=editMode;
  if(editMode)toggle();

  // Clone the document to avoid modifying visible DOM
  const clone=document.cloneNode(true);

  // Remove editor artifacts from clone
  clone.querySelectorAll('#ed-bar,#ed-fi,#ed-addimg-fi').forEach(e=>e.remove());
  clone.querySelectorAll('#ed-styles').forEach(e=>e.remove());
  clone.querySelectorAll('.ed-rz,.ed-iover').forEach(e=>e.remove());
  clone.querySelectorAll('.ed-sel,.ed-drag,.ed-text').forEach(e=>{
    e.classList.remove('ed-sel','ed-drag','ed-text');
    e.removeAttribute('contenteditable');
  });
  // Clean up new elements: remove editor-specific class, keep content
  clone.querySelectorAll('.ed-new-img').forEach(e=>{
    e.classList.remove('ed-new-img');
  });
  clone.querySelectorAll('.ed-new-text').forEach(e=>{
    e.classList.remove('ed-new-text');
    e.removeAttribute('contenteditable');
  });
  // Remove editor data attributes (keep transform for position changes)
  clone.querySelectorAll('[data-ed-x]').forEach(el=>{
    // Convert data-ed-x/ed-y transform to inline style position
    // Already applied via style.transform, just clean data attrs
    el.removeAttribute('data-ed-x');
    el.removeAttribute('data-ed-y');
  });
  // Remove any editor script
  clone.querySelectorAll('script').forEach(s=>{
    if(s.textContent.includes('guizang-ppt-editor'))s.remove();
  });

  const html='<!DOCTYPE html>\n'+clone.documentElement.outerHTML;
  const blob=new Blob([html],{type:'text/html;charset=utf-8'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download='index-edited.html';
  a.click();
  URL.revokeObjectURL(a.href);

  if(wasEdit)toggle();
}

// ─── Keyboard ───
document.addEventListener('keydown',e=>{
  const typing=document.activeElement?.getAttribute('contenteditable')==='true';
  if(e.key==='e'&&!typing&&!e.ctrlKey&&!e.metaKey){e.preventDefault();toggle();}
  if(e.key==='s'&&(e.ctrlKey||e.metaKey)){e.preventDefault();save();}
  if(!editMode&&!typing){
    if(e.key==='ArrowLeft')nav(-1);
    if(e.key==='ArrowRight')nav(1);
  }
  if(e.key==='Escape'){
    if(editMode){
      if(selectedEl?.classList.contains('ed-text')){
        selectedEl.classList.remove('ed-text');
        selectedEl.removeAttribute('contenteditable');
      }else if(selectedEl){deselect();}
      else toggle();
    }
  }
  if(e.key==='Delete'&&editMode&&selectedEl&&!typing){
    selectedEl.style.display='none';deselect();
  }
});

// ─── Wire buttons ───
btnE.onclick=toggle;
btnP.onclick=()=>nav(-1);
btnN.onclick=()=>nav(1);
btnS.onclick=save;
btnD.onclick=delSlide;

// ─── Add Image ───
btnAddImg.onclick=function(){
  if(!editMode)toggle();
  addImgFi.onchange=function(e){
    const f=e.target.files[0];if(!f)return;
    const r=new FileReader();
    r.onload=function(ev){
      const slide=slides[currentSlide];if(!slide)return;
      slide.style.position=slide.style.position||'relative';
      const div=document.createElement('div');
      div.className='ed-new-img';
      div.style.cssText='width:320px;height:220px;left:50%;top:50%;transform:translate(-50%,-50%)';
      const img=document.createElement('img');
      img.src=ev.target.result;
      img.style.cssText='width:100%;height:100%;object-fit:cover';
      div.appendChild(img);
      // Add resize handles
      ['tl','tr','bl','br'].forEach(function(p){
        const h=document.createElement('div');
        h.className='ed-rz ed-rz-'+p;
        h.addEventListener('mousedown',onResizeStart);
        div.appendChild(h);
      });
      // Add overlay with replace/delete
      const ov=document.createElement('div');
      ov.className='ed-iover';
      ov.innerHTML='<button class="ed-ibtn" data-a="replace">📷 替换</button><button class="ed-ibtn" data-a="delete">🗑 删除</button>';
      ov.querySelectorAll('.ed-ibtn').forEach(function(b){
        b.addEventListener('click',function(e){
          e.stopPropagation();
          if(b.dataset.a==='replace')doReplaceImg(div);
          else doDeleteImg(div);
        });
      });
      div.appendChild(ov);
      slide.appendChild(div);
      select(div);
      addImgFi.value='';
    };
    r.readAsDataURL(f);
  };
  addImgFi.click();
};

// ─── Add Text ───
btnAddTxt.onclick=function(){
  if(!editMode)toggle();
  const slide=slides[currentSlide];if(!slide)return;
  slide.style.position=slide.style.position||'relative';
  const div=document.createElement('div');
  div.className='ed-new-text';
  div.style.cssText='left:50%;top:50%;transform:translate(-50%,-50%)';
  div.textContent='双击编辑文本';
  slide.appendChild(div);
  select(div);
  // Auto-enter text edit mode
  div.setAttribute('contenteditable','true');
  div.classList.add('ed-text');
  // Select the placeholder text
  const range=document.createRange();
  range.selectNodeContents(div);
  const sel=window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  div.focus();
};

// ─── Boot ───
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);
else init();
setTimeout(init,600);
})();
