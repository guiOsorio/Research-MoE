# Research-MoE

## Understanding MoE
- [Adaptive Mixture of Local Experts](https://www.cs.toronto.edu/~hinton/absps/jjnh91.pdf) (July 1990)
- [Learning Factorized Representations in a Deep Mixture-of-Experts](https://arxiv.org/abs/1312.4314) (December 2013)
- [Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](https://arxiv.org/abs/1701.06538) (January 2017)
- [Towards Understanding MoE](https://arxiv.org/abs/2208.02813) (August 2022)
- [HuggingFace MoE Article](https://huggingface.co/blog/moe) (December 2023)
- [OpenMoE: An Early Effort on Open Mixture-of-Experts Language Models](https://arxiv.org/abs/2402.01739) (January 2024)

## Routing & Architecture
- [BASE Layers: Simplifying Training of Large, Sparse Models](https://arxiv.org/abs/2103.16716) (March 2021)
- [DSelect-k: Differentiable Selection in the Mixture of Experts with Applications to Multi-Task Learning](https://arxiv.org/abs/2106.03760) (June 2021)
- [Hash Layers for Large Sparse Models](https://arxiv.org/abs/2106.04426) (June 2021)
- [Mixture-of-Experts with Expert Choice Routing](https://arxiv.org/abs/2202.09368) (February 2022)
- [StableMoE: Stable Routing Strategy for Mixture of Experts](https://arxiv.org/abs/2204.08396) (April 2022)
- [From Sparse to Soft Mixture of Experts](https://arxiv.org/abs/2308.00951) (August 2023)
- [Mixture-of-Tokens: Efficient LLMs Through Cross-Example Aggregation](https://arxiv.org/abs/2310.15961) (October 2023)
- [Mixtral of Experts](https://arxiv.org/abs/2401.04088) + [Mistral 7B](https://arxiv.org/abs/2310.06825) (January 2024, October 2023)
- [DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models](https://arxiv.org/abs/2401.06066) (January 2024)

## Scaling & Stability
- [GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding](https://arxiv.org/abs/2006.16668) (June 2020)
- [Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](https://arxiv.org/abs/2101.03961) (January 2021)
- [GLaM: Efficient Scaling of Language Models with Mixture-of-Experts](https://arxiv.org/abs/2112.06905) (December 2021)
- [Efficient Large Scale Language Modeling with Mixtures of Experts](https://arxiv.org/abs/2112.10684) (December 2021)
- [Unified Scaling Laws for Routed Language Models](https://arxiv.org/abs/2202.01169) (February 2022)
- [ST-MoE: Designing Stable and Transferable Sparse Expert Models](https://arxiv.org/abs/2202.08906) (February 2022)

## Task/Domain-level MoE
- [Expert Gate: Lifelong Learning with a Network of Experts](https://arxiv.org/abs/1611.06194) (November 2016)
- [DEMix Layers: Disentangling Domains for Modular Language Modeling](https://arxiv.org/abs/2108.05036) (August 2021)
- [Beyond Distillation: Task-level Mixture-of-Experts for Efficient Inference](https://arxiv.org/abs/2110.03742) (September 2021)
- [Branch-Train-Merge: Embarrassingly Parallel Training of Expert Language Models](https://arxiv.org/abs/2208.03306) (August 2022)
- [Exploring the Benefits of Training Expert Language Models over Instruction Tuning](https://arxiv.org/abs/2302.03202) (February 2023)
- [Scaling Expert Language Models with Unsupervised Domain Discovery](https://arxiv.org/abs/2303.14177) (March 2023)

## MoE Efficiency
- [MegaBlocks: Efficient Sparse Training with Mixture-of-Experts](https://arxiv.org/abs/2211.15841) (November 2022)
- [Parameter-Efficient Mixture-of-Experts Architecture for Pre-Trained Language Models](https://arxiv.org/abs/2203.01104) (March 2022)
- [Fast Feedforward Networks](https://arxiv.org/abs/2308.14711) + [Exponentially Faster Language Modeling](https://arxiv.org/abs/2311.10770) (August 2023, November 2023)
- [Pushing Mixture-of-Experts to the Limit: Extremely Parameter Efficient MoE for Instruction Tuning](https://arxiv.org/abs/2309.05444) (September 2023)
- [QMoE: Practical Sub-1-Bit Compression of Trillion-Parameter Models](https://arxiv.org/abs/2310.16795) (October 2023)
- [Fast-Inference of Mixture-of-Experts Language Models with Offloading](https://arxiv.org/abs/2312.17238) (December 2023)
- [Parameter-Efficient Sparsity Crafting from Dense to Mixture-of-Experts for Instruction Tuning on General Tasks](https://arxiv.org/abs/2401.02731) (January 2024)

## Hybrid Approaches
- [EvoMoE: An Evolutional Mixture-of-Experts Training Framework via Dense-To-Sparse Gate](https://arxiv.org/abs/2112.14397) (December 2021)
- [Sparse Upcycling: Training Mixture-of-Experts from Dense Checkpoints](https://arxiv.org/abs/2212.05055) (December 2022)
- [Mixture-of-Experts Meets Instruction Tuning: A Winning Combination for Large Language Models](https://arxiv.org/abs/2305.14705) (May 2023)
- [Soft Merging of Experts with Adaptive Routing](https://arxiv.org/abs/2306.03745) (June 2023)
- [MoE-Mamba: Efficient Selective State Space Models with Mixture of Experts](https://arxiv.org/abs/2401.04081) (January 2024)
- [BlackMamba: Mixture of Experts for State-Space Models](https://arxiv.org/abs/2402.01771) (February 2024)




# Future Additions

- [Routing to the Expert: Efficient Reward-guided Ensemble of Large
Language Models](https://arxiv.org/abs/2311.08692) (November 2023)
- [Scalable Modular Network: a Framework for Adaptive Learning via Agreement Routing](https://openreview.net/forum?id=pEKJl5sflp) (January 2024)
- [ComPEFT: Compression for Communicating Parameter Efficient Updates via
Sparsification and Quantization](https://arxiv.org/abs/2311.13171) (November 2023)
- [Unlocking Emergent Modularity in Large Language Models](https://arxiv.org/abs/2310.10908) (October 2023)
- [Merge, Then Compress: Demystify Efficient SMOE With Hints From Its Routing Policy](https://arxiv.org/abs/2310.01334) (October 2023)
- [MOLE: Mixture of LoRA Experts](https://openreview.net/forum?id=uWvKBCYh4S) (January 2024)
- [Statistical Perspective of Top-k Sparse Softmax Gating Mixture of Experts](https://arxiv.org/abs/2309.13850) (September 2023)
- [Sparse Model Soups: A Recipe for Improved Pruning via Model Averaging](https://arxiv.org/abs/2306.16788) (June 2023)
- [Fusing Models With Complementary Expertise](https://arxiv.org/abs/2310.01542) (October 2023)
- [Divide and Not Forget: Ensemble of Selectively Trained Experts in Continual Learning](https://arxiv.org/abs/2401.10191) (January 2024)
- [Branch-Train-MiX: Mixing Expert LLMs into a Mixture-of-Experts LLM](https://arxiv.org/abs/2403.07816) (March 2024)
- [Dense Training, Sparse Inference: Rethinking Training of Mixture-of-Experts Language Models](https://arxiv.org/abs/2404.05567) (April 2024)

## Multimodal MoE
- [Multimodal Constractive Learning with LIMoE: the Language-Image Mixture of Experts](https://arxiv.org/abs/2206.02770) (June 2022)
- [MoE-Llava: Mixture of Experts for Large Vision-Language Models](https://arxiv.org/abs/2401.15947) + [Visual Instruction Tuning](https://arxiv.org/abs/2304.08485) (January 2024, April 2023)
- [Llava-Phi: Efficient Multi-Modal Assistant with Small Language Model](https://arxiv.org/abs/2401.02330) (January 2024)
