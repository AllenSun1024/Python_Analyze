# Python_Analyze

Python static analysis: Python AST + Jedi

扫出库中的所有python文件：
pycg $(find ./ -name "*.py" | awk '{print "directory" substr($0, 3)}' > pylist)

根据python文件列表生成json结果
pycg $(cat pylist) -o cg.json
