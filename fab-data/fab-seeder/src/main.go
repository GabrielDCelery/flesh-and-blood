package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"

	"database/sql"
	"log"

	"example.com/m/src/textextracts"
	"github.com/golang-migrate/migrate/v4"
	_ "github.com/golang-migrate/migrate/v4/database/postgres"
	_ "github.com/golang-migrate/migrate/v4/source/file"
	_ "github.com/mattn/go-sqlite3"
)

func main() {
	fab_extracts_db_driver := os.Getenv("FAB_EXTRACTS_DB_DRIVER")
	fab_extracts_dsn := os.Getenv("FAB_EXTRACTS_DSN")
	fab_app_db_driver := os.Getenv("FAB_APP_DB_DRIVER")
	fab_app_db_dsn := os.Getenv("FAB_APP_DSN")
	fab_app_db_migrations_dir := os.Getenv("FAB_APP_DB_MIGRATIONS_DIR")

	log.Println("init migrate connection")

	m, err := migrate.New(
		fmt.Sprintf("file://%s", fab_app_db_migrations_dir),
		fab_app_db_dsn,
	)

	defer m.Close()

	if err != nil {
		log.Fatal(err)
	}

	log.Println("migrate up")

	if err := m.Up(); err != nil && err != migrate.ErrNoChange {
		log.Fatal(err)
	}

	log.Println("connect to text extracts")

	extracts_db, err := sql.Open(fab_extracts_db_driver, fab_extracts_dsn)

	if err != nil {
		log.Fatal(err)
	}

	defer extracts_db.Close()

	rows, err := extracts_db.Query("SELECT * FROM extracts")

	if err != nil {
		log.Fatal(err)
	}

	defer rows.Close()

	count := 0

	text_extract_records := []textextracts.TextExtractRecord{}

	// Iterate over results
	for rows.Next() {
		// Scan row data
		var img_name string
		var model_name string
		var card_type int
		var segment_type int
		var text string
		err = rows.Scan(&img_name, &model_name, &card_type, &segment_type, &text)
		if err != nil {
			log.Fatal(err)
		}

		text_extract_records = append(text_extract_records, textextracts.TextExtractRecord{
			ImgName:     formatCardName(img_name),
			ModelName:   model_name,
			CardType:    card_type,
			SegmentType: segment_type,
			Text:        text,
		})

		count += 1
	}

	if err = rows.Err(); err != nil {
		log.Fatal("Error during row iteration:", err)
	}

	log.Printf("Total records processed: %d\n", count)

	app_db, err := sql.Open(fab_app_db_driver, fab_app_db_dsn)

	if err != nil {
		log.Fatalln(err)
	}

	defer app_db.Close()

	if err != nil {
		log.Fatalln(err)
	}

	for _, record := range text_extract_records {
		var cardID int
		err := app_db.QueryRow(`
		INSERT INTO cards (card_name, card_type) 
		VALUES ($1, $2)
		ON CONFLICT (card_name) DO UPDATE
		SET card_name = EXCLUDED.card_name
		RETURNING card_id;
		`, record.ImgName, getCardTypeString(record.CardType)).Scan(&cardID)

		if err != nil {
			// if err == sql.ErrNoRows {
			// 	// This means the INSERT didn't happen due to ON CONFLICT DO NOTHING
			// 	continue
			// }
			// log.Printf("failed to insert record %s, reason: %s", record.ImgName, err.Error())
			continue
		}

		_, err = app_db.Exec(`
		INSERT INTO card_segments (card_id, segment_type, text)
		VALUES ($1, $2, $3)
		ON CONFLICT (card_id, segment_type) DO UPDATE
		SET text = EXCLUDED.text;
		`, cardID, getSegmentTypeString(record.SegmentType), record.Text)

		if err != nil {
			log.Fatalln(err)
		}
	}

	_, err = app_db.Exec(`REFRESH MATERIALIZED VIEW card_details;`)

	if err != nil {
		log.Fatalln(err)
	}
}

func getCardTypeString(cardType int) string {
	cardTypes := map[int]string{
		0: "hero",
		1: "equipment",
		2: "weapon",
		3: "action",
		4: "attack_reaction",
		5: "defense_reaction",
		6: "instant",
	}
	return cardTypes[cardType]
}

func getSegmentTypeString(segmentType int) string {
	segmentTypes := map[int]string{
		0: "type",
		1: "title",
		2: "long_title",
		3: "pitch",
		4: "cost",
		5: "attack",
		6: "defense",
		7: "textbox",
	}
	return segmentTypes[segmentType]
}

func formatCardName(imgName string) string {
	// Remove .png extension
	name := strings.TrimSuffix(imgName, ".png")
	name = strings.ReplaceAll(name, "-", "")

	// Split by underscore
	parts := strings.Split(name, "_")
	if len(parts) != 2 {
		return name // Return original if not in expected format
	}

	// Convert number to integer and format with leading zeros
	num, err := strconv.Atoi(parts[1])
	if err != nil {
		return name // Return original if number conversion fails
	}

	// Combine prefix with zero-padded number
	return fmt.Sprintf("%s%03d", parts[0], num)
}
