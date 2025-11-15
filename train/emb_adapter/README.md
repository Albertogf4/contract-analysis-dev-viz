# Fine-Tuning Embedding Models for Specific Use Case

In this folder, we train a query-only model adapter as a first step to optimizing the embeddings process in a RAG pipeline. The explanation behind all this project will be detailed in the linked paper [@TODO: link to paper]

The training process wil follow the next steps:
1. The document will be preprocessed and cleaned with LlamaParse
2. The cleaned markdown file will be chunked
3. The LLM will generate questions out of each chunk of the PDF. 
4. The function loss will be the Triplet loss. THis function loss operates on triplets of:
    1. Anchor: question / query from the questions
    2. Positive: chunk that corresponds to the generated question
    3. Negative: an randomily chosen chunk from the rest of the chunks 
5. Run the training script with an scheduler + optimizer
6. Run the validation script
7. Analyze results


## Synthetic Dataset Generation

In order to do this, we will need a dataset to train this model. This dataset will be created with the help of an LLM out of a PDF document.


To create the index:
1. The document will be preprocessed and cleaned with LlamaParse
2. The cleaned markdown file will be chunked
3. The LLM will generate questions out of each chunk of the PDF. 

To create the index (Chroma) from your corpus PDF, execute:
```bash
python -m train.emb_adapter.scripts.build_index \
  --pdf ./data/salesforce-fy25-stakeholder-impact-report.pdf \
  --collection sf_collection \
  --db_path ./chroma_db \
  --reset
```



