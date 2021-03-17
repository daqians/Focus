# Focus
ICCS2021 Conference Paper - metric calculating


## Process

Use the KnowledgeScraper.xml and KnowledgeParser.xml process to run data downloading pipeline. 

Use [RapidMiner](https://rapidminer.com/) + the [Text Proecessing](https://marketplace.rapidminer.com/UpdateServer/faces/product_details.xhtml?productId=rmx_text) extension to run the process.

With downloaded Knowledge Based schemas (KBSs), Fcous metrics can be obtained by following scripts

FCAGenerator: generate FCAs by KBSs.

FCA_Analyzer: make a statistics of FCAs.

GenerateCues: generate Cues for KBSs and entity types (Etypes).

Sta_Cue&Freq: Statistics of Cues.

VennG4Etypes: visualization of all kinds of metrics.


