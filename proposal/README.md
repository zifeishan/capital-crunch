Proposal Directory
====

How to compile it
----

Now we switch to source tex files. DO NOT RUN "make all"

<!-- - Be sure you have pandoc on your computer.
  - For mac: sudo port install pandoc
- Run "make all".
 -->

How do I add my work
----

- Put your section under "src/". Never under "tex/".
- Modify "Makefile" to add rules for your section.
- Modify "template/template.tex" to add inputs for your section.


Directory Structure
----

.
├── Makefile          -- Modify this when added new sections
├── README.md
├── fixbib.sty
├── src                 -- All source files (md / tex / bib) are here
│   ├── aaai2013.bib
│   ├── abstract.md
│   ├── proposal.md
│   ├── related.bib
│   ├── related.tex
│   └── template.tex
├── template            -- AAAI template files.
│   ├── aaai.bst
│   ├── aaai.sty
│   ├── aaai_script.sh
│   └── template.tex    -- Modify this when added new sections
└── tex                 -- Output only -- DO NOT MODIFY FILES IN THIS! 
    ├── abstract.tex
    ├── proposal.tex
    └── related.tex
