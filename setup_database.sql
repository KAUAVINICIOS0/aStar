create database db_AStar;

use db_AStar;


/* CIDADES*/
create table tb_city(
    id_city int(11) primary key not null auto_increment,
    name_city varchar(255) not null
);

/* DISTANCIAS ENTRE CIDADES*/
create table tb_city_distance(
    id_city_distance int(11) primary key not null auto_increment,
    fk_id_city_origin int(11) not null,
    fk_id_city_destination int(11) not null,
    distance decimal(10,2) not null,
    foreign key (fk_id_city_origin) references tb_city(id_city),
    foreign key (fk_id_city_destination) references tb_city(id_city)
);


INSERT INTO tb_city (name_city) VALUES 
('Arad'),
('Zerind'),
('Oradea'),
('Sibiu'),
('Timisoara'),
('Lugoj'),
('Mehadia'),
('Dobreta'),
('Craiova'),
('Rimnicu'),
('Fagaras'),
('Pitesti'),
('Bucharest'),
('Giurgiu');

INSERT INTO tb_city_distance (fk_id_city_origin, fk_id_city_destination, distance) VALUES
(1, 2, 75.00),
(1, 4, 140.00),
(1, 5, 118.00),
(2, 1, 75.00),
(2, 3, 71.00),
(3, 2, 71.00),
(3, 4, 151.00),
(4, 3, 151.00),
(4, 1, 140.00),
(4, 11, 99.00),
(4, 10, 80.00),
(5, 1, 118.00),
(5, 6, 111.00),
(6, 5, 111.00),
(6, 7, 70.00),
(7, 6, 70.00),
(7, 8, 75.00),
(8, 7, 75.00),
(8, 9, 120.00),
(9, 8, 120.00),
(9, 12, 138.00),
(9, 10, 146.00),
(10, 9, 146.00),
(10, 4, 80.00),
(10, 12, 97.00),
(11, 4, 99.00),
(11, 13, 211.00),
(12, 10, 97.00),
(12, 9, 138.00),
(12, 13, 101.00),
(13, 11, 211.00),
(13, 12, 101.00),
(13, 14, 90.00); 