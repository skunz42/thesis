# Thesis Proposal

### Background

Worries about crime have increased throughout pandemic years
- Defund police movement has largely been defeated (eg Minneapolis)
- Political candidates have won elections based on fears of rise in crime (eg Eric Adams)
- Conservatives very vocal about the issue

(cite news sources here)

Media plays a role in perpetuating fears and shaping landscape of perceptions about crime
- exacerbate fear of crime
- many people get news/info from online and social media sources
- Influence of social media similar to traditional media

(cite geography/sociology/criminology papers here)

Reddit
- social media platform
- subreddits - communities about a single topic
- communities about communities

(cite cs papers here)

### Questions

1. How frequently are posts related to crime posted to city subreddits?
2. What is the profile of cities with high crime-posting frequency? (politics, size, actual crime rate)
3. What is the profile of people who post about crimes? (where do they post?)

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
- Most scraping will be written in Golang
- Data is being stored in a PostgreSQL DB - tables (posts, authors, author-info)
- Author-Overlap scraper will run in docker containers for increased scaling and isolation
- misc scraper - determine if post is about crime or not - NLP?

##### Visualization
- ArcGIS Enterprise (Server) - use to get GeoJSON files
- ArcGIS JS API - map makin
- JSON endpoint - for JS API

### For prof
- Setting up VM + DB
- Literature Review - how to find good papers?
- Ideas for additional analysis
- Visualization - website or no
