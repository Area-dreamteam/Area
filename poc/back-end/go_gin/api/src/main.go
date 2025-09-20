package main

import (
	"context"
	"log"

	"gin/app/routes"
	"gin/app/services"

	"github.com/gin-gonic/gin"
)

func main() {
	db, err := services.NewDatabase()
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}
	defer db.Close(context.Background())

	r := gin.Default()

	routes.ApplyRoutes(r, db)
}
