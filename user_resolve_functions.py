input_path = "/home/l/ghidra_scripts/input.txt"
output_path = "/home/l/ghidra_scripts/functions_listed.txt"
not_found_path = "/home/l/ghidra_scripts/resolve_not_found.txt"

def run():
    fm = currentProgram.getFunctionManager()
    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    with open(output_path, "w") as out, open(not_found_path, "w") as nf:
        for line in lines:
            try:
                addr = toAddr(line)
                if addr is None:
                    nf.write("%s -> INVALID ADDRESS\n" % line)
                    continue
                func = fm.getFunctionContaining(addr)
                if func is None:
                    nf.write("%s -> NO FUNCTION FOUND\n" % line)
                else:
                    out.write("%s\n" % func.getName())
            except Exception as e:
                nf.write("%s -> ERROR: %s\n" % (line, str(e)))

run()
