async function main() {
    let pyodide = await loadPyodide();

    await pyodide.runPython(await (await fetch("/reactive.py")).text());

    let pyodideGlobals = pyodide.globals.toJs();
    let pyodideGlobalsKeys = pyodide.globals.toJs().keys();
    for (i = 0; i < pyodideGlobals.size; i++) {
        let varName = pyodideGlobalsKeys.next().value;
        if (i > 8) {
            if (typeof(pyodide.globals.get(varName)) == "function") {
                window[varName] = pyodide.globals.get(varName)
            }
        }
    }
}
main();