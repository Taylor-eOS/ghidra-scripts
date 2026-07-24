from ghidra.program.model.symbol import SourceType

names_path = "/home/l/ghidra_scripts/names.txt"
not_found_path = "/home/l/ghidra_scripts/rename_not_found.txt"
skip_suffixed = False

def run():
    fm = currentProgram.getFunctionManager()
    with open(names_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    with open(not_found_path, "w") as nf:
        for line in lines:
            if not line.startswith("FUN_"):
                nf.write("%s -> NOT A FUN_ NAME\n" % line)
                continue
            rest = line[4:]
            underscore_idx = rest.find("_")
            if underscore_idx == -1:
                addr_str = rest
            else:
                addr_str = rest[:underscore_idx]
            try:
                addr = toAddr(addr_str)
            except Exception as e:
                nf.write("%s -> BAD ADDRESS: %s\n" % (line, str(e)))
                continue
            if addr is None:
                nf.write("%s -> INVALID ADDRESS\n" % line)
                continue
            func = fm.getFunctionContaining(addr)
            if func is None:
                nf.write("%s -> NO FUNCTION FOUND\n" % line)
                continue
            current_name = func.getName()
            expected_prefix = "FUN_" + addr_str + "_"
            expected_plain = "FUN_" + addr_str
            if current_name == expected_plain:
                try:
                    func.setName(line, SourceType.USER_DEFINED)
                except Exception as e:
                    nf.write("%s -> RENAME ERROR: %s\n" % (line, str(e)))
            elif current_name.startswith(expected_prefix):
                if skip_suffixed:
                    nf.write("%s -> SKIPPED SUFFIXED NAME: %s\n" % (line, current_name))
                else:
                    try:
                        func.setName(line, SourceType.USER_DEFINED)
                    except Exception as e:
                        nf.write("%s -> RENAME ERROR: %s\n" % (line, str(e)))
            else:
                nf.write("%s -> CURRENT NAME MISMATCH: %s\n" % (line, current_name))

run()
