import re

p = "/Users/satishgundu/Desktop/teachin/Visual_Learning_Material_TE/04_AI_Agent_LangGraph_TE.md"
s = open(p, encoding="utf-8").read()
new_line = '        S2["Annotated · List of str · operator.add reducer<br/>(append, not overwrite)"]'
s2 = re.sub(r'^[ \t]*S2\["Annotated.*$', new_line, s, flags=re.M)
open(p, "w", encoding="utf-8").write(s2)
for i, line in enumerate(s2.splitlines(), 1):
    if "S2[" in line:
        print(i, line)
print("CHANGED" if s2 != s else "NOCHANGE")
