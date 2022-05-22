CREATE SCHEMA metaland_accounts;

CREATE TABLE metaland_accounts.minecraft_account (
    id character varying(50) NOT NULL,
    user_email character varying(50) DEFAULT NULL::character varying,
    provider character varying(50),
    "display_name" character varying(50) DEFAULT NULL::character varying
);

CREATE TABLE metaland_accounts.users (
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
    ADD CONSTRAINT users_pkey PRIMARY KEY (email);


ALTER TABLE ONLY metaland_accounts.minecraft_account
    ADD CONSTRAINT minecraft_account_user_eemail_fkey FOREIGN KEY (user_email) REFERENCES metaland_accounts.users(email);



