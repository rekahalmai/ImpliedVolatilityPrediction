# Implied volatility prediction 

The repository contains time-series modeling approaches and stock option data from 2006-12-01 to 2015-10-0. 

The repository can be initialized in a docker container if desktop docker is available (download: https://docs.docker.com/install/) by the following commands: 

###### Create docker image 
``docker build -t vol_prediction .``

###### Start a docker container by running: 

``docker run --name vol_prediction ``

The Dockerfile contains the necessary package installations. If you want to run the code without the container, use the pip-tools package to install all packages. In this case create a virtual environment in Python 3.7, and run the following terminal command from the repository:  
``pip3 install pip-tools``

``pip-compile requirements.in``

``pip-sync requirements.in``
This imports all necessary packages to run anything from the repo. 

### Folder structure 

````
data
    └── spots_iv_index_spx_ai_daily.xlsx   # original data
    └── spots_iv_index_spx_ai_weekly.xlsx  # original data
    └── spots_iv_index_sx5e_ai_daily.xlsx  # original data
    └── spots_iv_index_sx5e_ai_weekly.xlsx # original data
    └── spx_daily.xlsx                     # changed dataset for easier import 
    └── spx_weekly.xlsx                    # changed dataset for easier import 
notebooks 
    └── ARIMA                              # AR, MA, ARIMA, SARIMA models
    └── DeepAR                             # DeepAR model 
    └── EDA-spx                            # EDA for the sx5 data 
    └── EDA-sx5e                           # EDA for the sx5 data
    └── TS_EDA_and_tests                   # Stationarity, exponential moving average EDA 
    └── TS_examples
src 
    └── data                               # data importation and transformation functions 
    └── data_analysis                      # correlation analysis functions
    └── graphs                             # visualization functions 
    └── ts_tests                           # TS tests and methods functions 
````

# Models and results
 
## EDA-sx5e and EDA-spx notebooks: 
Data exploration. Graphed the implied volatility and the "Change_in_implied_vol" for all strike-maturity combination. 
High correlation between the TS is observed (used stat: Pearson correlation). 
Conclusion: there is a strong correlation between the individual TS, a method that link them together might be preferred. 

## TS_EDA_and_tests notebook: 
Check TS statistics, (such as the ADF-test, ACF, PACF) individually for the TS of change_in_implied_vol for each 
strike-maturity option. 

Results: 
- All TS are stationarity although variance can change over time.  
- Graphed ACF and PACFs. Both show very high lag correlation between past values. 
(This determines and complicates the model selection in AR, MA and ARIMA models, as these graphs indicate that we should 
use high lags. 
On the other hand, high lags results in complicated AR and/ or MA models, long training, etc...)
- Graphed moving averages to better understand the mean and variance. Mean is always centered around 0 but variance 
changes - random walk type TS. No trend or seasonality is observed. 
- Graphed seasonal decomposition. No trend or seasonality, residuals are quite close to actual values -> 
the model is unable to differentiate between these. 


## ARIMA notebook: 
This notebook contains AR, MA, ARIMA, SARIMA and ES models for one TS. 

Results: 
- poor results, if model size increases, training time does too. Predictions center around 0, 
- Combination of AR and MA models give better results than individual AR or MA ones, even with increased lags. 
- SARIMA package is unstable, takes a very long time to train and gives worse results than simpler ARIMA models. 
The model is also too slow to be trained on all data - only trained on 100 past observations. 
- Exponential Smoothing model gives very poor results, can be neglected. 
- Conclusion: AR, MA and ARIMA models are not suitable for this data as a consequence of individual, slow and 
non-automatic parameter selection, slow training, very high desired lags and lack of forecasting capacity. If the 
model is well-trained, it gives predictions around the mean. SARIMA models give even worse results. 

## DeepAR notebook: 
