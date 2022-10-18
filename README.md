# Vantablack: The StepMania simfile linter

## What is vantablack?

***NOTE: Vantablack is currently a work-in-progress (pre-1.0). Both the implementation
and its documentation are still in development. They are both subject to change without
notice and may not be consistent with each other.***

Vantablack is an extendable [linter](https://en.wikipedia.org/wiki/Lint_(software)) for
validating [StepMania](https://www.stepmania.com) songs and song packs. It can be used to
automatically validate songs and song packs against a configurable list of rules.

Examples of rules include:
- Detecting `.old` files generated by the StepMania editor in song folders for removal before chart distribution.
- Detecting songs with missing or incorrectly-sized graphics.
- Enforcing a maximum length for the audio file.

## How do I lint my song pack?

Add a `vantablack.toml` file to your pack root.
For example:
```
Song Pack/
├─ vantablack.toml
├─ banner.png
├─ Song 1/
├─ Song 2/
└─ ...
```

This is a [TOML](http://toml.io) file that describes the set of rules to run against your pack.

Here's an example `vantablack.toml` 

```toml
vantablack.version = 0

[vantablack.rules]
# For every chart in an ssc file, assert that its credit has the value "bkirz".
ssc_chart.require_credit.value = "bkirz"

# Fail if any song is missing a jacket, background, or banner, or if any of those graphics have the wrong dimensions.
song.background.dimensions = { width = 1366, height = 768 }
song.banner.dimensions = { width = 418, height = 164 }
song.jacket.dimensions = { width = 512, height = 512 }

# All files should be directly referenced by a .ssc file.
song.no_extra_files.enabled = true

# Fail if any songs are missing a challenge chart.
song.require_difficulty.difficulty = 'Challenge'
song.require_difficulty.style = 'dance-single'

# Fail if any non-4-panel charts are included
chart.restrict_field.field = 'STEPSTYPE'
chart.restrict_field.value = 'dance-single'

# Fail if any charts have no notes
chart.fail_on_empty.enabled = true
```
