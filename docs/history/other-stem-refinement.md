# Other-stem refinement experiment

This experiment is closed. The [six-stem workflow](../operations/separation.md)
is the current default.

The MVSep Mega 53 Stems specialist models estimated `bowed_strings`, `brass`,
`woodwind`, `synth`, `keys`, and `percussion` independently from the original
mix. The experiment projected those estimates into the existing `other` stem
with time-frequency masks, leaving an additive residual. Main Theme (`01_01`)
passed format and additive reconstruction checks. Audible bleed and instrument
misclassification limited its value as a replacement for the six-stem result.

## Reproduction references

- [Experiment runner](../../src/other_refinement/run_other_refinement.py)
- [Mask projection](../../src/other_refinement/partition_other.py)
- [Format and reconstruction verifier](../../src/other_refinement/verify_other_refinement.py)
- [Model manifest](../../models/experimental/mvsep-mega-53/manifest.json)
- [Experimental dependencies](../../requirements/experimental.txt)

The historical run used MSST, local specialist checkpoints, and NVIDIA CUDA.
It first generated the standard six-stem result for the same source, then ran
`run_other_refinement.py --input-file /path/to/track.flac` from the project
root using the project interpreter. The default output root is the ignored
`outputs/experiments/other-refinement/`. Consult the
[remote execution policy](../governance/remote-execution-policy.md) before
preparing those dependencies, weights, or a new reproduction run.
