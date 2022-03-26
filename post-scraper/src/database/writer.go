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
    psql_info := credentials.ConstructDbConnString(database_data)
    db, err := sql.Open("postgres", psql_info)
    if err != nil {
        fmt.Println("Error on open")
        return
    }

    defer db.Close()

    sql_statement := `
    INSERT INTO users (username, fullname)
    VALUES ($1, $2)
    ON CONFLICT (fullname) DO NOTHING`

    for i := range(authors) {
        _, err = db.Exec(sql_statement, authors[i].Username, authors[i].Fullname)
        if err != nil {
            fmt.Println("Error writing authors to db: ")
            fmt.Println(err)
            return
        }
    }
}

func WritePosts(database_data *credentials.DbClient, posts []Post) {
    psql_info := credentials.ConstructDbConnString(database_data)
    db, err := sql.Open("postgres", psql_info)
    if err != nil {
        fmt.Println("Error on open")
        return
    }

    defer db.Close()

    sql_statement := `
    INSERT INTO posts (id, data)
    VALUES ($1, $2)
    ON CONFLICT (id) DO NOTHING`

    for i := range(posts) {
        _, err = db.Exec(sql_statement, posts[i].Id, posts[i].Blob)
        if err != nil {
            fmt.Println("Error writing posts to db: ")
            fmt.Println(err)
            return
        }
    }
}
