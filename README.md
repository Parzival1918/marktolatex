# marktolatex

Run `marktolatex.py` to convert a markdown file to a LaTeX file. 

It does very simple things, like converting `#` to `\section{}`, `##` to `\subsection{}`, etc. It also converts `*` to `\textit{}` and `**` to `\textbf{}`.

Ypu can use math mode with `$` and `$$` delimiters in the markdown file. The script will keep the math mode as it is.

## Usage

```bash
python marktolatex.py <input_file, .md extension>
```

The output file will be `<input_file>.tex`.