package main

import (
	"flesh-and-blood/internal/api"
	"flesh-and-blood/internal/config"
	"flesh-and-blood/internal/database"
	"fmt"
	"log"
)

func main() {
	appConfig, err := config.InitConfig()
	if err != nil {
		log.Fatalf("failed to initialize config: %v", err)
	}
	db, err := database.InitDB(database.DBConfig{
		Dsn:                      appConfig.DBDsn,
		MaxOpenConns:             25,
		MaxIdleConns:             5,
		ConnMaxLifetimeInMinutes: 5,
	})
	if err != nil {
		log.Fatalf("failed to initialize database: %v", err)
	}
	defer db.Close()
	router := api.SetupRouter(db)
	err = router.Run(fmt.Sprintf(":%d", appConfig.AppListenerPort))
	if err != nil {
		log.Fatalf("failed to start server: %v", err)
	}
}
