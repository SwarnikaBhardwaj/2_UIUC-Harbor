## Paragraph Definition

A paragraph is defined as one complete listing description from the dataset. Since each row in the CSV contains a full 
service or product listing, each row naturally serves as a paragraph-level unit. This approach ensures that paragraph 
boundaries are semantically meaningful and that chunking begins from complete units of text rather than arbitrary text 
fragments.

## Overlap Implementation

Overlap is implemented using a sliding window approach with a window size of 2 paragraphs and a stride of 1 paragraph. 
This means each chunk contains two adjacent paragraphs, and consecutive chunks share one paragraph of overlap. For 
example, Chunk 1 contains Paragraphs 1 and 2, while Chunk 2 contains Paragraphs 2 and 3. This overlap preserves 
continuity and improves retrieval when relevant information spans nearby paragraphs.

## Complete Thought Requirement

To ensure that each chunk represents a complete thought, chunk boundaries are placed only between full paragraphs, 
never inside sentences. In addition, the hybrid chunking strategy groups paragraphs by semantic category so that each 
chunk remains topically coherent and does not merge unrelated content.

## Compare Embedding Models

The large embedding model had large cosine similarity scores the most frequently compared to smaller models having
a much smaller value. The larger models were also better at handling queries that required semantic understanding 
rather than just keyword matching. Generally, the retrieval scores for the large model had higher quality and 
fewer results with hallucinations. However, larger models did not always perform better, when testing queries with 
keyword based matches (for example, calculus tutoring or graduation photos), the small and medium models performed 
just as well as the larger model. The larger model was still the only model that consistently performed well.

## Comparing Chunking Strategies

The Hybrid chunking strategy worked the best for this dataset. Outputs using that strategy had higher quality scores 
whereas the fixed-length chunking performed very poorly for some queries. By grouping the listings by the category, 
the system could ensure that a single service listing was not split in half, ensuring that the context remained whole.
The overlap and hybrid strategy improved the relevant chunk retrieval scores compared to the fixed chunking scores. 
Lastly, the chunking greatly affected the final answers. Fixed chunking typically led to incomplete answers while the 
hybrid retrieval model was better. While it sometimes provided too much text, it did provide the correct details.

## Data Scaling Experiment

As a dataset size increases, the retrieval quality must be able to handle similar yet distinct content. For example, 
finding the difference between types of Photography or beauty services provided. These specifications require having 
higher embedding precision to accurately obtain answers. Noise will also increase as the amount of data increases. 
Larger datasets require better filtering and semantic understanding to ensure LLMs are not distracted by noise or 
irrelevant information.

## Failure Analysis & Improvement
#### Retrieval Failure
Query: "Do any listings offer hair styling or makeup for events?"

Failure Description: The system failed to retrieve the relevant "Hairstylist" listing from the database. Instead, it 
returned chunks related to a "Nail Artist" and a "Photographer" because they shared the "event" context.

This was caused by the Small embedding model’s limited semantic resolution (384 dimensions) combined with Fixed 
Chunking. The fixed strategy likely split the hairstyling description in a way that diluted its primary keywords, 
making it rank lower than other service types.

#### Logic/Context Failure
Query: "Do any listings offer hair styling or makeup for events?"

Failure Description: Although the "Hairstylist" chunk was successfully retrieved at Rank 1, the LLM generated a 
negative response: "No, the provided listings do not offer hairstyling and makeup services together."

This was a Query Formulation and Prompting issue. The LLM interpreted the "and" in the user query too strictly. Because 
no single listing offered both services simultaneously, the model ignored the valid partial match for hairstyling

#### Incomplete Answer
Query: "Who offers graduation photography on campus?"

Failure Description: The LLM identified the correct service but provided a truncated response that ended mid-sentence: 
"...including the Quad, Alma Mater,".

This was a System Parameter failure. The max_new_tokens setting was capped at 60, which was insufficient for the model 
to finish describing the detailed marketplace listings.

### Implemented Fix: Parameter Scaling
To address the truncation and context issues, I increased the max_chars_per_chunk to 500 and the max_new_tokens to 100. 
This allowed the model to receive more complete listing descriptions and provided the necessary "room" to generate full 
responses without cutting off mid-sentence.

#### Before vs. After Comparison

Before Improvement : The response was cut off abruptly due to strict token limits: "A student photographer 
offers graduation photo sessions around popular UIUC landmarks including the Quad, Alma Mater,"

After Improvement: With the expanded limits, the model provided a comprehensive answer: "The UIUC junior in 
engineering offers personalized tutoring in calculus and linear algebra... The sessions are tailored to fit the 
student's syllabus, homework, and exam schedule... They provide customized sessions that align with your course 
materials..."

#### Results of the Change
This adjustment led to a significant improvement in answer quality, with the response length increasing from 
approximately 250 characters to 565 characters. While the system latency increased (from ~11s to ~24s for certain 
queries), the trade-off resulted in much more helpful and semantically complete information for the user.


