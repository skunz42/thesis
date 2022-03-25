package main

import (
    "fmt"
    "os"
    "skunz42/post-scraper/src/credentials"
    "skunz42/post-scraper/src/auth"
    "skunz42/post-scraper/src/scraper"
    "skunz42/post-scraper/src/database"
)

func main() {
    if len(os.Args) != 2 {
        fmt.Println("Arguments: <user credentials>")
        os.Exit(1)
    }

    //TODO change to env
    config_data := credentials.MakeClient(os.Args[1])
    database_data := credentials.MakeDbClient(os.Args[1])

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
