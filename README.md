# MAPS-KB
Code and data for the paper "MAPS-KB: A Million-scale Probabilistic Simile Knowledge Base" (AAAI 2023)(The rest of the files will be Coming Soon!)

## Data
You can download the following files from [this Google Drive URL](https://drive.google.com/drive/folders/1YUNFo4ZB4AuQOmzFT0cYyQB1IBqoU-un?usp=share_link):
- `MAPS-KB.csv`: Our million-scale probabilistic simile knowledge base, including 4.3 million simile triplets in the form of (*topic*, *property*, *vehicle*) along with two probabilistic metrics, *plausibility* and *typicality*, to model them.
- `Simile Instances`: The simile instances in the form of (*simile sentence*, *topic*, *property*, *vehicle*) that we used to construct MAPS-KB. We collect them from 70 GB corpora, including:
  - `simile_instance_bc.csv`: [BookCorpus](https://huggingface.co/datasets/bookcorpus)
  - `simile_instance_gutenburg.csv`: [Gutenburg](https://github.com/pgcorpus/gutenberg)
  - `simile_instance_opw.csv`: [Openwebtext](https://drive.google.com/drive/folders/1IaD_SIIB-K3Sij_-JjWoPy_UrWqQRdjx)
