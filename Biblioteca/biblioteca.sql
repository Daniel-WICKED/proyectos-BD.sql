PGDMP     2    9                {        
   biblioteca    15.1    15.1 *    %           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            &           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            '           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            (           1262    16398 
   biblioteca    DATABASE     ~   CREATE DATABASE biblioteca WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Mexico.1252';
    DROP DATABASE biblioteca;
                postgres    false            �            1259    16426    autores    TABLE     o   CREATE TABLE public.autores (
    codigo_autor integer NOT NULL,
    nombre character varying(100) NOT NULL
);
    DROP TABLE public.autores;
       public         heap    postgres    false            �            1259    16425    autores_codigo_autor_seq    SEQUENCE     �   CREATE SEQUENCE public.autores_codigo_autor_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.autores_codigo_autor_seq;
       public          postgres    false    215            )           0    0    autores_codigo_autor_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.autores_codigo_autor_seq OWNED BY public.autores.codigo_autor;
          public          postgres    false    214            �            1259    16440 
   ejemplares    TABLE     �   CREATE TABLE public.ejemplares (
    codigo_ejemplar integer NOT NULL,
    codigo_libro integer,
    localizacion character varying(100) NOT NULL
);
    DROP TABLE public.ejemplares;
       public         heap    postgres    false            �            1259    16439    ejemplares_codigo_ejemplar_seq    SEQUENCE     �   CREATE SEQUENCE public.ejemplares_codigo_ejemplar_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.ejemplares_codigo_ejemplar_seq;
       public          postgres    false    219            *           0    0    ejemplares_codigo_ejemplar_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.ejemplares_codigo_ejemplar_seq OWNED BY public.ejemplares.codigo_ejemplar;
          public          postgres    false    218            �            1259    16433    libros    TABLE     �   CREATE TABLE public.libros (
    codigo_libro integer NOT NULL,
    titulo character varying(100) NOT NULL,
    isbn character varying(20) NOT NULL,
    editorial character varying(100) NOT NULL,
    numero_pagina integer NOT NULL
);
    DROP TABLE public.libros;
       public         heap    postgres    false            �            1259    16432    libros_codigo_libro_seq    SEQUENCE     �   CREATE SEQUENCE public.libros_codigo_libro_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.libros_codigo_libro_seq;
       public          postgres    false    217            +           0    0    libros_codigo_libro_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.libros_codigo_libro_seq OWNED BY public.libros.codigo_libro;
          public          postgres    false    216            �            1259    16723 	   prestamos    TABLE     �   CREATE TABLE public.prestamos (
    codigo_prestamo integer NOT NULL,
    codigo_usuario integer,
    codigo_ejemplar integer,
    fecha_prestamo date NOT NULL,
    fecha_devolucion date NOT NULL
);
    DROP TABLE public.prestamos;
       public         heap    postgres    false            �            1259    16722    prestamos_codigo_prestamo_seq    SEQUENCE     �   CREATE SEQUENCE public.prestamos_codigo_prestamo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.prestamos_codigo_prestamo_seq;
       public          postgres    false    223            ,           0    0    prestamos_codigo_prestamo_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.prestamos_codigo_prestamo_seq OWNED BY public.prestamos.codigo_prestamo;
          public          postgres    false    222            �            1259    16716    usuarios    TABLE     �   CREATE TABLE public.usuarios (
    codigo_usuario integer NOT NULL,
    nombre character varying(100) NOT NULL,
    direccion character varying(100) NOT NULL,
    telefono character varying(20) NOT NULL
);
    DROP TABLE public.usuarios;
       public         heap    postgres    false            �            1259    16715    usuarios_codigo_usuario_seq    SEQUENCE     �   CREATE SEQUENCE public.usuarios_codigo_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.usuarios_codigo_usuario_seq;
       public          postgres    false    221            -           0    0    usuarios_codigo_usuario_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.usuarios_codigo_usuario_seq OWNED BY public.usuarios.codigo_usuario;
          public          postgres    false    220            y           2604    16429    autores codigo_autor    DEFAULT     |   ALTER TABLE ONLY public.autores ALTER COLUMN codigo_autor SET DEFAULT nextval('public.autores_codigo_autor_seq'::regclass);
 C   ALTER TABLE public.autores ALTER COLUMN codigo_autor DROP DEFAULT;
       public          postgres    false    215    214    215            {           2604    16443    ejemplares codigo_ejemplar    DEFAULT     �   ALTER TABLE ONLY public.ejemplares ALTER COLUMN codigo_ejemplar SET DEFAULT nextval('public.ejemplares_codigo_ejemplar_seq'::regclass);
 I   ALTER TABLE public.ejemplares ALTER COLUMN codigo_ejemplar DROP DEFAULT;
       public          postgres    false    218    219    219            z           2604    16436    libros codigo_libro    DEFAULT     z   ALTER TABLE ONLY public.libros ALTER COLUMN codigo_libro SET DEFAULT nextval('public.libros_codigo_libro_seq'::regclass);
 B   ALTER TABLE public.libros ALTER COLUMN codigo_libro DROP DEFAULT;
       public          postgres    false    217    216    217            }           2604    16726    prestamos codigo_prestamo    DEFAULT     �   ALTER TABLE ONLY public.prestamos ALTER COLUMN codigo_prestamo SET DEFAULT nextval('public.prestamos_codigo_prestamo_seq'::regclass);
 H   ALTER TABLE public.prestamos ALTER COLUMN codigo_prestamo DROP DEFAULT;
       public          postgres    false    223    222    223            |           2604    16719    usuarios codigo_usuario    DEFAULT     �   ALTER TABLE ONLY public.usuarios ALTER COLUMN codigo_usuario SET DEFAULT nextval('public.usuarios_codigo_usuario_seq'::regclass);
 F   ALTER TABLE public.usuarios ALTER COLUMN codigo_usuario DROP DEFAULT;
       public          postgres    false    221    220    221                      0    16426    autores 
   TABLE DATA           7   COPY public.autores (codigo_autor, nombre) FROM stdin;
    public          postgres    false    215   !1                 0    16440 
   ejemplares 
   TABLE DATA           Q   COPY public.ejemplares (codigo_ejemplar, codigo_libro, localizacion) FROM stdin;
    public          postgres    false    219   �1                 0    16433    libros 
   TABLE DATA           V   COPY public.libros (codigo_libro, titulo, isbn, editorial, numero_pagina) FROM stdin;
    public          postgres    false    217   �1       "          0    16723 	   prestamos 
   TABLE DATA           w   COPY public.prestamos (codigo_prestamo, codigo_usuario, codigo_ejemplar, fecha_prestamo, fecha_devolucion) FROM stdin;
    public          postgres    false    223   ]2                  0    16716    usuarios 
   TABLE DATA           O   COPY public.usuarios (codigo_usuario, nombre, direccion, telefono) FROM stdin;
    public          postgres    false    221   �2       .           0    0    autores_codigo_autor_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.autores_codigo_autor_seq', 6, true);
          public          postgres    false    214            /           0    0    ejemplares_codigo_ejemplar_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.ejemplares_codigo_ejemplar_seq', 3, true);
          public          postgres    false    218            0           0    0    libros_codigo_libro_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.libros_codigo_libro_seq', 3, true);
          public          postgres    false    216            1           0    0    prestamos_codigo_prestamo_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.prestamos_codigo_prestamo_seq', 2, true);
          public          postgres    false    222            2           0    0    usuarios_codigo_usuario_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.usuarios_codigo_usuario_seq', 3, true);
          public          postgres    false    220                       2606    16431    autores autores_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.autores
    ADD CONSTRAINT autores_pkey PRIMARY KEY (codigo_autor);
 >   ALTER TABLE ONLY public.autores DROP CONSTRAINT autores_pkey;
       public            postgres    false    215            �           2606    16445    ejemplares ejemplares_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.ejemplares
    ADD CONSTRAINT ejemplares_pkey PRIMARY KEY (codigo_ejemplar);
 D   ALTER TABLE ONLY public.ejemplares DROP CONSTRAINT ejemplares_pkey;
       public            postgres    false    219            �           2606    16438    libros libros_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.libros
    ADD CONSTRAINT libros_pkey PRIMARY KEY (codigo_libro);
 <   ALTER TABLE ONLY public.libros DROP CONSTRAINT libros_pkey;
       public            postgres    false    217            �           2606    16728    prestamos prestamos_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.prestamos
    ADD CONSTRAINT prestamos_pkey PRIMARY KEY (codigo_prestamo);
 B   ALTER TABLE ONLY public.prestamos DROP CONSTRAINT prestamos_pkey;
       public            postgres    false    223            �           2606    16721    usuarios usuarios_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (codigo_usuario);
 @   ALTER TABLE ONLY public.usuarios DROP CONSTRAINT usuarios_pkey;
       public            postgres    false    221            �           2606    16446 '   ejemplares ejemplares_codigo_libro_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.ejemplares
    ADD CONSTRAINT ejemplares_codigo_libro_fkey FOREIGN KEY (codigo_libro) REFERENCES public.libros(codigo_libro);
 Q   ALTER TABLE ONLY public.ejemplares DROP CONSTRAINT ejemplares_codigo_libro_fkey;
       public          postgres    false    219    217    3201            �           2606    16734 (   prestamos prestamos_codigo_ejemplar_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.prestamos
    ADD CONSTRAINT prestamos_codigo_ejemplar_fkey FOREIGN KEY (codigo_ejemplar) REFERENCES public.ejemplares(codigo_ejemplar);
 R   ALTER TABLE ONLY public.prestamos DROP CONSTRAINT prestamos_codigo_ejemplar_fkey;
       public          postgres    false    223    3203    219            �           2606    16729 '   prestamos prestamos_codigo_usuario_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.prestamos
    ADD CONSTRAINT prestamos_codigo_usuario_fkey FOREIGN KEY (codigo_usuario) REFERENCES public.usuarios(codigo_usuario);
 Q   ALTER TABLE ONLY public.prestamos DROP CONSTRAINT prestamos_codigo_usuario_fkey;
       public          postgres    false    221    223    3205               O   x�3�tOL*�L�QpO,J>�6Q���¢���*.#N���<���̒.cN�ļT��T.N���D��|q~W� �         +   x�3�4�t-.I�+IUp4�2�4�s����9��\gc�=... G�a         �   x�M˻
�0 ���+B>@�N:;TA��K�^j0�r�ſ������B����ik�W@���`�w0L�Ǌ*J�w��k.�'~[�w�˘i>���3�� �D$~G�Zs*���*?��Z����h�k�r����T�����yb�� q�/u      "   -   x�3�4B##c]S]#S(�L���ˈar�p9C�=... 3	�          k   x�3�t��LNU����+���442V�M��S.)JM-�455���pq:�')�f�dp���)���"�153��2��N-��N,��4�0U��IN��G1��0F��� u�!�     