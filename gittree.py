from os import X_OK,access,getcwd
from os.path import isdir,join,split
from subprocess import PIPE,Popen
C_GREEN,C_BLUE,C_END='\033[92m','\033[94m','\033[00m'
skippath=['']
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
  if item not in skippath:
   if index==len(items)-1:
    print(prefix+'└── '+appendColor(path,item,color))
    nextPrefix=prefix+' '
   else:
    print(prefix+'├── '+appendColor(path,item,color))
    nextPrefix=prefix+'│   '
   if 0<len(items[item]):displayItems(items[item],join(path,item),nextPrefix,color)
def appendColor(path,item,color=False):
 filepath,colorCode,endCode=join(path,item),'',C_END if color else ''
 if color:
  if isdir(filepath):colorCode=C_BLUE
  elif access(filepath,X_OK):colorCode=C_GREEN
  else:colorCode=C_END
 return colorCode+item+endCode
cmd='git ls-files'
p=Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)
p.wait()
stderr_data=p.stderr.read()
if len(stderr_data)>0:print(stderr_data,)
else:
 currentDir=split(getcwd())
 print(appendColor(currentDir[0],currentDir[1],True))
 displayItems(grouping(p.stdout.readlines()),'.','',True)