--
-- PostgreSQL database initialization
--

SET default_transaction_read_only = off;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Database "postgres" dump
--

\connect eventdb

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';
SET default_table_access_method = heap;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    categoryid integer NOT NULL,
    categoryname character varying(255) NOT NULL
);

ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: categories_categoryid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_categoryid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.categories_categoryid_seq OWNER TO postgres;

--
-- Name: categories_categoryid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_categoryid_seq OWNED BY public.categories.categoryid;

--
-- Name: departments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.departments (
    departmentid integer NOT NULL,
    name character varying(255) NOT NULL,
    contactemail character varying(255) NOT NULL,
    phonenumber character varying(50),
    website character varying(255)
);

ALTER TABLE public.departments OWNER TO postgres;

--
-- Name: departments_departmentid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.departments_departmentid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.departments_departmentid_seq OWNER TO postgres;

--
-- Name: departments_departmentid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.departments_departmentid_seq OWNED BY public.departments.departmentid;

--
-- Name: eventcategories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.eventcategories (
    eventid integer NOT NULL,
    categoryid integer NOT NULL
);

ALTER TABLE public.eventcategories OWNER TO postgres;

--
-- Name: events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.events (
    eventid integer NOT NULL,
    eventname character varying(255) NOT NULL,
    description text,
    starttime timestamp without time zone NOT NULL,
    endtime timestamp without time zone NOT NULL,
    departmentid integer NOT NULL,
    locationid integer NOT NULL
);

ALTER TABLE public.events OWNER TO postgres;

--
-- Name: events_eventid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.events_eventid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.events_eventid_seq OWNER TO postgres;

--
-- Name: events_eventid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.events_eventid_seq OWNED BY public.events.eventid;

--
-- Name: locations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.locations (
    locationid integer NOT NULL,
    address character varying(500) NOT NULL
);

ALTER TABLE public.locations OWNER TO postgres;

--
-- Name: locations_locationid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.locations_locationid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.locations_locationid_seq OWNER TO postgres;

--
-- Name: locations_locationid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.locations_locationid_seq OWNED BY public.locations.locationid;

--
-- Name: categories categoryid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN categoryid SET DEFAULT nextval('public.categories_categoryid_seq'::regclass);

--
-- Name: departments departmentid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departments ALTER COLUMN departmentid SET DEFAULT nextval('public.departments_departmentid_seq'::regclass);

--
-- Name: events eventid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events ALTER COLUMN eventid SET DEFAULT nextval('public.events_eventid_seq'::regclass);

--
-- Name: locations locationid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations ALTER COLUMN locationid SET DEFAULT nextval('public.locations_locationid_seq'::regclass);

--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (categoryid, categoryname) FROM stdin;
1	Breakfast Mixer
2	Lunch Mixer
3	Tutoring
4	Sporting Event
5	Watch Party
6	Career Fair
7	Art
8	Charity
9	Guest Speaker
10	Thrift
\.

--
-- Data for Name: departments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.departments (departmentid, name, contactemail, phonenumber, website) FROM stdin;
1	W. P. Carey School of Business	wpcadmissions@asu.edu	480-965-5187	https://wpcarey.asu.edu/
2	Herberger Institute for Design and the Arts	HerbergerAdmissions@asu.edu	480-727-4757	https://herbergerinstitute.asu.edu/
3	Ira A. Fulton Schools of Engineering	FultonSchools@asu.edu	480-965-2272	https://engineering.asu.edu/
4	Rob Walton College of Global Futures	cgf@asu.edu	480-727-6963	https://collegeofglobalfutures.asu.edu/
5	Thunderbird School of Global Management	admissions.tbird@asu.edu	602-496-7000	https://thunderbird.asu.edu/
6	College of Health Solutions	chs@asu.edu	602-496-3300	https://chs.asu.edu/
7	Edson College of Nursing and Health Innovation	nursingandhealth@asu.edu	602-496-2644	https://nursingandhealth.asu.edu/
8	Watts College of Public Service and Community Solutions	publicservice.recruitment@asu.edu	602-496-7827	https://publicservice.asu.edu/
9	Walter Cronkite School of Journalism and Mass Communication	cronkiteinfo@asu.edu	602-496-5555	https://cronkite.asu.edu/
10	The College of Liberal Arts and Sciences	thecollege@asu.edu	480-965-6506	https://thecollege.asu.edu/
\.

--
-- Data for Name: eventcategories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.eventcategories (eventid, categoryid) FROM stdin;
1	10
2	3
3	4
4	2
5	5
6	9
7	1
8	8
9	6
10	7
\.

--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.events (eventid, eventname, description, starttime, endtime, departmentid, locationid) FROM stdin;
1	Vintage Thrift	Come take a look at the great selection of vintage clothing at cheap prices	2025-04-01 09:00:00	2025-04-01 13:00:00	1	1
2	Open Tutoring	Need help with your course work? Come get assistance from asu grad tutors	2025-04-10 17:00:00	2025-04-10 18:30:00	3	3
3	Field Night	Enjoy the night with a variety of field sports	2025-04-20 19:00:00	2025-04-20 22:30:00	6	1
4	Finals Lunch	Prepare for finals week with sandwiches and tutors	2025-05-01 10:30:00	2025-05-01 14:00:00	1	2
5	Movie Night	Take a break from studying, grab some hot chocolate and enjoy Mamma Mia	2025-05-03 18:00:00	2025-05-15 20:00:00	10	1
6	Journalism Panel	Hear stories and get insights from professional journalists	2025-05-20 20:00:00	2025-05-20 21:00:00	9	7
7	Welcome Breakfast	Celebrate back to school and meet fellow Fulton students	2025-08-15 09:00:00	2025-08-15 12:00:00	3	4
8	Clothing Bank	Donate old or unused clothes for those in need	2025-08-25 18:30:00	2025-08-25 20:00:00	8	5
9	Career Fair	Talk to employers and find an internship for this year	2025-09-21 09:00:00	2025-09-21 12:00:00	7	6
10	Halloween Pumpkin Carving	Carve or paint a pumpkin to bring home and show off	2025-10-31 12:00:00	2025-10-31 17:00:00	2	8
\.

--
-- Data for Name: locations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.locations (locationid, address) FROM stdin;
1	400 E. Apache Blvd
2	400 E Lemon St
3	F Wing, 550 E Tyler Mall
4	H-Wing, 550 E Tyler Mall
5	400 E Tyler Mall
6	300 E Orange St
7	1200 S Forest Ave
8	810 S Forest Mall
9	1100 S McAllister Ave
10	400 E Orange St
\.

--
-- Name: categories_categoryid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_categoryid_seq', 20, true);

--
-- Name: departments_departmentid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.departments_departmentid_seq', 20, true);

--
-- Name: events_eventid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.events_eventid_seq', 20, true);

--
-- Name: locations_locationid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.locations_locationid_seq', 20, true);

--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (categoryid);

--
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (departmentid);

--
-- Name: eventcategories eventcategories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventcategories
    ADD CONSTRAINT eventcategories_pkey PRIMARY KEY (eventid, categoryid);

--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (eventid);

--
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (locationid);

--
-- Name: eventcategories eventcategories_categoryid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventcategories
    ADD CONSTRAINT eventcategories_categoryid_fkey FOREIGN KEY (categoryid) REFERENCES public.categories(categoryid);

--
-- Name: eventcategories eventcategories_eventid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventcategories
    ADD CONSTRAINT eventcategories_eventid_fkey FOREIGN KEY (eventid) REFERENCES public.events(eventid);

--
-- Name: events events_departmentid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_departmentid_fkey FOREIGN KEY (departmentid) REFERENCES public.departments(departmentid);

--
-- Name: events events_locationid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_locationid_fkey FOREIGN KEY (locationid) REFERENCES public.locations(locationid);

--
-- PostgreSQL database dump complete
--
