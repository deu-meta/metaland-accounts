CREATE SCHEMA metaland_accounts;
CREATE TABLE metaland_accounts.users (
    id character varying(36) NOT NULL PRIMARY KEY,
    email character varying(50) NOT NULL,
    role character varying(50),
    phone_number character varying(50),
    provider character varying(50),
    "display_name" character varying(50) DEFAULT NULL::character varying,
    "given_name" character varying(50),
    "job_title" character varying(50),
    "date_joined" timestamp NOT NULL DEFAULT now(),
    "last_login" timestamp NOT NULL DEFAULT now()
);
CREATE INDEX users_email_idx ON metaland_accounts.users(email);
CREATE TABLE metaland_accounts.minecraft_account (
    id character varying(50) NOT NULL PRIMARY KEY,
    user_id character varying(50) DEFAULT NULL::character varying,
    provider character varying(50),
    "display_name" character varying(50) DEFAULT NULL::character varying,
    FOREIGN KEY (user_id) REFERENCES metaland_accounts.users(id)
);