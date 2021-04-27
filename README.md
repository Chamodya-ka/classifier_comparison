# classifier_comparison

This repo contains the code used to compare SVM and NN classification methods for key point based Indian Sign Language Recognition system.
- NN_predict_2.py - Python code to run the NN based classifier
- SVM_predict_2.py- Python code to run the SVM based clasifier
- comp_NN.ipynb   - Jupyter notebooks used to train the NN
- comp_SVM.ipynb  - Jupyter notebooks used to train the SVM


## Confusion Matrix
### SVM
*The indexes are in alphabetical order excluding J
![SVM CF](https://github.com/Chamodya-ka/classifier_comparison/blob/master/models/SVM/SVM_II.png)

- Although the confusion matrix looks almost perfect there were alot of false positives for the following letters
- M, N and H have similar poses hence there is a confusion.

### NN
*The indexes are in alphabetical order excluding J
![NN CF](https://github.com/Chamodya-ka/classifier_comparison/blob/master/models/NN/II_CM_Fair.png)

- M, N and H have similar poses hence there is a confusion.
- Upon testing letter "R" was the most confused with other letters although its contradictory to the confusion matrix. 
- I assume the contradictions were caused due to bad lighting conditions.

## Conclusion 
Other than for the letters "M","N","H" the SVM approach performed better compared to the NN approach. With an added flash light the *Overall* accuracy of the extracted keypoints increased hence accuracy of the predictions of both the methods increased. Een with the added light however the SVM failed to distinguish between the letters "N" and "M" however the NN was able to distinguish the fine details. As of now I prefer the NN approach.

### To Do
Re check the SVM with "N" and "M" data and try another iteration lowering the error tolerence.
