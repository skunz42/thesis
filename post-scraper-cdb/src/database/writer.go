package database

import (
    "database/sql"
    "fmt"
    "context"
    _ "github.com/lib/pq"
    "github.com/cockroachdb/cockroach-go/crdb"
    "skunz42/post-scraper/src/credentials"
)

// Ping the database before attempting to make a connection
// to void any lost data and recover from failure
func PingDB(database_data *credentials.DbClient) (*sql.DB) {
    psql_info := credentials.ConstructDbConnString(database_data)
    db, err := sql.Open("postgres", psql_info)
    if err != nil {
        fmt.Println("Error on open")
        return nil
    }

    err = db.Ping()
    if err != nil {
        fmt.Println("Error on ping")
        return nil
    }
    return db
}

func writeAuthors(tx *sql.Tx, sql_statement string, username string, fullname string) error {
    if _, err := tx.Exec(sql_statement, username, fullname); err != nil {
        return err
    }
    return nil
}

func WriteAuthors(database_data *credentials.DbClient, authors []Author, db *sql.DB) {
    sql_statement := `
    INSERT INTO users (username, fullname)
    VALUES ($1, $2)
    ON CONFLICT (fullname) DO NOTHING`

    for i := range(authors) {
        err := crdb.ExecuteTx(context.Background(), db, nil, func(tx *sql.Tx) error {
            return writeAuthors(tx, sql_statement, authors[i].Username, authors[i].Fullname)
        })

        if err != nil {
            fmt.Println("Error writing authors to db: ")
            fmt.Println(err)
            return
        }
    }
}

func writePosts(tx *sql.Tx, sql_statement string, id string, blob []byte) error {
    if _, err := tx.Exec(sql_statement, id, blob); err != nil {
        return err
    }
    return nil
}

func WritePosts(database_data *credentials.DbClient, posts []Post, db *sql.DB) {
    defer db.Close()

    sql_statement := `
    INSERT INTO posts (id, data)
    VALUES ($1, $2)
    ON CONFLICT (id) DO NOTHING`

    for i := range(posts) {
        err := crdb.ExecuteTx(context.Background(), db, nil, func(tx *sql.Tx) error {
            return writePosts(tx, sql_statement, posts[i].Id, posts[i].Blob)
        })

        if err != nil {
            fmt.Println("Error writing posts to db: ")
            fmt.Println(err)
            return
        }
    }
}
