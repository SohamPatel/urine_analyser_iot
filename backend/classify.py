# This is a sample program on how to run the classifier
import random_forest_classifier as rfc_module


if __name__ == '__main__':
    # Data is a list of features in the following order:
    # [gravity, ph, bilirubin, urobilinogen, protein, glucose, ketones, hemoglobin, myoglobin, leukocyte_esterase, nitrite, colour]
    # Note that not all features were used, since some would just immediately set the urgency to medium/high,
    # so we could just use an if statement to look at those features instead of using a classifier
    # There's also a gen_training_data(sample_num) function in random_forest_classifier, which generates random data
    # When you want to predict data, load the classifier and chuck the data into predict(). The result will return a list of priorities the classifier predicts

    # Generate 1000 cases of training data
    data, actual_labels = rfc_module.gen_training_data(1000)
    # Load the classifier from files
    rfc = rfc_module.load('rfc')
    # predict data
    pred_labels = rfc.predict(data)
    # You can get the accuracy by calling a function from rfc
    print(f'Accuracy: {rfc_module.get_accuracy(actual_labels, pred_labels)}')
    # Alternatively you can call score() function to return the accuracy directly if you do not the prediction labels returned
    print(f'Accuracy: {rfc.score(data, actual_labels)}')
    # You can also print the confusion matrix to see where the incorrect classifications are happening
    print('Confusion matrx:')
    print('No, Low, Medium, High')
    print(rfc_module.metrics.confusion_matrix(actual_labels, pred_labels, labels=['No', 'Low', 'Medium', 'High']))
    # Accuracy is wildly fluctuating between 65% to 99% due to the way data was generated. Also crucial patient data such as weight, height, age, gender, family history is not included.
    # This is more of way to show that machine learning is useful and can be applied into the project.
    # In fact random forest classifiers are used for hospital diagnosis and urgency classifications!


