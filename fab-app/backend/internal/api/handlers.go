package api

import (
	"database/sql"

	"github.com/gin-gonic/gin"
)

type Record struct{}

type ApiHandler struct {
	db *sql.DB
}

func NewApiHandler(db *sql.DB) *ApiHandler {
	return &ApiHandler{
		db: db,
	}
}

func (h *ApiHandler) GetRecords(c *gin.Context) {
	_, err := h.db.Exec("SELECT 1")
	if err != nil {
		c.JSON(500, gin.H{"error": "failed to get records"})
		return
	}
	c.JSON(200, Record{})
}
