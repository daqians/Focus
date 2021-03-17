# Focus
ICCS2021 Conference Paper - metric calculating


## Process

Use the KnowledgeScraper.xml and KnowledgeParser process to run data downloading pipeline. 

Use [RapidMiner](https://rapidminer.com/) + the [Text Proecessing](https://marketplace.rapidminer.com/UpdateServer/faces/product_details.xhtml?productId=rmx_text) extension to run the process.

With downloaded ontologies, Fcous metrics can be obtained by following scripts

FCAGenerator: generate FCAs by schemas [FCA_singleEtype1, FCA_SumUpEtype1]
FCA_Analyzer: make a statistics of FCA of Schemas [Results/Sta_of_FCAs.csv]
GenerateCues: generate Cues for schemas [Cue/...]
Sta_Cue&Freq: Statistics of Cues and Freqs [Results/sta_schemas.csv]
VennG4Etypes: visualization of three kinds of statistics


