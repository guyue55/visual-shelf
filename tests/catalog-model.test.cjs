const {test}=require('node:test');
const assert=require('node:assert/strict');
const M=require('../site/catalog-model.js');
const registry={owners:[{id:'product:reader',name:'阅读器'}],series:[{id:'moon',name:'月夜系列'}],components:[{id:'launch',name:'启动组件'}]};
const a={id:'moon-logo',name:'月夜',description:'产品标识',kind:'logos',created:'2026-01-01',tags:['古风','status:ready','owner:product:reader'],organization:{owner:'product:reader',series:'moon',component:'launch',functions:['应用启动'],platforms:['macOS']}};
const b={...a,id:'moon-cover',kind:'covers',created:'2026-02-01',tags:['古风封面','status:draft'],organization:{...a.organization,platforms:['Web']}};
test('不同维度按 AND 组合，搜索涵盖登记名称和功能',()=>{
 assert.deepEqual(M.filter([a,b],{owner:'product:reader',series:'moon',component:'launch',function:'应用启动',platform:'macOS',status:'ready',q:'阅读器 月夜系列 启动组件'},registry).map(x=>x.id),[a.id]);
 assert.equal(M.filter([a,b],{platform:'macOS',kind:'covers'},registry).length,0);
});
test('标签精确筛选与自由搜索分开',()=>{
 assert.deepEqual(M.filter([a,b],{tag:'古风'},registry),[a]);
 assert.equal(M.filter([a,b],{q:'古风'},registry).length,2);
 assert.deepEqual(M.visibleTags(a),['古风']);
});
test('排序不改变原列表、无归属记录有独立分组',()=>{
 const items=[a,b]; assert.equal(M.filter(items,{sort:'newest'},registry)[0].id,b.id);assert.equal(items[0],a);
 assert.equal(M.groups([a,b]).get('moon').length,2);
 assert.equal(M.groups([{...a,organization:undefined}]).get('unassigned').length,1);
 assert.equal(M.filter([],{q:'阅'},registry).length,0);
});

test('未分组系列只返回缺失系列的素材',()=>{ const legacy={...a,organization:undefined}; assert.deepEqual(M.filter([a,legacy],{series:'__unassigned__'},registry),[legacy]); });
