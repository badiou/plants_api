-- Table: public.plants

-- DROP TABLE public.plants;

CREATE TABLE public.plants
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying COLLATE pg_catalog."default",
    scientific_name character varying COLLATE pg_catalog."default",
    is_poisonous boolean,
    primary_color character varying COLLATE pg_catalog."default",
    state character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT plants_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.plants
    OWNER to postgres;