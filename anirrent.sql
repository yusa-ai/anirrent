-- Adminer 4.8.1 PostgreSQL 16.0 (Debian 16.0-1.pgdg120+1) dump

\connect "anirrent";

DROP TABLE IF EXISTS "downloads";
CREATE TABLE "public"."downloads" (
    "download_uuid" uuid DEFAULT uuid_generate_v4() NOT NULL,
    "progress" numeric DEFAULT '0' NOT NULL,
    "status" status DEFAULT IN_PROGRESS NOT NULL,
    "started_at" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "finished_at" timestamp,
    "magnet_url" character varying NOT NULL,
    "entry_name" character varying(255) NOT NULL,
    "season" smallint,
    "episode" smallint,
    "file_name" character varying NOT NULL,
    CONSTRAINT "downloads_download_uuid" PRIMARY KEY ("download_uuid")
) WITH (oids = false);


DELIMITER ;;

CREATE TRIGGER "check_download_progress" AFTER UPDATE ON "public"."downloads" FOR EACH ROW EXECUTE FUNCTION create_upload_row();;

CREATE TRIGGER "check_complete" BEFORE UPDATE OF ON "public"."downloads" FOR EACH ROW EXECUTE FUNCTION set_download_complete();;

DELIMITER ;

DROP TABLE IF EXISTS "entries";
CREATE TABLE "public"."entries" (
    "entry_uuid" uuid DEFAULT uuid_generate_v4() NOT NULL,
    "entry_name" character varying NOT NULL,
    "entry_type" entry_type NOT NULL,
    CONSTRAINT "entries_entry_name" UNIQUE ("entry_name"),
    CONSTRAINT "entries_entry_uuid" PRIMARY KEY ("entry_uuid")
) WITH (oids = false);


DROP TABLE IF EXISTS "uploads";
CREATE TABLE "public"."uploads" (
    "download_uuid" uuid NOT NULL,
    "status" status DEFAULT IN_PROGRESS NOT NULL,
    "started_at" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "finished_at" timestamp,
    CONSTRAINT "uploads_download_uuid" PRIMARY KEY ("download_uuid")
) WITH (oids = false);


DELIMITER ;;

CREATE TRIGGER "check_complete" BEFORE UPDATE OF ON "public"."uploads" FOR EACH ROW EXECUTE FUNCTION set_upload_complete();;

DELIMITER ;

ALTER TABLE ONLY "public"."uploads" ADD CONSTRAINT "uploads_download_uuid_fkey" FOREIGN KEY (download_uuid) REFERENCES downloads(download_uuid) ON UPDATE RESTRICT ON DELETE CASCADE NOT DEFERRABLE;

-- 2023-10-05 22:14:56.211559+02
