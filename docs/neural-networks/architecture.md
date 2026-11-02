# Neural network architecture

SYNTHOS currently uses a compact feed-forward network for local execution. It is suitable for workflows where a minimal model is preferable to a large pre-trained system.

## Mathematical summary

The model computes:

- feature vector from token embeddings
- hidden activation using tanh
- logits from hidden to output
- cross-entropy style loss

## Tensor dimensions

- embedding: (vocab_size, embedding_dim)
- hidden projection: (embedding_dim, hidden_dim)
- output projection: (hidden_dim, 2)

This is a small, inspectable setup suitable for testing and workflow validation.
