package database

import (
	"database/sql"
	"fmt"
	"time"

	_ "github.com/lib/pq" // PostgreSQL driver
)

type DBConfig struct {
	Dsn                      string
	MaxOpenConns             int
	MaxIdleConns             int
	ConnMaxLifetimeInMinutes int
}

func InitDB(dbConfig DBConfig) (*sql.DB, error) {
	db, err := sql.Open("postgres", dbConfig.Dsn)
	if err != nil {
		return nil, fmt.Errorf("error opening fab-search database: %w", err)
	}
	db.SetMaxOpenConns(dbConfig.MaxOpenConns)
	db.SetMaxIdleConns(dbConfig.MaxIdleConns)
	db.SetConnMaxLifetime(time.Minute * time.Duration(dbConfig.ConnMaxLifetimeInMinutes))
	if err = db.Ping(); err != nil {
		return nil, fmt.Errorf("error connecting to database: %w", err)
	}
	return db, nil
}
