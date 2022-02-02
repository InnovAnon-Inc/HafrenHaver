#! /usr/bin/env python3

from enum      import Enum, unique
from itertools import starmap
from operator  import le
from random    import choice, random, randrange
import numpy

@unique
class Variance(Enum):
    SONG    = 1
    SECTION = 2
    PHRASE  = 3
    MEASURE = 4
    BEAT    = 5

@unique
class VarianceType(Enum):
    HARMONIC   = 1
    MODULATION = 2
    BORROW     = 3
    ACCENT     = 4
    DYNAMICS   = 5
    METER      = 6
    TEMPO      = 7
def random_variances():
    variances = {
        Variance.SONG    : 1.0 * 2**-1,
        Variance.SECTION : 1.0 * 2**-2,
        Variance.PHRASE  : 1.0 * 2**-3,
        Variance.MEASURE : 1.0 * 2**-4,
    }
    def get_choices(): return list(variances.keys())
    def get_weights():
        s = sum(variances.values())
        return [v / s for v in variances.values()]

    harmonic_variance                  = choice(list(Variance))
    if harmonic_variance in variances:
        variances[harmonic_variance]   = variances[harmonic_variance]   / 2

    if harmonic_variance.value > Variance.SONG.value:
        while True:
            modulation_variance        = numpy.random.choice(get_choices(), p=get_weights())
            if modulation_variance.value <= harmonic_variance.value: break
        variances[modulation_variance] = variances[modulation_variance] / 2
    else:   modulation_variance        = None
    if harmonic_variance.value > Variance.SONG.value:
        while True:
            borrow_variance            = numpy.random.choice(get_choices(), p=get_weights())
            if borrow_variance.value     <= harmonic_variance.value: break
        variances[borrow_variance]     = variances[borrow_variance]     / 2
    else:   borrow_variance            = None

    accent_variance                    = numpy.random.choice(get_choices(), p=get_weights())
    variances[accent_variance]         = variances[accent_variance]     / 2
    dynamics_variance                  = numpy.random.choice(get_choices(), p=get_weights())
    variances[dynamics_variance]       = variances[dynamics_variance]   / 2

    meter_variance                     = numpy.random.choice(get_choices(), p=get_weights())
    variances[meter_variance]          = variances[meter_variance]      / 2
    tempo_variance                     = numpy.random.choice(get_choices(), p=get_weights())
    variances[tempo_variance]          = variances[tempo_variance]      / 2

    return {
            VarianceType.HARMONIC   : harmonic_variance,
            VarianceType.MODULATION : modulation_variance,
            VarianceType.BORROW     : borrow_variance,
            VarianceType.ACCENT     : accent_variance,
            VarianceType.DYNAMICS   : dynamics_variance,
            VarianceType.METER      : meter_variance,
            VarianceType.TEMPO      : tempo_variance,
    }

#print("harmonic_variance  : %s" % (harmonic_variance,))
#print("modulation_variance: %s" % (modulation_variance,))
#print("borrow_variance    : %s" % (borrow_variance,))
#print("accent_variance    : %s" % (accent_variance,))
#print("dynamics_variance  : %s" % (dynamics_variance,))
#print("meter_variance     : %s" % (meter_variance,))
#print("tempo_variance     : %s" % (tempo_variance,))





# number of chord changes, number of modulations, number of borrowed chords
# consonance cadence, brightness cadence
# TODO meter, accents, rhythms

# 

# TODO count uniq song sections, decide # different verse structures

# dynamics
# 1: per section
# 2: per phrase
# 3: within phrases

# mode/key changes
# 1: none
# 2: per section
# 3: per phrase
# 4: within phrases

# tempo modulations
# 1-4

# t-s-d harmonic cadence
# 1-4

# secondary/borrowed cadence & chords

# bjorklund accent patterns
# 1-4

# rhythm cadence & rhythms
# whole, half, quarter, eighth, sixteenth, triplets


# ct-nct cadence

# chords
# melody
# countermelodies

