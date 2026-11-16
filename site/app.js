'use strict';
const $ = s => document.querySelector(s);
const M = CatalogModel;
const kindNames = {logos:'Logo / 标识',icons:'功能图标',legends:'图例',covers:'封面'};
const statusNames = {ready:'可用',draft:'候选',deprecated:'已替代',archived:'已归档',unlabeled:'未标注'};
const filterKeys = ['q','owner','series','component','function','platform','status','tag','kind'];
const defaults = {q:'',owner:'',series:'',component:'',function:'',platform:'',status:'',tag:'',kind:'',view:'assets',sort:'name',bg:'paper'};
let state = {...defaults}, items = [], registry = {owners:[],series:[],components:[],stats:{}}, toastTimer;
function el(tag,text,cls) { const n=document.createElement(tag); if(text!==undefined)n.textContent=text; if(cls)n.className=cls; return n; }
function nameFor(section,id,fallback='未分组') { return registry[section].find(x=>x.id===id)?.name || fallback; }
function option(value,text) { const n=el('option',text);n.value=value;return n; }
function notify(text) { $('#toast').textContent=text;$('#toast').classList.add('visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('visible'),2800); }
function assetURL(item) { return new URL(item.path,new URL('./',location.href)).href; }
async function copy(text) { try { await navigator.clipboard.writeText(text);notify('已复制，可以直接取用。'); } catch { const pre=el('pre',text);$('#detail-content').append(pre);notify('剪贴板不可用，请从详情下方手动复制。'); } }
function readState() { const p=new URLSearchParams(location.search);const next={...defaults};for(const key of Object.keys(defaults))next[key]=p.get(key)||defaults[key];if(!['assets','series'].includes(next.view))next.view='assets';if(!['paper','dark','checker'].includes(next.bg))next.bg='paper';if(!['name','newest'].includes(next.sort))next.sort='name';return next; }
function saveState() { const url=new URL(location.href);url.search='';for(const [key,value] of Object.entries(state))if(value&&value!==defaults[key])url.searchParams.set(key,value);history.replaceState(null,'',url); }
function clearFilters() { for(const key of filterKeys)state[key]=''; }
function navigateOwner(owner) { clearFilters();state.owner=owner;state.view='assets';render();closeMobile(); }
function navigateSeries(id) { const series=registry.series.find(x=>x.id===id);clearFilters();state.series=id;state.owner=series?.owner||'';state.view='assets';render();closeMobile(); }
function closeMobile(){document.body.classList.remove('nav-open');$('#mobile-nav').setAttribute('aria-expanded','false');}
function tree() {
  const container=$('#tree');container.replaceChildren();
  for(const owner of registry.owners.filter(x=>x.count>0)) {
    const section=el('div',undefined,'owner-group');
    const button=el('button',undefined,'owner-button');button.type='button';button.setAttribute('aria-pressed',String(state.owner===owner.id&&!state.series));if(state.owner===owner.id&&!state.series)button.classList.add('active');
    button.append(el('span',undefined,'folder-icon'),el('span',owner.name),el('span',String(owner.count),'side-count'));
    button.addEventListener('click',()=>navigateOwner(owner.id));section.append(button);
    const children=el('div',undefined,'series-nav');
    for(const series of registry.series.filter(x=>x.owner===owner.id&&x.count>0)) {
      const child=el('button');child.type='button';child.setAttribute('aria-pressed',String(state.series===series.id));if(state.series===series.id)child.classList.add('active');
      child.append(el('span',series.name.replace(owner.name+' ','')),el('span',String(series.count)));
      child.addEventListener('click',()=>navigateSeries(series.id));children.append(child);
    }
    section.append(children);container.append(section);
  }
  $('#nav-assets').classList.toggle('active',state.view==='assets'&&!state.owner&&!state.series);
  $('#nav-series').classList.toggle('active',state.view==='series');
}
function syncControls() {
  $('#search').value=state.q;$('#sort').value=state.sort;$('#background').value=state.bg;
  document.body.classList.toggle('bg-dark',state.bg==='dark');document.body.classList.toggle('bg-checker',state.bg==='checker');
  $('#view-assets').setAttribute('aria-pressed',String(state.view==='assets'));$('#view-series').setAttribute('aria-pressed',String(state.view==='series'));
  for(const b of $('#kinds').querySelectorAll('[data-kind]'))b.setAttribute('aria-pressed',String(b.dataset.kind===state.kind));
  for(const [field,label] of [['component','全部组件'],['function','全部功能'],['platform','全部平台']]) {
    const selected=state[field];const available=M.filter(items,{...state,[field]:''},registry);
    const values=new Map();
    for(const item of available) { const org=M.organization(item);const list=field==='component'?[org.component].filter(Boolean):(org[field==='function'?'functions':'platforms']||[]);for(const value of list)values.set(value,(values.get(value)||0)+1); }
    const select=$('#'+field);select.replaceChildren(option('',label));
    if(selected&&!values.has(selected))values.set(selected,0);
    for(const [value,count] of [...values.entries()].sort((a,b)=>a[0].localeCompare(b[0],'zh-CN')))select.append(option(value,`${field==='component'?nameFor('components',value,value):value} (${count})`));
    select.value=selected;
  }
  $('#status').value=state.status;
}
function chips() {
  const root=$('#active-filters');root.replaceChildren();
  const names={q:'搜索',owner:'归属',series:'系列',component:'组件',function:'功能',platform:'平台',status:'状态',tag:'标签',kind:'类型'};
  for(const key of filterKeys)if(state[key]) {
    let value=state[key];if(key==='owner')value=nameFor('owners',value,value);if(key==='series')value=value==='__unassigned__'?'未分组素材':nameFor('series',value,value);if(key==='component')value=nameFor('components',value,value);if(key==='status')value=statusNames[value]||value;if(key==='kind')value=kindNames[value]||value;
    const button=el('button',`${names[key]}：${value}`,'active-chip');button.append(el('span','×'));button.setAttribute('aria-label',`移除${names[key]}筛选`);
    button.addEventListener('click',()=>{state[key]='';if(key==='owner')state.series='';render();});root.append(button);
  }
}
function card(item) {
  const org=M.organization(item),status=M.status(item);const button=el('button',undefined,'asset-card');button.type='button';button.setAttribute('aria-label',`查看 ${item.name}`);
  const preview=el('div',undefined,'preview');preview.dataset.kind=item.kind;
  const img=el('img');img.src=item.path;img.alt=item.name;img.loading='lazy';
  const revision=item.tags.find(t=>t.startsWith('revision:'))?.slice(9);
  preview.append(el('span',item.path.split('.').pop().toUpperCase()+(revision?' · '+revision:''),'preview-format'),img,el('span','↗','preview-arrow'));
  const body=el('div',undefined,'card-info');body.append(el('h4',item.name,'card-title'));
  body.append(el('p',`${nameFor('owners',org.owner,'待整理')} / ${nameFor('components',org.component,'未标注组件')}`,'card-context'));
  const bottom=el('div',undefined,'card-bottom');const tags=M.visibleTags(item);bottom.append(el('span',tags.slice(0,2).map(t=>'#'+t).join('  '),'card-tags'));
  const badge=el('span',statusNames[status]||status,'state-badge');badge.dataset.state=status;bottom.append(badge);body.append(bottom);button.append(preview,body);button.addEventListener('click',()=>showDetail(item));return button;
}
function seriesCard(id,members) {
  const series=registry.series.find(x=>x.id===id)||{name:'未分组素材',description:'可在收录时补充系列信息。',owner:'unknown',accent:'sage'};
  const button=el('button',undefined,'series-card');button.type='button';button.setAttribute('aria-label',`浏览系列 ${series.name}`);
  const mosaic=el('div',undefined,'series-mosaic');mosaic.dataset.accent=series.accent||'sage';
  for(const item of members.slice(0,3)){const img=el('img');img.src=item.path;img.alt=item.name;img.loading='lazy';mosaic.append(img);}
  const body=el('div',undefined,'series-info');body.append(el('h3',series.name),el('p',series.description));
  const meta=el('div',undefined,'series-meta');meta.append(el('span',`${nameFor('owners',series.owner,'待整理')} · ${members.length} 份素材`),el('span','打开系列 ↗'));body.append(meta);button.append(mosaic,body);
  button.addEventListener('click',()=>{if(id==='unassigned'){state.series='__unassigned__';state.view='assets';render();}else navigateSeries(id);});return button;
}
function render() {
  saveState();tree();syncControls();chips();
  const selectedSeries=registry.series.find(x=>x.id===state.series),owner=registry.owners.find(x=>x.id===state.owner);
  const title=selectedSeries?.name||(state.series==='__unassigned__'?'未分组素材':null)||owner?.name||(state.view==='series'?'系列与合集':'全部素材');
  $('#page-title').textContent=title;$('#top-context').textContent=title;
  $('#page-description').textContent=selectedSeries?.description||owner?.description||(state.view==='series'?'把同一主题妥帖放在一起，再向细处探索。':'从系列出发，也可以按组件、功能和平台细找。');
  const list=M.filter(items,state,registry);const groups=M.groups(list);const results=$('#results');results.replaceChildren();
  if(state.view==='series') { const grid=el('div',undefined,'series-grid');for(const [id,members] of groups)grid.append(seriesCard(id,members));results.append(grid); }
  else for(const [id,members] of groups) {
    const section=el('section',undefined,'asset-group');const heading=el('div',undefined,'group-heading');const title=el('h3',nameFor('series',id,'未分组素材'));title.append(el('span',String(members.length).padStart(2,'0')));heading.append(title);
    if(!state.series&&id!=='unassigned'){const open=el('button','查看系列 ↗');open.addEventListener('click',()=>navigateSeries(id));heading.append(open);}
    const grid=el('div',undefined,'grid');for(const item of members)grid.append(card(item));section.append(heading,grid);results.append(section);
  }
  $('#count').textContent=state.view==='series'?`${groups.size} 个系列 · ${list.length} 份素材`:`共 ${list.length} 份素材 · ${groups.size} 个系列`;
  $('#empty').hidden=list.length>0;
  const tagCounts=new Map();for(const item of list)for(const tag of M.visibleTags(item))tagCounts.set(tag,(tagCounts.get(tag)||0)+1);
  $('#tag-list').replaceChildren();for(const [tag] of [...tagCounts.entries()].sort((a,b)=>b[1]-a[1]).slice(0,5)) {const b=el('button','#'+tag);b.setAttribute('aria-label',`筛选标签 ${tag}`);b.addEventListener('click',()=>{state.tag=tag;render();});$('#tag-list').append(b);}
}
function showDetail(item,updateHash=true) {
  const org=M.organization(item),status=M.status(item),body=$('#detail-content');body.replaceChildren();
  const preview=el('div',undefined,'detail-preview'),img=el('img');img.src=item.path;img.alt=item.name;preview.append(img);body.append(preview);
  const content=el('div',undefined,'detail-body');const heading=el('h2',item.name);heading.id='detail-title';
  content.append(el('div',`${nameFor('owners',org.owner,'待整理')} / ${nameFor('series',org.series,'未分组')} / ${nameFor('components',org.component,'未标注组件')}`,'detail-breadcrumb'),heading,el('p',item.description));
  const tags=el('div',undefined,'detail-tags');for(const tag of M.visibleTags(item)){const button=el('button','#'+tag);button.addEventListener('click',()=>{closeDetail();state.tag=tag;render();});tags.append(button);}content.append(tags);
  const values={'分类':kindNames[item.kind],'修订':item.tags.find(t=>t.startsWith('revision:'))?.slice(9)||'未标注','功能':(org.functions||[]).join(' / ')||'未标注','平台':(org.platforms||[]).join(' / ')||'未标注','状态':statusNames[status],'作者':item.author,'许可':item.license,'新增日期':item.created,'来源':item.source,'文件路径':item.path,'SHA-256':item.sha256};
  const dl=el('dl');for(const [key,value] of Object.entries(values)){const dd=el('dd');if(key==='来源'&&/^https?:\/\//.test(value)){const a=el('a',value);a.href=value;a.target='_blank';a.rel='noopener noreferrer';dd.append(a);}else dd.textContent=value;dl.append(el('dt',key),dd);}content.append(dl);
  const actions=el('div',undefined,'actions'),url=assetURL(item);const pageURL=new URL(location.href);pageURL.hash=new URLSearchParams({asset:item.id}).toString();
  for(const [text,value] of [['复制链接',url],['复制 Markdown',`![${item.name.replace(/[\[\]\\]/g,'')}](${url})`],['复制仓库路径',item.path],['分享此素材',pageURL.href]]){const button=el('button',text);button.addEventListener('click',()=>copy(value));actions.append(button);}
  const download=el('a','下载原文件');download.href=item.path;download.download=item.path.split('/').pop();download.className='secondary';actions.append(download);
  if(item.path.endsWith('.svg')){const b=el('button','复制 SVG','secondary');b.addEventListener('click',async()=>{try{const r=await fetch(item.path);if(!r.ok)throw Error();copy(await r.text());}catch{notify('读取失败，请检查文件是否存在。');}});actions.append(b);}
  content.append(actions);body.append(content);if(!$('#detail').open)$('#detail').showModal();
  if(updateHash){const url=new URL(location.href);url.hash=new URLSearchParams({asset:item.id}).toString();history.replaceState(null,'',url);}
}
function closeDetail(){ $('#detail').close();const url=new URL(location.href);url.hash='';history.replaceState(null,'',url); }
for(const id of ['help','sidebar-guide','workflow-help'])$('#'+id).addEventListener('click',()=>$('#guide').showModal());
for(const b of document.querySelectorAll('[data-close]'))b.addEventListener('click',()=>b.closest('dialog').id==='detail'?closeDetail():b.closest('dialog').close());
$('#detail').addEventListener('cancel',()=>{const url=new URL(location.href);url.hash='';history.replaceState(null,'',url);});
$('#nav-assets').addEventListener('click',()=>{clearFilters();state.view='assets';render();closeMobile();});
$('#nav-series').addEventListener('click',()=>{clearFilters();state.view='series';render();closeMobile();});
for(const id of ['view-assets','view-series'])$('#'+id).addEventListener('click',()=>{state.view=id==='view-assets'?'assets':'series';render();});
$('#explore-series').addEventListener('click',()=>{clearFilters();state.view='series';render();$('#workspace').scrollIntoView();});
$('#search').addEventListener('input',()=>{state.q=$('#search').value;render();});$('#sort').addEventListener('change',()=>{state.sort=$('#sort').value;render();});
for(const field of ['component','function','platform','status'])$('#'+field).addEventListener('change',()=>{state[field]=$('#'+field).value;render();});
$('#background').addEventListener('change',()=>{state.bg=$('#background').value;render();});
$('#kinds').addEventListener('click',event=>{const b=event.target.closest('[data-kind]');if(b){state.kind=b.dataset.kind;render();}});
for(const id of ['reset','empty-reset'])$('#'+id).addEventListener('click',()=>{clearFilters();render();});
$('#mobile-nav').addEventListener('click',()=>{const open=document.body.classList.toggle('nav-open');$('#mobile-nav').setAttribute('aria-expanded',String(open));});
document.addEventListener('keydown',event=>{if(event.key==='Escape')closeMobile();if(event.key==='/'&&!['INPUT','SELECT','TEXTAREA'].includes(document.activeElement.tagName)&&!document.querySelector('dialog[open]')){event.preventDefault();$('#search').focus();}});
window.addEventListener('popstate',()=>{state=readState();render();});
async function init(){try{const [assetsResponse,groupsResponse]=await Promise.all([fetch('catalog.json',{cache:'no-store'}),fetch('organization.json',{cache:'no-store'})]);if(!assetsResponse.ok||!groupsResponse.ok)throw Error();[items,registry]=await Promise.all([assetsResponse.json(),groupsResponse.json()]);state=readState();
const stats=registry.stats;$('#stat-assets').textContent=stats.assets;$('#stat-series').textContent=stats.series;$('#stat-products').textContent=stats.products+stats.projects;$('#stat-components').textContent=stats.components;$('#nav-total').textContent=stats.assets;$('#nav-series-count').textContent=stats.series;
const featured=items.find(x=>x.id==='product-macrightclick-app-icon-moonlit-blue-q96-v01-png')||items[0];if(featured){$('#hero-image').src=featured.path;$('#hero-image').alt=featured.name;$('#hero-image').hidden=false;$('#hero-name').textContent=featured.name.replace('MacRightClick · ','');$('#hero-asset').disabled=false;$('#hero-asset').addEventListener('click',()=>showDetail(featured));}
render();const id=new URLSearchParams(location.hash.slice(1)).get('asset');const selected=items.find(x=>x.id===id);if(selected)showDetail(selected,false);
}catch(error){$('#count').textContent='目录加载失败，请先构建并通过 HTTP 访问。';$('#empty').hidden=false;$('#empty h3').textContent='素材目录暂时无法读取';$('#empty p').textContent='请运行本地 start/restart，并检查 catalog.json 与 organization.json。';}}
init();
