import numpy as np

from mature import Mature
from reader import create_map_5p_3p, init_p, export_table_to_csv

# pre-mir-name: cin-mir-4074
# to ->
# seed: AACGUU
pre_mir_name_to_seeds_map = {}

# pre-mir-name: cin-mir-4074
# to ->
# mature-name-and-type: {{cin-miR-4074-3p, 3p}}
pre_mir_name_to_mature_5p_or_3p_map = {}


def table_from_txt_file(path_input, seed_length):
    pname_to_data = create_map_5p_3p("mature.txt")
    with open(path_input, "r") as f:
        split_txt = f.read().split('>')

    preMirName = []
    organisms = []
    preMirSeq = []

    fivePMatureMirName = []
    fivePMatureMirSeq = []
    fivePMatureMirSeed = []

    threePMatureMirName = []
    threePMatureMirSeq = []
    threePMatureMirSeed = []

    metazoaFamilies = [
        "Xenoturbella bocki",
        "Branchiostoma belcheri",
        "Branchiostoma floridae",
        "Ciona intestinalis",
        "Ciona savignyi",
        "Oikopleura dioica",
        "Petromyzon marinus",
        "Xenopus laevis",
        "Xenopus tropicalis",
        "Anas platyrhynchos",
        "Columba livia",
        "Gallus gallus",
        "Taeniopygia guttata",
        "Callorhinchus milii",
        "Echinops telfairi",
        "Canis familiaris",
        "Dasypus novemcinctus",
        "Oryctolagus cuniculus",
        "Artibeus jamaicensis",
        "Bubalus bubalis",
        "Equus caballus",
        "Eptesicus fuscus",
        "Pteropus alecto",
        "Monodelphis domestica",
        "Macropus eugenii",
        "Sarcophilus harrisii",
        "Ateles geoffroyi",
        "Lagothrix lagotricha",
        "Callithrix jacchus",
        "Saimiri boliviensis",
        "Saguinus labiatus",
        "Macaca mulatta",
        "Macaca nemestrina",
        "Pygathrix bieti",
        "Papio hamadryas",
        "Microcebus murinus",
        "Daubentonia madagascariensis",
        "Otolemur garnettii",
        "Gorilla gorilla",
        "Homo sapiens",
        "Pan paniscus",
        "Pongo pygmaeus",
        "Pan troglodytes",
        "Symphalangus syndactylus",
        "Nomascus leucogenys",
        "Lemur catta",
        "Ornithorhynchus anatinus",
        "Cricetulus griseus",
        "Cavia porcellus",
        "Mus musculus",
        "Rattus norvegicus",
        "Bos taurus",
        "Capra hircus",
        "Ovis aries",
        "Tupaia chinensis",
        "Sus scrofa",
        "Anolis carolinensis",
        "Alligator mississippiensis",
        "Chrysemys picta",
        "Ophiophagus hannah",
        "Python bivittatus",
        "Astatotilapia burtoni",
        "Carassius auratus",
        "Cyprinus carpio",
        "Danio rerio",
        "Electrophorus electricus",
        "Fugu rubripes",
        "Gadus morhua",
        "Hippoglossus hippoglossus",
        "Ictalurus punctatus",
        "Metriaclima zebra",
        "Neolamprologus brichardi",
        "Nothobranchius furzeri",
        "Oryzias latipes",
        "Oncorhynchus mykiss",
        "Oreochromis niloticus",
        "Pundamilia nyererei",
        "Paralichthys olivaceus",
        "Salmo salar",
        "Tetraodon nigroviridis",
        "Lytechinus variegatus",
        "Patiria miniata",
        "Strongylocentrotus purpuratus",
        "Saccoglossus kowalevskii",
        "Ixodes scapularis",
        "Parasteatoda tepidariorum",
        "Rhipicephalus microplus",
        "Tetranychus urticae",
        "Daphnia pulex",
        "Marsupenaeus japonicus",
        "Triops cancriformis",
        "Aedes aegypti",
        "Anopheles gambiae",
        "Aphis gossypii",
        "Apis mellifera",
        "Acyrthosiphon pisum",
        "Bactrocera dorsalis",
        "Biston betularia",
        "Bombyx mori",
        "Culex quinquefasciatus",
        "Drosophila ananassae",
        "Drosophila erecta",
        "Drosophila grimshawi",
        "Drosophila melanogaster",
        "Drosophila mojavensis",
        "Drosophila persimilis",
        "Drosophila pseudoobscura",
        "Dinoponera quadriceps",
        "Drosophila sechellia",
        "Drosophila simulans",
        "Drosophila virilis",
        "Drosophila willistoni",
        "Drosophila yakuba",
        "Heliconius melpomene",
        "Locusta migratoria",
        "Mayetiola destructor",
        "Manduca sexta",
        "Nasonia giraulti",
        "Nasonia longicornis",
        "Nasonia vitripennis",
        "Polistes canadensis",
        "Plutella xylostella",
        "Spodoptera frugiperda",
        "Tribolium castaneum",
        "Strigamia maritima",
        "Ascaris suum",
        "Brugia malayi",
        "Brugia pahangi",
        "Caenorhabditis brenneri",
        "Caenorhabditis briggsae",
        "Caenorhabditis elegans",
        "Caenorhabditis remanei",
        "Haemonchus contortus",
        "Heligmosomoides polygyrus",
        "Pristionchus pacificus",
        "Panagrellus redivivus",
        "Strongyloides ratti",
        "Capitella teleta",
        "Glottidia pyramidata",
        "Terebratulina retusa",
        "Haliotis rufescens",
        "Lottia gigantea",
        "Melibe leonina",
        "Cerebratulus lacteus",
        "Echinococcus granulosus",
        "Echinococcus multilocularis",
        "Fasciola hepatica",
        "Gyrodactylus salaris",
        "Mesocestoides corti",
        "Schistosoma japonicum",
        "Schistosoma mansoni",
        "Schmidtea mediterranea",
        "Aiptasia pallida",
        "Hydra magnipapillata",
        "Nematostella vectensis",
        "Amphimedon queenslandica",
        "Leucosolenia complicata",
        "Sycon ciliatum"
    ]

    for entry in split_txt:
        if len(entry) > 0:
            split_entry = entry.split(" ")
            organism = split_entry[2] + " " + split_entry[3]

            if organism in metazoaFamilies:
                pre_mir_name = split_entry[0]
                organisms.append(organism)
                preMirName.append(pre_mir_name)
                preMirSeq.append(split_entry[-1].replace("\n", '').replace('stem-loop', ''))

                # init 5p 3p
                entry_five_p = pname_to_data.get(pre_mir_name.lower() + "-5p", None)
                entry_three_p = pname_to_data.get(pre_mir_name + "-3p", None)

                pre_mir_name_to_seeds_map[pre_mir_name] = {}
                pre_mir_name_to_mature_5p_or_3p_map[pre_mir_name] = {}

                if entry_five_p is not None:
                    name, seq, seed = init_p(entry_five_p, seed_length)
                    pre_mir_name_to_seeds_map[pre_mir_name][seed] = entry_five_p

                    mature = Mature(pre_mir_name, name, "5p", seed)
                    pre_mir_name_to_mature_5p_or_3p_map[pre_mir_name]["5p"] = mature
                else:
                    name, seq, seed = None, None, None

                fivePMatureMirName.append(name)
                fivePMatureMirSeq.append(seq)
                fivePMatureMirSeed.append(seed)

                if entry_three_p is not None:
                    name, seq, seed = init_p(entry_three_p, seed_length)
                    pre_mir_name_to_seeds_map[pre_mir_name][seed] = entry_three_p

                    mature = Mature(pre_mir_name, name, "3p", seed)
                    pre_mir_name_to_mature_5p_or_3p_map[pre_mir_name]["3p"] = mature
                else:
                    name, seq, seed = None, None, None

                threePMatureMirName.append(name)
                threePMatureMirSeq.append(seq)
                threePMatureMirSeed.append(seed)

    data = np.array([preMirName,
                     organisms,
                     preMirSeq,
                     fivePMatureMirName,
                     fivePMatureMirSeq,
                     fivePMatureMirSeed,
                     threePMatureMirName,
                     threePMatureMirSeq,
                     threePMatureMirSeed])

    # export_table_to_csv([preMirName,
    #                      organisms,
    #                      preMirSeq,
    #                      fivePMatureMirName,
    #                      fivePMatureMirSeq,
    #                      fivePMatureMirSeed,
    #                      threePMatureMirName,
    #                      threePMatureMirSeq,
    #                      threePMatureMirSeed])

    return data
