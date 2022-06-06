CREATE SCHEMA metaland_accounts;
CREATE TABLE metaland_accounts.minecraft_account (
    id character varying(50) NOT NULL,
    user_id character varying(50) DEFAULT NULL::character varying,
    provider character varying(50),
    "display_name" character varying(50) DEFAULT NULL::character varying
);
CREATE TABLE metaland_accounts.users (
    id character varying(36) NOT NULL,
    email character varying(50) NOT NULL,
    role character varying(50),
    phone_number character varying(50),
    provider character varying(50),
    "display_name" character varying(50) DEFAULT NULL::character varying,
    "given_name" character varying(50),
    "job_title" character varying(50)
);
ALTER TABLE ONLY metaland_accounts.minecraft_account
ADD CONSTRAINT minecraft_account_pkey PRIMARY KEY (id);
ALTER TABLE ONLY metaland_accounts.users
ADD CONSTRAINT users_pkey PRIMARY KEY (id);
ALTER TABLE ONLY metaland_accounts.minecraft_account
ADD CONSTRAINT minecraft_account_user_id_fkey FOREIGN KEY (user_id) REFERENCES metaland_accounts.users(id);