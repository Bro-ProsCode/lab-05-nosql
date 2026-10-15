// Step 2: use bookstore (the 'use' command only works at the mongosh prompt)
db = db.getSiblingDB("bookstore")

// Step 3: load authors.json (drop first so reruns don't duplicate)
db.authors.drop()
var authorsData = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(authorsData)

// Step 4: load books.json
db.books.drop()
var booksData = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(booksData)

// Step 5: list authors and books
printjson(db.authors.find().toArray())
printjson(db.books.find().toArray())

// Step 6: insert two new books
db.books.insertMany([
  { title: "The Hobbit", published_year: 1937, author_ids: ["author_004"] },
  { title: "The Long Earth", published_year: 2012, author_ids: ["author_003", "author_005"] }
])

// Step 7: add missing authors
db.authors.insertMany([
  {
    _id: "author_004",
    name: "J.R.R. Tolkien",
    nationality: "British",
    bio: {
      short: "English author of The Hobbit and The Lord of the Rings.",
      long: "J.R.R. Tolkien was an English writer and philologist who created Middle-earth. His best known works are The Hobbit and The Lord of the Rings."
    }
  },
  {
    _id: "author_005",
    name: "Stephen Baxter",
    nationality: "British",
    bio: {
      short: "British science fiction author.",
      long: "Stephen Baxter is a British science fiction writer known for hard SF. He co-wrote The Long Earth series with Terry Pratchett."
    }
  }
])

// Step 8: filter books by a list of authors (one loaded, one added)
printjson(db.books.find({ author_ids: { $in: ["author_002", "author_004"] } }).toArray())
