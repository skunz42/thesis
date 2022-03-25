package database

import (
    "database/sql"
    "fmt"
    _ "github.com/lib/pq"
    "skunz42/post-scraper/src/credentials"
)

// Ping the database before attempting to make a connection
// to void any lost data and recover from failure
func PingDB(database_data *credentials.DbClient) (bool) {
    psql_info := credentials.ConstructDbConnString(database_data)
    db, err := sql.Open("postgres", psql_info)
    if err != nil {
        fmt.Println("Error on open")
        return false
    }

    defer db.Close()

    err = db.Ping()
    if err != nil {
        fmt.Println("Error on ping")
        return false
    }
    return true
}

func WriteAuthors(database_data *credentials.DbClient, authors []Author) {

}

func WritePosts(database_data *credentials.DbClient, posts []Post) {

}
