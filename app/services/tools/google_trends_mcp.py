from pytrends.request import TrendReq
import asyncio

# Pytrends setup
pytrends = TrendReq(hl='en-US', tz=360)

async def fetch_google_trends(keyword: str, region: str = 'GLOBAL', timeframe: str = 'today 12-m'):
    loop = asyncio.get_event_loop()

    def sync_fetch():
        try:
            # Build payload
            pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo='' if region=='GLOBAL' else region, gprop='')
            
            # 1️⃣ Interest over time
            over_time = pytrends.interest_over_time().to_dict(orient='records')
            
            # 2️⃣ Interest by region
            by_region = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True).to_dict(orient='records')
            
            # 3️⃣ Related queries
            related_queries = pytrends.related_queries()
            
            # 4️⃣ Keyword trends / rising / top
            top_queries = related_queries[keyword]['top'].to_dict(orient='records') if related_queries[keyword]['top'] is not None else []
            rising_queries = related_queries[keyword]['rising'].to_dict(orient='records') if related_queries[keyword]['rising'] is not None else []

            # 5️⃣ Popularity (average of interest over time)
            popularity = sum([entry.get(keyword, 0) for entry in over_time])/len(over_time) if over_time else 0
            
            return {
                "keyword": keyword,
                "popularity": popularity,
                "over_time_trend": over_time,
                "region_trend": by_region,
                "top_queries": top_queries,
                "rising_queries": rising_queries
            }
        except Exception as e:
            return {"error": str(e)}
    
    # Run sync code in threadpool to not block async
    result = await loop.run_in_executor(None, sync_fetch)
    return result
