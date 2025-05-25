select *
from users u
join bank_cards bk on u.id = bk.user_id
join transactions t on t.bank_card_id = bk.id;

select *
from users u
left join financial_groups fg on u.id = fg.user_id
left join transaction_categories tc on u.id = tc.user_id;

-- category in transaction must be null after this
delete from transaction_categories;

select *
from users u
left join financial_groups fg on u.id = fg.user_id
left join transaction_categories tc on u.id = tc.user_id

-- it must delete all related to financial_groups and bank_cards transactions
delete from financial_groups;
delete from bank_cards;

select * from transactions;
