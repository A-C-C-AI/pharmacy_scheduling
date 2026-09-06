"""Fail-closed validation of materialized schedules and artifact lineage."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_stage(stage):
    path = Path('output') / f'stage_{stage:02d}_manifest.json'
    manifest = json.loads(path.read_text())
    nb = next(Path('.').glob(f'{stage:02d}*.ipynb'))
    source = '\n'.join(''.join(c['source']) for c in json.loads(nb.read_text())['cells'])
    if hashlib.sha256(source.encode()).hexdigest() != manifest['notebook_source_sha256']:
        raise ValueError(f'Stage {stage:02d} notebook source changed; rerun this stage.')
    for name, expected in {**manifest['inputs'], **manifest['outputs']}.items():
        if not Path(name).is_file() or digest(name) != expected:
            raise ValueError(f'Stage {stage:02d} artifact changed or missing: {name}; rerun upstream notebooks.')


def write_stage(stage, inputs, outputs):
    # Code hashes identify the implementation actually used. They are provenance,
    # not signatures and not protection against deliberate manifest tampering.
    paths = list(inputs) + [str(p) for p in sorted(Path('.').glob(f'{stage:02d}*.ipynb'))]
    # Notebook bytes change when outputs are written; record code separately below.
    paths = [p for p in paths if not str(p).endswith('.ipynb')]
    paths += [str(p) for p in Path('.').glob('*.py') if p.name in {'common_metrics.py','validation.py','reporting.py'}]
    nb = next(Path('.').glob(f'{stage:02d}*.ipynb'))
    cells = json.loads(nb.read_text())['cells']
    source = '\n'.join(''.join(c['source']) for c in cells)
    manifest = {'stage':stage, 'inputs':{str(p):digest(p) for p in paths},
                'outputs':{str(p):digest(p) for p in outputs},
                'notebook_source_sha256':hashlib.sha256(source.encode()).hexdigest()}
    (Path('output')/f'stage_{stage:02d}_manifest.json').write_text(json.dumps(manifest,indent=2))


def validate_schedule(schedule, historical, spec, *, active_overrides=None, h24_overrides=None,
                      absence=None, approved_cross_pairs=(), recovery_h24_bounds=None):
    """Check every modeled hard constraint; optional pattern changes support recovery audits.

    Recovery does not lock optimal total range: absence can worsen total fairness.
    H24 annual bounds can be locked to the base schedule's observed optimum.
    """
    p=spec['parameters']; maps=spec['derived_maps']; primary=maps['primary_group_by_pharmacy']
    weekcols=['week_id','week_start','week_end','nT','rotation_group','rotation_round']
    base=schedule.copy()
    if active_overrides is not None:
        rows=[]
        attrs=historical.drop_duplicates('pharmacy_id').set_index('pharmacy_id')
        locations={(r.pharmacy_id,int(r.nT)):r.location_id for r in historical.itertuples()}
        locations.update({(r.pharmacy_id,int(r.nT)):r.location_id for r in schedule.itertuples()})
        weeks=historical[weekcols].drop_duplicates()
        for w in weeks.to_dict('records'):
            nt=int(w['nT'])
            for pharmacy in sorted(active_overrides[nt]):
                rows.append({**w,'pharmacy_id':pharmacy,'location_id':locations.get((pharmacy,nt),attrs.loc[pharmacy,'location_id']),
                             'access_mode':attrs.loc[pharmacy,'access_mode'],
                             'shift_type':'H24' if pharmacy in h24_overrides[nt] else 'STANDARD'})
        base=pd.DataFrame(rows)
    errors=[]
    def check(condition,label):
        if not bool(condition): errors.append(label)
    check(not base.empty,'nonempty schedule')
    check(not base.duplicated(['week_id','pharmacy_id']).any(),'duplicate pharmacy-week')
    check(not base[weekcols+['pharmacy_id','location_id','shift_type','access_mode']].isna().any().any(),'missing fields')
    check(set(base.pharmacy_id)<=set(primary),'unknown pharmacy')
    check(base.shift_type.isin(['H24','STANDARD']).all(),'shift type')
    check(base.access_mode.isin(['P','C']).all(),'access mode')
    expected=historical[weekcols].drop_duplicates().copy()
    actual=base[weekcols].drop_duplicates().copy()
    for frame in [expected,actual]:
        for c in ['week_start','week_end']:frame[c]=pd.to_datetime(frame[c]).dt.strftime('%Y-%m-%d')
    check(actual.sort_values('week_id').reset_index(drop=True).equals(expected.sort_values('week_id').reset_index(drop=True)),'week metadata')
    ids=expected.week_id
    check(base.groupby('week_id').size().reindex(ids,fill_value=0).ge(p['weekly_staffing_floor']).all(),'weekly staffing floor')
    check(base[base.shift_type=='H24'].groupby('week_id').size().reindex(ids,fill_value=0).eq(p['weekly_h24_required']).all(),'weekly H24 count')
    check(base.groupby('pharmacy_id').size().max()<=p['maximum_annual_workload'],'annual workload ceiling')
    allowed=set(approved_cross_pairs)
    check(all(primary.get(r.pharmacy_id)==int(r.rotation_group) or (r.pharmacy_id,int(r.nT)) in allowed for r in base.itertuples()),'group eligibility')
    lookup=set(zip(historical.pharmacy_id,historical.location_id,historical.access_mode))
    check(all((r.pharmacy_id,r.location_id,r.access_mode) in lookup for r in base.itertuples()),'pharmacy location/access metadata')
    signatures={}
    for (nt,week),g in base.groupby(['nT','week_id']):
        sig=frozenset(zip(g.pharmacy_id,g.location_id,g.shift_type,g.access_mode))
        if nt in signatures:check(sig==signatures[nt],'repeated pattern identity')
        signatures[nt]=sig
    cycle=base[base.shift_type=='H24'].drop_duplicates(['pharmacy_id','nT']).groupby('pharmacy_id').size()
    for pharmacy,g in primary.items():
        bounds=p['h24_cycle_bounds_by_group'][str(g)]
        check(bounds['minimum']<=cycle.get(pharmacy,0)<=bounds['maximum'],f'H24 cycle bounds: {pharmacy}')
    if absence:
        pharmacy,nt=absence
        check(not ((base.pharmacy_id==pharmacy)&(base.nT==nt)).any(),'absence respected')
    if recovery_h24_bounds is not None:
        h=base[base.shift_type=='H24'].groupby('pharmacy_id').size().reindex(primary,fill_value=0)
        check(h.between(*recovery_h24_bounds).all(),'recovery H24 annual bounds')
    if errors:raise ValueError('; '.join(sorted(set(errors))))
    return {'assignments':int(len(base)),'hard_constraints':'PASS'}
