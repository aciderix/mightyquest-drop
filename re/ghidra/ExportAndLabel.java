// ExportAndLabel.java — Ghidra post-analysis script for the Mighty Quest client.
//
// 1) Uses the binary's assert/source-path strings (D:\HQ\...\*.cpp) to label the
//    functions that reference them: adds a PLATE comment with the source file and
//    renames unnamed FUN_ functions to src_<file>_<addr>. This recovers a rough
//    function->source-file map for free, since the build kept full paths.
// 2) Exports a CSV catalog of all functions (address, size, name, source hint).
//
// Run via analyzeHeadless ... -postScript ExportAndLabel.java <out.csv>
//
//@category MightyQuest
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.data.StringDataInstance;
import ghidra.program.model.mem.MemoryAccessException;
import java.io.*;
import java.util.regex.*;

public class ExportAndLabel extends GhidraScript {
    // matches  D:\HQ\...\SomeFile.cpp  (the build's source paths)
    static final Pattern SRC = Pattern.compile(
        "(?i)[A-Z]:\\\\HQ\\\\[^\"\\n]*?\\\\([A-Za-z0-9_]+)\\.(cpp|h|inl)");

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        String outPath = args.length > 0 ? args[0] : "functions.csv";

        Listing listing = currentProgram.getListing();
        ReferenceManager refs = currentProgram.getReferenceManager();
        SymbolTable st = currentProgram.getSymbolTable();

        int labeled = 0;
        DataIterator data = listing.getDefinedData(true);
        while (data.hasNext() && !monitor.isCancelled()) {
            Data d = data.next();
            if (d == null || !d.hasStringValue()) continue;
            String s = d.getDefaultValueRepresentation();
            Matcher m = SRC.matcher(s);
            if (!m.find()) continue;
            String file = m.group(1) + "." + m.group(2);
            ReferenceIterator ri = refs.getReferencesTo(d.getAddress());
            while (ri.hasNext()) {
                Reference r = ri.next();
                Function fn = listing.getFunctionContaining(r.getFromAddress());
                if (fn == null) continue;
                String pc = fn.getComment();
                if (pc == null || !pc.contains(file)) {
                    fn.setComment((pc == null ? "" : pc + "\n") + "src: " + file);
                }
                if (fn.getName().startsWith("FUN_")) {
                    try {
                        fn.setName("src_" + m.group(1) + "_" + fn.getEntryPoint(),
                                   SourceType.ANALYSIS);
                        labeled++;
                    } catch (Exception ignore) {}
                }
            }
        }

        int total = 0;
        try (PrintWriter w = new PrintWriter(new FileWriter(outPath))) {
            w.println("address,size,name,source_hint");
            FunctionIterator fi = listing.getFunctions(true);
            while (fi.hasNext() && !monitor.isCancelled()) {
                Function fn = fi.next();
                String hint = "";
                String c = fn.getComment();
                if (c != null) {
                    Matcher mm = Pattern.compile("src: (\\S+)").matcher(c);
                    if (mm.find()) hint = mm.group(1);
                }
                w.printf("0x%s,%d,%s,%s%n",
                    fn.getEntryPoint(), fn.getBody().getNumAddresses(),
                    fn.getName().replace(',', '_'), hint);
                total++;
            }
        }
        println("[ExportAndLabel] functions=" + total + " labeled_from_source=" + labeled);
        println("[ExportAndLabel] csv -> " + outPath);
    }
}
