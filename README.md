# Focus
ICCS2021 Conference Paper - metric calculating


## Process

Use the .xml process to run ETR full pipeline. 

Use [RapidMiner](https://rapidminer.com/) + the [Text Proecessing](https://marketplace.rapidminer.com/UpdateServer/faces/product_details.xhtml?productId=rmx_text) extension to run the process.

## Files

Each file encodes the portion of the reference KB used in the experiments (i.e., Schema.org, SUMO, OpenCyc and DBpedia)


## Usage

3.Orders on processing programs:
  DataAnalyzer: statistics of the Etpes and property of each schema [Results/Sta_of_Schemas.csv]
  DataExplorer: calulate Balance of schemas [Balance]
  FCAGenerator: generate FCAs by schemas [FCA_singleEtype1, FCA_SumUpEtype1]
  FCA_Analyzer: make a statistics of FCA of Schemas [Results/Sta_of_FCAs.csv]
  GenerateCues: generate Cues for schemas [Cue/...]
  GenerateFreqs: generate Freqs for schemas [Freq/...]
  Sta_Cue&Freq: Statistics of Cues and Freqs [Results/sta_schemas.csv]
  Sta_SoA: using some Schemas to test SoAs [Sta_SoA/...]


4.Visualization:
  InterVenn: class of Visualization
  VennG4Etypes: visualization of three kinds of statistics
