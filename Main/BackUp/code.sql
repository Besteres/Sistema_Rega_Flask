--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1 (Debian 16.1-1.pgdg120+1)
-- Dumped by pg_dump version 16.0

-- Started on 2023-12-04 19:57:29

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 216 (class 1255 OID 16432)
-- Name: get_data_for_day(date, boolean); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_data_for_day(target_date date, target_ativo boolean) RETURNS TABLE(precipitacao integer, humidade double precision, times timestamp without time zone, regando boolean)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT
        "Precipitacao" AS precipitacao,
        "Humidade" AS humidade,
        "TimeStamp" AS times,
		"regar" AS regando
    FROM
        valor_registo
    WHERE
        DATE("TimeStamp") = target_date;
END;
$$;


ALTER FUNCTION public.get_data_for_day(target_date date, target_ativo boolean) OWNER TO postgres;

--
-- TOC entry 217 (class 1255 OID 16428)
-- Name: insert_registo(integer, double precision, boolean); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.insert_registo(IN prec integer, IN humid double precision, IN ativado boolean)
    LANGUAGE sql
    AS $$ 
INSERT INTO public.valor_registo(
    "Precipitacao", "Humidade", "TimeStamp","regar")
    VALUES (prec, humid, CURRENT_TIMESTAMP,ativado);
$$;


ALTER PROCEDURE public.insert_registo(IN prec integer, IN humid double precision, IN ativado boolean) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 16451)
-- Name: valor_registo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.valor_registo (
    "Precipitacao" integer,
    "Humidade" double precision,
    "TimeStamp" timestamp without time zone,
    regar boolean
);


ALTER TABLE public.valor_registo OWNER TO postgres;

-- Completed on 2023-12-04 19:57:29

--
-- PostgreSQL database dump complete
--

