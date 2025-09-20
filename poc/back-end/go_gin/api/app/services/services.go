// Package services
package services

import (
	"context"
	"fmt"
	"gin/app/models"
	"gin/app/utils"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

type Database struct {
	Driver neo4j.DriverWithContext
}

func NewDatabase() (*Database, error) {
	uri := utils.GetEnv("NEO4J_URI", "bolt://localhost:7687")
	username := utils.GetEnv("NEO4J_USERNAME", "neo4j")
	password := utils.GetEnv("NEO4J_PASSWORD", "1234")

	driver, err := neo4j.NewDriverWithContext(uri, neo4j.BasicAuth(username, password, ""))
	if err != nil {
		return nil, fmt.Errorf("failed to create driver: %w", err)
	}

	ctx := context.Background()
	err = driver.VerifyConnectivity(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to verify connectivity: %w", err)
	}

	return &Database{Driver: driver}, nil
}

func (db *Database) Close(ctx context.Context) error {
	return db.Driver.Close(ctx)
}

func (db *Database) createUser(ctx context.Context, user models.User) (*models.User, error) {
	session := db.Driver.NewSession(ctx, neo4j.SessionConfig{DatabaseName: "neo4j"})
	defer session.Close(ctx)

	result, err := session.ExecuteWrite(ctx, func(tx neo4j.ManagedTransaction) (any, error) {
		query := `
			CREATE (u:User {name: $name, email: $email, age: $age})
			RETURN u, ID(u) as id
		`
		params := map[string]any{
			"name":  user.Name,
			"email": user.Email,
			"age":   user.Age,
		}

		result, err := tx.Run(ctx, query, params)
		if err != nil {
			return nil, err
		}

		record, err := result.Single(ctx)
		if err != nil {
			return nil, err
		}

		id, _ := record.Get("id")
		userNode, _ := record.Get("u")

		userProps := userNode.(neo4j.Node).Props

		return &models.User{
			ID:    id.(int64),
			Name:  userProps["name"].(string),
			Email: userProps["email"].(string),
			Age:   int(userProps["age"].(int64)),
		}, nil
	})
	if err != nil {
		return nil, err
	}

	return result.(*models.User), nil
}

func (db *Database) GetUser(ctx context.Context, id int64) (*models.User, error) {
	session := db.Driver.NewSession(ctx, neo4j.SessionConfig{DatabaseName: "neo4j"})
	defer session.Close(ctx)

	result, err := session.ExecuteRead(ctx, func(tx neo4j.ManagedTransaction) (any, error) {
		query := `MATCH (u:User) WHERE ID(u) = $id RETURN u, ID(u) as id`
		params := map[string]any{"id": id}

		result, err := tx.Run(ctx, query, params)
		if err != nil {
			return nil, err
		}

		if result.Next(ctx) {
			record := result.Record()
			nodeID, _ := record.Get("id")
			userNode, _ := record.Get("u")

			userProps := userNode.(neo4j.Node).Props

			return &models.User{
				ID:    nodeID.(int64),
				Name:  userProps["name"].(string),
				Email: userProps["email"].(string),
				Age:   int(userProps["age"].(int64)),
			}, nil
		}

		return nil, fmt.Errorf("user not found")
	})
	if err != nil {
		return nil, err
	}

	return result.(*models.User), nil
}

func (db *Database) GetAllUsers(ctx context.Context) ([]models.User, error) {
	session := db.Driver.NewSession(ctx, neo4j.SessionConfig{DatabaseName: "neo4j"})
	defer session.Close(ctx)

	result, err := session.ExecuteRead(ctx, func(tx neo4j.ManagedTransaction) (any, error) {
		query := `MATCH (u:User) RETURN u, ID(u) as id ORDER BY u.name`

		result, err := tx.Run(ctx, query, nil)
		if err != nil {
			return nil, err
		}

		var users []models.User
		for result.Next(ctx) {
			record := result.Record()
			nodeID, _ := record.Get("id")
			userNode, _ := record.Get("u")

			userProps := userNode.(neo4j.Node).Props

			user := models.User{
				ID:    nodeID.(int64),
				Name:  userProps["name"].(string),
				Email: userProps["email"].(string),
				Age:   int(userProps["age"].(int64)),
			}
			users = append(users, user)
		}

		return users, nil
	})
	if err != nil {
		return nil, err
	}

	return result.([]models.User), nil
}

func (db *Database) UpdateUser(ctx context.Context, id int64, user models.User) (*models.User, error) {
	session := db.Driver.NewSession(ctx, neo4j.SessionConfig{DatabaseName: "neo4j"})
	defer session.Close(ctx)

	result, err := session.ExecuteWrite(ctx, func(tx neo4j.ManagedTransaction) (any, error) {
		query := `
			MATCH (u:User) WHERE ID(u) = $id
			SET u.name = $name, u.email = $email, u.age = $age
			RETURN u, ID(u) as id
		`
		params := map[string]any{
			"id":    id,
			"name":  user.Name,
			"email": user.Email,
			"age":   user.Age,
		}

		result, err := tx.Run(ctx, query, params)
		if err != nil {
			return nil, err
		}

		if result.Next(ctx) {
			record := result.Record()
			nodeID, _ := record.Get("id")
			userNode, _ := record.Get("u")

			userProps := userNode.(neo4j.Node).Props

			return &models.User{
				ID:    nodeID.(int64),
				Name:  userProps["name"].(string),
				Email: userProps["email"].(string),
				Age:   int(userProps["age"].(int64)),
			}, nil
		}

		return nil, fmt.Errorf("user not found")
	})
	if err != nil {
		return nil, err
	}

	return result.(*models.User), nil
}

func (db *Database) DeleteUser(ctx context.Context, id int64) error {
	session := db.Driver.NewSession(ctx, neo4j.SessionConfig{DatabaseName: "neo4j"})
	defer session.Close(ctx)

	_, err := session.ExecuteWrite(ctx, func(tx neo4j.ManagedTransaction) (any, error) {
		query := `MATCH (u:User) WHERE ID(u) = $id DELETE u`
		params := map[string]any{"id": id}

		result, err := tx.Run(ctx, query, params)
		if err != nil {
			return nil, err
		}

		summary, err := result.Consume(ctx)
		if err != nil {
			return nil, err
		}

		if summary.Counters().NodesDeleted() == 0 {
			return nil, fmt.Errorf("user not found")
		}

		return nil, nil
	})

	return err
}

func (db *Database) CreateUserHandler(c *gin.Context) {
	var user models.User
	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	createdUser, err := db.createUser(c.Request.Context(), user)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, createdUser)
}

func (db *Database) GetUserHandler(c *gin.Context) {
	idStr := c.Param("id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user ID"})
		return
	}

	user, err := db.GetUser(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, user)
}

func (db *Database) GetAllUsersHandler(c *gin.Context) {
	users, err := db.GetAllUsers(c.Request.Context())
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, users)
}

func (db *Database) UpdateUserHandler(c *gin.Context) {
	idStr := c.Param("id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user ID"})
		return
	}

	var user models.User
	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	updatedUser, err := db.UpdateUser(c.Request.Context(), id, user)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, updatedUser)
}

func (db *Database) DeleteUserHandler(c *gin.Context) {
	idStr := c.Param("id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user ID"})
		return
	}

	err = db.DeleteUser(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "User deleted successfully"})
}
