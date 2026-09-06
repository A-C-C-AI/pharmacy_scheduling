from pathlib import Path
import base64
import json
import shutil
import subprocess
import sys
import tempfile

MODULES=('common_metrics.py','validation.py','reporting.py','run_all.py')

def stage_notebook(folder):
    return next(folder.glob('*.ipynb'))

def prepare(folder,work):
    inputs=folder/'inputs'
    for item in inputs.iterdir():
        if item.name=='provenance':
            for source in item.glob('*.ipynb.json'):
                shutil.copy2(source,work/source.name.removesuffix('.json'))
        elif item.is_dir():shutil.copytree(item,work/item.name,dirs_exist_ok=True)
        else:shutil.copy2(item,work/item.name)
    (work/'output').mkdir(exist_ok=True)
    nb=stage_notebook(folder)
    shutil.copy2(nb,work/nb.name)
    return work/nb.name

def snapshot(folder,work,stage):
    inputs=folder/'inputs'
    if inputs.exists():shutil.rmtree(inputs)
    inputs.mkdir()
    for name in MODULES:shutil.copy2(work/name,inputs/name)
    shutil.copytree(work/'data',inputs/'data')
    (inputs/'output').mkdir()
    (inputs/'provenance').mkdir()
    for upstream in range(stage):
        mpath=work/'output'/f'stage_{upstream:02d}_manifest.json'
        manifest=json.loads(mpath.read_text())
        shutil.copy2(mpath,inputs/'output'/mpath.name)
        for name in manifest['outputs']:
            dest=inputs/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(work/name,dest)
        nbpath=next(work.glob(f'{upstream:02d}*.ipynb'))
        nb=json.loads(nbpath.read_text())
        for cell in nb['cells']:
            if cell['cell_type']=='code':cell['outputs']=[];cell['execution_count']=None
        (inputs/'provenance'/(nbpath.name+'.json')).write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n')

def collect(folder,work):
    nbpath=work/stage_notebook(folder).name
    shutil.copy2(nbpath,folder/nbpath.name)
    stage=int(folder.name[-2:])
    mpath=work/'output'/f'stage_{stage:02d}_manifest.json'
    manifest=json.loads(mpath.read_text())
    outputs=folder/'outputs';outputs.mkdir(exist_ok=True)
    for name in manifest['outputs']:shutil.copy2(work/name,outputs/Path(name).name)
    shutil.copy2(mpath,outputs/mpath.name)
    plots=outputs/'plots'
    if plots.exists():shutil.rmtree(plots)
    for index,cell in enumerate(json.loads(nbpath.read_text())['cells']):
        for j,out in enumerate(cell.get('outputs',[])):
            if 'image/png' in out.get('data',{}):
                plots.mkdir(exist_ok=True)
                (plots/f'cell_{index//2+1:02d}_plot_{j+1}.png').write_bytes(base64.b64decode(''.join(out['data']['image/png'])))

def execute(folder,work):
    nb=work/stage_notebook(folder).name
    subprocess.run([sys.executable,str(work/'run_all.py'),str(nb)],cwd=work,check=True)
    collect(folder,work)

def run_one(folder):
    with tempfile.TemporaryDirectory(prefix='pharmacy_notebook_') as td:
        work=Path(td);prepare(folder,work);execute(folder,work)
    print('PASS:',folder.name,'executed; outputs refreshed.')

def run_project(root):
    with tempfile.TemporaryDirectory(prefix='pharmacy_project_') as td:
        work=Path(td)
        for stage in range(6):
            folder=root/f'notebook_{stage:02d}'
            if stage==0:prepare(folder,work)
            else:
                snapshot(folder,work,stage)
                nb=stage_notebook(folder);shutil.copy2(nb,work/nb.name)
            print('RUN',folder.name,flush=True);execute(folder,work)
            print('PASS',folder.name,flush=True)
    print('All notebook folders and downstream input snapshots refreshed.')

def assemble_final(root,work):
    folder=root/'notebook_05';prepare(folder,work)
    for f in (folder/'outputs').iterdir():
        if f.is_file():shutil.copy2(f,work/'output'/f.name)

if __name__=='__main__':run_one(Path(__file__).resolve().parent)
