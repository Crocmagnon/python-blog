import sqlite3


def main():
    writefreely = sqlite3.connect("db/writefreely.db")
    db = sqlite3.connect("db/db.sqlite3")
    writefreely_c = writefreely.cursor()
    db_c = db.cursor()
    writefreely_c.execute(
        "SELECT slug, created, updated, view_count, title, content, pinned_position FROM posts;"
    )
    for line in writefreely_c.fetchall():
        ret = db_c.execute(
            "INSERT INTO articles_article(title, content, status, published_at, created_at, updated_at, author_id, views_count, slug) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
            (
                line[4],
                line[5],
                "published",
                line[1],
                line[1],
                line[2],
                1,
                line[3],
                line[0],
            ),
        )
        if line[6] is not None:
            db_c.execute(
                "INSERT INTO articles_page(article_ptr_id) VALUES (?);",
                (ret.lastrowid,),
            )
    db.commit()


if __name__ == "__main__":
    main()
