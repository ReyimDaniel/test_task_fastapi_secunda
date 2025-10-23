--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

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

ALTER TABLE IF EXISTS ONLY public.phone_number DROP CONSTRAINT IF EXISTS phone_number_organization_id_fkey;
ALTER TABLE IF EXISTS ONLY public.organization DROP CONSTRAINT IF EXISTS organization_building_id_fkey;
ALTER TABLE IF EXISTS ONLY public.organization_activity DROP CONSTRAINT IF EXISTS organization_activity_organization_id_fkey;
ALTER TABLE IF EXISTS ONLY public.organization_activity DROP CONSTRAINT IF EXISTS organization_activity_activity_id_fkey;
ALTER TABLE IF EXISTS ONLY public.activity DROP CONSTRAINT IF EXISTS activity_parent_id_fkey;
ALTER TABLE IF EXISTS ONLY public.phone_number DROP CONSTRAINT IF EXISTS phone_number_pkey;
ALTER TABLE IF EXISTS ONLY public.organization DROP CONSTRAINT IF EXISTS organization_pkey;
ALTER TABLE IF EXISTS ONLY public.organization_activity DROP CONSTRAINT IF EXISTS organization_activity_pkey;
ALTER TABLE IF EXISTS ONLY public.building DROP CONSTRAINT IF EXISTS building_pkey;
ALTER TABLE IF EXISTS ONLY public.alembic_version DROP CONSTRAINT IF EXISTS alembic_version_pkc;
ALTER TABLE IF EXISTS ONLY public.activity DROP CONSTRAINT IF EXISTS activity_pkey;
ALTER TABLE IF EXISTS public.phone_number ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.organization ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.building ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.activity ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.phone_number_id_seq;
DROP TABLE IF EXISTS public.phone_number;
DROP SEQUENCE IF EXISTS public.organization_id_seq;
DROP TABLE IF EXISTS public.organization_activity;
DROP TABLE IF EXISTS public.organization;
DROP SEQUENCE IF EXISTS public.building_id_seq;
DROP TABLE IF EXISTS public.building;
DROP TABLE IF EXISTS public.alembic_version;
DROP SEQUENCE IF EXISTS public.activity_id_seq;
DROP TABLE IF EXISTS public.activity;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activity; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    parent_id integer
);


--
-- Name: activity_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activity_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: activity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activity_id_seq OWNED BY public.activity.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: building; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.building (
    id integer NOT NULL,
    address character varying(255) NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL
);


--
-- Name: building_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.building_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: building_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.building_id_seq OWNED BY public.building.id;


--
-- Name: organization; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.organization (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    building_id integer
);


--
-- Name: organization_activity; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.organization_activity (
    organization_id integer NOT NULL,
    activity_id integer NOT NULL
);


--
-- Name: organization_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.organization_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: organization_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.organization_id_seq OWNED BY public.organization.id;


--
-- Name: phone_number; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.phone_number (
    id integer NOT NULL,
    number character varying(50) NOT NULL,
    organization_id integer NOT NULL
);


--
-- Name: phone_number_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.phone_number_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: phone_number_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.phone_number_id_seq OWNED BY public.phone_number.id;


--
-- Name: activity id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity ALTER COLUMN id SET DEFAULT nextval('public.activity_id_seq'::regclass);


--
-- Name: building id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.building ALTER COLUMN id SET DEFAULT nextval('public.building_id_seq'::regclass);


--
-- Name: organization id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organization ALTER COLUMN id SET DEFAULT nextval('public.organization_id_seq'::regclass);


--
-- Name: phone_number id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.phone_number ALTER COLUMN id SET DEFAULT nextval('public.phone_number_id_seq'::regclass);


--
-- Data for Name: activity; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity (id, name, parent_id) FROM stdin;
1	Еда	\N
2	Автомобили	\N
3	Запчасти	\N
4	Аксессуары	\N
5	Мясная продукция	1
6	Молочная продукция	1
7	Грузовые	2
8	Легковые	2
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
ba0c3e3ebbe1
\.


--
-- Data for Name: building; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.building (id, address, latitude, longitude) FROM stdin;
1	Улица Пушкина, д. 48	59	60
2	Большая Морская, д. 115	70	85
\.


--
-- Data for Name: organization; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.organization (id, name, building_id) FROM stdin;
1	ИП “ГрузАвто”	1
2	ООО Продуктовый 	2
3	ООО “Автозапчасти 24”	1
4	ИП “Николаевич”	2
5	ООО Пятерочка	2
\.


--
-- Data for Name: organization_activity; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.organization_activity (organization_id, activity_id) FROM stdin;
1	7
1	8
2	5
2	6
3	7
3	8
4	8
4	7
5	6
5	5
\.


--
-- Data for Name: phone_number; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.phone_number (id, number, organization_id) FROM stdin;
1	88003691458	1
2	89002583625	2
\.


--
-- Name: activity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.activity_id_seq', 10, true);


--
-- Name: building_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.building_id_seq', 2, true);


--
-- Name: organization_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.organization_id_seq', 5, true);


--
-- Name: phone_number_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.phone_number_id_seq', 2, true);


--
-- Name: activity activity_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity
    ADD CONSTRAINT activity_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: building building_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.building
    ADD CONSTRAINT building_pkey PRIMARY KEY (id);


--
-- Name: organization_activity organization_activity_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organization_activity
    ADD CONSTRAINT organization_activity_pkey PRIMARY KEY (organization_id, activity_id);


--
-- Name: organization organization_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organization
    ADD CONSTRAINT organization_pkey PRIMARY KEY (id);


--
-- Name: phone_number phone_number_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.phone_number
    ADD CONSTRAINT phone_number_pkey PRIMARY KEY (id);


--
-- Name: activity activity_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity
    ADD CONSTRAINT activity_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.activity(id);


--
-- Name: organization_activity organization_activity_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organization_activity
    ADD CONSTRAINT organization_activity_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activity(id);


--
-- Name: organization_activity organization_activity_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organization_activity
    ADD CONSTRAINT organization_activity_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organization(id);


--
-- Name: organization organization_building_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organization
    ADD CONSTRAINT organization_building_id_fkey FOREIGN KEY (building_id) REFERENCES public.building(id);


--
-- Name: phone_number phone_number_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.phone_number
    ADD CONSTRAINT phone_number_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organization(id);


--
-- PostgreSQL database dump complete
--

