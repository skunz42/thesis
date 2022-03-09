package main

import (
    "fmt"
    "os"
    "skunz42/post-scraper/src/credentials"
    "skunz42/post-scraper/src/auth"
    "skunz42/post-scraper/src/scraper"
)

func main() {
    if len(os.Args) != 2 {
        fmt.Println("Arguments: <user credentials>")
        os.Exit(1)
    }

    config_data := credentials.MakeClient(os.Args[1])
    database_data := credentials.MakeDbClient(os.Args[1])

    fmt.Println(database_data.Db_Username)
    fmt.Println(config_data.Reddit_Username)

    auth.GetToken(config_data)

    ids, _ := scraper.GetSubPosts(config_data)
    for i := range(ids) {
        fmt.Println(ids[i])
    }
}
