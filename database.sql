DROP TABLE IF EXISTS movies;
CREATE TABLE "movies" ("_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "name" VARCHAR NOT NULL , "poster_url" VARCHAR, "douban_url" VARCHAR, "imdb_url" VARCHAR, "storylines" VARCHAR, "plot_keywords" VARCHAR, "official_sites" VARCHAR, "runtime" DOUBLE, "also_known_as" VARCHAR, "release_date" DATETIME, "language" INTEGER, "country" INTEGER, "ratings" DOUBLE DEFAULT 0, "director" VARCHAR, "writers" VARCHAR, "awards" VARCHAR, "url" VARCHAR NOT NULL  DEFAULT '', "file_name" VARCHAR NOT NULL  DEFAULT '', "is_active" BOOL DEFAULT true, "tags" VARCHAR, "created_date" DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE INDEX "idx_movies_also_known_as" ON "movies" ("also_known_as" ASC);
CREATE INDEX "idx_movies_name" ON "movies" ("name" ASC);
CREATE INDEX "idx_movies_plot_keywords" ON "movies" ("plot_keywords" ASC);
CREATE INDEX "idx_movies_ratings" ON "movies" ("ratings" DESC);
CREATE INDEX "idx_movies_release_date" ON "movies" ("release_date" DESC);