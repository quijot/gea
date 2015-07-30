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
        NEW.api = (SELECT dvapi(dp_dp, ds_ds, sd_sd, NEW.pii, NEW.subpii));
    END IF;
    RETURN NEW;
END;
$$;


--
-- Name: dvapi_update; Type: TRIGGER;
--

CREATE TRIGGER dvapi_update
    BEFORE INSERT OR UPDATE OF sd, pii, subpii ON partida
    FOR EACH ROW
    EXECUTE PROCEDURE update_dvapi();


--
-- Name: fix_nombres_apellidos(); Type: FUNCTION;
--

CREATE FUNCTION fix_nombres_apellidos() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF (NEW.apellidos IS NOT NULL) THEN
        NEW.apellidos := upper(NEW.apellidos);
    END IF;
    IF (NEW.apellidos_alternativos IS NOT NULL) THEN
        NEW.apellidos_alternativos := upper(NEW.apellidos_alternativos);
    END IF;
    IF (NEW.nombres IS NOT NULL) THEN
        NEW.nombres := initcap(NEW.nombres);
    END IF;
    IF (NEW.nombres_alternativos IS NOT NULL) THEN
        NEW.nombres_alternativos := initcap(NEW.nombres_alternativos);
    END IF;
    RETURN NEW;
END;
$$;


--
-- Name: fix_nombres_apellidos; Type: TRIGGER;
--

CREATE TRIGGER fix_nombres_apellidos_trigger
    BEFORE INSERT OR UPDATE OF nombres, apellidos, nombres_alternativos, apellidos_alternativos ON persona
    FOR EACH ROW
    EXECUTE PROCEDURE fix_nombres_apellidos();


--
-- Name: complete_antecedente(); Type: FUNCTION;
--

CREATE FUNCTION complete_antecedente() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    pr varchar(100);
BEGIN
    IF (NEW.expediente_modificado_id IS NOT NULL AND NEW.inscripcion_numero IS NULL) THEN
    -- si ingresan "expediente_id" y NO ingresan "inscripcion_numero"
        -- completa "inscripcion_numero"
        NEW.inscripcion_numero := (SELECT inscripcion_numero FROM expediente WHERE id = NEW.expediente_modificado_id);
        -- completa "duplicado"
        NEW.duplicado := (SELECT duplicado FROM expediente WHERE id = NEW.expediente_modificado_id);
        pr := (SELECT plano_ruta FROM expediente WHERE id = NEW.expediente_modificado_id);
        IF (pr IS NOT NULL) THEN
            NEW.plano_ruta := pr;
        END IF;
    ELSIF (NEW.expediente_modificado_id IS NULL AND NEW.inscripcion_numero IS NOT NULL) THEN
    -- si ingresan "inscripcion_numero" y NO ingresan "expediente_id"
        NEW.expediente_modificado_id := (SELECT id FROM expediente WHERE inscripcion_numero = NEW.inscripcion_numero);
        pr := (SELECT plano_ruta FROM expediente WHERE inscripcion_numero = NEW.inscripcion_numero);
        IF (pr IS NOT NULL) THEN
            NEW.plano_ruta := pr;
        END IF;
    END IF;
    RETURN NEW;
END;
$$;


--
-- Name: complete_antecedente; Type: TRIGGER;
--

CREATE TRIGGER complete_antecedente_trigger
    BEFORE INSERT OR UPDATE OF expediente_modificado_id, inscripcion_numero, duplicado ON antecedente
    FOR EACH ROW
    EXECUTE PROCEDURE complete_antecedente();
