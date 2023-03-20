# Capstone


### Combatting Infant Mortality With Gradient Boosted Machines

**Alexander Mason**

#### Executive summary

Infant mortality is a tragic and pervasive issue within the united states. It disproportionally affects minority groups and those with less access to healthcare. Furthermore, the infant mortality rate of the united states when compared to similarly develpoed nations is unconsionably high. If we are to make some profoundly naive assumptions about the cause of the united states' unreasonably high infant mortality rate we could come to the conclusion that the infant mortality rate could be lowered if there existed a tool to more effeciently allocate medical resources to high risk infants. In this repo we construct a predictive model to classify infants as likely to die or survive, based on demographic and medical data available on the birth certificate.


#### Rationale


As previously stated, the United States of America has an unfortunately high infant mortality rate compared to other similarly developed counties, especially smaller countries like Estonia or Iceland. However, even when compared with countries such as Australia or Canada the USA is consistently behind the curve. This tragic aspect of American demography is what this repo is focused on. We will examine the numerous risk factors associated with infant death from two concatenated data sets for the years 2014 to 2015. The raw data is available at https://www.nber.org/research/data/linked-birthinfant-death-cohort-data but a subset of said data has been cleaned and included in this repo as a parquet file. The aforementioned data sets are the 2014 and 2015 cohort-linked birth/infant death data sets which contain birth records in the united states for 2014-2015 linked to infant death data if an infant born in said years were to die before its first birthday. The birth data recorded in these two files is that of the  U.S. Standard Certificate of Live Birth and includes a significant amount of demographic and medical information able to inform a predictive model. Any tool or strategy to combat infant mortality would be a force for good. With a model able to accurately predict infant mortality, medical resources could be allocated to infants classified as likely to perish before their first birthday. 
 
#### Research Question

Is it possible to create a model able to predict infant mortality based on data primarily available on the birth certificate? How precisely can an infant’s survival be predicted using only data that would be available up until and moments after birth? What trends can be identified as predictors of infant mortality and how important are demographic characteristics as opposed to purely medical characteristics?

#### Data Sources

The Data used for this project is available through the CDC’s National Vital Statistics System. I used the linked birth and infant death data sets from 2014 and 2015. 

“The linked birth and infant death data set is a valuable tool for monitoring and exploring the complex inter-relationships between infant death and risk factors present at birth. In the linked birth and infant death data set the information from the death certificate is linked to the information from the birth certificate for each infant under 1 year of age who dies in the United States, Puerto Rico, The Virgin Islands, and Guam. The purpose of the linkage is to use the many additional variables available from the birth certificate to conduct more detailed analyses of infant mortality patterns. The linked files include information from the birth certificate such as age, race, and Hispanic origin of the parents, birth weight, period of gestation, plurality, prenatal care usage, maternal education, live birth order, marital status, and maternal smoking, linked to information from the death certificate such as age at death and underlying and multiple cause of death.”
The data sets are available at: https://www.nber.org/research/data/linked-birthinfant-death-cohort-data


#### Methodology
What methods are you using to answer the question?

Data sets from 2014 and 2015 were combined in order to ensure there would be enough mortality data to properly train a model. These datasets were able to be subjected to the same data-cleaning processes as they shared a majority of feature names and encoding formats. The data cleaning process was not particularly advanced, although somewhat tedious. Care was taken to insert the actual categorical values for features with demographic significance. 
 The convention for denoting missing or unknown data in the linked-birth-infant-death cohort data is to enter a 9, 99, 999, or some other numerical value comprised of nines. This is unfortunate for numerical features as one has to identify the specific arbitrary numerical combination of nines for each feature and replace it with a more appropriate value, and because this is data available through the US Government there are often inconsistencies with what is stated in public-use documentation of the data set and what is actually present. Regardless, the cleaned data set is available in this repo as a parquet file. 
The aforementioned cleaned data set consists of 7.9 million births with just under fifty thousand infant deaths. 

Once a cleaned and useable dataset was obtained it was then split into training and test sets and to the training set was applied random under-sampling to ensure a balanced training set. Extensive exploratory data analysis (on just the 2015 cohort) demonstrated that the best results for classification on this kind of data would be obtained by using some form of gradient boosting classifier. Ultimately XGBoost, LightGBM, and the native GradientBoostingClassifier from sklearn’s ensemble module were chosen. 
Before the three selected classifiers were trained and their hyperparameters tuned, a helper module was written to aid in the process. This helper module contains a few functions and one “wrapper” class. The functions are used primarily to automate the process of plotting confusion matrices and displaying the basic classifier metrics, recall, precision, accuracy, etc. 
The wrapper class was mainly written to offer an easy method of creating pipelines that include a classifier, a standard scaler for numerical features, and a one-hot encoder for categorical features. The wrapper class makes the training of classifiers much easier and at the very least serves as a container for a basic column encoding pipeline if used without a specific classifier. Finally, with all of the aforementioned data infrastructure in place, we are ready to begin training and hyperparameter tuning on the three chosen classifiers. 


 

#### Results

Hyperparameter tuning was accomplished through the use of cross-validation and the novel hyperparameter-tuning library, optuna. Initially, models were trained with the standard accuracy metric for cross-validation. Each type of classifier was able to easily reach over 90% accuracy on the unbalanced test set. However, the utility of this is questionable at best as the data is so imbalanced that a model that classified every infant as likely to survive would have an accuracy score of approx 99.4%. It quickly becomes apparent that using accuracy as a metric for these classifiers is counterproductive to the ultimate goal of producing a useful and/or usable tool for combatting infant mortality. 
A useful model would be able to consistently identify infants likely to die without intervention so that resources can be allocated to save their lives. Classifying all infants as likely to survive would incur the highest possible number of false positives, which in this case is the most costly type of error. To combat false positives each of the selected models had hyperparameters tuned using the false-positive rate as a cost function and the best combination of hyperparameters was chosen to minimize said metric. 

Of the three chosen classifiers LightGBM performed the best, albeit by a small margin. Of infants deaths the models were able to accurately classify just over eighty percent of the data while for infants that survived the models accuractely classified over nintey percent of the data.  










#### Outline of project

- [Demonstration and Discussion of Preliminary Methods](https://github.com/alexanderomason/Capstone/blob/main/Capstone.ipynb)
- [More Rigorus Hyperparameter Tuning](https://github.com/alexanderomason/Capstone/blob/main/capstone_hyperparams.ipynb)
- [Visualizations and Brief Discussion of Demography](https://github.com/alexanderomason/Capstone/blob/main/Visualizations.ipynb)


##### Contact and Further Information

