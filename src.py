print("Importing Libraries")
import pandas as pd
import json
import numpy as np
import time
import logging
import datetime

def read_people_data(filename):
	with open(filename, 'r') as f:
		json_dict = [json.loads(line.strip()) for line in f]

	BMI_data = pd.DataFrame.from_records(json_dict)
	print(BMI_data.head())

	return BMI_data


def read_BMI_chart(filename):
	bmi_chart = pd.read_csv(filename)
	
	print(bmi_chart.head())

	# Preprocess Data and add new values
	bmi_chart[['minWT','maxWT']] = bmi_chart['BMI Range (kg/m2)'].str.split('-', n=1, expand=True)
	bmi_chart


	bmi_chart.loc[(bmi_chart['maxWT'].isnull() & bmi_chart['minWT'].str.contains('below')), ['minWT', 'maxWT']] = [0,18.4]
	bmi_chart.loc[(bmi_chart['maxWT'].isnull() & bmi_chart['minWT'].str.contains('above')), ['minWT', 'maxWT']] = [40,999]
	bmi_chart = bmi_chart.astype({'minWT':'float16', 'maxWT':'float16'})

	return bmi_chart


def find_category(bmi):
		return bmi_chart.loc[(bmi >= bmi_chart['minWT']) & (bmi < bmi_chart['maxWT']), 'BMI Category'].values[0]
	

if __name__ == '__main__':


	logging.basicConfig(filename=datetime.datetime.now().strftime('logfile_%H_%M_%d_%m_%Y_BMI.log'), encoding='utf-8', level=logging.DEBUG)
	logging.info("-----------------Starting execution-----------------")
	start = time.time()

	logging.info("Reading Height and Weight data of people")
	BMI_data =  read_people_data("json_data.txt")

	logging.info("Reading BMI chart data")
	bmi_chart = read_BMI_chart("BMI_chart.csv")


	logging.info("Calculating BMI of every person")
	BMI_data['BMI'] = BMI_data['WeightKg'] / np.power(BMI_data['HeightCm']/100, 2)
	
	logging.info(BMI_data.head())

	logging.info(f"Total number of overweigth people are {np.sum(BMI_data['BMI'] >= 25)}")

	logging.info("Applying BMI category to everyone")
	BMI_data['BMI Category'] =  BMI_data.apply(lambda row : find_category(row['BMI']), axis=1)

	logging.info("-----------------execution completed-----------------")
	logging.info("Time taken : " + str(time.time() - start) + " secs")

