import json
from tvDatafeed import Interval

def return_time(time):
   try:
      if time == "1 Minute":
         return Interval.in_1_minute       
      elif time == "3 Minutes":
         return Interval.in_3_minute
      elif time == "5 Minutes":
         return Interval.in_5_minute
      elif time =="15 Minutes":
         return Interval.in_15_minute
      elif time == "30 Minutes":
         return Interval.in_30_minute
      elif time == "45 Minutes":
         return Interval.in_45_minute
      elif time == "1 Hour":
         return Interval.in_1_hour
      elif time == "2 Hours":
         return Interval.in_2_hour
      elif time == "3 Hours":
         return Interval.in_3_hour
      elif time == "4 Hours":
         return Interval.in_4_hour
      elif time == "1 Day":
         return Interval.in_daily
      elif time == "1 Week":
         return Interval.in_weekly
      elif time == "1 Month":
         return Interval.in_monthly
   except:
        return "Unknown time format"

def cus_str2json(text_input):
   _dt = ''
   data = []
   for indx in range(len(text_input)):
      if text_input[indx] == '{':
         if _dt != '':
            _dt = ''
         _dt +=  text_input[indx]
      elif _dt != '':
         _dt +=  text_input[indx]

      if text_input[indx] == '}':
         try:
            data.append(json.loads(_dt))
         except:
            pass
         _dt=''
   if data != []:
      return data
   else:
      return [{}]

def logic_str2json(text_input, value):
   if text_input == None:
      return ''
   new1 = text_input.replace('df', value)
   new2 = new1.replace('\n', '')
   new = new2.replace("\\", '')
   return new
