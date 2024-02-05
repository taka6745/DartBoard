#ifndef DATABASE_OPERATIONS_H
#define DATABASE_OPERATIONS_H

#include <sqlite3.h>
#include <string>

// Function declarations
sqlite3* connect_db();
void read_from_db(sqlite3* db);
void write_to_db(sqlite3* db, const std::string& name, double average_301_score, double average_501_score, double average_cricket_score);

#endif // DATABASE_OPERATIONS_H
