from sklearn import cross_validation
from readfacedatabases import *
import copy

# TODO: move to common?
def splitTrainTest(data1, data2, labels1, labels2, ratio):
  assert len(data1) == len(data2)
  assert len(labels1) == len(labels2)
  assert len(labels1) == len(data1)
  assert len(labels1) == len(labels2)

  data1, data2, labels1, labels2 = shuffle(data1, data2, labels1, labels2)

  # Random data for training and testing
  kf = cross_validation.KFold(n=len(data1), n_folds=ratio)
  for train, test in kf:
    break

  return (data1[train], data1[test], data2[train], data2[test],
          labels1[train], labels1[test], labels2[train], labels2[test])

def splitShuffling(shuffling, labelsShuffling):

  shuffling, labelsShuffling = shuffle(shuffling, labelsShuffling)

  labels = np.unique(labelsShuffling)

  # TODO: we already had this? maybe not remake it
  labelsToData = {}
  for label in labels:
    labelsToData[label] = list(shuffling[labels == label])

  shuffledData1 = []
  shuffledData2 = []
  labelsData1 = []
  labelsData2 = []

  # currentLabels = list(labelsShuffling)

  while len(labelsShuffling) >= 2:
    chosenLabels = np.random.choice(labels, 2)
    label1 = chosenLabels[0]
    label2 = chosenLabels[1]

    if label1 == label2:
      continue

    dataLabel1 = labelsToData[label1]
    dataLabel2 = labelsToData[label2]
    if len(dataLabel1) == 0 or len(dataLabel2) == 0:
      continue

    # data1LabelIndex = np.random.choice(len(labelsToData[label1]))
    # data2LabelIndex = np.random.choice(len(labelsToData[label2]))
    shuffledData1 += [dataLabel1[0]]
    shuffledData2 += [dataLabel2[0]]
    labelsData1 += [label1]
    labelsData2 += [label2]

    labelsShuffling.remove(label1)
    labelsShuffling.remove(label2)

    del labelsToData[label1][0]
    del labelsToData[label2][0]


  shuffledData1 = np.vstack(shuffledData1)
  shuffledData2 = np.vstack(shuffledData2)

  labelsData1 = np.hstack(labelsData1)
  labelsData2 = np.hstack(labelsData2)

  # remaing = list(shuffling)
  # remaininLabels = list(labelsShuffling)

  # print "shuffling size"
  # print len(shuffling)

  # shuffledData1 = []
  # shuffledData2 = []
  # labelsData1 = []
  # labelsData2 = []

  # for label in labels:
  #   print "label"
  #   print label

  #   nrRemainingData = len(remaing)

  #   if nrRemainingData == 0:
  #     break

  #   labelIndices = np.array(remaininLabels) == label
  #   concreteIndices = np.arange(nrRemainingData)[labelIndices]

  #   # If nothing of this label is left, just continue
  #   if len(concreteIndices) == 0:
  #     continue

  #   otherIndices = np.arange(nrRemainingData)[np.invert(labelIndices)]

  #   if len(otherIndices) == 0:
  #     continue

  #   indicesToTake = min(len(concreteIndices), len(otherIndices))

  #   otherIndices = np.random.choice(otherIndices, indicesToTake, replace=False)


  #   # concreteData = np.array(remaing)[concreteIndices]

  #   shuffledData1 += [np.array(remaing)[concreteIndices]]
  #   labelsData1 += [np.array(remaininLabels)[concreteIndices]]

  #   shuffledData2 += [np.array(remaing)[otherIndices]]
  #   labelsData2 += [np.array(remaininLabels)[otherIndices]]

  #   indicesToRemove = np.hstack((otherIndices, concreteIndices))
  #   remaing = [v for i, v in enumerate(remaing) if i not in indicesToRemove]
  #   remaininLabels = [v for i, v in enumerate(remaininLabels) if i not in indicesToRemove]

  #   assert len(remaing) == len(remaininLabels)

  # shuffledData1 = np.vstack(shuffledData1)
  # shuffledData2 = np.vstack(shuffledData2)

  # labelsData1 = np.hstack(labelsData1)
  # labelsData2 = np.hstack(labelsData2)

  # print shuffledData1.shape
  # print shuffledData2.shape

  # assert len(shuffledData1) == len(shuffledData2)
  # assert len(labelsData1) == len(labelsData2)

  # assert len(shuffledData1) <= len(shuffling) / 2

  """  STOP NEW METHOD """
  # shuffledData1 = shuffling[0: len(shuffling) / 2]
  # shuffledData2 = shuffling[len(shuffling)/2 :]

  # labelsData1 = labelsShuffling[0: len(shuffling) /2]
  # labelsData2 = labelsShuffling[len(shuffling)/2:]

  # shuffledData1 = np.array(shuffledData1)
  # shuffledData1 = np.array(shuffledData2)
  # labelsData1 = np.array(labelsData1)
  # labelsData2 = np.array(labelsData2)

  return shuffledData1, shuffledData2, labelsData1, labelsData2

# TODO: I think this can be written easier with the code similar to the Emotions one
# you can create more tuples than just one per image
# you can put each image in 5 tuples and that will probably owrk better
# it might be useful to also give the same image twice
def splitDataMultiPIESubject(imgsPerLabel=None):
  subjectsToImgs = readMultiPIESubjects()

  data1, data2, subjects1, subjects2, shuffling, subjectsShuffling = splitDataInPairsWithLabels(subjectsToImgs, imgsPerLabel, None)

  trainData1, testData1, trainData2, testData2, trainSubjects1, testSubjects1,\
        trainSubjects2, testSubjects2 = splitTrainTest(data1, data2, subjects1, subjects2, 5)

  print "trainData1.shape"
  print trainData1.shape

  shuffledData1, shuffledData2, subjectsData1, subjectsData2 = splitShuffling(shuffling, subjectsShuffling)

  print len(shuffledData1)
  print len(shuffledData2)

  trainShuffedData1, testShuffedData1, trainShuffedData2, testShuffedData2,\
    trainShuffledSubjects1, testShuffledSubjects1, trainShuffledSubjects2, testShuffledSubjects2 =\
        splitTrainTest(shuffledData1, shuffledData2,
                      subjectsData1, subjectsData2, 5)

  trainData1 = np.vstack((trainData1, trainShuffedData1))

  print "trainData1.shape"
  print trainData1.shape

  trainData2 = np.vstack((trainData2, trainShuffedData2))

  testData1 = np.vstack((testData1, testShuffedData1))
  testData2 = np.vstack((testData2, testShuffedData2))

  trainSubjects1 = np.hstack((trainSubjects1, trainShuffledSubjects1))
  testSubjects1 = np.hstack((testSubjects1, testShuffledSubjects1))

  trainSubjects2 = np.hstack((trainSubjects2, trainShuffledSubjects2))
  testSubjects2 = np.hstack((testSubjects2, testShuffledSubjects2))

  assert len(subjects1) == len(subjects2)
  assert len(trainSubjects1) == len(trainSubjects1)
  assert len(testSubjects1) == len(testSubjects2)

  similaritiesTrain = similarityDifferentLabels(trainSubjects1, trainSubjects2)
  similaritiesTest = similarityDifferentLabels(testSubjects1, testSubjects2)

  print "trainSubjects1.shape"
  print trainSubjects1.shape

  print "similaritiesTrain.shape"
  print similaritiesTrain.shape
  # print similaritiesTrain

  assert len(trainData1) == len(trainData2)
  assert len(testData1) == len(testData2)

  trainData1, trainData2, similaritiesTrain = shuffle3(trainData1, trainData2, similaritiesTrain)
  testData1, testData2, similaritiesTest = shuffle3(testData1, testData2, similaritiesTest)

  return trainData1, trainData2, testData1, testData2, similaritiesTrain, similaritiesTest


def splitDataInPairsWithLabels(labelsToImages, imgsPerLabel, labelsToTake=None):
  data1 = []
  data2 = []

  shuffling = []
  labelsShuffling = []
  labels1 = []
  labels2 = []

  for label, images in labelsToImages.iteritems():
    if labelsToTake is not None and label not in labelsToTake:
      print "skipping subject"
      continue

    # The database might contain the labels in similar
    # poses, and illumination conditions, so shuffle before
    np.random.shuffle(images)

    if imgsPerLabel is not None:
      images = images[:imgsPerLabel]

    delta = len(images) / 4 + label % 2
    last2Index = 2 * delta
    data1 += images[0: delta]
    data2 += images[delta: last2Index]

    labels1 += [label] * delta
    labels2 += [label] * delta

    imagesForShuffling = images[last2Index : ]
    shuffling += imagesForShuffling
    labelsShuffling += [label] * len(imagesForShuffling)

  print "len(labelsShuffling)"
  print len(labelsShuffling)

  print "shuffling"
  print len(shuffling)

  assert len(shuffling) == len(labelsShuffling)
  shuffling, labelsShuffling = shuffleList(shuffling, labelsShuffling)

  print len(data1)
  print len(data2)
  assert len(data1) == len(data2)

  data1 = np.array(data1)
  data2 = np.array(data2)
  labels1 = np.array(labels1)
  labels2 = np.array(labels2)
  shuffling = np.array(shuffling)
  labelsShuffling = np.array(labelsShuffling)

  return data1, data2, labels1, labels2, shuffling, labelsShuffling

def splitDataAccordingToLabels(labelsToImages, labelsToTake, imgsPerLabel=None):
  data1, data2, labels1, labels2, shuffling, labelsShuffling  = splitDataInPairsWithLabels(labelsToImages, imgsPerLabel, labelsToTake=labelsToTake)

  shuffledData1, shuffledData2, labelsData1, labelsData2 = splitShuffling(shuffling, labelsShuffling)

  data1 = np.vstack((data1, shuffledData1))
  data2 = np.vstack((data2, shuffledData2))

  labels1 = np.hstack((labels1, labelsData1))
  labels2 = np.hstack((labels2, labelsData2))

  return data1, data2, labels1, labels2

def similarityDifferentLabels(labels1, labels2):
  assert len(labels1) == len(labels2)
  return labels1 == labels2

def splitSimilarityYale():
  subjectsToImgs = readCroppedYaleSubjects()

  # Get all subjects
  data1, data2, subjects1, subjects2 = splitDataAccordingToLabels(subjectsToImgs,
                                          None, imgsPerLabel=None)

  return data1, data2, similarityDifferentLabels(subjects1, subjects2)

def splitSimilaritiesPIEEmotions():
  emotionToImages = readMultiPIEEmotions()
  # Get all emotions
  data1, data2, emotions1, emotions2 = splitDataAccordingToLabels(emotionToImages,
                                          None, imgsPerLabel=None)
  labels = similarityDifferentLabels(emotions1, emotions2)

  data1, data2, labels = shuffle3(data1, data2, labels)

  kf = cross_validation.KFold(n=len(data1), n_folds=5)
  for train, test in kf:
    break

  return (data1[train], data2[train], labels[train],
          data1[test], data2[test], labels[test])

def splitEmotionsMultiPieKeepSubjects():
  subjectToEmotions = readMultiPIEEmotionsPerSubject()

  totalData1 = []
  totalData2 = []
  totalLabels1 = []
  totalLabels2 = []
  for subject, emotionToImages in subjectToEmotions.iteritems():
    data1, data2, labels1, labels2 = splitDataAccordingToLabels(emotionToImages, None, None)
    totalData1 += [data1]
    totalData2 += [data2]
    totalLabels1 += [labels1]
    totalLabels2 += [labels2]

  totalData1 = np.vstack(totalData1)
  totalData1 = np.vstack(totalData2)
  totalLabels1 = np.hstack(totalLabels1)
  totalLabels2 = np.hstack(totalLabels2)
  return totalData1, totalData2, totalLabels1, totalLabels2

def splitEmotionsMultiPieKeepSubjectsTestTrain():
  kf = cross_validation.KFold(n=len(totalData1), n_folds=5)
  for train, test in kf:
    break

  labels = similarityDifferentLabels(totalLabels1, totalLabels2)

  return (totalData1[train], totalData2[train], labels[train],
          totalData1[test], totalData2[test], labels[test])


def testShuffling():
  shuffling = [1,2,3, 4]
  labelsShuffling = [1,2,3, 4]
  a, b, c, d  = splitShuffling(shuffling, labelsShuffling)
  assert not c[0] ==  d[0]
  assert not c[1] ==  d[1]
  assert sorted(list(a) + list(b)) == [1,2,3,4]

  shuffling = [1,2,3]
  labelsShuffling = [1,2,3]
  a, b, c, d  = splitShuffling(shuffling, labelsShuffling)
  assert not c[0] ==  d[0]
  assert not a[0] == b[0]

  shuffling = [1,2,4,5]
  labelsShuffling = [1,2,1,2]
  a, b, c, d  = splitShuffling(shuffling, labelsShuffling)
  assert not c[0] ==  d[0]
  assert not c[1] == d[1]

  fst = sorted(list(a[0]))
  snd = sorted(list(b[0]))

  assert fst == [1,4] or fst == [2,5]
  assert snd == [2,5] or snd == [1,4]

  if fst == [1,4]:
    assert c[0] == 1
  else:
    assert c[0] == 2

  shuffling = [ np.array([1,1]), np.array([2,2]), np.array([4,4]), np.array([5,5]),
                np.array([6, 6]), np.array([7, 7]) ]
  labelsShuffling = [1, 2, 3, 2, 1, 3]
  a, b, c, d  = splitShuffling(shuffling, labelsShuffling)
  assert not c[0] ==  d[0]
  assert not c[1] == d[1]
  assert not c[2] == d[2]

  print zip(a, c)
  print zip(b, d)

if __name__ == '__main__':
  # print shuffleList([1,2], [3,4])
  print len(shuffle([1,2], [3,4]))
  testShuffling()
