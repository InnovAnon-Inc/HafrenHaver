# HafrenHaver
Arcane Audio-Visual Computations
==========
[![CircleCI](https://img.shields.io/circleci/build/github/InnovAnon-Inc/HafrenHaver?color=%23FF1100&logo=InnovAnon%2C%20Inc.&logoColor=%23FF1133&style=plastic)](https://circleci.com/gh/InnovAnon-Inc/HafrenHaver)
[![Repo Size](https://img.shields.io/github/repo-size/InnovAnon-Inc/HafrenHaver?color=%23FF1100&logo=InnovAnon%2C%20Inc.&logoColor=%23FF1133&style=plastic)](https://github.com/InnovAnon-Inc/HafrenHaver)
![Lines of code](https://img.shields.io/tokei/lines/github/InnovAnon-Inc/HafrenHaver?color=FF1100&logo=InnovAnon-Inc&logoColor=FF1133&style=plastic)
![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/InnovAnon-Inc/HafrenHaver?color=FF1100&logo=InnovAnon-Inc&logoColor=FF1133&style=plastic)

[![Latest Release](https://img.shields.io/github/commits-since/InnovAnon-Inc/HafrenHaver/latest?color=%23FF1100&include_prereleases&logo=InnovAnon%2C%20Inc.&logoColor=%23FF1133&style=plastic)](https://github.com/InnovAnon-Inc/HafrenHaver/releases/latest)
![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/InnovAnon-Inc/HafrenHaver?color=FF1100&logoColor=FF1133&style=plastic)
[![License Summary](https://img.shields.io/github/license/InnovAnon-Inc/HafrenHaver?color=%23FF1100&label=Free%20Code%20for%20a%20Free%20World%21&logo=InnovAnon%2C%20Inc.&logoColor=%23FF1133&style=plastic)](https://tldrlegal.com/license/unlicense#summary)

![PyPI - Implementation](https://img.shields.io/pypi/implementation/HafrenHaver?color=FF1100&logo=InnovAnon-Inc&logoColor=FF1133&style=plastic)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/HafrenHaver?color=FF1100&logo=InnovAnon-Inc&logoColor=FF1133&style=plastic)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/HafrenHaver?color=FF1100&logo=InnovAnon-Inc&logoColor=FF1133&style=plastic)
![PyPI - Downloads](https://img.shields.io/pypi/dd/HafrenHaver?color=FF1100&logo=InnovAnon-Inc&logoColor=FF1133&style=plastic)
![PyPI - Format](https://img.shields.io/pypi/format/HafrenHaver?color=FF1100&logo=InnovAnon-Inc&logoColor=FF1133&style=plastic)
![PyPI - Status](https://img.shields.io/pypi/status/HafrenHaver?color=FF1100&logo=InnovAnon-Inc&logoColor=FF1133&style=plastic)
![PyPI - License](https://img.shields.io/pypi/l/HafrenHaver?color=FF1100&logo=InnovAnon-Inc&logoColor=FF1133&style=plastic)
![PyPI](https://img.shields.io/pypi/v/HafrenHaver?color=FF1100&logo=InnovAnon-Inc&logoColor=FF1133&style=plastic)

(Work in progress...)

Proof of concept for InnovAnon's Human Programming Technology;
a tool for accelerating alchemical works.

The core functionality will be a myriad apps for modeling, viewing and
controlling complex (and often cyclical) data.
Transposing a harmonic structure (i.e., song) should be as simple as
turning a dial.
There should also be ways for comparing harmonic structures,
such as the differences between scales and chords
under different tuning systems.

The goal is to provide high level descriptions of music, graphical layouts,
lyrics, etc., and to generate sounds and visuals satisfying the constraints.
And to use known spiritual technologies to enhancs or replace rigorous
sadhanas with a form of worship better suited to the Western lifestyle:
relatively instant results, presented in a gamified fashion so its fun.
Bald eagles and cheeseburgers!

Currently, the implementation of song meter involves a combination
of cadences (binary sequences specifying whether one thing is the same
as or different than another) and hash functions (to implement repetition
of motifs... i.e., a section cadence may specify that first and second
phrases differ from each other, but rather than generating a unique
phrase cadence for the second one, it might reuse a phrase cadence 
from elsewhere in the piece).

# SevernSieve (TODO needs to be rewritten. expensive ops don't have to be done so often)
P.o.C. for variable-length wheel factorization
==========
An implementation of variable-length wheel factorization
(a compression technique for the sieve of eratosthenes)
that theoretically has a slightly lower upper bound to its
asymptotic complexity.

There's one problem of efficiency to be resolved in the implementation.
Hashing could be used as a work-around until a formula is derived.

# HAL
Primitive Precursor of the YellShell
==========
Uses speech recognition to convert voice commands to text,
which are preprocessed (i.e., stopwords are removed,
NATO phonetics are converted, etc.),
then interpreted as an English-like domain-specific language,
converting the commands to Event objects the underlying GUI
can recognize and forward to the contained App(s).

# CircleApp, SquareApp, AngleApp, PentaApp, HexaApp (TODO semi-complete)
App Geometries based on 2D Projections of Platonic Solids
==========
Animations can rotate the underlying 3D shape implied by these app
geometries, implying that what we perceive is the shadow of the true
nature of things.

# RecursiveComposite
Automatic Fractalizer to Fill Negative Space caused by Null Child Nodes
==========
Implies the fractal nature of existence.

# Magic/Matrix
Display Arbitrary Code using Patterns based on (Relatively) Prime Numbers
==========
Implies the mathematical nature of existence.

Code is preprocessed for display. Comments and imports are removed.
TODO shorten/rename variables

Currently available in Circular Ring pattern and in filled square pattern.
TODO filled circle and rectangular frame.
TODO figure out something with triangles, etc.

# AestheticLayout (TODO)
Layout Manager for Non-Standard Geometries
==========
The specialized layout manager will manage app geometries,
positive and negative space, etc., as well as framing sets of apps.
These "frames" will be decorated with designs such as the recursive
composite and the matrix text.

# GPS App (TODO temp, pressure, alt display and underlying middleware)
Graphical Representation of an Astronomical Observer
==========
Allows user to select map projection,
centering the projection at the user's coordinates.

Uses an exotic-style display for temperature, pressure and altitude.

# Classical Clock App
Graphical Representation of the Classical Time given an Astronomical Observer
==========
It's gonna be steam punk, yo.

# Solfeggio App (TODO)
Graphical Selector for Base Frequency
==========
Two Styles:
- Using traditional solfeggio frequencies, and the option of standard or classical hertz
- Empirical tuning, initial guess based on temperature and pressure

# ColorManager (TODO)
Manages Color Palettes and Color Schemes for Apps
==========
Color palettes as a function of base frequency, scale, and brainwave:
the formula for synesthesia.

The above subprojects are the requirements for the pre-alpha release: Tuning the Yellow Bell
The alpha release will actually have sound.

# OnePunch (TODO)
Paginated Rate-Limit-Aware Memoizing Cache for REST APIs
==========
Keeps track of API and artist credits.

With logic for recycling cached results and fetching new results.

Maybe with load balancing.

# Usage Notes
Common Operations
==========
- (Un)Install (TODO):
      ```python3 -m pip {|un}install --upgrade .```
- Install API Keys:
      ```grep -qF '*.key' .gitignore &&
      echo -n '<API KEY>' >| <funcname>.key```
- Run Unit Tests (TODO):
      ```for k in *.py ; do PATH=.:$PATH $k || break ; done```
- Blast the Caches:
      ```rm *.cache```

# TODO
----------
- binaural beats
- isochronic pulses (including graphics)
- monaural beats
- other effects... like phasing
- poetic meter
- subliminal programming
- ndimensional and possibly true non-euclidean topologies

# Underlying Concepts
----------
- graphics based on sacred geometry
- automatic management of aesthetics:
  - color schemes
  - layouts
  - balancing circular vs angular geometries
  - animation speeds and types
- management of tick speeds, including sample rate and frame rate
- exploring in a reasonable way
  the vast harmonic space made possible by the combination of:
  - just intonation
  - exotic modes
- synchronization of:
  - implied isochronic pulse caused by polyrhythms
  - acoustic beat (i.e., monaural beat) caused by polytonic harmonies
  - color palette (colors selected as a function of base frequency and scale)
  - tempo
- fractals
- tuning the yellow bell: how to select solfeggio frequencies
  (i.e., base frequencies), scales and modes.
- computing from the ground up with a good college try given to abandoning
  musical tradition while maintaining an awareness of it...
  in other words, traditional structures in Western and Eastern music
  should be reduced to a collection of presets.
  Ultimately, it should break free from the preset scale length of 12
  notes, instead deriving scale lengths using the harmonic variation of
  Euclid's algorithm.

# Project Name
----------
HafrenHaver (verb):

To go on and on about a legendary British princess who was drowned
in the River Severn by her repudiated stepmother Gwendolen.

SevernSieve (noun):

A device for separating wanted elements from unwanted material
in the River Severn.

# Purpose
----------
To what end are we engineering literal mind control technology?

The state of the art in brainwave entrainment technology is really
quite amazing, making attaining advanced states of consciousness
that previously took decades (or lifetimes according to some dogmas)
possible within a few months of consistent practice.

The implications of this is that the neigh-mythical state of turiya is
easily accessible to even "armchair" mystics. However, the
implementations of these technologies are lagging behind the current
research. Listening to isochronic pulses can be nerve-wracking and
downright repetitive, even when masked with pink noise such as nature
sounds and buzzword musical textures, such as singing bowls, which is
known to reduce the effectiveness of the isochronic technologies.

Thus, the state of the art is to either shine a proverbial laser into
your ear-balls or to reduce the effectiveness of the technology.
Furthermore, isochronic technology is known to be effective over both
audible and visual wavelengths, but few known implementations implement
the latter, much less both.

This framework will make it quick and easy to stand up apps that have
these technologies embedded in them at a fundamental level.
While our focus is on generating tolerable pink noise
and creating an interface for controlling the
necessary models, the middleware will be able to manage layouts,
colorschemes, audio, etc., for any sort of app, including games:
imagine, for example, a tetris implementation that can induce
trancelike states, enhancing the effectiveness of positive affirmations
to enhance your gaming experience. Play games, get turiya for free.

That layer will enable a useful subproject:
gamifying the learning process,
as well as generating mnemonic songs
given plain natural language statements,
and facilitating the synchronization
of the classroom in reciting these songs.
For anyone who has taken classical Latin,
this process technique should be familiar.

In a nutshell:
- target a cymatic base frequency, such as salinated water
- use prime number math (plus a layer for keys, tetrachords, scales, modes and chords)
  for all tempos, acoustic beats (caused by harmonies) and even color schemes
- induce a particular brainwave frequency via the combination of
  monaural beats, visual and audible isochronic pulses

So... what's the result like? Imagine that you spend all day working
on some great project, you inevitably get tired and go to sleep,
but when you enter your dream cycle, you remember that break time is over,
sit down at your terminal, and continue coding in the dream world,
switching to your desk with a paper and pencil
if the terminal is getting too dreamlike, then,
when you wake up refreshed, and continue coding in the waking world,
the code is easier and quicker to write, because you've already
written it before.

That is what is possible in a Level 1 Dream State on a night when your
turiya is strong enough.
Though being the world's most productive office worker is not the point.
That's just the beginning of what can be achieved:
that's only a Level 1 Dream State.
These technologies will help make the other dream levels accessible
as well, if used while sleeping.

After attaining a Level 4 Dream State, the next strange state of
consciousness is Level 4 Ascension, when you begin to dream in four
dimensions.

Admittedly, the advanced topologies will require exotic physics engines,
including multidimensional raycasting at a minimum,
as well as curious computations related to audio engineering.
That is a TODO for far in the future,
but that will make Level 4 Ascension accessible to the masses,
at least the ones who have stereophonic input to their listening
devices--headphones for their ears.

That layer will enable a fun subproject, a massive undertaking in its
own right: a sandbox to merge game genres into a single universe,
allowing for focus from FPS-scale gameplay to simtower-, simcity-,
civ-level and beyond.
There will be a focus on randomized content generation;
AIs will be trained within this sandbox,
in an effort to generate more realistic, randomized buildings
and city structures:
Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn.

Once completed, this project should contribute to our effort to achieve
a critical mass of individuals who have achieved turiya and 
Level 4 Ascension, which should, in theory, make these abilities
the default for human consciousness.

Bigger picture: what next after we make the three dimensional world
obselete for the collective unconscious?
Well, we build drones to replace our niche in the ecosystem,
making ourselves obselete to this world,
and turn our attention toward getting the Hell off this rock.

# Credits
----------
The lionshare of the credit goes to that inner monologue
that gives voice to subtle and vague impressions from the
subconscious mind-brain (yeah... "mind-brain") or perhaps a
supernatural entity that nobody has actually seen.
Thanks InnovAnon!

S. Faust for his exploration of turiya and its possibilities
and for his mentorship.

TruthStream: their entertaining spin on these technologies
has been downright inspirational during this undertaking.

Other credits are specifically linked in the source,
such as StackOverflow threads where the good people ensured
forward progress, even on days when I watched several sunrises.

# Dedication
----------
Honorable mention to known Western code monks,
who may not have contributed anything to this particular project,
but rather to the Western cyber-monastic tradition in general:
- Terry A. Davis
- Sasha Gallagher

# License
----------
If we wrote it, then you own it:
we write technology that no one should have,
and release it to the public domain...
one sinister line at a time.

Other code, obviously, retains the original licenses.

# Innovations Anonymous
Free Code for a Free World!
==========
![Corporate Logo](https://i.imgur.com/UD8y4Is.gif)
