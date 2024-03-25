This folder contains example source files from a Clinical Trial Project during Pattern Recognition and Data Mining I at Northern Illinois University. The project report and presentation can be found in the .pdf files.
<p><b>Included Files:</b></p>
<p><b>Correlation_Processing.ipynb</b> contains the code for finding the correlation coefficients of each numerical attribute of the clinical trial dataset.</p>
<p><b>Project Preproessing.ipynb</b> contains the initial preprocessing steps:<br>
  <ol>
    <li>Data Exploration</li>
    <li>Creation of the clinical trial "Numeric Phase" attribute.</li>
    <li>Computing a description of the data.</li>
    <li>Plotting a histogram and a boxplot of the Altmetric Attention Score</li>
    <li>Creating the "Altmetric Title Length" attribute as the length of each clincial trial title.</li>
    <li>Creating the "Total Mentions" attribute from the totla number of media mentions for each clinical trial.</li>
    <li>Saving the resulting .csv file.</li>
    <li> Joining the dataset with the Dimensions dataset from Altmentric.com</li>
    <li>Additional attribute creation based on the cancer types of each study.</li>
  </ol>
</p>
<p><b>RunModels_Numeric.ipynb</b> contains code for model creation using the attributes that were found to correlate best with the Altmetric Attention Score. In each case, the training accuracy, test accuracy
  confusion matrix, precision, recal, f1-score, support, spcificity, ROC curve, and PR curve were found.<br>
  The following classifiers were used:
  <ul>
    <li>Decision Tree</li>
    <li>Support Vector Machine</li>
    <li>Logistic Regression</li>
    <li>Naive Bayes Classifier</li>
  </ul><br>
  The following ensemble methods were used with cross validation set to 10:
  <ul>
    <li>Bagging with</li>
    <ul>
      <li>Decision Tree</li>
      <li>SVM</li>
      <li>Logistic Regression</li>
    </ul>
    <li>Random Forest</li>
      <ul>
        <li>Grid Search CV</li>
        <li>Random Search CV</li>
      </ul>
    <li>Boosting with</li>
      <ul>
          <li>Decision Tree with Adaboost</li>
          <li>XGBoost using DMatrix</li>
          <li>XGBoost using the sklearn API type</li>
          <li>XGBoost using the sklearn type API and GridSearchCV</li>
          <li>XGBoost using the sklearn type API and RandomizedSearchCV</li>
      </ul>
        
  </ul>
  <br>
</p>
<p><b>make_figures.ipynb</b> contains code to produce plots comparing the performances of the different numerical feature based models.</p>


