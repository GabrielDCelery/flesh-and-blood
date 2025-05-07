package database

import (
	"database/sql"
	"fmt"

	_ "github.com/lib/pq" // PostgreSQL driver
)

type DBConfig struct {
	Dsn string
}

func InitDB(dbConfig DBConfig) (*sql.DB, error) {
	db, err := sql.Open("postgres", dbConfig.Dsn)
	if err != nil {
		return nil, fmt.Errorf("error opening fab-search database: %w", err)
	}
	if err = db.Ping(); err != nil {
		return nil, fmt.Errorf("error connecting to database: %w", err)
	}
	return db, nil
}
