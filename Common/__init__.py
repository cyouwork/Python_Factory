# coding=utf-8
# author=season
#   import struct
#   import socket
#   import urllib2
#   import json
#   import datetime
#   from ip2country import iplocate
#   from dbconn import DbConn
#   from logger import getlogger
#   from colorLogger import coloLogger
#   from subprocess import Popen, PIPE
#   try:
#       import xml.etree.cElementTree as ET
#   except ImportError:
#       import xml.etree.ElementTree as ET
#   
#   
#   class CommonError(Exception):
#       pass
#   
#   
#   def iptoint(ip):
#       return struct.unpack('!I', socket.inet_aton(ip))[0]
#   
#   
#   def read_db(sql, dbconn):
#       """从Mysql中读取数据"""
#       dbconn_conf = {
#           'host': dbconn._host,
#           'port': dbconn._port,
#           'user': dbconn._user,
#           'password': dbconn._password,
#           'database': dbconn._database,
#           'sql': sql
#       }
#       cmd = """mysql -X -C -h {host} -P {port} -u {user} -p'{password}' \
#       {database} --default-character-set=utf8 -s  -e "{sql}" | iconv -t US-ASCII -c | sed 's///g'""".format(**dbconn_conf)
#       return Popen(cmd, stdout=PIPE, shell=True).stdout
#   
#   
#   def read_db_csv(sql, dbconn):
#       """从Mysql中读取数据"""
#       dbconn_conf = {
#           'host': dbconn._host,
#           'port': dbconn._port,
#           'user': dbconn._user,
#           'password': dbconn._password,
#           'database': dbconn._database,
#           'sql': sql
#       }
#       cmd = """mysql  -C -h {host} -P {port} -u {user} -p'{password}' \
#       {database} --default-character-set=utf8 -s  -e "{sql}" """.format(**dbconn_conf)
#       return Popen(cmd, stdout=PIPE, shell=True).stdout
#   
#   
#   def xml_to_csv(source):
#       '''将xml文件转成csv'''
#       tree = ET.fromstring(source)
#       to_list = []
#       mylist = [t.getchildren() for t in tree.getchildren()]
#       for i in [t for t in mylist]:
#           text = [ii.text for ii in i]
#           line = '"%s"' % '","'.join([x if x else 'None' for x in text])
#           to_list.append(line)
#       return to_list
#   
#   
#   def csv_to_list(source):
#       '''将csv文件转成list'''
#       for line in source.split('\n'):
#           if line:
#               yield line
#   
#   
#   def gameid_to_name(url='http://10.59.96.91/app.37wanwan.com/port/gamelist.php'):
#       '''游戏id对应到游戏名'''
#       request = urllib2.urlopen(url, timeout=10)
#       content = json.loads(request.read(), encoding='gbk')
#       return dict([(gameid, content[gameid]['name']) for gameid in content])
#   
#   
#   _DATETIME_FORMATS = [
#       '%a %b %d %H:%M:%S %Y',
#       '%Y-%m-%d %H:%M:%S',
#       '%Y-%m-%d %H:%M',
#       '%Y-%m-%d %H',
#       '%Y-%m-%d',
#       '%Y%m%d%H%M%S',
#       '%Y%m%d%H%M',
#       '%Y%m%d%H',
#       '%Y%m%d'
#   ]
#   
#   
#   def parse_datetime(in_datetime):
#       if isinstance(in_datetime, datetime.datetime):
#           return in_datetime
#       for format in _DATETIME_FORMATS:
#           try:
#               return datetime.datetime.strptime(in_datetime, format)
#           except ValueError, err:
#               pass
#       raise CommonError('Unrecognized date/time format: %r' % in_datetime)
#   
#   
#   def bsearch(Sdict):
#       Sdict = Sdict
#       Keys = sorted(Sdict.keys())
#       started = 0
#       ended = len(Keys) - 1
#   
#       def wapper(key, started=started, ended=ended):
#           if started > ended:
#               return None
#           index = (started + ended) / 2
#           if Keys[index][0] <= key <= Keys[index][1]:
#               return Sdict[Keys[index]]
#           elif key < Keys[index][0]:
#               return wapper(key, started=started, ended=index - 1)
#           elif key > Keys[index][1]:
#               return wapper(key, started=index + 1, ended=ended)
#       return wapper
#   
#   
#   _SPIDER_AGENTS = {
#       '"Mozilla/4.0"': True,
#   }
#   
#   
#   def spider_filter(agent):
#       return _SPIDER_AGENTS.get(agent, False)
#   
#   if __name__ == '__main__':
#       import sys
#       parse_datetime(sys.argv[1])
