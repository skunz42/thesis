package main

import (
    "fmt"
    "time"
    "skunz42/post-scraper/src/credentials"
    "skunz42/post-scraper/src/auth"
    "skunz42/post-scraper/src/scraper"
    "skunz42/post-scraper/src/database"
)

func main() {
    config_data := credentials.MakeClient()
    database_data := credentials.MakeDbClient()

    for {
        // Get a reddit token
        fmt.Println("=======================================================")
        auth.GetToken(config_data)

        // Fetch posts from reddit
        posts, authors := scraper.GetSubPosts(config_data, database_data)

        // Ping DB
        get_ping := database.PingDB(database_data)

        // If the ping is successful
        if get_ping != nil {
            database.WriteAuthors(database_data, authors, get_ping)
            fmt.Println("wrote authors")
            database.WritePosts(database_data, posts, get_ping)
            fmt.Println("wrote posts")
//        fmt.Println("cool, swag")
        } else {
            fmt.Println("Could not ping database")
        }

        fmt.Println("See you in an hour :^)")
        fmt.Println("=======================================================")
        time.Sleep(3300 * time.Second)
        fmt.Println("Waking back up")
    }
}
