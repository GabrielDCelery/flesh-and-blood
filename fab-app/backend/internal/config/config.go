package config

import (
	"github.com/spf13/viper"
)

type AppConfig struct {
	DBDsn           string
	AppListenerPort int
}

func InitConfig() (AppConfig, error) {
	// Set up configuration
	// viper.SetConfigName("config")
	// viper.SetConfigType("yaml")
	// viper.AddConfigPath(".")
	viper.AutomaticEnv()

	// Set defaults
	viper.SetDefault("SEARCH_DB_DSN", "")
	viper.SetDefault("APP_LISTENER_PORT", 8080)

	viper.BindEnv("SEARCH_DB_DSN")
	viper.BindEnv("APP_LISTENER_PORT")
	// viper.SetDefault("database.port", 5432)
	// viper.SetDefault("database.user", "postgres")
	// viper.SetDefault("database.password", "")
	// viper.SetDefault("database.name", "flesh_and_blood")
	// viper.SetDefault("server.port", "8080")

	// if err := viper.ReadInConfig(); err != nil {
	// 	if _, ok := err.(viper.ConfigFileNotFoundError); !ok {
	// 		return AppConfig{}, fmt.Errorf("error reading config file: %w", err)
	// 	}
	// 	log.Println("no config file found, using defaults")
	// }
	return AppConfig{
		DBDsn:           viper.GetString("SEARCH_DB_DSN"),
		AppListenerPort: viper.GetInt("APP_LISTENER_PORT"),
	}, nil
}
