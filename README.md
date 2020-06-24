# Verb-Particle-Constructions

The project involves developing a broad-coverage deep semantic lexicon for a system (TRIPS) that parses sentences into a logical form expressed in a rich ontology (TRIPS Ontology) that supports reasoning. This repository specifically concerns verb particle constructions (VPCs).

To execute the heuristics script (VPCCompositionalityHeuristics.py), provide as inputs the particles' list, light verbs' list and the list of VPCs for which compositionality type is to be determined. For example, try the following: 

`python VPCCompositionalityHeuristics.py --particles docs/particles.txt --light-verbs docs/light_verbs.txt --test-cases docs/test_vpc.txt`


### Reference:
Archna Bhatia, Choh Man Teng & James F. Allen. 2018. Identifying senses of particles in verb-particle constructions. In Stella Markantonatou, Carlos Ramisch, Agata Savary & Veronika Vincze (eds.), Multiword expressions at length and in depth: Extended papers from the MWE 2017 workshop, 61–86. Berlin: Language Science Press. DOI:10.5281/zenodo.1469555 

Archna Bhatia, Choh Man Teng, and James F. Allen. 2017. Compositionality in Verb-Particle Constructions. In Proceedings of the 13th Workshop on Multiword Expressions (MWE 2017), pages 139–148, Valencia, Spain, April 4. http://aclweb.org/anthology/W/W17/W17-1719.pdf
