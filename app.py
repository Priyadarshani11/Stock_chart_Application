from flask import Flask, render_template, request
from dateutil.relativedelta import relativedelta
import datetime
import requests

# Flask application instantiation
app = Flask(__name__)

# Generate 30 days starting from 1 may to 30 may 
dates_=[]
def generate_dates():
    today = datetime.date.today()
    first_day_of_current_month = today.replace(day=1)
    first_day_of_previous_month = first_day_of_current_month - relativedelta(months=1)
    end_date = first_day_of_previous_month + relativedelta(day=30)

    current_date = first_day_of_previous_month
    while current_date <= end_date:
        # Print the date in the desired format
        dates_.append(current_date.strftime("%m/%d/%Y")) 
        # Increment the date by 1 day 
        current_date += datetime.timedelta(days=1) 

#bind URL to the function         
@app.route('/', methods=['GET', 'POST'])
def stock_chart():
    if request.method == 'POST':
        Symbol = request.form['symbol']
        api_key = '048EDA4A3196428C8B777A5C4A26B3EC'
        
        date_with_price= {}
        for date in dates_:

            url = f'https://factsetestimates.xignite.com/xFactSetEstimates.json/GetEstimatesRange?IdentifierType=Symbol&Identifier={Symbol}&EstimateTypes=EPS,Sales&ReportType=Quarterly&EstimateFiscalPeriod=2023FY&StartDate={date}&EndDate={date}&UpdatedSince=&_token={api_key}'

            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

                # Extract date and price datewise 
                
                if data is not None and 'EstimatesSets' in data and data['EstimatesSets']:
                    datee = data['EstimatesSets'][0]['Estimates'][0]["Date"]
                    pricess =data['EstimatesSets'][0]['Estimates'][0]["Value"]
                    date_with_price[datee]=pricess
                                                    
                else:
                    return f"Error: Invalid response data"
            else:
                return f"Error: {response.status_code}"

        return render_template('chart.html', symbol=Symbol, data=date_with_price)

    return render_template('form.html')

if __name__ == '__main__':
    generate_dates()
    app.run()
