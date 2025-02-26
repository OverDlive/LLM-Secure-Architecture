def replace_includes(uml_code: str) -> str:
    return uml_code.replace("!include <c4/C4_Context>", "!include ../plantuml_libs/C4_Context.puml")