#### Use pandas module since this is what wrds python interface adopts.
import pandas as pd

datapath = "/media/markxueyuan/Data/Erturk/"


### read in data

    # SEO data

seo = pd.read_csv(
    datapath + 'seasoned_offering_1.csv',
    dtype = str # read in as string
)
    # Name data
stocknames = pd.read_csv(
    datapath + 'stocknames',
    dtype = str
)


### Prepare data for subsequent match

    # Change string to date
def to_date(col, df=stocknames, fmt='%Y-%m-%d'):
    df[col] = pd.to_datetime(df[col],
                             format=fmt,
                             errors='ignore')
    print(col + ' is transformed to date format.')

to_date('NAMEDT')
to_date('NAMEENDDT')
to_date('  Date', df=seo, fmt='%m/%d/%y')

    # Get 6 digit CUSIP
stocknames['CUSIP_6'] = [i[:6] for i in stocknames['NCUSIP']]


### Match data

def query(cusip, date):
    s = stocknames[(stocknames.CUSIP_6 == cusip)
                   & (stocknames.NAMEDT <= date)
                   & (stocknames.NAMEENDDT >= date)]
    if s.empty:
        return ""
    else:
        return s.iloc[0].PERMNO

    # Add PERMNO column to SEO data
seo['PERMNO']  = [query(r['CUSIP'], r['  Date'])
                 for _, r in seo.iterrows()]


    # Export matched data to csv file
seo.to_csv(datapath + 'seo_PERMNO_added.csv')


### Filter data

    # Setup filter criterion
exchange = "Primary\nExchange\nWhere\nIssuer's\nStock\nTrades"
ex_set = ['Nasdaq', 'NYSE MKT', 'NYSE Amex',
              'NYSE Alter', 'NYSE Arca',
              'American', 'Amer Emerg']

tfmiddle = 'TF Mid Description'
tf_set = ['REITs']

target = 'Target Market\nLong Description'
trg_reg = 'United States of America'




    # Filter data
seo_filtered = seo[
    (seo[exchange].isin(ex_set))
    &
    (~seo[tfmiddle].isin(tf_set))
    &
    (seo[target].str.match(trg_reg))
]

    # Export filtered data to csv file

seo_filtered.to_csv(datapath + 'seo_PERMNO_added_filtered.csv')

