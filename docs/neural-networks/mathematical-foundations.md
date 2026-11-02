# Mathematical foundations

The core computation is built around a differentiable feed-forward stack.

### Feature encoding

Each token is mapped to a vector from the token embedding table.

### Hidden layer

`h = tanh(x @ W1 + b1)`

### Output layer

`y = h @ W2 + b2`

### Loss

The model computes a softmax cross-entropy style loss over the output logits.
