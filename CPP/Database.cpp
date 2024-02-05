#include "DatabaseOperations.h"
#include <fstream>
#include <iostream>
#include <vector>


// Function declarations
sqlite3* connect_db();
void read_from_db(sqlite3* db);
void write_to_db(sqlite3* db, const std::string& name, double average_301_score, double average_501_score, double average_cricket_score);

// Connect to the database and ensure the 'players' table exists
sqlite3* connect_db() {
    sqlite3* db;
    int rc = sqlite3_open("your_database.db", &db);
    if (rc != SQLITE_OK) {
        std::cerr << "Cannot open database: " << sqlite3_errmsg(db) << std::endl;
        return nullptr;
    }

    // Attempt to read and execute SQL from the file directly
    std::ifstream file("../database_init.sql");
    if (file.is_open()) {
        std::string sql((std::istreambuf_iterator<char>(file)),
                         std::istreambuf_iterator<char>());
        file.close();

        char* errMsg = nullptr;
        rc = sqlite3_exec(db, sql.c_str(), nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            std::cerr << "SQL error: " << errMsg << std::endl;
            sqlite3_free(errMsg);
            sqlite3_close(db);
            return nullptr;
        }
    } else {
        std::cerr << "Failed to open database_init.sql" << std::endl;
        sqlite3_close(db);
        return nullptr;
    }

    return db;
}

// Example function to read entries from the database
void read_from_db(sqlite3* db) {
    const char* query = "SELECT * FROM players";
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(db, query, -1, &stmt, nullptr);

    if (rc != SQLITE_OK) {
        std::cerr << "Preparation failed: " << sqlite3_errmsg(db) << std::endl;
        return;
    }

    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
        int id = sqlite3_column_int(stmt, 0);
        const char* name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
        double average_301_score = sqlite3_column_double(stmt, 2);
        double average_501_score = sqlite3_column_double(stmt, 3);
        double average_cricket_score = sqlite3_column_double(stmt, 4);

        std::cout << "ID: " << id << ", Name: " << name 
                  << ", Average 301 Score: " << average_301_score 
                  << ", Average 501 Score: " << average_501_score 
                  << ", Average Cricket Score: " << average_cricket_score << std::endl;
    }

    sqlite3_finalize(stmt);
}

// Example function to insert a new player into the database
void write_to_db(sqlite3* db, const std::string& name, double average_301_score, double average_501_score, double average_cricket_score) {
    const char* query = "INSERT INTO players (name, average_301_score, average_501_score, average_cricket_score) VALUES (?, ?, ?, ?)";
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(db, query, -1, &stmt, nullptr);

    if (rc != SQLITE_OK) {
        std::cerr << "Preparation failed: " << sqlite3_errmsg(db) << std::endl;
        return;
    }

    // Bind the values to the prepared statement
    sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_double(stmt, 2, average_301_score);
    sqlite3_bind_double(stmt, 3, average_501_score);
    sqlite3_bind_double(stmt, 4, average_cricket_score);

    rc = sqlite3_step(stmt);
    if (rc != SQLITE_DONE) {
        std::cerr << "Insertion failed: " << sqlite3_errmsg(db) << std::endl;
    } else {
        std::cout << "A new player has been added successfully." << std::endl;
    }

    sqlite3_finalize(stmt);
}

int main() {
    // Example usage
    sqlite3* db = connect_db();
    if (db != nullptr) {
        // Write a new player to the database
        write_to_db(db, "John Doe", 50.5, 60.5, 70.5);

        // Read all players from the database
        read_from_db(db);

        sqlite3_close(db);
    }

    return 0;
}
