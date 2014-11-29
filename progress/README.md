Progress report
====

We use MarkDown to write up this document.

How to compile it
----

- Be sure you have pandoc on your computer.
  - http://johnmacfarlane.net/pandoc/installing.html

- Run `make` to translate markdowns to PDF.


How do I add my work
----

- Put your section under `src/`. Never under `build/`.
- Modify `Makefile` to add rules for your section.
- Modify `template/template*.tex` to add inputs for your section.


Directory Structure
----

```
.
├── Makefile
├── README.md
├── build                -- Output only -- DO NOT MODIFY FILES IN THIS! 
│   └── proposal.tex
├── proposal.pdf
├── src                  -- All source files (md / tex / bib) are here
│   ├── cs221.bib
│   └── proposal.md
└── template
    ├── sig-alternate.cls
    └── templateacm.tex  -- LaTeX Template file
```

