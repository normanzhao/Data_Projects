from bs4 import BeautifulSoup
import urllib2
import time
from sqlalchemy import create_engine

fields = ['aerospace-engineering', 'agricultural-engineering', 'architectural-engineering', 'biomedical-engineering', 'chemical-engineering', \
        'civil-engineering', 'computer-engineering', 'construction-engineering', 'electrical-engineering','environmental-engineering', \
        'financial-engineering', 'geotechnical-engineering', 'industrial-engineering', 'manufacturing-engineering', 'marine-engineering', 'materials-engineering', \
        'mechanical-engineering', 'metallurgical-engineering', 'mining-engineering', 'network-engineering', 'nuclear-engineering', 'packaging-engineering',\
        'petroleum-engineering', 'process-engineering', 'project-engineering', 'quality-engineering', 'safety-engineering', 'sales-engineering', 'software-engineering',\
        'solar-engineering', 'structural-engineering', 'systems-engineering']

engine = create_engine('mysql+pymysql://adder:@localhost:3306/jobsend.io?charset=utf8', encoding='utf8', echo=False)
