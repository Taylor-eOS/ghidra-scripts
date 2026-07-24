output_path = "/home/l/ghidra_scripts/fun_unrenamed.txt"

def run():
    fm = currentProgram.getFunctionManager()
    funcs = fm.getFunctions(True)
    with open(output_path, "w") as of:
        for func in funcs:
            name = func.getName()
            if not name.startswith("FUN_"):
                continue
            rest = name[4:]
            if "_" in rest:
                continue
            of.write("%s\n" % name)

run()
