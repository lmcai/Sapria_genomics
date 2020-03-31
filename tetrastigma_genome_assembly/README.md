Tetrastiga genome assembly
===============

The genome assembly of Tetrastigma voinierianum is a merged assembly from three nanopore de novo assemblies using miniasm, CANU, and Shasta, respectively.

Prior to assembly, we removed nanopore reads shorter than 10kb. The scripts used for three assembly pipeline and the final merging step is as follows:
## 1. minimap-miniasm-pilon pipeline
- This pipeline generates an all-by-all alignment of nanopore reads using minimap. Then the miniasm assembler will generate a de novo assembly based on the alignment. Finally, the assembly is iteratively polished by Illumina reads using pilon.
- script: `minimap_miniasm_pilon.sh`
## 2. CANU pipeline
- CANU automatically correct, trim, and assemble nanopore reads to generate an assembly.
- script: `canu.sh`
## 3. Shasta pipeline
- Shasta is the most recently developed de novo assembler from Oxford Nanopore reads.
- script: `shasta.sh`
## 4. Assembly merge
- We used Quickmerge to merge three assemblies and improve contiguity of genome assemblies based on nanopore sequences.
- script: `quickmerge.sh`
