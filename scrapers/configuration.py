from enum import Enum

from simple_pdf_parser import retrieve_simple_pdf_results
from enhanced_id_parser import retrieve_enhanced_id_results
from clarity_elections_parser import retrieve_clarity_elections_results

class ResultsParser(Enum):
    SIMPLE_PDF = 1
    COMPLEX_PDF = 2
    GREEN_PDF = 3
    ENHANCED_ID = 4
    CLARITY_ELECTIONS = 5
    CUSTOM = 6
    MANUAL = 7

counties_to_parse = {
    "oakland": {
        "parser": ResultsParser.CLARITY_ELECTIONS,
        "link": "https://results.enr.clarityelections.com/MI/Oakland/122075/web.317647/#/summary",
        "start_word": "Harper",
        "end_word": "Representative",
        "precinct_column": 0,
        "total_vote_column": 26,
        "dem_column": 13,
        "rep_column": 7
    },
    "macomb": {
        "parser": ResultsParser.CLARITY_ELECTIONS,
        "link": "https://results.enr.clarityelections.com/MI/Macomb/122156/web.345435/#/summary",
        "start_word": "Harper",
        "end_word": "Representative",
        "precinct_column": 0,
        "total_vote_column": 14,
        "dem_column": 5,
        "rep_column": 9
    }
}

counties_to_parse2 = {
    "alger": {
        "parser": ResultsParser.SIMPLE_PDF,
        "link": "https://cms2.revize.com/revize/algercounty/document_center/Departments/Clerk_RoD/Elections/2022/November%208,%202022%20General%20Election.pdf",
        "start_page": 3,
        "end_page": 3,
        "start_row": 3,
        "end_row": 12,
        "should_skip_every_other_page": True,
        "precinct_column": 0,
        "total_vote_column": 1,
        "dem_column": 4,
        "rep_column": 6
    },
    "alpena": {
        "parser": ResultsParser.SIMPLE_PDF,
        "link": "https://www.alpenacounty.org/DocumentCenter/View/101/2020-November-Precinct-by-Precinct-PDF",
        "start_page": 3,
        "end_page": 3,
        "start_row": 3,
        "end_row": 17,
        "should_skip_every_other_page": True,
        "precinct_column": 0,
        "total_vote_column": 1,
        "dem_column": 3,
        "rep_column": 4
    },
    "kent": {
        "parser": ResultsParser.ENHANCED_ID,
        "link": "https://app.enhancedvoting.com/results/public/kent-county-MI/elections/August2024StatePrimary",
        "dem_index": "2",
        "rep_index": "3"
    },
    "saginaw": {
        "parser": ResultsParser.ENHANCED_ID,
        "link": "https://app.enhancedvoting.com/results/public/saginaw-county-MI/elections/August2024Primary",
        "dem_index": "35",
        "rep_index": "34"
    }
}

for county_name in counties_to_parse:
    county_details = counties_to_parse[county_name]

    if county_details["parser"] is ResultsParser.SIMPLE_PDF:
        df = retrieve_simple_pdf_results(
            county_name, 
            county_details["link"], 
            county_details["start_page"], 
            county_details["end_page"], 
            county_details["start_row"], 
            county_details["end_row"], 
            county_details["should_skip_every_other_page"], 
            county_details["precinct_column"],
            county_details["total_vote_column"], 
            county_details["dem_column"], 
            county_details["rep_column"]
        )
    elif county_details["parser"] is ResultsParser.ENHANCED_ID:
        df = retrieve_enhanced_id_results(
            county_name,
            county_details["link"],
            county_details["dem_index"],
            county_details["rep_index"] 
        )
    elif county_details["parser"] is ResultsParser.CLARITY_ELECTIONS:
        df = retrieve_clarity_elections_results(
            county_name,
            county_details["link"],
            county_details["start_word"],
            county_details["end_word"],
            county_details["precinct_column"],
            county_details["total_vote_column"], 
            county_details["dem_column"], 
            county_details["rep_column"]
        )

        print(df)
