-- upgrade --
CREATE TABLE IF NOT EXISTS "testmodel2" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL
);
-- downgrade --
DROP TABLE IF EXISTS "testmodel2";
