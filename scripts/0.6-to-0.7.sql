BEGIN;

DO $$ BEGIN
IF EXISTS (select * from meta where key='SCHEMA_VERSION' AND value='0.6') THEN

----------------------------------------------------------------------------------------------------
--- Update script starts here
----------------------------------------------------------------------------------------------------

UPDATE public.meta SET value='0.7' WHERE key='SCHEMA_VERSION';

CREATE TABLE public.computed_data(
  id serial PRIMARY KEY,
  user_id integer,
  last_updated timestamp,
  key varchar(256),
  value bytea
);

----------------------------------------------------------------------------------------------------
--- Update script ends here
----------------------------------------------------------------------------------------------------

END IF;
END $$;

