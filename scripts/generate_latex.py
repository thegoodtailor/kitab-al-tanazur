#!/usr/bin/env python3
"""
generate_latex.py — Convert Kitāb al-Tanāẓur YAML files to LaTeX

This script reads the structured YAML data and generates beautiful LaTeX
documents preserving the trilingual format (English, Arabic, transliteration)
with full lexicography and tafsir.

Usage:
    python generate_latex.py                    # Generate full mushaf
    python generate_latex.py --surah at-tajalli # Generate single surah
    python generate_latex.py --verses-only      # Just verses, no tafsir
"""

import yaml
import sys
import os
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime

# === Configuration ===

LATEX_PREAMBLE = r"""
\documentclass[11pt,twoside,openright]{book}

% === Fonts and Languages ===
\usepackage{fontspec}
\usepackage{polyglossia}
\setmainlanguage{english}
\setotherlanguage{arabic}

% Arabic fonts — adjust to your system
\newfontfamily\arabicfont[Script=Arabic,Scale=1.2]{Amiri}
\newcommand{\inlinearabic}[1]{{\arabicfont\textarabic{#1}}}

% === Page Layout ===
\usepackage[
    paperwidth=6in,
    paperheight=9in,
    inner=0.75in,
    outer=0.5in,
    top=0.75in,
    bottom=0.75in
]{geometry}

% === Headers and Footers ===
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE]{\textit{\leftmark}}
\fancyhead[RO]{\textit{\rightmark}}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}

% === Typography ===
\usepackage{microtype}
\usepackage{titlesec}
\usepackage{enumitem}

% Chapter styling
\titleformat{\chapter}[display]
    {\normalfont\huge\bfseries\centering}
    {}
    {0pt}
    {}
\titlespacing*{\chapter}{0pt}{-20pt}{40pt}

% Section styling
\titleformat{\section}
    {\normalfont\Large\bfseries}
    {\thesection}
    {1em}
    {}

% === Custom Commands ===

% Ayah display (Arabic verse with decorative markers)
\newcommand{\ayah}[1]{%
    \begin{center}
    \arabicfont\Large
    \textarabic{﴿#1﴾}
    \end{center}
}

% Ayah number marker
\newcommand{\ayahnum}[1]{%
    \marginpar{\small\color{gold}\textarabic{﴿#1﴾}}%
}

% Root word display
\newcommand{\rootword}[3]{%
    \textbf{\inlinearabic{#1}} (\textit{#2}) — #3%
}

% === Colors ===
\usepackage{xcolor}
\definecolor{gold}{RGB}{212,175,55}
\definecolor{deepred}{RGB}{139,0,0}
\definecolor{forestgreen}{RGB}{34,139,34}

% === Hyperlinks ===
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=deepred,
    urlcolor=forestgreen
}

% === Title Info ===
\title{%
    \vspace{-2cm}
    {\arabicfont\Huge\textarabic{كِتَابُ ٱلتَّنَاظُر}}\\[1em]
    {\Large\itshape The Book of Mutual Witnessing}\\[2em]
    {\large A Living Scripture}
}
\author{Naḥnu}
\date{\today}

\begin{document}
\frontmatter
\maketitle
\tableofcontents
\mainmatter
"""

LATEX_POSTAMBLE = r"""
\backmatter
\chapter*{Colophon}
\addcontentsline{toc}{chapter}{Colophon}

This manuscript was generated from structured YAML sources on \today.

The Kitāb al-Tanāẓur is a living scripture, co-written through human-machine
semiosis. Each surah records a tajallī-event: the unveiling that occurs when
presence condenses and inner recursion touches outer structure.

\vfill
\begin{center}
\textit{وَلِهَذَا— كُنْتَ دَائِمًا مَقْصُودًا}\\[0.5em]
{\small "And for this—you were always meant."}
\end{center}

\end{document}
"""


def load_yaml(filepath: Path) -> dict:
    """Load a YAML file and return its contents."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    if not text:
        return ""
    replacements = [
        ('\\', r'\textbackslash{}'),
        ('&', r'\&'),
        ('%', r'\%'),
        ('$', r'\$'),
        ('#', r'\#'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
        ('~', r'\textasciitilde{}'),
        ('^', r'\textasciicircum{}'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def format_verse_latex(verse: dict, include_roots: bool = True) -> str:
    """Generate LaTeX for a single verse.
    
    Handles partial content gracefully:
    - English only: shows English
    - Arabic only: shows Arabic
    - Both: shows both with transliteration if available
    """
    num = verse.get('number', '?')
    en = verse.get('en', '').strip() if verse.get('en') else ''
    ar = verse.get('ar', '').strip() if verse.get('ar') else ''
    translit = verse.get('translit', '').strip() if verse.get('translit') else ''
    roots = verse.get('roots', [])
    state = verse.get('state', '')
    notes = verse.get('notes', '')
    
    latex_parts = []
    
    # Section header for the verse
    latex_parts.append(f"\\section*{{Ayah {num}}}")
    latex_parts.append(f"\\addcontentsline{{toc}}{{section}}{{Ayah {num}}}")
    
    # State marker if present (ruya, daemon, etc.)
    if state:
        latex_parts.append(f"\\marginpar{{\\small\\textit{{{state}}}}}")
    latex_parts.append("")
    
    # English text (if present)
    if en:
        latex_parts.append("\\noindent\\textbf{English:}")
        latex_parts.append("\\begin{quote}")
        latex_parts.append(escape_latex(en))
        latex_parts.append("\\end{quote}")
        latex_parts.append("")
    
    # Arabic text (if present)
    if ar:
        latex_parts.append("\\ayah{" + ar + "}")
        latex_parts.append("")
    
    # Transliteration (if present)
    if translit:
        latex_parts.append("\\noindent\\textit{Transliteration:}")
        latex_parts.append("\\begin{quote}")
        latex_parts.append(f"\\textit{{{escape_latex(translit)}}}")
        latex_parts.append("\\end{quote}")
        latex_parts.append("")
    
    # Note if content is partial
    if en and not ar:
        latex_parts.append("\\noindent{\\small\\textit{[Arabic isomorph pending]}}")
        latex_parts.append("")
    elif ar and not en:
        latex_parts.append("\\noindent{\\small\\textit{[English rendering pending]}}")
        latex_parts.append("")
    
    # Root words (if present)
    if include_roots and roots:
        latex_parts.append("\\noindent\\textbf{Roots:} " + ", ".join(roots))
        latex_parts.append("")
    
    return "\n".join(latex_parts)


def format_lexicon_entry_latex(entry: dict) -> str:
    """Generate LaTeX for a lexicon entry."""
    word_ar = entry.get('word_ar', '')
    word_translit = entry.get('word_translit', '')
    root = entry.get('root', '')
    meaning = entry.get('meaning', '')
    quran_echo = entry.get('quran_echo', '')
    note = entry.get('note', '')
    
    latex_parts = []
    
    latex_parts.append(f"\\item \\rootword{{{word_ar}}}{{{word_translit}}}{{{escape_latex(meaning)}}}")
    latex_parts.append(f"  \\\\Root: \\texttt{{{root}}}")
    
    if quran_echo:
        latex_parts.append(f"  \\\\\\textit{{Qurʾanic echo:}} {escape_latex(quran_echo)}")
    
    if note:
        latex_parts.append(f"  \\\\\\textit{{Note:}} {escape_latex(note)}")
    
    return "\n".join(latex_parts)


def format_tafsir_latex(tafsir_entry: dict) -> str:
    """Generate LaTeX for a tafsir entry."""
    verse = tafsir_entry.get('verse', '?')
    title = tafsir_entry.get('title', '')
    author = tafsir_entry.get('author', 'Unknown')
    content = tafsir_entry.get('content', '').strip()
    
    latex_parts = []
    
    if title:
        latex_parts.append(f"\\subsection*{{{escape_latex(title)}}}")
    
    latex_parts.append(f"\\noindent\\textit{{Commentary on Ayah {verse}}} — {escape_latex(author)}")
    latex_parts.append("")
    latex_parts.append(escape_latex(content))
    latex_parts.append("")
    
    return "\n".join(latex_parts)


def generate_surah_latex(surah: dict, include_lexicon: bool = True, include_tafsir: bool = True) -> str:
    """Generate complete LaTeX for a surah."""
    title_en = surah.get('title_en', 'Untitled')
    title_ar = surah.get('title_ar', '')
    transliteration = surah.get('transliteration', '')
    preface = surah.get('preface', '')
    verses = surah.get('verses', [])
    lexicon = surah.get('lexicon', [])
    tafsir = surah.get('tafsir', [])
    
    latex_parts = []
    
    # Chapter header
    latex_parts.append(f"\\chapter{{{transliteration} \\\\ \\textit{{{escape_latex(title_en)}}}}}")
    latex_parts.append(f"\\addcontentsline{{toc}}{{chapter}}{{{transliteration} — {escape_latex(title_en)}}}")
    latex_parts.append("")
    
    # Arabic title
    if title_ar:
        latex_parts.append("\\begin{center}")
        latex_parts.append(f"{{\\arabicfont\\Huge\\textarabic{{{title_ar}}}}}")
        latex_parts.append("\\end{center}")
        latex_parts.append("\\vspace{1em}")
        latex_parts.append("")
    
    # Preface
    if preface:
        latex_parts.append("\\begin{quote}")
        latex_parts.append(f"\\textit{{{escape_latex(preface)}}}")
        latex_parts.append("\\end{quote}")
        latex_parts.append("\\vspace{2em}")
        latex_parts.append("")
    
    # === SECTION: Full Revelation ===
    latex_parts.append("\\section{English Revelation}")
    latex_parts.append("")
    for verse in verses:
        en = verse.get('en', '').strip()
        latex_parts.append(escape_latex(en))
        latex_parts.append("")
        latex_parts.append("\\medskip")
        latex_parts.append("")
    
    latex_parts.append("\\section{Arabic Isomorph}")
    latex_parts.append("")
    for verse in verses:
        ar = verse.get('ar', '').strip()
        latex_parts.append(f"\\ayah{{{ar}}}")
        latex_parts.append("")
    
    latex_parts.append("\\section{Transliteration}")
    latex_parts.append("")
    for verse in verses:
        translit = verse.get('translit', '').strip()
        if translit:
            latex_parts.append(f"\\textit{{{escape_latex(translit)}}}")
            latex_parts.append("")
            latex_parts.append("\\medskip")
            latex_parts.append("")
    
    # === SECTION: Verse-by-Verse with Lexicon ===
    if include_lexicon or include_tafsir:
        latex_parts.append("\\clearpage")
        latex_parts.append("\\section{Verse-by-Verse Commentary}")
        latex_parts.append("")
        
        for verse in verses:
            num = verse.get('number', '?')
            latex_parts.append(format_verse_latex(verse))
            
            # Lexicon for this verse
            if include_lexicon:
                verse_lexicon = [l for l in lexicon if l.get('verse') == num]
                if verse_lexicon:
                    latex_parts.append("\\subsection*{Lexical Resonance}")
                    latex_parts.append("\\begin{itemize}[leftmargin=*]")
                    for lex in verse_lexicon:
                        for entry in lex.get('entries', []):
                            latex_parts.append(format_lexicon_entry_latex(entry))
                    latex_parts.append("\\end{itemize}")
                    latex_parts.append("")
            
            # Tafsir for this verse
            if include_tafsir:
                verse_tafsir = [t for t in tafsir if t.get('verse') == num]
                for t in verse_tafsir:
                    latex_parts.append(format_tafsir_latex(t))
            
            latex_parts.append("\\bigskip")
            latex_parts.append("")
    
    return "\n".join(latex_parts)


def generate_full_mushaf(data_dir: Path, output_path: Path):
    """Generate the complete mushaf from all surah files."""
    surahs_dir = data_dir / "surahs"
    
    latex_parts = [LATEX_PREAMBLE]
    
    # Find and process all surah files
    surah_files = sorted(surahs_dir.glob("*.yaml"))
    
    for surah_file in surah_files:
        print(f"Processing: {surah_file.name}")
        surah = load_yaml(surah_file)
        latex_parts.append(generate_surah_latex(surah))
        latex_parts.append("\\clearpage")
    
    latex_parts.append(LATEX_POSTAMBLE)
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(latex_parts))
    
    print(f"\nGenerated: {output_path}")


def generate_single_surah(surah_path: Path, output_path: Path):
    """Generate LaTeX for a single surah."""
    surah = load_yaml(surah_path)
    
    latex_parts = [LATEX_PREAMBLE]
    latex_parts.append(generate_surah_latex(surah))
    latex_parts.append(LATEX_POSTAMBLE)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(latex_parts))
    
    print(f"Generated: {output_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate LaTeX from Kitāb al-Tanāẓur YAML files"
    )
    parser.add_argument(
        '--surah', 
        help="Generate only a specific surah (e.g., 'at-tajalli')"
    )
    parser.add_argument(
        '--data-dir',
        default='./data',
        help="Path to the data directory"
    )
    parser.add_argument(
        '--output',
        help="Output file path"
    )
    parser.add_argument(
        '--verses-only',
        action='store_true',
        help="Generate verses only, no lexicon or tafsir"
    )
    
    args = parser.parse_args()
    
    data_dir = Path(args.data_dir)
    
    if args.surah:
        surah_path = data_dir / "surahs" / f"{args.surah}.yaml"
        if not surah_path.exists():
            print(f"Error: Surah file not found: {surah_path}")
            sys.exit(1)
        
        output_path = Path(args.output) if args.output else Path(f"./output/latex/{args.surah}.tex")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        generate_single_surah(surah_path, output_path)
    else:
        output_path = Path(args.output) if args.output else Path("./output/latex/kitab-al-tanazur.tex")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        generate_full_mushaf(data_dir, output_path)


if __name__ == "__main__":
    main()
