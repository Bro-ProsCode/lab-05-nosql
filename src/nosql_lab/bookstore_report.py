#!/usr/bin/env python3
"""Print a report of books for a list of authors from the bookstore database."""

import logging
import os

import pymongo
from pymongo.server_api import ServerApi

# Credentials come from environment variables
MONGODB_ATLAS_URL = os.environ.get("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.environ.get("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.environ.get("MONGODB_ATLAS_PWD")

# The Author IDs
AUTHOR_IDS = ["author_002", "author_003", "author_004"]

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def print_author_report(authors, books, author_ids):
    """Print the author count, then each author with their linked books.

    Args:
        authors: PyMongo collection of author documents.
        books: PyMongo collection of book documents.
        author_ids: List of author _id values to report on.
    """
    # Count how many of the requested authors exist in the collection
    total = authors.count_documents({"_id": {"$in": author_ids}})
    print(f"Authors: {total}\n")

    for author_id in author_ids:
        author = authors.find_one({"_id": author_id})
        if author is None:
            # An id in my list has no matching author document
            logging.warning("No author found with _id %s", author_id)
            continue

        print(author["name"])
        # Join: find every book whose author_ids list contains this author's _id
        for book in books.find({"author_ids": author["_id"]}):
            print(f"  {book['title']} ({book['published_year']})")
        print()


def main():
    """Connect to MongoDB Atlas and print the bookstore report."""
    client = None
    try:
        # Connect with the URL plus username and password from the environment
        client = pymongo.MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            server_api=ServerApi("1"),
        )
        client.admin.command("ping")  # Fail fast if the connection is bad
        logging.info("Connected to MongoDB Atlas")

        # Select the database and both collections
        db = client["bookstore"]
        print_author_report(db["authors"], db["books"], AUTHOR_IDS)
    except Exception as err:
        logging.error("Could not complete the report: %s", err)
    finally:
        # Always close the client, even after an error
        if client is not None:
            client.close()
            logging.info("Connection closed")

# Only run the file if directly being exected and not being imported
if __name__ == "__main__":
    main()
