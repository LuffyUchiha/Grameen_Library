-- Table: grlib.book

-- DROP TABLE grlib.book;

CREATE TABLE grlib.book
(
    book_id integer NOT NULL DEFAULT nextval('grlib.book_book_id_seq'::regclass),
    donor_id integer,
    donate_date date,
    isbn character(13) COLLATE pg_catalog."default",
    book_name character varying(50) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE grlib.book
    OWNER to postgres;

GRANT ALL ON TABLE grlib.book TO grlib;

GRANT ALL ON TABLE grlib.book TO postgres;



-- Table: grlib.book_category

-- DROP TABLE grlib.book_category;

CREATE TABLE grlib.book_category
(
    category_id integer NOT NULL,
    category_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT book_category_pkey PRIMARY KEY (category_id)
)

TABLESPACE pg_default;

ALTER TABLE grlib.book_category
    OWNER to postgres;

GRANT ALL ON TABLE grlib.book_category TO grlib;

GRANT ALL ON TABLE grlib.book_category TO postgres;


-- Table: grlib.book_details

-- DROP TABLE grlib.book_details;

CREATE TABLE grlib.book_details
(
    book_title text COLLATE pg_catalog."default",
    author_name text COLLATE pg_catalog."default",
    publisher_name text COLLATE pg_catalog."default",
    publication_year character(4) COLLATE pg_catalog."default",
    book_language character varying(20) COLLATE pg_catalog."default",
    no_of_copies_actual integer,
    no_of_copies_current integer,
    ISBN character(13) COLLATE pg_catalog."default" NOT NULL,
    category_id integer,
    CONSTRAINT isbn PRIMARY KEY (ISBN)
)

TABLESPACE pg_default;

ALTER TABLE grlib.book_details
    OWNER to postgres;

GRANT ALL ON TABLE grlib.book_details TO grlib;

GRANT ALL ON TABLE grlib.book_details TO postgres;


-- Table: grlib.book_distribution

-- DROP TABLE grlib.book_distribution;

CREATE TABLE grlib.book_distribution
(
    village_id integer NOT NULL,
    book_id integer NOT NULL,
    issued_date date NOT NULL,
    returned_date date NOT NULL,
    quantity_issued integer NOT NULL,
    village_contact_mobile character(10) COLLATE pg_catalog."default",
    last_modified_date date,
    user_id integer NOT NULL,
    village_contact_name text COLLATE pg_catalog."default",
    CONSTRAINT book_distribution_pkey PRIMARY KEY (village_id, book_id, user_id)
)

TABLESPACE pg_default;

ALTER TABLE grlib.book_distribution
    OWNER to postgres;

GRANT ALL ON TABLE grlib.book_distribution TO grlib;

GRANT ALL ON TABLE grlib.book_distribution TO postgres;



-- Table: grlib.borrower

-- DROP TABLE grlib.borrower;

CREATE TABLE grlib.borrower
(
    borrower_id integer NOT NULL,
    book_id integer NOT NULL,
    user_id integer NOT NULL,
    borrower_mobile character varying(10) COLLATE pg_catalog."default",
    borrowed_from_date date,
    borrowed_to_date date,
    issued_date date,
    returned_date date,
    last_modified_date date,
    CONSTRAINT borrower_pkey PRIMARY KEY (borrower_id, book_id)
)

TABLESPACE pg_default;

ALTER TABLE grlib.borrower
    OWNER to postgres;

GRANT ALL ON TABLE grlib.borrower TO grlib;

GRANT ALL ON TABLE grlib.borrower TO postgres;

-- Table: grlib.borrower_profile

-- DROP TABLE grlib.borrower_profile;

CREATE TABLE grlib.borrower_profile
(
    borrower_id integer NOT NULL,
    village_id integer NOT NULL,
    borrower_first_name character varying(50) COLLATE pg_catalog."default",
    borrower_last_name character varying(50) COLLATE pg_catalog."default",
    borrower_mobile character(10) COLLATE pg_catalog."default",
    CONSTRAINT borrower_profile_pkey PRIMARY KEY (borrower_id)
)

TABLESPACE pg_default;

ALTER TABLE grlib.borrower_profile
    OWNER to postgres;

GRANT ALL ON TABLE grlib.borrower_profile TO grlib;

GRANT ALL ON TABLE grlib.borrower_profile TO postgres;


-- Table: grlib.donor

-- DROP TABLE grlib.donor;

CREATE TABLE grlib.donor
(
    donor_id integer NOT NULL,
    donor_first_name character varying(50) COLLATE pg_catalog."default",
    donor_last_name character varying(50) COLLATE pg_catalog."default",
    donor_mobile character(10) COLLATE pg_catalog."default",
    no_of_books_donated integer NOT NULL DEFAULT 0,
    donor_email character varying(50) COLLATE pg_catalog."default",
    is_pmi_member boolean,
    CONSTRAINT donor_pkey PRIMARY KEY (donor_id)
)

TABLESPACE pg_default;

ALTER TABLE grlib.donor
    OWNER to postgres;

GRANT ALL ON TABLE grlib.donor TO grlib;

GRANT ALL ON TABLE grlib.donor TO postgres;

-- Table: grlib.role

-- DROP TABLE grlib.role;

CREATE TABLE grlib.role
(
    role_id integer NOT NULL,
    role_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT role_pkey PRIMARY KEY (role_id)
)

TABLESPACE pg_default;

ALTER TABLE grlib.role
    OWNER to postgres;

GRANT ALL ON TABLE grlib.role TO grlib;

GRANT ALL ON TABLE grlib.role TO postgres;

-- Table: grlib.user

-- DROP TABLE grlib."user";

CREATE TABLE grlib."user"
(
    user_id integer NOT NULL DEFAULT nextval('grlib.user_user_id_seq'::regclass),
    user_first_name character varying(50) COLLATE pg_catalog."default",
    user_last_name character varying(50) COLLATE pg_catalog."default",
    user_mobile character(10) COLLATE pg_catalog."default",
    role_id integer NOT NULL,
    password character varying(8) COLLATE pg_catalog."default",
    CONSTRAINT user_pkey PRIMARY KEY (user_id)
)

TABLESPACE pg_default;

ALTER TABLE grlib."user"
    OWNER to postgres;

GRANT ALL ON TABLE grlib."user" TO grlib;

GRANT ALL ON TABLE grlib."user" TO postgres;


-- Table: grlib.village

-- DROP TABLE grlib.village;

CREATE TABLE grlib.village
(
    village_id integer NOT NULL,
    village_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    panchayat_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    village_address text COLLATE pg_catalog."default" NOT NULL,
    village_contact_name text COLLATE pg_catalog."default",
    village_contact_mobile character(10) COLLATE pg_catalog."default",
    Village_Contact_Email character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT village_pkey PRIMARY KEY (village_id)
)

TABLESPACE pg_default;

ALTER TABLE grlib.village
    OWNER to postgres;

GRANT ALL ON TABLE grlib.village TO grlib;

GRANT ALL ON TABLE grlib.village TO postgres;


-- SEQUENCE: grlib.book_book_id_seq

-- DROP SEQUENCE grlib.book_book_id_seq;

CREATE SEQUENCE grlib.book_book_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE grlib.book_book_id_seq
    OWNER TO postgres;

GRANT USAGE ON SEQUENCE grlib.book_book_id_seq TO grlib;

GRANT ALL ON SEQUENCE grlib.book_book_id_seq TO postgres;


-- SEQUENCE: grlib.donor_donor_id_seq

-- DROP SEQUENCE grlib.donor_donor_id_seq;

CREATE SEQUENCE grlib.donor_donor_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE grlib.donor_donor_id_seq
    OWNER TO postgres;

GRANT USAGE ON SEQUENCE grlib.donor_donor_id_seq TO grlib;

GRANT ALL ON SEQUENCE grlib.donor_donor_id_seq TO postgres;


-- SEQUENCE: grlib.user_user_id_seq

-- DROP SEQUENCE grlib.user_user_id_seq;

CREATE SEQUENCE grlib.user_user_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE grlib.user_user_id_seq
    OWNER TO postgres;

GRANT ALL ON SEQUENCE grlib.user_user_id_seq TO grlib;

GRANT ALL ON SEQUENCE grlib.user_user_id_seq TO postgres;


-- SEQUENCE: grlib.village_villager_id_seq

-- DROP SEQUENCE grlib.village_villager_id_seq;

CREATE SEQUENCE grlib.village_villager_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE grlib.village_villager_id_seq
    OWNER TO postgres;

GRANT USAGE ON SEQUENCE grlib.village_villager_id_seq TO grlib;

GRANT ALL ON SEQUENCE grlib.village_villager_id_seq TO postgres;


