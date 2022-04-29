package credentials

import "fmt"

type DbClient struct {
    Port int
    Host string
    Db_Username string
    db_password string
    Db_Name string
}

func setDbPort(port int, c *DbClient) {
    c.Port = port
}

func setDbHost(host string, c *DbClient) {
    c.Host = host
}

func setDbUsername(username string, c *DbClient) {
    c.Db_Username = username
}

func setDbPassword(password string, c *DbClient) {
    c.db_password = password
}

func setDbName(dbname string, c *DbClient) {
    c.Db_Name = dbname
}

func ConstructDbConnString(c *DbClient) (string) {
    psqlInfo := fmt.Sprintf("host=%s port=%d user=%s "+
        "password=%s dbname=%s sslmode=disable",
        c.Host, c.Port, c.Db_Username, c.db_password, c.Db_Name)

    return psqlInfo
}
