#!/usr/bin/env python
#-*-coding: utf-8 -*-


import random
import argparse
from nltk.corpus import wordnet as wn


def get_compositionality_type(particles, light_verbs, VPCs2check):
    """
    Determine compositionality type for a given VPC. Its arguments are the particles' list, the light verbs' list and the list of VPCs for which we want to determine compositionality type.
    Relevant synsets for the VPCs are also identified for which a specific compositionality type is assigned. These can be printed by uncommenting the relevant commented out parts.
    """

    heur1_LVC = []
    heur2_symm_VPC = []

    heur3_LPC = []
    heur3_LPC_specific_synset = {}

    heur4_symm_VPC_LPC = []
    heur4_symm_VPC_LPC_specific_synset = {}

    heur5_symm_VPC_LPC = []
    heur5_symm_VPC_LPC_specific_synset = {}

    heur6_symm_VPC_LPC = []
    heur6_symm_VPC_LPC_specific_synset = {}

    heur7_symm_VPC_LPC = []
    heur7_symm_VPC_LPC_LVC_specific_synset = {}

    heur8_noncomp_VPC = []
    potential_heur8_noncomp_VPC_sense_names = []
    heur8_noncomp_VPC_sense_names = []
    heur8_noncomp_VPC_sense_name_dict = {}
    heur8_noncomp_VPC_sense_name_dict_final = {}
    heur8_noncomp_VPC = []

    for VPC2check in VPCs2check:
        splitVPC2check = VPC2check.split("_")
        VERB = splitVPC2check[0]
        PRTCL = splitVPC2check[1]
        # HEURISTIC 1: If the verb in VPC is among the list of light verbs and
        # WordNet does not have an entry for the VPC, it most likely is
        # LV-compositional.
        if VERB in light_verbs:
            if not wn.synsets(VPC2check):
                heur1_LVC.append(VPC2check)
        # HEURISTIC 2: For a given VPC, if WordNet has an entry for the verb as
        # well as for the particle but no entry for the VPC, it is
        # Symmetrically compositional.
        elif (wn.synsets(VERB) and wn.synsets(PRTCL)) and (not wn.synsets(VPC2check)):
            heur2_symm_VPC.append(VPC2check)
            # print wn.synsets(VPC2check) #This should be an empty list.
        else:
            for sense in wn.synsets(
                    VPC2check):  # HEURISTIC 3,6,7, & partially 8
                senses_names3 = []
                senses_names4 = []
                senses_names5 = []
                senses_names6 = []
                senses_names7 = []

                # HEURISTIC 8: Noncompositional VPCs - If the VPC is in WordNet
                # but the sysnet containing it does not have any other item in
                # it, the VPC is likely idiomatic provided further conditions
                # for Heuristic 8 also apply, see below.
                if len(sense.lemmas()) == 1:
                    potential_heur8_noncomp_VPC_sense_names.append(
                        sense.name())
                    heur8_noncomp_VPC_sense_name_dict[sense.name().encode(
                        'utf-8')] = VPC2check

                for lemma in sense.lemmas():
                    splitlemma = str(lemma).split(".")[3].rstrip("')")
                    splitlemma_ = splitlemma.split("_")
                    if "_" in splitlemma:  # For Heuristics 6 & 7
                        # HEURISTIC 6: If WordNet has the relevant VPC as well
                        # as another VPC with the particle replaced with
                        # another particle in the same synset, VPC is either
                        # Symmetrically compositional or LP-compositional.
                        if (VERB == splitlemma_[0]) and (
                                PRTCL != splitlemma_[1]) and (splitlemma_[1] in particles):
                            if VPC2check not in heur6_symm_VPC_LPC:
                                heur6_symm_VPC_LPC.append(VPC2check)
                            if sense.name() not in senses_names6:
                                senses_names6.append(sense.name())
                            heur6_symm_VPC_LPC_specific_synset[VPC2check] = senses_names6

                        # HEURISTIC 7: If WordNet has the relevant VPC as well
                        # as another VPC with the verb replaced with another
                        # verb in the same synset, VPC is compositional
                        # (Symmetrically compositional or LP-compositional or
                        # LV-compositional).
                        if (VERB != splitlemma_[0]) and (
                                PRTCL == splitlemma_[1]):
                            if VPC2check not in heur7_symm_VPC_LPC:
                                heur7_symm_VPC_LPC.append(VPC2check)
                            if sense.name() not in senses_names7:
                                senses_names7.append(sense.name())
                            heur7_symm_VPC_LPC_LVC_specific_synset[VPC2check] = senses_names7

                    # HEURISTIC 3: If WordNet has the VPC as well as the verb
                    # in the same synset, VPC is LP-compositional.
                    if VERB == (splitlemma):
                        if VPC2check not in heur3_LPC:
                            heur3_LPC.append(VPC2check)
                        if sense.name() not in senses_names3:
                            senses_names3.append(sense.name())
                        heur3_LPC_specific_synset[VPC2check] = senses_names3
                        break

                # HEURISTIC 4: If WordNet has the verb as a hypernym for the
                # VPC, VPC is likely either Symmetrically compositional or
                # LP-compositional.
                if sense.hypernyms():
                    for lemma in sense.hypernyms()[0].lemmas():
                        if VERB == (splitlemma):
                            if VPC2check not in heur4_symm_VPC_LPC:
                                heur4_symm_VPC_LPC.append(VPC2check)
                            if sense.name() not in senses_names4:
                                senses_names4.append(sense.name())
                            heur4_symm_VPC_LPC_specific_synset[VPC2check] = senses_names4
                # HEURISTIC 5: If WordNet has the verb in the definition in the
                # synset where VPC appears, VPC is either Symmetrically
                # compositional or LP-compositional.
                if VERB in sense.definition().split():
                    if VPC2check not in heur5_symm_VPC_LPC:
                        heur5_symm_VPC_LPC.append(VPC2check)
                    if sense.name() not in senses_names5:
                        senses_names5.append(sense.name())
                    heur5_symm_VPC_LPC_specific_synset[VPC2check] = senses_names5

    heur3 = [item for sublist in heur3_LPC_specific_synset.values()
             for item in sublist]
    heur3 = [item.encode('utf-8') for item in heur3]

    heur4 = [item for sublist in heur4_symm_VPC_LPC_specific_synset.values()
             for item in sublist]
    heur4 = [item.encode('utf-8') for item in heur4]

    heur5 = [item for sublist in heur5_symm_VPC_LPC_specific_synset.values()
             for item in sublist]
    heur5 = [item.encode('utf-8') for item in heur5]

    heur6 = [item for sublist in heur6_symm_VPC_LPC_specific_synset.values()
             for item in sublist]
    heur6 = [item.encode('utf-8') for item in heur6]

    heur7 = [item for sublist in heur7_symm_VPC_LPC_LVC_specific_synset.values()
             for item in sublist]
    heur7 = [item.encode('utf-8') for item in heur7]

    potential_heur8_noncomp_VPC_sense_names = [item.encode(
        'utf-8') for item in potential_heur8_noncomp_VPC_sense_names]

    # HEURISTIC 8: Noncompositional VPCs - If none of the other heuristics
    # apply and the preliminary conditions for Heuristic 8 mentioned above
    # (i.e., the VPC is in WordNet but the sysnet containing it does not have
    # any other item in it) apply, the VPC is most likely idiomatic.

    # TEST = ['put_out.v.02', 'put_out.v.06', 'down.v.05', 'chicken_out.v.01']

    for item_sense_name in potential_heur8_noncomp_VPC_sense_names:
        if (
            item_sense_name not in heur3) and (
            item_sense_name not in heur4) and (
            item_sense_name not in heur5) and (
                item_sense_name not in heur6) and (
                    item_sense_name not in heur7):
            heur8_noncomp_VPC_sense_names.append(item_sense_name)

#######################################################
#PRINT all annotated VPCs according to the heuristics:#
#######################################################

    print "\n\nCOMPOSITIONAL VPCs BASED ON HEURISTICS 1-7:"
    print "\nHeuristic 1 based LV-compositional VPCs: %s" % (heur1_LVC)
    print "\n\nHeuristic 2 based Symmetrically compositional VPCs: %s" % (heur2_symm_VPC)

    print "\n\nHeuristic 3 based LP-compositional VPCs: %s" % (heur3_LPC)
    # print "\nHeuristic 3 based LP-compositional VPCs with the relevant
    # synset: %s" % (heur3_LPC_specific_synset)

    print "\n\nHeuristic 4 based Symmetrically compositional VPCs or LP-compositional VPCs with the relevant synset: %s" % (heur4_symm_VPC_LPC)
    # print "\nHeuristic 4 based Symmetrically compositional VPCs or
    # LP-compositional VPCs with the relevant synset(s): %s" %
    # (heur4_symm_VPC_LPC_specific_synset)

    print "\nHeuristic 5 based Symmetrically compositional VPCs or LP-compositional VPCs with the relevant synset: %s" % (heur5_symm_VPC_LPC)
    # print "\nHeuristic 5 based Symmetrically compositional VPCs or
    # LP-compositional VPCs with the relevant synset(s): %s" %
    # (heur5_symm_VPC_LPC_specific_synset)

    print "\nHeuristic 6 based Symmetrically compositional VPCs or LP-compositional VPCs with the relevant synset: %s" % (heur6_symm_VPC_LPC)
    # print "\nHeuristic 6 based Symmetrically compositional VPCs or
    # LP-compositional VPCs with the relevant synset(s): %s" %
    # (heur6_symm_VPC_LPC_specific_synset)

    print "\nHeuristic 7 based Symmetrically compositional VPCs or LP-compositional VPCs or LV-compositional VPCs with the relevant synset: %s" % (heur7_symm_VPC_LPC)
    # print "\nHeuristic 7 based Symmetrically compositional VPCs or
    # LP-compositional VPCs or LV-compositional VPCs with the relevant
    # synset(s): %s" % (heur7_symm_VPC_LPC_LVC_specific_synset)

    print "\n\nNONCOMPOSITIONAL VPCs BASED ON HEURISTIC 8:"
    # print "\npotential_heur8_noncomp_VPC: %s" % (potential_heur8_noncomp_VPC_sense_names)
    # print "\nheur8_noncomp_VPC_sense_names: %s" % (heur8_noncomp_VPC_sense_names)
    # print "\nheur8_noncomp_VPC_sense_name_dict: %s" %
    # (heur8_noncomp_VPC_sense_name_dict)
    for key in heur8_noncomp_VPC_sense_names:
        heur8_noncomp_VPC_sense_name_dict_final[key] = heur8_noncomp_VPC_sense_name_dict[key]
    # print "\nheur8_noncomp_VPC_sense_name_dict_final: %s" %
    # (heur8_noncomp_VPC_sense_name_dict_final)
    heur8_noncomp_VPC = list(set(heur8_noncomp_VPC_sense_name_dict.values()))
    print "\nHeuristic 8 based Noncompositional VPCs: %s" % (heur8_noncomp_VPC)
    print "\n"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This is a script to determine compositionality type for a given VPC using a set of heuristics. Bhatia et al (2017) provides a description of the compositionality types for VPCs and heurtistics used to identify the types.')
    parser.add_argument(
        "--particles", dest="particles",
        required=True,
        help='path to the list of particles')
    parser.add_argument(
        "--light-verbs", dest="lverbs",
        required=True,
        help='path to the list of light verbs')
    parser.add_argument(
        "--test-cases",
        dest="tests",
        required=True,
        help='path to the list of VPCs for which we want to determine the compositionality type (format of a VPC: verb_particle)')

    args = parser.parse_args()

    with open(args.particles, "r") as fp_p, \
            open(args.lverbs, "r") as fp_lvs, \
            open(args.tests, "r") as fp_vps:

        particles = [particle.strip() for particle in fp_p]
        light_verbs = [lv.strip() for lv in fp_lvs]
        VPCs2check = [vp.strip() for vp in fp_vps]

    get_compositionality_type(particles, light_verbs, VPCs2check)
