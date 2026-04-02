### Paragraph Definition

A paragraph is defined as one complete listing description from the dataset. Since each row in the CSV contains a full service or product listing, each row naturally serves as a paragraph-level unit. This approach ensures that paragraph boundaries are semantically meaningful and that chunking begins from complete units of text rather than arbitrary text fragments.

### Overlap Implementation

Overlap is implemented using a sliding window approach with a window size of 2 paragraphs and a stride of 1 paragraph. This means each chunk contains two adjacent paragraphs, and consecutive chunks share one paragraph of overlap. For example, Chunk 1 contains Paragraphs 1 and 2, while Chunk 2 contains Paragraphs 2 and 3. This overlap preserves continuity and improves retrieval when relevant information spans nearby paragraphs.

### Complete Thought Requirement

To ensure that each chunk represents a complete thought, chunk boundaries are placed only between full paragraphs, never inside sentences. In addition, the hybrid chunking strategy groups paragraphs by semantic category so that each chunk remains topically coherent and does not merge unrelated content.