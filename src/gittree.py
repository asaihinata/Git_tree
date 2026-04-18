import os
import subprocess
C_GREEN='\033[92m'
C_BLUE='\033[94m'
C_END='\033[00m'
skip=None
def displayItems(items,path,prefix,color,lens=0):
    for index,item in enumerate(sorted(items.keys())):
        if skip is not None and ((isinstance(skip,str) and item==skip) or (isinstance(skip,(list,tuple)) and item in skip)):continue
        if index==len(items)-1:
            show=f'{prefix}└── '
            nextPrefix=f'{prefix}    '
        else:
            show=f'{prefix}├── '
            nextPrefix=f'{prefix}│   '
        print(show+appendColor(path,item,color))
        if prefix=='':lens=0
        else:lens=len(show)
        if len(items[item])>0:
            displayItems(items[item],os.path.join(path,item),nextPrefix,color,lens)
def appendColor(path,item,color=False):
    filepath=os.path.join(path,item)
    endCode=C_END if color else ''
    colorCode=''
    if color:
        if os.path.isdir(filepath):colorCode=C_BLUE
        elif os.access(filepath,os.X_OK):colorCode=C_GREEN
        else:colorCode=C_END
    return colorCode+item+endCode
def grouping(fileList):
    root={}
    for path in fileList:
        path,current=path.decode('utf-8'),root
        for p in path.rstrip('\n').split('/'):
            current.setdefault(p,{})
            current=current[p]
    return root
def main():
    cmd='git ls-files'
    p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    stdout_data=p.stdout.readlines()
    stderr_data=p.stderr.read()
    if len(stderr_data)>0:print(stderr_data,)
    else:
        currentDir=os.path.split(os.getcwd())
        print(appendColor(currentDir[0],currentDir[1],True))
        displayItems(grouping(stdout_data),'.','',True,0)
if __name__=='__main__':
    main()