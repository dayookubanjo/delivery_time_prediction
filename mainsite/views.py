from django.shortcuts import render, redirect
import pandas as pd 
import numpy as np 
import pickle 
from django.contrib import messages
import boto3
from django.core.files.storage import default_storage as storage
from django.conf import settings

# Create your views here.

def error_404(request, exception):
        data = {}
        return render(request,'mainsite/404.html', data)


def index(request): 
  context = {
  }
  return render(request, "index.html", context)

def predict(request):
    if request.method == 'POST':
        pickup_monthday = request.POST['pickup_monthday']
        pickup_weekday = request.POST['pickup_weekday']
        temperature = request.POST['temperature']
        precipitation = request.POST['precipitation']
        pickup_latitude = request.POST['pickup_latitude']
        pickup_longitude = request.POST['pickup_longitude']
        destination_latitude = request.POST['destination_latitude']
        destination_longitude = request.POST['destination_longitude']        
        pickup_hour = request.POST['pickup_hour']
        pickup_minute = request.POST['pickup_minute']
        pickup_second = request.POST['pickup_second']
        #data = [pickup_monthday,pickup_weekday,temperature,precipitation,pickup_latitude,pickup_longitude,destination_latitude,destination_longitude,pickup_hour,pickup_minute,pickup_second]
        #test_df = pd.DataFrame([data], columns = ["pickup_monthday","pickup_weekday","temperature","precipitation","pickup_latitude","pickup_longitude","destination_latitude","destination_longitude","pickup_hour","pickup_minute,pickup_second"])

        test_array = np.array([[pickup_monthday,pickup_weekday,temperature,precipitation,pickup_latitude,pickup_longitude,destination_latitude,destination_longitude,pickup_hour,pickup_minute,pickup_second]])

        
        X_SC = pickle.load(open('delivery_time_pred_ml/x_scaler.sav','rb'))
        X_SC.clip = False
        test_array = X_SC.transform(test_array, )
        RFR = pickle.load(open('delivery_time_pred_ml/RFR.sav','rb'))
        y_pred = RFR.predict(test_array)
        SC = pickle.load(open('delivery_time_pred_ml/scaler.sav','rb'))
        y_pred = SC.inverse_transform(y_pred.reshape(-1, 1) )
        prediction = round(y_pred[0,0] , 2)

        messages.success(request, f"Your delivery will take {prediction} minutes.")

    return redirect ("index")
    #return render(request, "index.html",{"prediction": prediction})
