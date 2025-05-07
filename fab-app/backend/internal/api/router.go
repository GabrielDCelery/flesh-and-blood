package api

import (
	"database/sql"

	"github.com/gin-gonic/gin"
)

func SetupRouter(db *sql.DB) *gin.Engine {
	router := gin.Default()
	handler := NewApiHandler(db)
	v1 := router.Group("/api/v1")
	v1.GET("/records", handler.GetRecords)
	return router
}
