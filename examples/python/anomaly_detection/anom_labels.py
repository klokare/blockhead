# ==============================================================================
# anom_labels.py
# ==============================================================================
from brainblocks.blocks import LabelTransformer, SequenceLearner
from sklearn import preprocessing

values = [
    'a', 'a', 'a', 'a', 'a', 'b', 'c', 'd', 'e', 'f',
    'a', 'a', 'a', 'a', 'a', 'b', 'c', 'd', 'e', 'f',
    'a', 'a', 'a', 'a', 'a', 'b', 'c', 'g', 'e', 'f']

scores = [0.0 for _ in range(len(values))]

# Convert to integer value labels
le = preprocessing.LabelEncoder()
le.fit(values)
labels = le.transform(values)

# Setup blocks
lt = LabelTransformer(
    num_l=26,  # number of labels
    num_s=208) # number of statelets

sl = SequenceLearner(
    num_spc=10,  # number of statelets per column
    num_dps=10,  # number of dendrites per statelet
    num_rpd=12,  # number of receptors per dendrite
    d_thresh=6,  # dendrite threshold
    perm_thr=20, # receptor permanence threshold
    perm_inc=2,  # receptor permanence increment
    perm_dec=1)  # receptor permanence decrement

# Connect blocks
sl.input.add_child(lt.output, 0)

# Loop through the values
for i in range(len(labels)):

    # Set scalar transformer value
    lt.set_value(labels[i])

    # Compute the scalar transformer
    lt.feedforward()

    # Compute the sequence learner
    sl.feedforward(learn=True)

    # Get anomaly score
    scores[i] = sl.get_anomaly_score()

# Print output
print("val, scr")
for i in range(len(values)):
    print("%3s, %0.1f" % (values[i], scores[i]))
