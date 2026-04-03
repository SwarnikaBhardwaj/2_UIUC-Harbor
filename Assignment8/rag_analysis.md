### Paragraph Definition

A paragraph is defined as one complete listing description from the dataset. Since each row in the CSV contains a full 
service or product listing, each row naturally serves as a paragraph-level unit. This approach ensures that paragraph 
boundaries are semantically meaningful and that chunking begins from complete units of text rather than arbitrary text 
fragments.

### Overlap Implementation

Overlap is implemented using a sliding window approach with a window size of 2 paragraphs and a stride of 1 paragraph. 
This means each chunk contains two adjacent paragraphs, and consecutive chunks share one paragraph of overlap. For 
example, Chunk 1 contains Paragraphs 1 and 2, while Chunk 2 contains Paragraphs 2 and 3. This overlap preserves 
continuity and improves retrieval when relevant information spans nearby paragraphs.

### Complete Thought Requirement

To ensure that each chunk represents a complete thought, chunk boundaries are placed only between full paragraphs, 
never inside sentences. In addition, the hybrid chunking strategy groups paragraphs by semantic category so that each 
chunk remains topically coherent and does not merge unrelated content.

### Compare Embedding Models

The large embedding model had large cosine similarity scores the most frequently compared to smaller models having
a much smaller value. The larger models were also better at handling queries that required semantic understanding 
rather than just keyword matching. Generally, the retrieval scores for the large model had higher quality and 
fewer results with hallucinations. However, larger models did not always perform better, when testing queries with 
keyword based matches (for example, calculus tutoring or graduation photos), the small and medium models performed 
just as well as the larger model. The larger model was still the only model that consistently performed well.

### Comparing Chunking Strategies

The Hybrid chunking strategy worked the best for this dataset. Outputs using that strategy had higher quality scores 
whereas the fixed-length chunking performed very poorly for some queries. By grouping the listings by the category, 
the system could ensure that a single service listing was not split in half, ensuring that the context remained whole.
The overlap and hybrid strategy improved the relevant chunk retrieval scores compared to the fixed chunking scores. 
Lastly, the chunking greatly affected the final answers. Fixed chunking typically led to incomplete answers while the 
hybrid retrieval model was better. While it sometimes provided too much text, it did provide the correct details.

### Data Scaling Experiment

As a dataset size increases, the retrieval quality must be able to handle similar yet distinct content. For example, 
finding the difference between types of Photography or beauty services provided. These specifications require having 
higher embedding precision to accurately obtain answers. Noise will also increase as the amount of data increases. 
Larger datasets require better filtering and semantic understanding to ensure LLMs are not distracted by noise or 
irrelevant information.
