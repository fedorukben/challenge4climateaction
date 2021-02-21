import sqlite3 as sql
from utils import Debugger

class FieldManager(object):
  def __init__(self, conn, db_name, dictionary):
    self.conn = conn
    self.db_name = db_name
    # Dictionary is generated if none is specified
    if dictionary == None:
      dictionary = {}
    else:
      self.dictionary = dictionary
  # Adds specified field from specified db to a list
  # Adds this list to the dictionary 
  # dict is optional, if no dict is provided one will be generated
  def add_field_list(self, field, param):
    # Predefined querie
    q = f'SELECT {field} FROM {self.db_name} {param}'
    # Lists for field values
    obj_list = []
    # Get data from specified fields
    for r in self.conn.query(q):
      obj_list.append(r)
    # Place generated list into dictionary
    self.dictionary[f'{field}'] = obj_list
    # return lists
    return self.dictionary

class SQLConnection(object):
  def __init__(self, addr):
    self.addr = addr
    self.conn = sql.connect(addr)
    self.crsr = self.conn.cursor()
    self.debug = Debugger()
    self.debug.prn(self, 'SQLConnection object created.')
    self.debug.prn(self, 'Connection established.')
  def class_name(self):
    return 'SQLConnection'
  def get_addr(self):
    return self.addr
  def set_addr(self, addr):
    self.addr = addr
  def get_conn(self):
    return self.conn
  def get_crsr(self):
    return self.crsr
  def queue(self, sql_code):
    self.crsr.execute(sql_code)
    self.debug.prn(self, 'Queued command.')
  def queue_script(self, script):
    self.crsr.executescript(script)
    self.debug.prn(self, 'Queued script.')
  def queue_for_all(self, sql_code, data):
    self.crsr.executemany(sql_code, data)
    self.debug.prn(self, 'Queued command for all.')
  def commit(self):
    self.conn.commit()
    self.debug.prn(self, 'Committed queue.')
  def close(self):
    self.conn.close()
    self.debug.prn(self, 'Connection terminated.')
  def fetch(self, select_code=None):
    if select_code != None:
      self.queue(select_code)
    self.debug.prn(self, 'Data fetched.')
    return self.crsr.fetchall()