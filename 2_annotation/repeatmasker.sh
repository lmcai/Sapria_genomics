module load RepeatMasker/4.0.5-fasrc05
RepeatMasker -gff -pa 16  -no_is -lib Sapria_10k-families.fa Sapria_V1.softmasked.fa -xsmall -dir repeatmasker


#result summarization

bases masked: 1011685580 bp ( 79.02 %)
==================================================
               number of      length   percentage
               elements*    occupied  of sequence
--------------------------------------------------
SINEs:            15844      2406366 bp    0.19 %
      ALUs            0            0 bp    0.00 %
      MIRs            0            0 bp    0.00 %
LINEs:            85488     83828325 bp    6.55 %
      LINE1       48048     65084465 bp    5.08 %
      LINE2        7067      1800093 bp    0.14 %
      L3/CR1          0            0 bp    0.00 %
LTR elements:    300622    210689527 bp   16.46 %
      ERVL            0            0 bp    0.00 %
      ERVL-MaLRs      0            0 bp    0.00 %
      ERV_classI    245       127745 bp    0.01 %
      ERV_classII   443       152302 bp    0.01 %
DNA elements:    544571    535494731 bp   41.83 %
     hAT-Charlie      0            0 bp    0.00 %
     TcMar-Tigger     0            0 bp    0.00 %
Unclassified:    375636    143982973 bp   11.25 %
Total interspersed repeats:976401922 bp   76.27 %
Small RNA:        16102      2633433 bp    0.21 %
Satelmnlites:       16325      3940112 bp    0.31 %
Simple repeats:  240010     31870223 bp    2.49 %
Low complexity:   30962      9354324 bp    0.73 %
==================================================