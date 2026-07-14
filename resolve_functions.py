input_path = "/home/l/ghidra_scripts/input.txt"
output_path = "/home/l/ghidra_scripts/output.txt"

def run():
    fm = currentProgram.getFunctionManager()
    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    with open(output_path, "w") as out:
        for line in lines:
            try:
                addr = toAddr(line)
                if addr is None:
                    out.write("%s -> INVALID ADDRESS\n" % line)
                    continue
                func = fm.getFunctionContaining(addr)
                if func is None:
                    out.write("%s -> NO FUNCTION FOUND\n" % line)
                else:
                    out.write("%s -> %s\n" % (line, func.getName()))
            except Exception as e:
                out.write("%s -> ERROR: %s\n" % (line, str(e)))

run()
