# Retrieval evaluation

Actual execution; synthetic / controlled perturbation evaluation. Not student career outcome accuracy.

   metric  self_top1  self_top3  self_top10  perturb_top1  perturb_top3  perturb_top10
euclidean        1.0        1.0         1.0      0.987912      1.000000            1.0
manhattan        1.0        1.0         1.0      0.981319      1.000000            1.0
   cosine        1.0        1.0         1.0      0.982418      0.997802            1.0

Seed 2026, independent Gaussian noise sigma 0.05 per normalized dimension, clipped to [0,1]. All 910 occupations remain in the reference index. Top-K counts retrieval of the originating occupation code. Self-retrieval is a sanity check. Tied profiles can obscure identity. Continuous noise does not emulate discrete student ratings. No student ground truth, holdout classification accuracy or career success prediction is claimed.

Euclidean is used by specification because it preserves absolute level differences. The alternative metrics are diagnostics, not a claim of superiority. Normalization uses Level / 7 based on the documented O*NET scale, replacing the old observed-maximum /6 calibration. Prior evaluation numbers therefore do not describe this model.
