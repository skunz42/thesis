package database

type Post struct {
    Id string // this will change to uuid when ported to cockroach
    Blob []byte
}

type Author struct {
    Username string
    Fullname string
}
