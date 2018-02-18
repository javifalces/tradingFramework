import os

alpha_vantage_token = 'token'
dir_path = os.path.dirname(os.path.realpath(__file__))
csvData = dir_path + os.sep + 'csvData'
logsPath = dir_path + os.sep + 'logs' + os.sep
backtestData = dir_path + os.sep + 'backtestResults' + os.sep
backtestPicsData = dir_path + os.sep + 'backtestResultsPics' + os.sep
