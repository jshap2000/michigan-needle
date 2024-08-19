# michigan-needle

**Part 1: Precinct Similarity Clustering**

Using demographic, political, economic, and educational data, use a clustering algorithm to determine the "distance" or similarity of precincts to one another. This distance will be used on election night to improve the forecast.

**Part 2: Live Forecast**

Before election night starts, we establish a baseline estimate for each precinct determined by polling average, 2020 results, and expected turnout. When precincts start to report, we employ a weighted average of similar precincts (and their comparison to the initial baseline) to adjust both turnout and the percent of vote estimates. 

**Part 3: Live Scraping**

In order to process results fast enough, we will need to live scrape as much precinct data as possible. Precincts are reported by individual counties.

**Part 4: The visuals (if time)**

Create a map that shows votes counted and votes remaining. This requires shapefiles and data.
