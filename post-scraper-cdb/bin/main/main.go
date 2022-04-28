package main

import (
    "fmt"
    "skunz42/post-scraper/src/credentials"
    "skunz42/post-scraper/src/auth"
    "skunz42/post-scraper/src/scraper"
    "skunz42/post-scraper/src/database"
)

func main() {
    config_data := credentials.MakeClient()
    database_data := credentials.MakeDbClient()

    // Get a reddit token
    auth.GetToken(config_data)

    // Fetch posts from reddit
    posts, authors := scraper.GetSubPosts(config_data)

    // Ping DB
    get_ping := database.PingDB(database_data)

    // If the ping is successful
    if get_ping {
        database.WriteAuthors(database_data, authors)
        database.WritePosts(database_data, posts)
    } else {
        fmt.Println("Could not ping database")
    }
}
