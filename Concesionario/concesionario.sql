PGDMP                         {           concesionario    15.1    15.1 	               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16739    concesionario    DATABASE     �   CREATE DATABASE concesionario WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Mexico.1252';
    DROP DATABASE concesionario;
                postgres    false                      0    17263    clientes 
   TABLE DATA           O   COPY public.clientes (dni, nombre, apellidos, direccion, telefono) FROM stdin;
    public          postgres    false    215   �                 0    17258    coches 
   TABLE DATA           d   COPY public.coches (matricula, modelo, marca, color, tipo, unidades_nuevas, kilometros) FROM stdin;
    public          postgres    false    214   k                 0    17268    fichas 
   TABLE DATA           L   COPY public.fichas (dni_cliente, matricula_coche, fecha_compra) FROM stdin;
    public          postgres    false    216   �                 0    17283 	   mecanicos 
   TABLE DATA           X   COPY public.mecanicos (dni, nombre, apellidos, fecha_contratacion, salario) FROM stdin;
    public          postgres    false    217   V	                 0    17288    reparaciones 
   TABLE DATA           i   COPY public.reparaciones (dni_mecanico, matricula_coche, fecha_reparacion, horas_trabajadas) FROM stdin;
    public          postgres    false    218   �	          �   x�%�M
1��uz�\@!�t~��B���D�E�N%����Z�ϛ/d]��a������|��9.�.�dx�wԠ�ơ���kb�˽���)2��*�������Yk�s������jx��Q2�X��F�j�\�Ƙ/��*N            x�m�;�0F�/?FLc}�5���>�.SJ$�B����ѳ�Ñ������G����OF���Q��DֲP8�8��7�c�*���9_<�wr�G2��eF4�i��A��>в7�&�����_!>"�+         L   x�-˹�@A[�E�vu��9�@��3`�\j�2N3B'ͳ!ko���,��T��+ �!�q��g��z�z��~         p   x�-ʻ�0���_R�v��bB�,���Ur���'R+��Rj��5\�㆛��?01G�8+��&��RR՜3��]����};�<�u��,"��2fw�l{�zT�L���B�Wv�         V   x�-ʻ�0�z�^X@�پ�{p�u\�'"Hf���c��N�VUw���|�����4S ���]��	56J�6����0     