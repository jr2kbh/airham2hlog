from ast import Is
from datetime import datetime ,timedelta
from pytz import timezone
import csv
import sys
import argparse
import re
from dateutil import tz

freq2lambda = {'430MHz': '430','7MHz':'7','21MHz':'21','1.9MHz':'1.9','3.5MHz':'3.5',
               '3.8MHz':'3.8','14MHz':'14','18MHz': '18','24MHz':'24','28MHz':'28','50MHz':'50','144MHz':'144',
               '1200MHz': '1200'}
mode2lambda ={'FM':'FM','CW': 'CW','SSB(LSB)':'SSB','SSB(USB)':'SSB','AM':'AM','FT4':'FT4','FT8':'FT8','D-STAR(DV)':'DV'}


def main(config):
    csv_file = open(config['csv_filepath'],encoding='utf8')
    ff = csv.DictReader(csv_file,
                       delimiter=",",
                       doublequote=True,
                       lineterminator="\r\n",
                       quotechar='"',
                       skipinitialspace=True)
    print(config['from_date'])
    with open(f"{config['output_prefix']}.csv",
                    'w',encoding='shift_jis')  as f:
        for row in ff:
            callsign = row['callsign']
            sent_qth = row['sent_qth']
            if ':' in sent_qth:
                qth_number = '%' + sent_qth.split('-')[0] +'%'
            else:
                qth_number = sent_qth
           
            if len(row['portable']) > 0:
                callsign += '/' + row['portable']
            # print(row['qso_at'][-3])
            if row['qso_at'][-3:] == 'UTC':
                va='%Y-%m-%d %H:%M:%S %Z'
                isUtc=True
            else:
                va='%Y-%m-%d %H:%M:%S %z'
                isUtc=False
            ts = datetime.strptime(
                row['qso_at'],
                va)  # '2020-12-12 16:51:00 +0900'--->JST,,, UTC の時は　%Z　大文字
            JST = tz.gettz('Asia/Tokyo')
            UTC = tz.gettz("UTC")
            # print(ts.tzinfo,ts)
            #dir
            # print(ts)
            # print(datetime.strptime(config['from_date'],'%y/%m/%d').replace(tzinfo=UTC))
            if isUtc :
                # print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
                ts=ts.replace(tzinfo=UTC) # UTC の時は　強制的にUTCつけないとだめ
            if ts<datetime.strptime(config['from_date'],'%y/%m/%d').replace(tzinfo=UTC):
                continue
            m= re.match('^J[A-S]|^[7-8][J-N]',callsign)
            
            print(callsign, file=f,end=",") #1)call sign
            # print(ts.isoformat())
            t1=ts.astimezone(JST)
            # print(t1.isoformat())
            t2=ts.astimezone(UTC)
            # print(t2.isoformat())
            
            if m :
                ts_date = t1.strftime('%y/%m/%d')
                ts_time = t1.strftime('%H:%MJ')
            else:
                ts_date = t2.strftime('%y/%m/%d')
                ts_time = t2.strftime('%H:%MU')
            print(t1,callsign)
            print(ts_date, file=f,end=",") #2) QSO DATE
            print(ts_time, file=f,end=",") #3) QSO TIME
            print(row['sent_rst'],file=f,end=",") #4) His
            print(row['received_rst'],file=f,end=",") #5) My
            freq = freq2lambda[row['frequency']]
            print(freq, file=f,end=",") #6) FREQ
            mode=mode2lambda [row['mode']]
            print(mode, file=f,end=",") #7) mode
            qth=row['received_qth'] 
            m=re.search(r'(\d+): (.+) -.*\((.+)\)', qth) 
            
            # print(row)
            if m == None:
                print('',file=f,end=",")
            else:
                qth=m.group(2)+'/'+m.group(3)
                print(m.group(1),file=f,end=",") #8) code
            print('', file=f,end=",") #9) GLID
            qsl_sent = ' *' if row['is_qsl_sent'] == 'true' else ''
            print(qsl_sent, file=f,end=",") #10)QSL
            
            print(row['received_qra'],file=f,end=",") #11) Name
           
            print(qth,file=f,end=",") #12) QTH
            print(qth_number +row['remarks'], file=f,end=",") #13) remark1
            print(row['card_remarks'], file=f,end=",") #14) remark2
            print('', file=f)

    return 0


def cli():
    # td=datetime.now()
    td=datetime.today().date().strftime('%y/%m/%d')
   
    parser = argparse.ArgumentParser(
        description='Airtest airHamlog CSV to Hamlog CSV Converter')
    parser.add_argument('csv_filepath')
    parser.add_argument('-f',
                        '--from_date',
                        help='from date yy/mm/dd',
                        default=td)
    parser.add_argument('-o',
                        '--output-prefix',
                        help='filename prefix for output CSV files',
                        default='export_')
    args = parser.parse_args()
    # print('default',td,'->',vars(args['from_date']))
    return main(vars(args))


if __name__ == '__main__':
    sys.exit(cli())