# Sexual_Assualt_Project
The project contains 3 parts: UI, integration with whatsapp and nlp.
In the nlp part there are 4 parts:
1. **data** - contains 2 dirctories:
   
   1.1. **inputs** - contains 2 direcories one for hebrew data and one for english. There are several types of files that used for the nlp models. There are file with or without classification, files with dummy data, 
       files with cancated data by type of classification. In another, there are files that are outpup of sentiment predictions models that used for classification predictions.
   
   1.2. **results** - contains 2 direcories one for hebrew data and one for english. Every directory contains different results for different models.
   
2. **models** - ontain the saved models that trained in google colab. contain 3 parts - models for classification with all the sentiments, models for classification with all the sentiments that predicted by another model, models for predict the sentiments. All of them splited to models english or hebrew based on their trained data. Some of them we used the the project eventually. 

3. **notebooks** - contains all the notebooks of the saved models.

4. **scripts** - contains all the backend logic of the nlp part of the project.
