package credentials

import (
    "net/http"
    "time"
    "os"
    "bufio"
)

const file_line_nums = 9
const reddit_lines = 5
const db_lines = 4

// FORMAT
// Line 0: Reddit Client ID
// Line 1: Reddit Client Secret
// Line 2: Reddit User Agent
// Line 3: Reddit Username
// Line 4: Reddit Password
// Line 5: Database IP
// Line 6: Database Username
// Line 7: Database Password
// Line 8: Databse Name

func MakeClient(fn string) *Client {
    c := &Client {
        Http_Client: &http.Client{ Timeout: time.Second * 10, },
    }

    file, _ := os.Open(fn)

    defer file.Close()

    scanner := bufio.NewScanner(file)
    i := 0

    for scanner.Scan() {
        if i >= reddit_lines {
            break
        }

        if i%file_line_nums == 0 {
            setClientId(scanner.Text(), c)
        } else if i%file_line_nums == 1 {
            setClientSecret(scanner.Text(), c)
        } else if i%file_line_nums == 2 {
            setUserAgent(scanner.Text(), c)
        } else if i%file_line_nums == 3 {
            setUsername(scanner.Text(), c)
        } else if i%file_line_nums == 4 {
            setPassword(scanner.Text(), c)
        } else {
            break
        }

        i += 1
    }

    return c
}

func MakeDbClient(fn string) *DbClient {
    c := &DbClient {
        Port: 5432,
    }

    file, _ := os.Open(fn)

    defer file.Close()

    scanner := bufio.NewScanner(file)
    i := 0

    for scanner.Scan() {
        if i%file_line_nums == 5 {
            setDbHost(scanner.Text(), c)
        } else if i%file_line_nums == 6 {
            setDbUsername(scanner.Text(), c)
        } else if i%file_line_nums == 7 {
            setDbPassword(scanner.Text(), c)
        } else if i%file_line_nums == 8 {
            setDbName(scanner.Text(), c)
        } else if i >= file_line_nums {
            break
        }

        i += 1
    }

    return c
}
