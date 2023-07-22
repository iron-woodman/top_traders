use top_traders_deals;

-- select tr.name, al.symbol, al.opened, al.closed, al.profit, td.amount, td.leverage
-- from all_trades al, traders tr, trades td
-- where
-- tr.uid=al.trader_uid
-- and
-- al.trade_id=td.id
-- and
-- tr.name='沧海一声笑2021'
-- order by tr.name;


select * from trades;


-- select tr.name, sum(al.profit)
-- from all_trades al, traders tr, trades td
-- where
-- tr.uid=al.trader_uid
-- and
-- al.trade_id=td.id
-- group by tr.name
-- order by tr.name;

-- select tr.name, count(*)
-- from all_trades al, traders tr, trades td
-- where
-- tr.uid=al.trader_uid
-- and
-- al.trade_id=td.id
-- group by tr.name
-- order by tr.name;


-- select tr.name
-- from all_trades al, traders tr, trades td
-- where
-- tr.uid=al.trader_uid
-- and
-- al.trade_id=td.id
-- group by tr.name
-- order by tr.name;



 -- select * from trades;
 -- select * from all_trades;
-- select * from traders;
-- select * from daily_trades;