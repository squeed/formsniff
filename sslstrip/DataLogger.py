# Copyright (c) 2011 Casey Callendrello
# Based heavily on 'sslstrip' released by Moxie Marlinspike <moxie@thoughtcrime.org>
#    (which can be found at http://www.thoughtcrime.org/software/sslstrip/)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA
#

import os
import logging
import sqlite3



class DataLogger:
    
    '''
    This class is responsible for logging any and all POST requests that come our way.
    
    It stores them in a configurable SQLite database.
    
    Oh, and this is responsible for storing the "magic string"
    '''
    _instance = None
    
    @staticmethod    
    def getInstance( filename = None):
        if DataLogger._instance == None:
            DataLogger._instance = DataLogger(filename)
        
        return DataLogger._instance
    
    
    def __init__(self, db_path):
        """
        Constructor; creates DB file if not extant.
        """
        
        if not os.path.exists(db_path):
            logging.debug("Opening new database at %s" % db_path )
        
        else:
            logging.debug("Opening existing database at %s" % db_path )
            
        self.db_path = db_path
        
        c = self._conn()
        
        create_table = """ create table if not exists hit (
        hitid INTEGER PRIMARY KEY,
        ip string not null,
        conntime integer DEFAULT current_timestamp,
        url string not null
        )
        """
        
        c.execute(create_table)
        
        create_table = """
        create table if not exists postdatum (
            hitid  REFERENCES hit(hitid),
            key BLOB,
            value BLOB
        )
        """
        
        c.execute(create_table)
        
        c.commit()
        
    
    def _conn(self):
        return sqlite3.connect(self.db_path)

    def log_request(self, client_ip, uri, postdata):
        """ 
        Takes request information and stores it in the DB
        
        """
        
        
        conn = self._conn()
        
        c = conn.cursor()
        
        c.execute('begin;') #probably superfluous
        
        sql = """
        insert into hit (ip, url) values (?, ?)
        """
        
        c.execute(sql, (client_ip, uri))
        
        hitid = c.lastrowid
        
        for key in postdata:
            for val in postdata[key]:
           	try:
			vv = unicode(val)
			kk = unicode(key) 
	                sql = """insert into postdatum (hitid, key, value)
        	        values (?, ?, ?)
       	 
        	        """
                	c.execute(sql, (hitid, key, val))
			print sql, key, val
		except Exception, e:
			raise e 
        
        conn.commit()        

    
    def get_all_hits(self):
        conn = self._conn()
        c = conn.cursor()
        get_sql = """
        select h.hitid, h.ip, h.conntime, h.url,
            d.key, d.value
        from hit h, postdatum d
        where h.hitid = d.hitid
        order by h.conntime, h.hitid
        """
        c.execute(get_sql)

        return c.fetchall()

 
