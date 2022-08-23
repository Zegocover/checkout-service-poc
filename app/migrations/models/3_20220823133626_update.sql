-- upgrade --
CREATE TABLE IF NOT EXISTS "checkoutitemdb" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "type" TEXT NOT NULL,
    "amount" DECIMAL(30,2) NOT NULL,
    "description" TEXT NOT NULL,
    "external_id" UUID NOT NULL,
    "checkout_session_id_id" UUID NOT NULL REFERENCES "checkoutsessiondb" ("id") ON DELETE CASCADE
);;
CREATE TABLE IF NOT EXISTS "checkoutsessiondb" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "session_token" UUID NOT NULL UNIQUE,
    "success_url" VARCHAR(2048) NOT NULL,
    "cancel_url" VARCHAR(2048) NOT NULL
);-- downgrade --
DROP TABLE IF EXISTS "checkoutitemdb";
DROP TABLE IF EXISTS "checkoutsessiondb";
