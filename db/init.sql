CREATE SCHEMA metaland_accounts;

CREATE TABLE metaland_accounts.minecraft_account (
    id character varying(50) NOT NULL,
    user_mail character varying(50) DEFAULT NULL::character varying,
    provider character varying(50),
    "displayName" character varying(50) DEFAULT NULL::character varying
);

CREATE TABLE metaland_accounts.users (
    mail character varying(50) NOT NULL,
    role character varying(50),
    phone character varying(50),
    provider character varying(50),
    "displayName" character varying(50) DEFAULT NULL::character varying,
    "givenName" character varying(50),
    "jobTitle" character varying(50)
);


ALTER TABLE ONLY metaland_accounts.minecraft_account
    ADD CONSTRAINT minecraft_account_pkey PRIMARY KEY (id);


ALTER TABLE ONLY metaland_accounts.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (mail);


ALTER TABLE ONLY metaland_accounts.minecraft_account
    ADD CONSTRAINT minecraft_account_user_email_fkey FOREIGN KEY (user_mail) REFERENCES metaland_accounts.users(mail);



