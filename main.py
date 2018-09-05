# coding: utf-8
#libs used
import urllib3
import io
from textprocess import process, check
from data import newstage
from graph import plot

import traceback
import data

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning
                        )  #otherwise gives warnings I dont know how to fix.

http = urllib3.PoolManager()
#gather the data
for etape in range(1, 23):
    print('working on stage:' + str(etape))
    URL = 'https://www.procyclingstats.com/race/vuelta-a-espana/2018/stage-' + str(
        etape)
    #download the data
    try:
        r = http.request('GET', URL)  #get the actual site
    except Exception as ex:
        print(ex)
        print('Internet not working.')
        break
    page = r.data.decode('UTF-8')
    #check if ready
    if not check(page):
        print(str(etape) + ' is not ready.')
        break
    #open the file
    newstage(etape)
    process(page)
    print(str(etape) + ' is processed')
print('processing done')
plot(etape)  #get the actual site
