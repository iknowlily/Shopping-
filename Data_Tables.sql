create
database fuzhuang character set 'utf8mb4';
use
fuzhuang;
show
databases;
drop
database comment;
drop table user_ORM;
create table user_ORM
(
    id           int primary key auto_increment,
    username     varchar(128)           not null,
    password     varchar(128)           not null,
    sex          varchar(128) default 'male' null,
    birthday     varchar(128) null,
    phone_number varchar(128) null,
    email        varchar(128) null,
    address      varchar(128) null,
    admin_id     int          default 0 not null
);

create table category
(
    id            int primary key auto_increment,
    category_name varchar(525) not null
);

create table products
(
    id               int primary key auto_increment,
    category_id      int not null,
    user_id          int not null,
    products_name    varchar(128) null,
    merchant_name    varchar(128) null,
    price            int null,
    merchant_address varchar(128) null,
    cover            varchar(888) null,
    content          varchar(128) null,
    new_price         int null,
    duration         varchar(128) null,
    promotion_reason varchar(128) null,
    count            int null,
    out_count        int null,
    status           int null,
    likes            int          null,
    not_likes        int          null,
    constraint fk_user_id foreign key (user_id) references user_ORM (id),
    constraint fk_category_id foreign key (category_id) references category (id)
);

create table comment
(
    id          int primary key auto_increment,
    product_id  int          not null,
    user_id     int          not null,
    content     varchar(128) not null,
    create_time datetime     not null,
    constraint fk_product_id foreign key (product_id) references products (id),
    constraint fk_user_id foreign key (user_id) references user_ORM (id)
);

create table shopping_cart
(
    id         int primary key auto_increment,
    product_id int not null,
    user_id    int not null,
    count      int not null,
    status     int default 0 null,
    constraint fk_product_id foreign key (product_id) references products (id),
    constraint fk_user_id foreign key (user_id) references user_ORM (id)
);

insert into user_ORM (`username`, `password`)
values (123, 123);
select *
from comment
where user_id = 1;
select count(*)
from comment;
select *
from category
where category_name = 'ass';
select *
from user_ORM
where id = 1;
UPDATE shopping_cart
SET status=1
WHERE product_id = 3
  and user_id = 2;
alter table products add column create_time datetime null;

ALTER TABLE products
DROP create_time;

alter table products add column ts_time timestamp NOT NULL DEFAULT NOW();