"""Execute notebooks in order, saving fresh text, tables, and plot outputs.

Uses an in-process IPython shell in a separate Python process per notebook. This
needs no Jupyter socket server; code cells still execute with IPython semantics.
Usage: python run_all.py  (from any directory).
"""
from pathlib import Path
import os
import subprocess
import sys
import time


def execute(path):
    import nbformat
    from IPython.core.interactiveshell import InteractiveShell
    from IPython.utils.capture import capture_output
    from matplotlib_inline.backend_inline import configure_inline_support
    import matplotlib
    matplotlib.use('module://matplotlib_inline.backend_inline')
    root=path.parent
    os.chdir(root)
    sys.path.insert(0,str(root))
    shell=InteractiveShell.instance()
    configure_inline_support(shell,'module://matplotlib_inline.backend_inline')
    nb=nbformat.read(path,as_version=4)
    count=0
    for index,cell in enumerate(nb.cells):
        if cell.cell_type!='code':continue
        count+=1
        cell.outputs=[];cell.execution_count=count
        with capture_output(stdout=True,stderr=True,display=True) as captured:
            result=shell.run_cell(cell.source,store_history=True)
        if captured.stdout:cell.outputs.append(nbformat.v4.new_output('stream',name='stdout',text=captured.stdout))
        if captured.stderr:cell.outputs.append(nbformat.v4.new_output('stream',name='stderr',text=captured.stderr))
        for output in captured.outputs:
            cell.outputs.append(nbformat.v4.new_output('display_data',data=output.data,metadata=output.metadata))
        if not result.success:
            nbformat.write(nb,path)
            raise RuntimeError(f'{path.name}, cell {index}: {result.error_before_exec or result.error_in_exec}\n{captured.stdout}\n{captured.stderr}')
    nb.metadata['review_execution']={'method':'IPython in-process; isolated process per notebook','python':sys.version.split()[0]}
    nbformat.validate(nb)
    nbformat.write(nb,path)


if __name__=='__main__':
    if len(sys.argv)>1:execute(Path(sys.argv[1]).resolve())
    else:
        root=Path(__file__).resolve().parent
        for path in sorted(root.glob('0[0-5]*.ipynb')):
            start=time.time();print('RUN',path.name,flush=True)
            subprocess.run([sys.executable,__file__,str(path)],check=True,cwd=root)
            print('PASS',path.name,round(time.time()-start,2),'seconds',flush=True)
