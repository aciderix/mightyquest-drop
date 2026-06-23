// DecompileFunctions.java — decompile a set of functions to C and dump to file.
//
// Reopens an already-analyzed program (use analyzeHeadless ... -process) and
// decompiles each function whose entry address is listed in an addresses file
// (one hex address per line, e.g. 0x00656510). Writes C-like decompiler output.
//
// Usage:
//   analyzeHeadless <proj> MQ -process mq_client.exe -noanalysis \
//     -scriptPath re/ghidra -postScript DecompileFunctions.java <addrs.txt> <out.c>
//
//@category MightyQuest
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import java.io.*;
import java.nio.file.*;
import java.util.*;

public class DecompileFunctions extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 2) { println("need <addrs.txt> <out.c>"); return; }
        List<String> lines = Files.readAllLines(Paths.get(args[0]));

        DecompInterface ifc = new DecompInterface();
        ifc.openProgram(currentProgram);

        try (PrintWriter w = new PrintWriter(new FileWriter(args[1]))) {
            for (String ln : lines) {
                ln = ln.trim();
                if (ln.isEmpty() || ln.startsWith("#")) continue;
                long off = Long.parseLong(ln.replaceFirst("^0x", ""), 16);
                Address a = toAddr(off);
                Function fn = getFunctionAt(a);
                if (fn == null) fn = getFunctionContaining(a);
                if (fn == null) { w.println("// no function at " + ln + "\n"); continue; }
                w.println("// ==== " + fn.getName() + " @ " + fn.getEntryPoint()
                          + "  (" + fn.getBody().getNumAddresses() + " bytes) ====");
                String c = fn.getComment();
                if (c != null) w.println("// " + c.replace("\n", "\n// "));
                DecompileResults res = ifc.decompileFunction(fn, 60, monitor);
                if (res != null && res.decompileCompleted()) {
                    w.println(res.getDecompiledFunction().getC());
                } else {
                    w.println("// decompile failed: "
                              + (res == null ? "null" : res.getErrorMessage()));
                }
                w.println();
            }
        }
        println("[DecompileFunctions] wrote " + args[1]);
    }
}
