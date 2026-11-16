'use strict';
const $ = (s) => document.querySelector(s);
const labels = {logos:'Logo', icons:'图标', legends:'图例', covers:'封面'};
let items = [], kind = 'all', toastTimer;
function el(tag, text, className) { const node = document.createElement(tag); if (text !== undefined) node.textContent = text; if (className) node.className = className; return node; }
function notify(text) { $('#toast').textContent = text; $('#toast').classList.add('visible'); clearTimeout(toastTimer); toastTimer = setTimeout(() => $('#toast').classList.remove('visible'), 2800); }
async function copy(text) {
  try { await navigator.clipboard.writeText(text); notify('已复制'); }
  catch { notify('无法访问剪贴板，请手动复制下面的引用'); const pre = el('pre', text); $('#detail-content').append(pre); }
}
function render() {
  const q = $('#search').value.trim().toLocaleLowerCase();
  const tokens = q.split(/\s+/).filter(Boolean);
  const list = items.filter(x => (kind === 'all' || kind === x.kind) && tokens.every(t => [x.name, x.id, x.description, ...x.tags].join(' ').toLocaleLowerCase().includes(t)));
  list.sort($('#sort').value === 'newest' ? (a,b) => b.created.localeCompare(a.created) || a.id.localeCompare(b.id) : (a,b) => a.name.localeCompare(b.name, 'zh-CN'));
  $('#grid').replaceChildren();
  for (const item of list) {
    const card = el('button', undefined, 'card'); card.type = 'button'; card.setAttribute('aria-label', `查看 ${item.name}`);
    const preview = el('div', undefined, 'preview'); preview.dataset.kind = item.kind;
    const img = el('img'); img.src = item.path; img.alt = item.name; img.loading = 'lazy'; preview.append(img);
    const info = el('div', undefined, 'card-info'), top = el('div', undefined, 'card-top');
    top.append(el('h2', item.name), el('span', item.path.split('.').pop().toUpperCase(), 'format'));
    info.append(top, el('p', `${labels[item.kind]} / ${item.tags.slice(0,3).join(' · ')}`));
    card.append(preview, info); card.addEventListener('click', () => showDetail(item)); $('#grid').append(card);
  }
  $('#count').textContent = `${list.length} 份素材${q ? ` · 搜索「${$('#search').value.trim()}」` : ''}`;
  $('#empty').hidden = list.length > 0;
}
function showDetail(item) {
  const body = $('#detail-content'); body.replaceChildren();
  const preview = el('div', undefined, 'detail-preview'), img = el('img'); img.src = item.path; img.alt = item.name; preview.append(img);
  body.append(preview, el('h2', item.name), el('p', item.description));
  const dl = el('dl');
  for (const [label, value] of Object.entries({'分类':labels[item.kind], '标签':item.tags.join(' / '), '许可':item.license, '作者':item.author, '来源':item.source, '新增日期':item.created, '文件路径':item.path})) {
    const dd = el('dd');
    if (label === '来源' && /^https?:\/\//.test(value)) { const a = el('a', value); a.href = value; a.target = '_blank'; a.rel = 'noopener noreferrer'; dd.append(a); }
    else dd.textContent = value;
    dl.append(el('dt', label), dd);
  }
  body.append(dl);
  const url = new URL(item.path, location.href).href;
  const actions = el('div', undefined, 'actions');
  for (const [label, value] of [['复制链接',url], ['复制 Markdown',`![${item.name.replace(/[\[\]\\]/g,'')}](${url})`], ['复制仓库路径',item.path]]) {
    const button = el('button', label); button.addEventListener('click', () => copy(value)); actions.append(button);
  }
  const download = el('a','下载原文件'); download.href = item.path; download.download = item.path.split('/').pop(); actions.append(download);
  if (item.path.endsWith('.svg')) { const button = el('button','复制 SVG'); button.addEventListener('click', async () => { try { const response = await fetch(item.path); if (!response.ok) throw new Error(); await copy(await response.text()); } catch { notify('读取 SVG 失败'); } }); actions.append(button); }
  body.append(actions); $('#detail').showModal();
}
$('#search').addEventListener('input', render); $('#sort').addEventListener('change', render);
$('#filters').addEventListener('click', event => { const button = event.target.closest('[data-kind]'); if (!button) return; kind = button.dataset.kind; for (const b of $('#filters').querySelectorAll('button')) b.setAttribute('aria-pressed', String(b === button)); render(); });
$('#background').addEventListener('click', () => { const dark = document.body.classList.toggle('dark-preview'); $('#background').setAttribute('aria-pressed', String(dark)); $('#background').textContent = dark ? '◑ 浅色底预览' : '◐ 深色底预览'; });
$('#help').addEventListener('click', () => $('#guide').showModal());
for (const button of document.querySelectorAll('[data-close]')) button.addEventListener('click', () => button.closest('dialog').close());
document.addEventListener('keydown', event => { if (event.key === '/' && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName) && !document.querySelector('dialog[open]')) { event.preventDefault(); $('#search').focus(); } });
async function init() { try { const response = await fetch('catalog.json'); if (!response.ok) throw new Error(`HTTP ${response.status}`); items = await response.json(); $('#total').textContent = String(items.length).padStart(2,'0'); render(); } catch { $('#count').textContent = '素材目录加载失败。请先运行 build，并通过 HTTP 服务打开预览。'; } }
init();
