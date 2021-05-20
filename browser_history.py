import sqlite3
from histories import HistoryRecord
import itertools
import operator


# strips query parameters from a url string (utm_campaign junk)
def strip_query(url):
    return url[:url.find('?')]


# Get the listing history from the sqlite path
def get_listing_history(connect_path):

    raw_results = get_raw_results(connect_path)
    result_strings = [result[0] for result in raw_results]
    results_no_query_params = {strip_query(result) for result in result_strings}
    history_records = [HistoryRecord.fromUrl(url) for url in sorted(results_no_query_params)]

    domain_getter = operator.attrgetter('domain')

    # domain => HistoryRecord map
    domains_to_history_records = {domain: set(history_record) for domain, history_record in itertools.groupby(history_records, domain_getter)}

    return domains_to_history_records


def get_raw_results(connect_path):
    con = sqlite3.connect(connect_path)
    c = con.cursor()
    # @TODO date range
    try:
        c.execute("""
                SELECT url FROM urls 
                    WHERE url LIKE 'https://www.zillow.com/homedetails%'
                    OR url LIKE 'https://www.trulia.com/p/%'
                    OR url LIKE 'https://hotpads.com%/pad%'
                    OR url LIKE 'https://www.apartments.com/%-st-%'
                    OR url LIKE 'https://www.apartments.com/%-street-%'
                    OR url LIKE 'https://www.apartments.com/%-ave-%'
                    OR url LIKE 'https://www.apartments.com/%-rd-%'
                    OR url LIKE 'https://www.apartments.com/%-road-%'
                    OR url LIKE 'https://www.rent.com/washington/seattle-houses/%' 
                        AND url NOT LIKE 'https://www.rent.com/%property-type=%'
                    OR url LIKE 'https://www.padmapper.com/apartments/%'
                    OR url LIKE 'https://www.padmapper.com/buildings/%'
                    OR url LIKE 'https://www.kw.com/property/%'
                    OR url LIKE 'https://www.forrent.com/wa/seattle/%'
                    OR url LIKE 'https://www.apartmentlist.com/wa/seattle/%'
                    OR url LIKE 'https://www.seattlerentals.com/_%'
                        AND url NOT LIKE 'https://www.seattlerentals.com/%search%'
                    OR url LIKE 'https://showmojo.com/l/%'
                    OR url LIKE 'https://seattle.craigslist.org/see/apa/d/'
                    ;
            """)
        results = c.fetchall()
        return results
    except Exception as err:
        print("failed " + str(err))
    c.close()
    return None
