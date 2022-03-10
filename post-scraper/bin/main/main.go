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

    config_data := credentials.MakeClient(os.Args[1])
    database_data := credentials.MakeDbClient(os.Args[1])

    auth.GetToken(config_data)

    ids, blobs := scraper.GetSubPosts(config_data)

    get_ping := database.PingDB(database_data)
    if get_ping {
        database.WriteIds(database_data, ids)
        database.WriteBlobs(database_data, blobs)
    } else {
        fmt.Println("Could not ping database")
    }
}
