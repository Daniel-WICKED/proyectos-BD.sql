PGDMP                         {           concesionario    15.1    15.1                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16739    concesionario    DATABASE     �   CREATE DATABASE concesionario WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Mexico.1252';
    DROP DATABASE concesionario;
                postgres    false            �            1259    17263    clientes    TABLE     �   CREATE TABLE public.clientes (
    dni character varying(10) NOT NULL,
    nombre character varying(50),
    apellidos character varying(50),
    direccion character varying(100),
    telefono character varying(20)
);
    DROP TABLE public.clientes;
       public         heap    postgres    false            �            1259    17258    coches    TABLE       CREATE TABLE public.coches (
    matricula character varying(10) NOT NULL,
    modelo character varying(50),
    marca character varying(50),
    color character varying(20),
    tipo character varying(10),
    unidades_nuevas integer,
    kilometros integer
);
    DROP TABLE public.coches;
       public         heap    postgres    false            �            1259    17268    fichas    TABLE     �   CREATE TABLE public.fichas (
    dni_cliente character varying(10) NOT NULL,
    matricula_coche character varying(10) NOT NULL,
    fecha_compra date
);
    DROP TABLE public.fichas;
       public         heap    postgres    false            �            1259    17283 	   mecanicos    TABLE     �   CREATE TABLE public.mecanicos (
    dni character varying(10) NOT NULL,
    nombre character varying(50),
    apellidos character varying(50),
    fecha_contratacion date,
    salario numeric(8,2)
);
    DROP TABLE public.mecanicos;
       public         heap    postgres    false            �            1259    17288    reparaciones    TABLE     �   CREATE TABLE public.reparaciones (
    dni_mecanico character varying(10) NOT NULL,
    matricula_coche character varying(10) NOT NULL,
    fecha_reparacion date NOT NULL,
    horas_trabajadas numeric(5,2)
);
     DROP TABLE public.reparaciones;
       public         heap    postgres    false                      0    17263    clientes 
   TABLE DATA           O   COPY public.clientes (dni, nombre, apellidos, direccion, telefono) FROM stdin;
    public          postgres    false    215                     0    17258    coches 
   TABLE DATA           d   COPY public.coches (matricula, modelo, marca, color, tipo, unidades_nuevas, kilometros) FROM stdin;
    public          postgres    false    214   �                 0    17268    fichas 
   TABLE DATA           L   COPY public.fichas (dni_cliente, matricula_coche, fecha_compra) FROM stdin;
    public          postgres    false    216   )                 0    17283 	   mecanicos 
   TABLE DATA           X   COPY public.mecanicos (dni, nombre, apellidos, fecha_contratacion, salario) FROM stdin;
    public          postgres    false    217   �                 0    17288    reparaciones 
   TABLE DATA           i   COPY public.reparaciones (dni_mecanico, matricula_coche, fecha_reparacion, horas_trabajadas) FROM stdin;
    public          postgres    false    218          w           2606    17267    clientes clientes_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_pkey PRIMARY KEY (dni);
 @   ALTER TABLE ONLY public.clientes DROP CONSTRAINT clientes_pkey;
       public            postgres    false    215            u           2606    17262    coches coches_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.coches
    ADD CONSTRAINT coches_pkey PRIMARY KEY (matricula);
 <   ALTER TABLE ONLY public.coches DROP CONSTRAINT coches_pkey;
       public            postgres    false    214            y           2606    17272    fichas fichas_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.fichas
    ADD CONSTRAINT fichas_pkey PRIMARY KEY (dni_cliente, matricula_coche);
 <   ALTER TABLE ONLY public.fichas DROP CONSTRAINT fichas_pkey;
       public            postgres    false    216    216            {           2606    17287    mecanicos mecanicos_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.mecanicos
    ADD CONSTRAINT mecanicos_pkey PRIMARY KEY (dni);
 B   ALTER TABLE ONLY public.mecanicos DROP CONSTRAINT mecanicos_pkey;
       public            postgres    false    217            }           2606    17292    reparaciones reparaciones_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.reparaciones
    ADD CONSTRAINT reparaciones_pkey PRIMARY KEY (dni_mecanico, matricula_coche, fecha_reparacion);
 H   ALTER TABLE ONLY public.reparaciones DROP CONSTRAINT reparaciones_pkey;
       public            postgres    false    218    218    218            ~           2606    17273    fichas fichas_dni_cliente_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.fichas
    ADD CONSTRAINT fichas_dni_cliente_fkey FOREIGN KEY (dni_cliente) REFERENCES public.clientes(dni);
 H   ALTER TABLE ONLY public.fichas DROP CONSTRAINT fichas_dni_cliente_fkey;
       public          postgres    false    215    216    3191                       2606    17278 "   fichas fichas_matricula_coche_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.fichas
    ADD CONSTRAINT fichas_matricula_coche_fkey FOREIGN KEY (matricula_coche) REFERENCES public.coches(matricula);
 L   ALTER TABLE ONLY public.fichas DROP CONSTRAINT fichas_matricula_coche_fkey;
       public          postgres    false    216    214    3189            �           2606    17293 +   reparaciones reparaciones_dni_mecanico_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.reparaciones
    ADD CONSTRAINT reparaciones_dni_mecanico_fkey FOREIGN KEY (dni_mecanico) REFERENCES public.mecanicos(dni);
 U   ALTER TABLE ONLY public.reparaciones DROP CONSTRAINT reparaciones_dni_mecanico_fkey;
       public          postgres    false    218    3195    217            �           2606    17298 .   reparaciones reparaciones_matricula_coche_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.reparaciones
    ADD CONSTRAINT reparaciones_matricula_coche_fkey FOREIGN KEY (matricula_coche) REFERENCES public.coches(matricula);
 X   ALTER TABLE ONLY public.reparaciones DROP CONSTRAINT reparaciones_matricula_coche_fkey;
       public          postgres    false    214    3189    218               �   x�%�M
1��uz�\@!�t~��B���D�E�N%����Z�ϛ/d]��a������|��9.�.�dx�wԠ�ơ���kb�˽���)2��*�������Yk�s������jx��Q2�X��F�j�\�Ƙ/��*N            x�m�;�0F�/?FLc}�5���>�.SJ$�B����ѳ�Ñ������G����OF���Q��DֲP8�8��7�c�*���9_<�wr�G2��eF4�i��A��>в7�&�����_!>"�+         L   x�-˹�@A[�E�vu��9�@��3`�\j�2N3B'ͳ!ko���,��T��+ �!�q��g��z�z��~         p   x�-ʻ�0���_R�v��bB�,���Ur���'R+��Rj��5\�㆛��?01G�8+��&��RR՜3��]����};�<�u��,"��2fw�l{�zT�L���B�Wv�         V   x�-ʻ�0�z�^X@�پ�{p�u\�'"Hf���c��N�VUw���|�����4S ���]��	56J�6����0     