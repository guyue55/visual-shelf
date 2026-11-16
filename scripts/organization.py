"""Canonical organization registry and backwards-compatible asset grouping."""
import json
from pathlib import Path
import re

SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
OWNER = re.compile(r'^(?:product|project):[a-z0-9]+(?:-[a-z0-9]+)*$')


def registry(root):
    path = root / 'organization.json'
    if not path.exists():
        return {'version':1,'owners':[],'series':[],'components':[]}
    if path.is_symlink():
        raise ValueError('分组配置不得为符号链接')
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or data.get('version') != 1:
        raise ValueError('organization.json version 须为 1')
    for section in ('owners','series','components'):
        ids = set()
        if not isinstance(data.get(section), list):
            raise ValueError(f'分组 {section} 必须为数组')
        for entry in data[section]:
            if not isinstance(entry, dict):
                raise ValueError(f'分组 {section} 条目必须为对象')
            identifier = entry.get('id')
            valid = isinstance(identifier, str) and (identifier in ('shared','unknown') or bool(OWNER.fullmatch(identifier))) if section == 'owners' else isinstance(identifier,str) and bool(SLUG.fullmatch(identifier))
            if not valid or identifier in ids or not isinstance(entry.get('name'),str) or not entry['name'].strip():
                raise ValueError(f'分组 {section} 标识重复或无效')
            ids.add(identifier)
    owners={x['id'] for x in data['owners']}
    for entry in data['series']:
        if entry.get('owner') not in owners:
            raise ValueError('系列引用不存在的归属')
    return data


def validate_organization(value, data):
    if not isinstance(value,dict) or set(value)-{'owner','series','component','functions','platforms'}:
        raise ValueError('organization 仅接受 owner/series/component/functions/platforms')
    owners={x['id'] for x in data['owners']}
    series={x['id']:x for x in data['series']}
    components={x['id'] for x in data['components']}
    if value.get('owner') not in owners:
        raise ValueError('素材归属未在 organization.json 登记')
    if value.get('series') is not None:
        if value['series'] not in series or series[value['series']]['owner'] != value['owner']:
            raise ValueError('素材系列不存在或归属不一致')
    if value.get('component') is not None and value['component'] not in components:
        raise ValueError('素材组件未登记')
    for key in ('functions','platforms'):
        values=value.get(key,[])
        if not isinstance(values,list) or not all(isinstance(x,str) and x.strip() for x in values) or len(values)!=len(set(values)):
            raise ValueError(f'{key} 必须为无重复非空文本数组')
    return value


def organization_for(item, data):
    if 'organization' in item:
        return validate_organization(item['organization'],data)
    # Legacy files stay readable; unknowns are never guessed from names.
    tags=item.get('tags',[])
    owner=next((t[6:] for t in tags if t.startswith('owner:')),'unknown')
    if owner not in {x['id'] for x in data['owners']}:
        owner='unknown'
    return {'owner':owner,'series':None,'component':None,'functions':[],'platforms':[]}


def public_registry(root, items):
    data=registry(root)
    result=json.loads(json.dumps(data))
    for section,key in [('owners','owner'),('series','series'),('components','component')]:
        for entry in result[section]:
            members=[x for x in items if organization_for(x,data).get(key)==entry['id']]
            entry['count']=len(members)
            if section=='series':
                entry['samples']=[x['id'] for x in members[:3]]
    result['stats']={'assets':len(items),'bytes':sum((root/x['path']).stat().st_size for x in items),
                     'series':sum(x['count']>0 for x in result['series']),
                     'products':sum(x['count']>0 and x['id'].startswith('product:') for x in result['owners']),
                     'projects':sum(x['count']>0 and x['id'].startswith('project:') for x in result['owners']),
                     'components':sum(x['count']>0 for x in result['components'])}
    return result
