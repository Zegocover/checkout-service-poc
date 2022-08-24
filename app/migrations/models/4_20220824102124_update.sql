-- upgrade --
ALTER TABLE "checkoutsessiondb" ADD "user_type" VARCHAR(32);
-- downgrade --
ALTER TABLE "checkoutsessiondb" DROP COLUMN "user_type";
