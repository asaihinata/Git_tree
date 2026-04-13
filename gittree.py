import os
import subprocess
C_GREEN,C_BLUE,C_END='\033[92m','\033[94m','\033[00m'
skippath=None
def grouping(fileList):
    root={}
    for path in fileList:
        path,current=path.decode('utf-8'),root
    for p in path.rstrip('\n').split('/'):
        current.setdefault(p,{})
        current=current[p]
    return root
def displayItems(items,path,prefix,color):
    for index,item in enumerate(sorted(items.keys())):
        if(isinstance(skippath,(list,tuple)) and item in skippath)or(isinstance(skippath,str) and item==skippath):break
        if index==len(items)-1:
            print(prefix+'└── '+appendColor(path,item,color))
            nextPrefix=prefix+' '
        else:
            print(prefix+'├── '+appendColor(path,item,color))
            nextPrefix=prefix+'│   '
        if 0<len(items[item]):displayItems(items[item],os.path.join(path,item),nextPrefix,color)
def appendColor(path,item,color=False):
    filepath,colorCode,endCode=os.path.join(path,item),'',C_END if color else ''
    if color:
        if os.path.isdir(filepath):colorCode=C_BLUE
        elif os.access(filepath,os.X_OK):colorCode=C_GREEN
        else:colorCode=C_END
    return colorCode+item+endCode
def main():
    cmd='git ls-files'
    p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    stderr_data=p.stderr.read()
    if len(stderr_data)>0:print(stderr_data,)
    else:
        currentDir=os.path.split(os.getcwd())
        print(appendColor(currentDir[0],currentDir[1],True))
        displayItems(grouping(p.stdout.readlines()),'.','',True)
if __name__=='__main__':
    main()