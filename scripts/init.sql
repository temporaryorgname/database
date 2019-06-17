DROP TABLE public.users CASCADE;
DROP TABLE public.food CASCADE;
DROP TABLE public.food_photos CASCADE;
DROP TABLE public.body CASCADE;

CREATE TABLE public.users (
	id serial PRIMARY KEY,
	name varchar(255),
	email varchar(255) NOT NULL UNIQUE,
	password bytea NOT NULL
);

CREATE TABLE public.food
(
	id serial PRIMARY KEY,
	user_id integer REFERENCES public.users(id),
	"date" date NOT NULL,
	"time" time without time zone,
	name VARCHAR(255) NOT NULL,
	quantity VARCHAR(64),
	calories numeric,
	protein numeric
);

CREATE TABLE public.food_photos
(
	id serial PRIMARY KEY,
	food_id integer REFERENCES public.food(id),
	file_name VARCHAR(255) NOT NULL
);

CREATE TABLE public.body (
	id serial PRIMARY KEY,
	user_id integer REFERENCES public.users(id),
	"date" date NOT NULL,
	"time" time without time zone,
	bodyweight numeric
);
