package database

import (
    "database/sql"
//    "fmt"
    "log"
    "context"
    _ "github.com/lib/pq"
    "github.com/cockroachdb/cockroach-go/crdb"
    "skunz42/post-scraper/src/credentials"
)

func updateMRP(tx *sql.Tx, sql_statement string, id string, city string) error {
    if _, err := tx.Exec(sql_statement, id, city); err != nil {
        return err
    }
    return nil
}

func UpdateMRP(database_data *credentials.DbClient, post_id string, city string) error {
    psql_info := credentials.ConstructDbConnString(database_data)
    db, err := sql.Open("postgres", psql_info)
    if err != nil {
        log.Println("Error on open (UpdateMRP)")
        return err
    }

    err = db.Ping()
    if err != nil {
        log.Println("Error on ping (UpdateMRP)")
        return err
    }

    defer db.Close()

    sql_statement := `UPDATE last_scraped SET scraped = $1 where subreddit=$2`

    err = crdb.ExecuteTx(context.Background(), db, nil, func(tx *sql.Tx) error {
        return updateMRP(tx, sql_statement, post_id, city)
    })

    if err != nil {
        log.Println("Error updating posts to db: ")
        log.Println(err)
        return err
    }

    return nil
}

func getLatestPost(sql_statement string, db *sql.DB, city string) (string, error) {
    rows, err := db.Query(sql_statement, city)

    if err != nil {
        log.Println("getLatestPost: Error on query")
        return "EMPTY", err
    }

    defer rows.Close()

    var pid string

    for rows.Next() {
        err = rows.Scan(&pid)
        if err != nil {
            log.Println("getLatestPost: Error on row scan")
            return "EMPTY", err
        }
    }
    err = rows.Err()
    if err != nil {
        x := "EMPTY"
        log.Println("getLatestPost: Error on rows")
        return x, err
    }
    log.Println("PREVIOUS PID: " + pid)
    return pid, err
}

func GetLatestPost(database_data *credentials.DbClient, subreddit string) (string, error) {
    psql_info := credentials.ConstructDbConnString(database_data)
    db, err := sql.Open("postgres", psql_info)
    if err != nil {
        log.Println("Error on open")
        return "", err
    }

    err = db.Ping()
    if err != nil {
        log.Println("Error on ping")
        return "", err
    }

    defer db.Close()

    sql_statement := `SELECT scraped FROM last_scraped where subreddit = $1`

    return getLatestPost(sql_statement, db, subreddit)
}
