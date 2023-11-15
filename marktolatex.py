# Imports ########
import sys
from pathlib import Path
import datetime
##################

template = r"""
\documentclass[12pt,a4paper]{article}

% Packages %%%%%%%%%%%%
\usepackage[margin=2cm]{geometry}
%%%%%%%%%%%%%%%%%%%%%%%

% <-- Doc authors title and date -->

\begin{document}

\maketitle

% <-- Doc content -->

\end{document}
"""

def save_to_latex(contents: dict, latex_file_name: Path) -> None:
    """Save the contents from a dict[] to a LaTeX document"""
    title_authors_date = contents["title"] + "\n" + contents["author"] + "\n" + contents["date"]
    content = "\n".join(contents["content"])

    filled_template = template.replace("% <-- Doc authors title and date -->", title_authors_date)
    filled_template = filled_template.replace("% <-- Doc content -->", content)

    with open(latex_file_name, 'w') as file:
        file.write(filled_template)

def check_for_bold_italic(text: str) -> str:
    """Return the text of a line formatted by adding \textbf{} ir \textit{}"""
    new_text = ""
    split_text = text.split("*",1)
    if len(split_text) == 1:
        new_text = text
    else:
        while len(split_text) > 1:
            # print(split_text)
            if split_text[1] == "\n":
                new_text += split_text[0] + "\n"
                break

            if split_text[1].startswith("**"):
                new_text += split_text[0] + r"\textbf{\textit{" + split_text[1].split("***",1)[0][2:] + "}}"
                split_text = split_text[1].split("***",1)[1].split("*",1)
            elif split_text[1].startswith("*"):
                new_text += split_text[0] + r"\textbf{" + split_text[1].split("**",1)[0][1:] + "}"
                split_text = split_text[1].split("**",1)[1].split("*",1)
            # elif split_text[1].startswith(" "):
            else:
                new_text += split_text[0] + r"\textit{" + split_text[1].split("*",1)[0] + "}"
                split_text = split_text[1].split("*",1)[1].split("*",1)
            # else:
            #     new_text += split_text[0] + split_text[1]

        new_text += split_text[0]


    return new_text

def get_file_contents(file_path: Path) -> dict:
    """Extract the contents of a .md file and save them in a dict[]"""

    authors = ["Pedro Juan Royo"] # List of authors, change to whatever you want but keep it as a list

    contents = {
        "title": "",
        "author": r"\author{" + r' \and '.join(authors) + "}", # Format: Author1 \and Author2 \and Author3" 
        "date": f"\date{{{datetime.date.today().strftime('%d %B %Y')}}}", # Format: DD Month YYYY
        "content": [], # List of strings, each string is a line of the document
    }

    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("# "):
                if contents["title"] == "":
                    contents["title"] = r"\title{" + check_for_bold_italic(line.strip()[2:]) + "}"
                else:
                    raise Exception("Multiple title lines found in file")
            else:
                # contents["content"].append(line)
                # Check if it is a section, subsection, subsubsection, etc.
                if line.startswith("## "):
                    contents["content"].append(r"\section{" + check_for_bold_italic(line.strip()[3:]) + "}")
                elif line.startswith("### "):
                    contents["content"].append(r"\subsection{" + check_for_bold_italic(line.strip()[4:]) + "}")
                elif line.startswith("#### "):
                    contents["content"].append(r"\subsubsection{" + check_for_bold_italic(line.strip()[5:]) + "}")
                else:
                    contents["content"].append(check_for_bold_italic(line.strip()))

    return contents

if __name__ == '__main__':
    # Get name of file to convert as argument
    if len(sys.argv) != 2:
        print("Usage: python marktolatex.py <file>")
        sys.exit(1)

    # Get file name
    file = sys.argv[1]
    file_path = Path(file)

    # Check if file exists
    if not file_path.exists():
        print(f"File '{file_path}' does not exist")
        sys.exit(1)
    elif not file_path.is_file():
        print("Input is not a file")
        sys.exit(1)
    elif file_path.suffix != ".md":
        print("File is not a markdown file")
        sys.exit(1)

    # Get contents of file
    contents = get_file_contents(file_path)

    # Create LaTeX file
    latex_file_name = file_path.with_suffix(".tex")
    save_to_latex(contents, latex_file_name)
