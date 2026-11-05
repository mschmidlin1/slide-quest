"""Paint the pygbag page around the square after a fresh web build."""
from pathlib import Path

INDEX = Path("build/web/index.html")


def main():
    text = INDEX.read_text(encoding="utf-8")
    text = text.replace("#7f7f7f", "#0B2A51")
    text = text.replace("background-color:powderblue;", "background-color: #0B2A51;")
    anchor = "            margin: 0 auto;\n"
    frame = anchor + "            outline: 2px solid #43B8D6;\n            outline-offset: 0;\n"
    if anchor not in text:
        raise SystemExit("canvas CSS anchor missing from build/web/index.html")
    if "outline: 2px solid #43B8D6" not in text:
        text = text.replace(anchor, frame, 1)
    INDEX.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
