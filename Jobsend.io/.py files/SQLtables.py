import sqlalchemy
from sqlalchemy import create_engine

fields = ['aerospace-engineering', 'agricultural-engineering', 'architectural-engineering', 'biomedical-engineering', 'chemical-engineering', \
        'civil-engineering', 'computer-engineering', 'construction-engineering', 'electrical-engineering', 'environmental-engineering', \
        'financial-engineering', 'geotechnical-engineering', 'industrial-engineering', 'manufacturing-engineering', 'marine-engineering', 'materials-engineering', \
        'mechanical-engineering', 'metallurgical-engineering', 'mining-engineering', 'network-engineering', 'nuclear-engineering', 'packaging-engineering',\
        'petroleum-engineering', 'process-engineering', 'project-engineering', 'quality-engineering', 'safety-engineering', 'sales-engineering', 'software-engineering',\
        'solar-engineering', 'structural-engineering', 'systems-engineering']

engine = create_engine('mysql+pymysql://root:V05lw5hCkPsB3cJW@localhost:3306/jobsend.io')
conn = engine.connect()


for field in fields:
    sql = '''CREATE TABLE `%s-jobs` (
  `title` text,
  `link` text,
  `company` text,
  `location` text,
  `state` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''%(field)
    conn.execute(sql)

table_sql = '''CREATE TABLE `emails` (
  `email` text NOT NULL,
  `field` text NOT NULL,
  `location` text NOT NULL,
  `position` text NOT NULL,
  `unsub` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
    
conn.execute(table_sql)

statuses_sql = '''CREATE TABLE `statuses` (
  `careerbuilder` text,
  `engineerjobs` text,
  `firstjobs` text,
  `indeed` text,
  `monster` text,
  `overall` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
    
conn.execute(statuses_sql)