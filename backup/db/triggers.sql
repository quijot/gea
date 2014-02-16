--
-- Name: plpgsql; Type: EXTENSION; 
--

CREATE EXTENSION IF NOT EXISTS plpgsql;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: plpythonu; Type: PROCEDURAL LANGUAGE; 
--

CREATE OR REPLACE PROCEDURAL LANGUAGE plpythonu;


--
-- Name: dvapi(integer, integer, integer, integer, integer); Type: FUNCTION; 
--

CREATE FUNCTION dvapi(dp integer, ds integer, sd integer, pii integer, subpii integer) RETURNS integer
    LANGUAGE plpythonu
    AS $$
    # PL/Python function body
    coef = '9731'
    _coef = coef + coef + coef + coef
    strpii = '%02d%02d%02d%06d%04d' % (dp, ds, sd, pii, subpii)
    suma = 0
    for i in range(0, len(strpii)):
        m = str(int(strpii[i]) * int(_coef[i]))
        suma += int(m[len(m) - 1])
    return (10 - (suma % 10)) % 10
$$;


--
-- Name: update_dvapi(); Type: FUNCTION;
--

CREATE FUNCTION update_dvapi() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    sd_sd integer;
    ds_id integer;
    ds_ds integer;
    dp_dp integer;
BEGIN
    IF (NEW.sd IS NOT NULL) THEN
        sd_sd := (SELECT sd FROM sd WHERE id=NEW.sd);
        ds_id := (SELECT ds FROM sd WHERE id=NEW.sd);
        ds_ds := (SELECT ds FROM ds WHERE id=ds_id);
        dp_dp := (SELECT dp FROM ds WHERE id=ds_id);
        UPDATE partida SET api = (SELECT dvapi(dp_dp, ds_ds, sd_sd, NEW.pii, NEW.subpii)) WHERE pii = NEW.pii AND subpii = NEW.subpii;
    END IF;
    RETURN NULL;
END;
$$;


--
-- Name: dvapi_insert; Type: TRIGGER;
--

CREATE TRIGGER dvapi_insert AFTER INSERT ON partida FOR EACH ROW EXECUTE PROCEDURE update_dvapi();


--
-- Name: dvapi_update; Type: TRIGGER;
--

CREATE TRIGGER dvapi_update AFTER UPDATE OF sd, pii, subpii ON partida FOR EACH ROW EXECUTE PROCEDURE update_dvapi();


