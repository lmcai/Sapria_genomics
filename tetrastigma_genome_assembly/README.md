Tetrastiga genome assembly
===============

The genome assembly of Tetrastigma voinierianum is a merged assembly from three nanopore de novo assemblies using miniasm, CANU, and Shasta, respectively.

Prior to assembly, we removed nanopore reads shorter than 10kb. The scripts used for three assembly pipeline and the final merging step is as follows:
1. minimap-miniasm-pilon pipeline
- This pipeline generates an all-by-all alignment of nanopore reads first using minimap. Then the miniasm assembler will generate a de novo assembly based on the reads alignment. Finally, the assembly is iteratively polished by mapping Illumina reads to the assembly.
- script: minimap_miniasm.sh
2. CANU pipeline: canu.sh
3. Shasta pipeline: shasta.sh
4. Assembly merge: quickmerge.sh
