/* Pure catalog queries shared by the static UI and offline tests. */
(function (root) {
  'use strict';
  const reserved = /^(owner|family|variant|revision|status|project|product):/;
  function status(item) { return item.tags.find(t => t.startsWith('status:'))?.slice(7) || 'unlabeled'; }
  function organization(item) { return item.organization || {owner:'unknown',series:null,component:null,functions:[],platforms:[]}; }
  function visibleTags(item) { return item.tags.filter(t => !reserved.test(t)); }
  function match(item, state, registry) {
    const org = organization(item);
    if (state.kind && item.kind !== state.kind) return false;
    for (const field of ['owner','series','component']) if (state[field] && (field==='series' && state[field]==='__unassigned__' ? Boolean(org.series) : org[field] !== state[field])) return false;
    if (state.function && !(org.functions || []).includes(state.function)) return false;
    if (state.platform && !(org.platforms || []).includes(state.platform)) return false;
    if (state.tag && !item.tags.includes(state.tag)) return false;
    if (state.status && status(item) !== state.status) return false;
    const names = ['owners','series','components'].flatMap((key,index) => registry[key].filter(x => x.id === org[['owner','series','component'][index]]).map(x=>x.name));
    const haystack = [item.id,item.name,item.description,...item.tags,...names,...(org.functions||[]),...(org.platforms||[])].join(' ').toLocaleLowerCase();
    return (state.q || '').trim().toLocaleLowerCase().split(/\s+/).filter(Boolean).every(t => haystack.includes(t));
  }
  function filter(items,state,registry) { return items.filter(item => match(item,state,registry)).sort(state.sort === 'newest' ? (a,b) => b.created.localeCompare(a.created) || a.id.localeCompare(b.id) : (a,b) => a.name.localeCompare(b.name,'zh-CN')); }
  function groups(items) {
    const map = new Map();
    for (const item of items) { const key = organization(item).series || 'unassigned'; if (!map.has(key)) map.set(key,[]); map.get(key).push(item); }
    return map;
  }
  const api = {status,organization,visibleTags,match,filter,groups};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.CatalogModel = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
