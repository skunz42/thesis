# Thesis Proposal

### General Idea

I plan on tracking crime posting on Reddit communities that represent real Ameican cities (r/nyc, r/sanfrancisco, etc.). I will then look at the characteristics of the various cities and attempt to answer these three questions:

1. How frequently are posts related to crime posted to city subreddits?
2. What is the profile of cities with high crime-posting frequency and low crime-posting frequency? (politics, size, actual crime rate)
3. What is the profile of people who post about crimes? (where else do they post?)

### Background and Related Work

I plan on splitting the background into four major subsections:

1. Politics surrounding the issue. I plan on addressing the defund the police movement and elections about the issue (eg NYC mayoral race). I'll try to cite news articles here (not sure if this is common in research papers, though).
2. The role media plays in perpetuating fears and shaping perceptions about crime. This will tie into the related works section, as I'm sure there are papers about how traditional media shapes perceptions of crime. There might also be papers out there about social media's effect on crime perception, but I feel that these will be more on the sociology/geography side and will be less technical.
3. What Reddit is and some basic background/terminology. I'll also try to use papers about Reddit for the related works section.
4. Definition of some of the geography-based terms (metropolitan statistical areas, urbanazied areas/clusters, etc.).

### Data Sources

There will be a mix of qualitative and quantitative data

Data for cities/qualitative analysis:
- Demographic data - US Census Bureau
- Crime data - FBI Crime Statistics
- Political data - New York Times/Associated Press
- GeoJSON data - US Census Tiger Files / ArcGIS Enterprise Server

Data from Reddit:
- Reddit API
- Posts from subreddits for the principal cities of the 385 metropolitan statistical areas
- Storing titles, contents, dates, authors
- Will write code to determine if post is about crime or not

Data for overlap metrics:
- User post info - subreddit, karma

### Technology

##### Scraping
- Two main scrapers: post scraper and user-info scraper
- Scraping will be written in Golang
- Data is being stored in a PostgreSQL DB with three tables (posts, authors, author-info)
- Author-Overlap scraper will run in docker containers for increased scaling and isolation as it can be fairly slow/intensive

##### Crime Post Identification
- Probably Golang/Python
- Simple - look for keywords (murdered, shot, assaulted, etc.) - possibility of false negatives/positives
- Advanced - some sort of text analysis to determine if a post is about crime (eg `Man shot on Main Street' vs `I shot a picture of the sunset')
- Not a lot of background here - will try to find examples in related work

##### Additional Analysis
- Might include additional analysis if previous is not sufficicent, but not sure what yet - will try to find inspiration in related works

##### Visualization
- Right now, planning on making a simple companion website for data visualization
- ArcGIS Enterprise (Server) will be used to get GeoJSON files to map out boundaries
- ArcGIS JS API will be used for map making on the web side and ArcGIS Pro will be used to include visualiztions in the report
- I'll also have a JSON endpoint for JS API

### Timeline
- January -> Mid-March - literature review
- Early-February -> Mid-February - Finish posts-scraper (data collection fully ready)
- Mid-February -> Mid-March - Finish overlap-scraper
- Mid-March -> Mid-May - Write background / related works sections of paper
- Mid-May -> Mid-June - Finish crime-post detection tool
- Mid-June -> Mid-July - Finish website / additional analysis
- Mid-June -> End-July - Data analysis
- End of July - Finish paper and be ready to present

### Questions For Jeremy
- Setting up VM + DB - can I have something similar to to CS 515
- Literature Review - how to find good papers? (especially for non-cs topics)
- Ideas for additional analysis, if needed
- Visualization - website or no
