package routes

import (
	"net/http"

	"gin/app/services"

	"github.com/gin-gonic/gin"
)

func ApplyRoutes(r *gin.Engine, db *services.Database) {
	api := r.Group("/api/v1")
	{
		users := api.Group("/users")
		{
			users.POST("", db.CreateUserHandler)
			users.GET("", db.GetAllUsersHandler)
			users.GET("/:id", db.GetUserHandler)
			users.PUT("/:id", db.UpdateUserHandler)
			users.DELETE("/:id", db.DeleteUserHandler)
		}
	}

	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status":   "healthy",
			"database": "connected",
		})
	})
}
