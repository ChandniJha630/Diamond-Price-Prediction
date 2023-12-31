from flask import Flask,request,render_template,jsonify
from src.pipelines.prediction_pipeline import CustomData,PredictPipeline

application=Flask(__name__)
app=application

@app.route('/',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        print("Rendering Template")
        return render_template('index.html')
    else:
        data=CustomData(
            carat=float(request.form.get('carat')),
            depth=float(request.form.get('depth')),
            table=float(request.form.get('table')),
            x=float(request.form.get('x')),
            y=float(request.form.get('y')),
            z=float(request.form.get('z')),
            cut=request.form.get('cut'),
            color=request.form.get('color'),
            clarity=request.form.get('clarity')
        )
        final_new_data=data.get_data_as_dataframe()
        predict_pipeline=PredictPipeline()
        pred=predict_pipeline.predict(feature=final_new_data)
        
        result=round(pred[0],2)
        final_ans= f"Cost of Your Diamond is  {result}"
        return render_template  ('index.html',result=final_ans)
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
