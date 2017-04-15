# Verb-Particle-Constructions

The project involves developing a broad-coverage deep semantic lexicon for a system (TRIPS) that parses sentences into a logical form expressed in a rich ontology (TRIPS Ontology) that supports reasoning. This repository specifically concerns verb particle constructions (VPCs).

To execute the heuristics script (vpc-compositionality-heuristics.py), provide as inputs the particles' list, light verbs' list and the list of VPCs for which compositionality type is to be determined. For example, try the following: 

python VPCCompositionalityHeuristics.py --particles docs/particles.txt --light-verbs docs/light_verbs.txt --test-cases docs/test_vpc.txt
