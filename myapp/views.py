try:
    from django.shortcuts import render
except Exception:
    # Fallback stub for environments without Django (prevents import errors in editors/tests)
    def render(request, template_name, context=None):
        # simple placeholder return value to allow basic testing without Django
        return {"template": template_name, "context": context or {}}

import os
import joblib
import pandas as pd
from .models import History

path = os.path.dirname(__file__)  # provide root path of myapp

# Load model and label encoder safely; if files are missing or load fails, set to None
model = None
label_encoder = None
try:
    model = joblib.load(os.path.join(path, 'best_model.pkl'))
except Exception:
    model = None

try:
    label_encoder = joblib.load(os.path.join(path, 'label_encoder.pkl'))
except Exception:
    label_encoder = None

# Create your views here.
def index(req):
    return render(req, "index.html")

def prediction(req):
    if req.method == 'POST':
        # use get to avoid KeyError if a field is missing
        fever = req.POST.get('fever', 0)
        headache = req.POST.get('headache', 0)
        nausea = req.POST.get('nausea', 0)
        vomiting = req.POST.get('vomiting', 0)
        fatigue = req.POST.get('fatigue', 0)
        joint_pain = req.POST.get('joint_pain', 0)
        skin_rash = req.POST.get('skin_rash', 0)
        cough = req.POST.get('cough', 0)
        weight_loss = req.POST.get('weight_loss', 0)
        yellow_eyes = req.POST.get('yellow_eyes', 0)
        symptoms = ['fever','headache','nausea','vomiting','fatigue','joint_pain','skin_rash','cough','weight_loss','yellow_eyes']
        user_input = [fever, headache, nausea, vomiting, fatigue, joint_pain, skin_rash, cough, weight_loss, yellow_eyes]

        # build DataFrame and convert values to numeric (model likely expects numbers)
        input_df = pd.DataFrame([user_input], columns=symptoms)
        input_df = input_df.apply(pd.to_numeric, errors='coerce').fillna(0)

        res = "Model or encoder not available"
        try:
            if model is None:
                raise RuntimeError("Model file not loaded.")
            # corrected method name: predict
            result = model.predict(input_df)
            if label_encoder is not None:
                # inverse_transform expects array-like
                res = label_encoder.inverse_transform([result[0]])[0]
            else:
                res = str(result[0])
        except Exception as e:
            # return a helpful message rather than crashing
            res = f"Prediction error: {e}"

        #ORM object Relationship Mapping
        his = History(fever = fever, headache = headache, nausea = nausea, vomiting = vomiting, fatigue = fatigue, joint_pain= joint_pain, skin_rash = skin_rash, cough = cough, weight_loss = weight_loss, yellow_eyes = yellow_eyes, res = res)
        his.save()
        
        # keep template name unchanged (pridiction.html) to match your existing templates/urls
        return render(req, "pridiction.html", {"res": res})
    return render(req, "pridiction.html")

# alias to match existing URLs that reference views.pridiction
pridiction = prediction

def history(req):
    his = History.objects.all() #select
    return render(req, "history.html",{"his":his})