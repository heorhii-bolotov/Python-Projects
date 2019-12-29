use test;
set names utf8;

-- 1. Выбрать все товары (все поля)
select * FROM product;

-- 2. Выбрать названия всех автоматизированных складов
select name FROM store WHERE is_automated = 1;

-- 3. Посчитать общую сумму в деньгах всех продаж
select SUM(total) FROM sale;

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
-- select distinct(store_id) from sale
select DISTINCT sale.store_id 
FROM sale, store 
WHERE sale.store_id = store.store_id;

-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
-- select store_id from store natural left join sale where sale.store_id is null
select store_id 
FROM store 
WHERE NOT EXISTS (
	SELECT store_id 
    FROM sale 
    WHERE sale.store_id = store.store_id
);

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
select name, AVG(total / quantity) AS 'avg(total/quantity)'
FROM product, sale 
WHERE product.product_id = sale.product_id 
GROUP BY name;

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
-- select name from product natural join sale group by product_id having count(distinct store_id) = 1
select name 
FROM (
	select DISTINCT name, store_id 
    FROM sale, product 
    WHERE sale.product_id = product.product_id 
) as n 
GROUP BY name 
HAVING COUNT(store_id) = 1;

-- 8. Получить названия всех складов, с которых продавался только один продукт
-- select name from store natural join sale group by store_id having count(distinct product_id) = 1
select name
FROM (
	select DISTINCT name, product_id 
    FROM sale, store 
    WHERE sale.store_id = store.store_id
) as n
GROUP BY name
HAVING COUNT(product_id) = 1;

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
select * 
FROM sale 
WHERE total = (
	select MAX(total) 
	FROM sale
);

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select date FROM sale GROUP BY date ORDER BY SUM(total) DESC LIMIT 1;
