[0;31m---------------------------------------------------------------------------[0m
[0;31mAttributeError[0m                            Traceback (most recent call last)
[0;32m/home/sebastien/Projects/Local/bin/sugar2[0m in [0;36m<module>[0;34m()[0m
[1;32m      1[0m [0;31m#!/usr/bin/env python[0m[0;34m[0m[0;34m[0m[0m
[1;32m      2[0m [0;32mimport[0m [0msugar2[0m[0;34m,[0m [0msys[0m[0;34m[0m[0m
[0;32m----> 3[0;31m [0msugar2[0m[0;34m.[0m[0mrun[0m[0;34m([0m[0msys[0m[0;34m.[0m[0margv[0m[0;34m[[0m[0;36m1[0m[0;34m:[0m[0;34m][0m[0;34m)[0m[0;34m[0m[0m
[0m[1;32m      4[0m [0;31m# EOF[0m[0;34m[0m[0;34m[0m[0m
[1;32m      5[0m [0;34m[0m[0m

[0;32m/home/sebastien/Projects/Local/lib/python/sugar2.pyc[0m in [0;36mrun[0;34m(arguments)[0m
[1;32m   1077[0m         [0mself[0m[0;34m=[0m[0m__module__[0m[0;34m[0m[0m
[1;32m   1078[0m         [0mcommand[0m[0;34m=[0m[0mSugarCommand[0m[0;34m([0m[0;34m'sugar'[0m[0;34m)[0m[0;34m[0m[0m
[0;32m-> 1079[0;31m         [0mcommand[0m[0;34m.[0m[0mrun[0m[0;34m([0m[0;34m([0m[0marguments[0m [0;32mor[0m [0;34m[[0m[0;34m'--help'[0m[0;34m][0m[0;34m)[0m[0;34m)[0m[0;34m[0m[0m
[0m[1;32m   1080[0m [0;34m[0m[0m
[1;32m   1081[0m [0;34m[0m[0m

[0;32m/home/sebastien/Projects/Local/lib/python/lambdafactory/main.pyc[0m in [0;36mrun[0;34m(self, arguments, output)[0m
[1;32m    112[0m                                         [0mthrow[0m[0;34m.[0m[0mException[0m[0;34m([0m[0;34m'Only one source file is accepted with the -m option'[0m[0;34m)[0m[0;34m[0m[0m
[1;32m    113[0m                         [0;32mfor[0m [0msource_path[0m [0;32min[0m [0margs[0m[0;34m:[0m[0;34m[0m[0m
[0;32m--> 114[0;31m                                 [0mresult_module[0m[0;34m=[0m[0mself[0m[0;34m.[0m[0mparseFile[0m[0;34m([0m[0msource_path[0m[0;34m,[0m [0moptions[0m[0;34m.[0m[0mmodule[0m[0;34m)[0m[0;34m[0m[0m
[0m[1;32m    115[0m                                 [0mprogram[0m[0;34m.[0m[0maddModule[0m[0;34m([0m[0mresult_module[0m[0;34m)[0m[0;34m[0m[0m
[1;32m    116[0m                                 [0;32mif[0m [0;34m([0m[0;32mnot[0m [0mlanguage[0m[0;34m)[0m[0;34m:[0m[0;34m[0m[0m

[0;32m/home/sebastien/Projects/Local/lib/python/lambdafactory/main.pyc[0m in [0;36mparseFile[0;34m(self, sourcePath, moduleName)[0m
[1;32m    178[0m         [0;32mdef[0m [0mparseFile[0m[0;34m([0m[0mself[0m[0;34m,[0m [0msourcePath[0m[0;34m,[0m [0mmoduleName[0m[0;34m=[0m[0mNone[0m[0;34m)[0m[0;34m:[0m[0;34m[0m[0m
[1;32m    179[0m                 [0;32mif[0m [0mmoduleName[0m [0;32mis[0m [0mNone[0m[0;34m:[0m [0mmoduleName[0m [0;34m=[0m [0mNone[0m[0;34m[0m[0m
[0;32m--> 180[0;31m                 [0;32mreturn[0m [0mself[0m[0;34m.[0m[0menvironment[0m[0;34m.[0m[0mparseFile[0m[0;34m([0m[0msourcePath[0m[0;34m,[0m [0mmoduleName[0m[0;34m)[0m[0;34m[0m[0m
[0m[1;32m    181[0m [0;34m[0m[0m
[1;32m    182[0m         [0;32mdef[0m [0mparseString[0m[0;34m([0m[0mself[0m[0;34m,[0m [0mtext[0m[0;34m,[0m [0mextension[0m[0;34m,[0m [0mmoduleName[0m[0;34m=[0m[0mNone[0m[0;34m)[0m[0;34m:[0m[0;34m[0m[0m

[0;32m/home/sebastien/Projects/Local/lib/python/lambdafactory/environment.pyc[0m in [0;36mparseFile[0;34m(self, path, moduleName)[0m
[1;32m    249[0m                 [0mtext[0m[0;34m=[0m[0mf[0m[0;34m.[0m[0mread[0m[0;34m([0m[0;34m)[0m[0;34m[0m[0m
[1;32m    250[0m                 [0mf[0m[0;34m.[0m[0mclose[0m[0;34m([0m[0;34m)[0m[0;34m[0m[0m
[0;32m--> 251[0;31m                 [0;32mreturn[0m [0mself[0m[0;34m.[0m[0mparseString[0m[0;34m([0m[0mtext[0m[0;34m,[0m [0mpath[0m[0;34m,[0m [0mmoduleName[0m[0;34m)[0m[0;34m[0m[0m
[0m[1;32m    252[0m [0;34m[0m[0m
[1;32m    253[0m         [0;32mdef[0m [0mparseString[0m[0;34m([0m[0mself[0m[0;34m,[0m [0mtext[0m[0;34m,[0m [0mpath[0m[0;34m,[0m [0mmoduleName[0m[0;34m=[0m[0mNone[0m[0;34m)[0m[0;34m:[0m[0;34m[0m[0m

[0;32m/home/sebastien/Projects/Local/lib/python/lambdafactory/environment.pyc[0m in [0;36mparseString[0;34m(self, text, path, moduleName)[0m
[1;32m    260[0m                                 [0mparser[0m [0;34m=[0m [0mself[0m[0;34m.[0m[0mparsers[0m[0;34m.[0m[0mget[0m[0;34m([0m[0;34m'sg'[0m[0;34m)[0m[0;34m[0m[0m
[1;32m    261[0m                         [0msource_and_module[0m [0;34m=[0m [0mparser[0m[0;34m.[0m[0mparseString[0m[0;34m([0m[0mtext[0m[0;34m,[0m [0mmoduleName[0m[0;34m,[0m [0mpath[0m[0;34m)[0m[0;34m[0m[0m
[0;32m--> 262[0;31m                         [0mres[0m[0;34m=[0m[0;34m[[0m[0msource_and_module[0m[0;34m[[0m[0;36m0[0m[0;34m][0m[0;34m,[0m [0msource_and_module[0m[0;34m[[0m[0;36m1[0m[0;34m][0m[0;34m.[0m[0mcopy[0m[0;34m([0m[0;34m)[0m[0;34m.[0m[0mdetach[0m[0;34m([0m[0;34m)[0m[0;34m][0m[0;34m[0m[0m
[0m[1;32m    263[0m                         [0;32massert[0m[0;34m([0m[0;34m([0m[0mres[0m[0;34m[[0m[0;36m0[0m[0;34m][0m [0;34m==[0m [0mtext[0m[0;34m)[0m[0;34m)[0m[0;34m[0m[0m
[1;32m    264[0m                         [0mres[0m[0;34m[[0m[0;36m1[0m[0;34m][0m[0;34m.[0m[0msetSource[0m[0;34m([0m[0mres[0m[0;34m[[0m[0;36m0[0m[0;34m][0m[0;34m)[0m[0;34m[0m[0m

[0;31mAttributeError[0m: 'NoneType' object has no attribute 'copy'
