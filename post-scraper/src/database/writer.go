package database

import (
    "database/sql"
    "fmt"
    _ "github.com/lib/pq"
    "skunz42/post-scraper/src/credentials"
)

func PingDB(database_data *credentials.DbClient) (bool) {
    psql_info := credentials.ConstructDbConnString(database_data)
    fmt.Println(psql_info)
    db, err := sql.Open("postgres", psql_info)
    if err != nil {
        fmt.Println("Error on open")
        return false
    }

    defer db.Close()

    err = db.Ping()
    if err != nil {
        fmt.Println("Error on ping")
        panic(err)
        return false
    }
    return true
}

func WriteIds(database_data *credentials.DbClient, ids []string) {

}

func WriteBlobs(database_data *credentials.DbClient, blobs [][]byte) {

}
