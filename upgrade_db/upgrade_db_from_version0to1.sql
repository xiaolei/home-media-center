ALTER TABLE "main"."movies" ADD COLUMN "type" VARCHAR DEFAULT 'movie';
CREATE TABLE "settings" ("_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "key" VARCHAR NOT NULL  UNIQUE , "value" VARCHAR);
INSERT INTO "settings" ("key","value") VALUES ('version', '1');